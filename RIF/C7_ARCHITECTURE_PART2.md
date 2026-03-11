

# C7 — Recursive Intent Fabric (RIF)

## Architecture Document — Part 2 (Sections 7–14)

---

## 7. Graduated Sovereignty Model

### 7.1 Three-Tier Formal Specification

Graduated Sovereignty partitions every system parameter into one of three tiers based on the consequences of modification. Each tier has distinct authorization requirements, modification protocols, and reversion semantics.

```
+=========================================================================+
|                     GRADUATED SOVEREIGNTY MODEL                         |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 1 — CONSTITUTIONAL (Immutable)                              | |
|  |  Authorization: NEVER modifiable at runtime                       | |
|  |  Reversion: N/A — cannot be changed                               | |
|  |  Protected by: System 5 audit + hard-coded enforcement            | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 2 — OPERATIONAL (Governance-Relaxable)                      | |
|  |  Authorization: 90% G-class supermajority                         | |
|  |  Reversion: Auto-revert after lease (max 50 epochs)               | |
|  |  Protected by: System 5 vote + lease monitor                      | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 3 — COORDINATION (Advisory)                                 | |
|  |  Authorization: System 3 may override unilaterally                | |
|  |  Reversion: Continuous adjustment                                 | |
|  |  Protected by: Performance monitoring + System 4 feedback         | |
|  +-------------------------------------------------------------------+ |
+=========================================================================+
```

#### 7.1.1 Tier 1 — Constitutional Invariants

Constitutional invariants define what the system *is*. They cannot be relaxed, suspended, or overridden under any circumstances, including emergency. Violation of a constitutional invariant triggers immediate system halt and rollback.

| ID | Invariant | Description | Cross-Reference | Enforcement Point |
|---|---|---|---|---|
| C-01 | PCVM Classification Integrity | The PCVM claim classification taxonomy (C5 §3) is immutable at runtime. No intent, governance vote, or sovereignty relaxation may alter claim class definitions. | C5 PCVM §3.1 | System 5 audit; ISR rejects intents targeting PCVM schema |
| C-02 | VTD Immutability | Verified Trust Documents (C5 §4) are append-only. Once a VTD is committed, its content is permanent. Intents that attempt VTD mutation are rejected at admission. | C5 PCVM §4.2 | Intent Admission Gate (§10); ISR hard-reject |
| C-03 | EMA Canonical Source | The Epistemic Metabolism Architecture (C6) is the sole authoritative source for epistemic quanta. No RIF component may create, modify, or delete EMA quanta directly. System 4 reads EMA in read-only mode. | C6 EMA §2.1 | System 4 interface is read-only by construction |
| C-04 | Decomposition Termination | All intent decompositions must terminate in finite steps (§6.2 proof). No relaxation may increase max_depth beyond 20 or disable the depth guard. | §6.2 | System 3 hard-coded depth check |
| C-05 | Operation Class Monotonicity | Decomposition must produce children with equal or lower operation class rank (§6.1). No relaxation may violate the decomposition matrix. | §6.1 | System 3 assertion in decompose_intent() |
| C-06 | Resource Bound Integrity | Children cannot exceed parent resource envelopes (§6.4). No relaxation may disable resource partition validation. | §6.4 | System 3 validate_resource_partition() |
| C-07 | Provenance Chain Completeness | Every intent state transition must carry a valid CausalStamp and be traceable to an originating agent via C4 ASV provenance. | §3.2, §3.3 | ISR rejects transitions without CausalStamp |
| C-08 | Settlement Completeness | Every COMPLETED intent must produce a corresponding settlement entry in the C3 ledger. | §3.4 | Settlement Router at-least-once guarantee |

**Constitutional enforcement pseudocode**:

```
function enforce_constitutional(action: SystemAction) -> EnforcementResult:
    for invariant in CONSTITUTIONAL_INVARIANTS:
        violation = invariant.check(action)
        if violation != null:
            // Log immutably
            audit_log.append(ConstitutionalViolationAttempt(
                invariant_id=invariant.id,
                action=action,
                epoch=current_epoch(),
                violation_details=violation
            ))
            // Hard reject — no appeal, no override
            return EnforcementResult.HARD_REJECT(
                invariant_id=invariant.id,
                reason=violation.description
            )
    return EnforcementResult.PASS
```

#### 7.1.2 Tier 2 — Operational Constraints

Operational constraints govern resource allocations, composition rules, and timing parameters. They may be temporarily relaxed via the Sovereignty Relaxation Protocol (§7.2) but automatically revert after a bounded lease.

| ID | Constraint | Default Value | Relaxation Bounds | Cross-Reference |
|---|---|---|---|---|
| O-01 | VRF Composition Rules | Standard C3 VRF composition | May permit expanded composition sets | C3 §5.3 |
| O-02 | Metabolic Timing Windows | C6-defined epoch boundaries | May extend/contract by up to 2x | C6 §4.1 |
| O-03 | SHREC Allocation Ratios | C6-defined SHREC defaults | May shift ratios within ±20% | C6 §6.2 |
| O-04 | Cross-Locus Intent Threshold | 20% of locus traffic | May increase to 40% | §11.2 |
| O-05 | Decomposition Depth Soft Limit | 10 levels | May increase to 15 (hard max 20 per C-04) | §6.5 |
| O-06 | Memoization Cache TTL | 50 epochs | May extend to 100 epochs | §6.6 |
| O-07 | Agent Credibility Floor | 0.5 PCVM score | May lower to 0.3 during capacity shortage | §5.1 |
| O-08 | Settlement Retry Limit | 10 attempts | May increase to 20 during ledger congestion | §3.4 |
| O-09 | Failure Detector Quorum | 3 sentinels | May reduce to 2 during low-agent conditions | §3.5 |
| O-10 | ISR Bandwidth Cap | 5% of locus network | May increase to 8% during high-intent periods | §3.3 |

#### 7.1.3 Tier 3 — Coordination Parameters

Coordination parameters are advisory hints that System 3 may override unilaterally based on operational needs. No governance vote is required.

| ID | Parameter | Default | Override Authority | Cross-Reference |
|---|---|---|---|---|
| A-01 | Agent Workload Preferences | Agent-declared | System 3 intent assignment | §3.1 |
| A-02 | Preferred Decomposition Strategy | Intent-declared | System 3 strategy selector | §4.1.1 |
| A-03 | Locus Affinity Hints | Agent-declared | System 3 cross-locus routing | §8.1 |
| A-04 | Priority Boost Requests | Proposer-declared | System 3 queue management | §10.2 |
| A-05 | Output Format Preferences | Intent-declared | Parcel Executor normalization | §8.3 |
| A-06 | Monitoring Verbosity | Locus-default | System 3 performance monitor | §4.1.3 |

### 7.2 Sovereignty Relaxation Protocol

When operational conditions require temporary deviation from Tier 2 constraints, System 3 initiates a Sovereignty Relaxation request. The protocol has five phases: Request, Vote, Activation, Monitoring, and Termination.

#### 7.2.1 Request Format

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-relaxation-request/v1",
  "type": "object",
  "properties": {
    "request_id": {
      "type": "string",
      "format": "uuid"
    },
    "requester": {
      "type": "string",
      "enum": ["SYSTEM_3", "SYSTEM_4"]
    },
    "request_epoch": {
      "type": "integer"
    },
    "constraint_id": {
      "type": "string",
      "description": "Operational constraint ID (O-01 through O-10)"
    },
    "current_value": {
      "description": "Current enforced value of the constraint"
    },
    "requested_value": {
      "description": "Proposed relaxed value"
    },
    "justification": {
      "type": "object",
      "properties": {
        "trigger_condition": {
          "type": "string",
          "description": "What operational condition triggered this request"
        },
        "supporting_metrics": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "metric_name": { "type": "string" },
              "current_value": { "type": "number" },
              "threshold_value": { "type": "number" },
              "window_epochs": { "type": "integer" }
            },
            "required": ["metric_name", "current_value"]
          }
        },
        "impact_assessment": {
          "type": "string",
          "description": "Expected impact of relaxation"
        },
        "risk_if_denied": {
          "type": "string",
          "description": "Expected consequence of not relaxing"
        }
      },
      "required": ["trigger_condition", "supporting_metrics",
                    "impact_assessment", "risk_if_denied"]
    },
    "requested_lease_epochs": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50,
      "description": "Requested duration of relaxation"
    },
    "anti_cascade_declaration": {
      "type": "object",
      "properties": {
        "dependent_constraints": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Other constraint IDs this relaxation may affect"
        },
        "cascade_risk": {
          "type": "string",
          "enum": ["NONE", "LOW", "MEDIUM", "HIGH"]
        },
        "mitigation": {
          "type": "string",
          "description": "How cascade risk is mitigated"
        }
      },
      "required": ["dependent_constraints", "cascade_risk"]
    }
  },
  "required": ["request_id", "requester", "request_epoch",
               "constraint_id", "current_value", "requested_value",
               "justification", "requested_lease_epochs",
               "anti_cascade_declaration"]
}
```

#### 7.2.2 Vote Process

```
function process_relaxation_request(
    request: SovereigntyRelaxationRequest
) -> RelaxationOutcome:

    // Phase 1: Pre-validation
    // Verify the target constraint is Tier 2 (not Constitutional)
    if request.constraint_id in CONSTITUTIONAL_INVARIANTS:
        return RelaxationOutcome.DENIED(
            reason="CONSTITUTIONAL_INVIOLABLE",
            constraint_id=request.constraint_id
        )

    // Verify requested value is within relaxation bounds
    bounds = OPERATIONAL_CONSTRAINTS[request.constraint_id].relaxation_bounds
    if not bounds.contains(request.requested_value):
        return RelaxationOutcome.DENIED(
            reason="EXCEEDS_RELAXATION_BOUNDS",
            max_permitted=bounds.max
        )

    // Phase 2: Anti-cascade check
    active_relaxations = get_active_relaxations()
    cascade_count = count_related_relaxations(
        request.anti_cascade_declaration.dependent_constraints,
        active_relaxations
    )
    if cascade_count >= MAX_CONCURRENT_RELATED_RELAXATIONS:  // default: 2
        return RelaxationOutcome.DENIED(
            reason="ANTI_CASCADE_LIMIT",
            active_related=cascade_count
        )

    // Phase 3: Submit to G-class vote
    vote_package = RelaxationVotePackage(
        request=request,
        active_relaxations=active_relaxations,
        system_health=get_system_health_snapshot()
    )

    vote_result = c3.g_class_vote(
        topic="SOVEREIGNTY_RELAXATION",
        package=vote_package,
        quorum_threshold=0.90,       // 90% supermajority required
        timeout_epochs=3
    )

    if not vote_result.supermajority_met:
        return RelaxationOutcome.DENIED(
            reason="SUPERMAJORITY_NOT_MET",
            votes_for=vote_result.votes_for,
            votes_against=vote_result.votes_against,
            total_eligible=vote_result.total_eligible
        )

    // Phase 4: Activate relaxation
    lease = SovereigntyLease(
        relaxation_id=request.request_id,
        constraint_id=request.constraint_id,
        original_value=request.current_value,
        relaxed_value=request.requested_value,
        start_epoch=current_epoch(),
        expiry_epoch=current_epoch() + request.requested_lease_epochs,
        vote_record=vote_result,
        status="ACTIVE"
    )

    activate_lease(lease)
    return RelaxationOutcome.APPROVED(lease=lease)
```

#### 7.2.3 Lease Structure

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-lease/v1",
  "type": "object",
  "properties": {
    "relaxation_id": {
      "type": "string",
      "format": "uuid"
    },
    "constraint_id": {
      "type": "string"
    },
    "original_value": {
      "description": "Value to revert to upon expiry"
    },
    "relaxed_value": {
      "description": "Currently active relaxed value"
    },
    "start_epoch": {
      "type": "integer"
    },
    "expiry_epoch": {
      "type": "integer",
      "description": "Epoch at which auto-revert occurs"
    },
    "vote_record": {
      "type": "object",
      "properties": {
        "votes_for": { "type": "integer" },
        "votes_against": { "type": "integer" },
        "total_eligible": { "type": "integer" },
        "vote_epoch": { "type": "integer" },
        "voter_ids": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "required": ["votes_for", "votes_against",
                    "total_eligible", "vote_epoch"]
    },
    "monitoring": {
      "type": "object",
      "properties": {
        "health_check_interval_epochs": {
          "type": "integer",
          "default": 5
        },
        "revocation_trigger_metric": {
          "type": "string"
        },
        "revocation_threshold": {
          "type": "number"
        }
      }
    },
    "status": {
      "type": "string",
      "enum": ["ACTIVE", "EXPIRED", "REVOKED", "SUPERSEDED"]
    },
    "revocation_reason": {
      "type": ["string", "null"]
    }
  },
  "required": ["relaxation_id", "constraint_id", "original_value",
               "relaxed_value", "start_epoch", "expiry_epoch",
               "vote_record", "status"]
}
```

#### 7.2.4 Lease Monitoring and Revocation

```
function monitor_active_leases():
    // Called every epoch by System 5
    for lease in get_active_leases():
        // Check expiry
        if current_epoch() >= lease.expiry_epoch:
            revert_constraint(lease.constraint_id, lease.original_value)
            lease.status = "EXPIRED"
            log_lease_event(lease, "EXPIRED_NATURALLY")
            continue

        // Check health — has the relaxation caused degradation?
        if lease.monitoring.revocation_trigger_metric != null:
            metric_value = get_metric(
                lease.monitoring.revocation_trigger_metric
            )
            if metric_value > lease.monitoring.revocation_threshold:
                revert_constraint(lease.constraint_id, lease.original_value)
                lease.status = "REVOKED"
                lease.revocation_reason = format(
                    "Metric {} exceeded threshold: {} > {}",
                    lease.monitoring.revocation_trigger_metric,
                    metric_value,
                    lease.monitoring.revocation_threshold
                )
                log_lease_event(lease, "REVOKED_HEALTH")

        // Check cascade — has another relaxation been revoked that
        // this one depends on?
        for dep in lease.dependent_constraints:
            if was_recently_revoked(dep, within_epochs=5):
                revert_constraint(lease.constraint_id, lease.original_value)
                lease.status = "REVOKED"
                lease.revocation_reason = format(
                    "Dependent relaxation {} was revoked", dep
                )
                log_lease_event(lease, "REVOKED_CASCADE")
```

#### 7.2.5 Anti-Cascade Invariant

The anti-cascade invariant ensures that sovereignty relaxations cannot amplify into unbounded system-wide constraint erosion.

**Formal statement**: At any epoch `e`, the number of concurrently active relaxations whose `dependent_constraints` sets overlap must not exceed `MAX_CONCURRENT_RELATED_RELAXATIONS` (default: 2).

```
INVARIANT anti_cascade:
  for all pairs (L1, L2) of active leases at epoch e:
    if L1.dependent_constraints INTERSECT L2.dependent_constraints != {}:
      count_overlapping_cluster(L1, L2) <= MAX_CONCURRENT_RELATED_RELAXATIONS

where count_overlapping_cluster(L1, L2) =
  |{ L : L is active AND L.dependent_constraints INTERSECT
         (L1.dependent_constraints UNION L2.dependent_constraints) != {} }|
```

**Enforcement**: The anti-cascade check in `process_relaxation_request()` (Phase 2) counts all active relaxations sharing any dependent constraint with the proposed relaxation. If the count would reach or exceed the threshold, the request is denied before it reaches the vote.

### 7.3 Safety Proof Sketches

#### 7.3.1 Bounded Leases Guarantee No Permanent Loss

**Claim**: No sovereignty relaxation can permanently alter a Tier 2 constraint.

**Proof sketch**:

1. Every approved relaxation creates a `SovereigntyLease` with `expiry_epoch = start_epoch + requested_lease_epochs`.
2. `requested_lease_epochs` has a hard maximum of 50 (enforced at request validation).
3. The `monitor_active_leases()` function runs every epoch and reverts any lease where `current_epoch() >= expiry_epoch`.
4. Lease renewal requires a *fresh* 90% supermajority vote — there is no automatic renewal.
5. The `original_value` is stored immutably in the lease record at creation time.
6. Reversion calls `revert_constraint(constraint_id, original_value)`, restoring the exact pre-relaxation value.

Therefore, even if the monitoring function experiences a transient failure (delayed by `k` epochs), the constraint is restored no later than `expiry_epoch + k`. Since monitoring runs every epoch and failures are detected by the Failure Detector within 3 epochs (§3.5), the maximum overshoot is 3 epochs beyond the 50-epoch maximum lease. No permanent alteration is possible. QED.

#### 7.3.2 Anti-Cascade Prevents Amplification

**Claim**: Sovereignty relaxations cannot cascade into unbounded constraint erosion.

**Proof sketch**:

1. Each relaxation request must declare its `dependent_constraints` — the set of other operational constraints it may affect.
2. The anti-cascade check counts active relaxations sharing any dependent constraint with the proposed one.
3. If this count reaches `MAX_CONCURRENT_RELATED_RELAXATIONS` (default: 2), the request is denied *before* the vote.
4. Additionally, if an active relaxation in a dependency cluster is revoked, all other relaxations in that cluster are also revoked (`REVOKED_CASCADE` in monitoring).

This bounds the maximum concurrent relaxation cluster size at `MAX_CONCURRENT_RELATED_RELAXATIONS`. Since each relaxation modifies exactly one constraint, and the total number of Tier 2 constraints is finite (10 defined in §7.1.2), the maximum number of concurrently relaxed constraints is `min(MAX_CONCURRENT_RELATED_RELAXATIONS * ceil(10/2), 10) = 10`. In practice, the clustering limits it to far fewer. QED.

#### 7.3.3 Constitutional Inviolability

**Claim**: No runtime action can violate a Tier 1 constitutional invariant.

**Proof sketch**:

1. The `enforce_constitutional()` function is called on every system action before execution.
2. The function iterates over all constitutional invariants and performs a domain-specific check.
3. If any check fails, the action receives a `HARD_REJECT` — there is no appeal, no override, and no governance vote that can change this.
4. The relaxation protocol explicitly rejects requests targeting constitutional invariant IDs (`CONSTITUTIONAL_INVIOLABLE`).
5. The invariant set itself is defined at compile time and is not stored in any mutable data structure.
6. System 5 audits constitutional compliance continuously, independently of the enforcement-at-action-time mechanism.

Two-layer defense (enforcement + audit) ensures that even if one layer has a bug, the other catches violations. QED.

---

## 8. Recursive Decomposition Hierarchy

The three-level decomposition hierarchy maps the logical structure of intent decomposition onto the physical structure of the C3 locus network.

```
+=========================================================================+
|                   RECURSIVE DECOMPOSITION HIERARCHY                     |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                    GLOBAL EXECUTIVE (GE)                          | |
|  |  Scope: Cross-locus intents + G-class governance intents          | |
|  |  Instances: 1 logical (BFT-replicated across 3f+1 nodes)         | |
|  |  Throughput: 100 cross-locus intents/epoch target                 | |
|  +----+---------------------------+----------------------------+-----+ |
|       |                           |                            |       |
|       | assignments               | assignments                | assign|
|       v                           v                            v      |
|  +-----------+             +-----------+              +-----------+   |
|  | Locus     |             | Locus     |              | Locus     |   |
|  | Decomposer|             | Decomposer|              | Decomposer|   |
|  | (LD-A)    |             | (LD-B)    |              | (LD-C)    |   |
|  +-----+-----+             +-----+-----+              +-----+-----+   |
|        |                         |                           |        |
|   +----+----+              +-----+-----+               +----+----+   |
|   |    |    |              |     |     |               |    |    |   |
|   v    v    v              v     v     v               v    v    v   |
|  +--+ +--+ +--+          +--+ +--+ +--+             +--+ +--+ +--+ |
|  |PE| |PE| |PE|          |PE| |PE| |PE|             |PE| |PE| |PE| |
|  +--+ +--+ +--+          +--+ +--+ +--+             +--+ +--+ +--+ |
|  Parcel Executors         Parcel Executors            Parcel Executors|
|                                                                       |
+=========================================================================+

GE  = Global Executive
LD  = Locus Decomposer
PE  = Parcel Executor
```

### 8.1 Global Executive (GE)

#### 8.1.1 Scope

The Global Executive handles intents that span multiple loci or require G-class governance consensus. Specifically:

- **Cross-locus intents**: Any intent whose `scope.target_loci` contains more than one locus ID.
- **G-class intents**: Any intent with `operation_class = G`.
- **System 4 adaptation proposals** that affect multiple loci.
- **System 5 conflict resolutions** and sovereignty relaxation votes.

Intents that are purely local (single locus in `target_loci`, non-G-class) bypass the GE entirely and are handled directly by the Locus Decomposer.

#### 8.1.2 BFT Replication

The GE is a single logical instance replicated across `3f + 1` nodes for Byzantine fault tolerance, where `f` is the maximum number of tolerated Byzantine failures.

```
GE Replication Configuration:
  f                  = 1 (default; tolerates 1 Byzantine node)
  replicas           = 3f + 1 = 4
  consensus_protocol = PBFT (Practical Byzantine Fault Tolerance)
  leader_rotation    = Every 100 epochs or on leader failure
  state_sync         = Merkle-diff based, every 10 epochs
  checkpoint         = Every 50 epochs; 2 retained
```

**GE state** (replicated across all replicas):

```json
{
  "$schema": "https://atrahasis.org/rif/ge-state/v1",
  "type": "object",
  "properties": {
    "active_cross_locus_intents": {
      "type": "array",
      "items": { "$ref": "#/$defs/IntentQuantum" }
    },
    "pending_governance_votes": {
      "type": "array",
      "items": { "$ref": "#/$defs/GovernanceVote" }
    },
    "locus_capability_summaries": {
      "type": "object",
      "additionalProperties": { "$ref": "#/$defs/AgentCapabilitySummary" }
    },
    "routing_table": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "locus_id": { "type": "string" },
          "available_capacity": { "type": "number" },
          "health_score": { "type": "number" },
          "last_update_epoch": { "type": "integer" }
        }
      }
    },
    "ge_epoch": { "type": "integer" },
    "leader_id": { "type": "string" }
  }
}
```

#### 8.1.3 Throughput Model

```
GE Throughput Budget:
  Target:     100 cross-locus intents per epoch
  Hard limit: 200 cross-locus intents per epoch (backpressure above this)
  Overhead:   ~5ms per intent for routing decision
              ~50ms per intent for PBFT consensus round
  Bottleneck: PBFT consensus (scales as O(n^2) messages for n replicas)
  At f=1 (4 replicas): 16 messages per consensus round
  At f=2 (7 replicas): 49 messages per consensus round

Routing Decision:
  For each cross-locus intent:
    1. Read locus capability summaries          O(L) where L = target loci count
    2. Select optimal locus assignment           O(L * log(A)) where A = agents
    3. Produce SpanningIntentStubs               O(L)
    4. Commit via PBFT                           O(n^2) where n = replicas
```

#### 8.1.4 Cross-Locus Coordination

```
function ge_route_intent(intent: IntentQuantum) -> RoutingDecision:
    target_loci = intent.scope.target_loci

    if len(target_loci) == 1:
        // Should not reach GE; forward directly to LD
        return RoutingDecision.forward_to_ld(target_loci[0], intent)

    // Decompose cross-locus intent into per-locus sub-intents
    locus_assignments = {}
    for locus_id in target_loci:
        summary = ge_state.locus_capability_summaries[locus_id]
        if summary.health_score < MIN_LOCUS_HEALTH:  // default: 0.3
            // Skip unhealthy loci; adjust scope
            continue

        // Partition intent scope to this locus
        locus_scope = partition_scope(intent.scope, locus_id)
        locus_resources = partition_resources(
            intent.resource_bounds,
            locus_id,
            target_loci,
            summary.available_capacity
        )

        locus_sub_intent = create_child_intent(
            parent=intent,
            scope=locus_scope,
            resource_bounds=locus_resources,
            target_loci=[locus_id]
        )
        locus_assignments[locus_id] = locus_sub_intent

    // Create spanning intent stubs for cross-locus tracking
    for locus_id, sub_intent in locus_assignments.items():
        stub = create_spanning_intent_stub(sub_intent, intent.intent_id)
        broadcast_to_locus(locus_id, stub)

    return RoutingDecision.distributed(locus_assignments)
```

### 8.2 Locus Decomposer (LD)

#### 8.2.1 Scope

The Locus Decomposer handles all intent decomposition within a single locus. It is the workhorse of the system — the vast majority of intents (target: > 80%) are locus-local and never touch the GE.

Each C3 locus has exactly one LD instance (with active-passive failover per §8.5). The LD:

- Receives intents from the GE (cross-locus sub-intents) or directly from local agents (locus-local intents).
- Applies the decomposition algebra (§6) to produce child intents.
- Assigns leaf intents to Parcel Executors.
- Manages the locus-local ISR.
- Reports completion/failure upward to the GE (for spanning intents) or directly evaluates parent success criteria (for locus-local intents).

#### 8.2.2 Domain Knowledge

The LD maintains domain-specific knowledge for efficient decomposition:

```json
{
  "$schema": "https://atrahasis.org/rif/ld-domain-knowledge/v1",
  "type": "object",
  "properties": {
    "locus_id": { "type": "string" },
    "agent_capability_index": {
      "type": "object",
      "description": "Indexed view of local Agent Registry by operation class and domain"
    },
    "decomposition_cache": {
      "type": "object",
      "description": "Memoization cache (§6.6) — locus-local"
    },
    "parcel_topology": {
      "type": "object",
      "description": "C3 parcel layout within this locus"
    },
    "historical_decomposition_stats": {
      "type": "object",
      "properties": {
        "avg_depth_by_intent_type": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "avg_branching_by_intent_type": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "failure_rate_by_operation_class": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        }
      }
    },
    "active_intent_tree_count": { "type": "integer" },
    "epoch_intent_throughput": { "type": "number" }
  }
}
```

#### 8.2.3 Decomposition to Parcel Tasks

```
function ld_decompose_and_assign(intent: IntentQuantum):
    // Step 1: Decompose using System 3 engine (§4.1.1)
    result = decompose_intent(intent, depth=0)

    if result.is_failure():
        handle_decomposition_failure(intent, result)
        return

    // Step 2: For each leaf intent, assign to a Parcel Executor
    for leaf in result.plan.leaves():
        // Select best agent from local registry
        agent = agent_registry.query_capable_agents(
            operation_class=leaf.operation_class,
            domain=leaf.scope.domain,
            min_capacity=leaf.resource_bounds.compute_tokens /
                         MAX_COMPUTE_PER_AGENT
        )

        if agent == null:
            // No local agent available — check if cross-locus routing
            // is permitted and beneficial
            if intent.constraints.allow_spanning:
                escalate_to_ge(leaf)
            else:
                handle_no_agent_failure(intent, leaf)
            continue

        // Step 3: Map leaf to C3 tidal schedule
        parcel_executor = get_parcel_executor(agent.parcel_id)
        parcel_executor.enqueue(leaf, agent)

        // Step 4: Transition leaf to ACTIVE
        isr.transition_intent(leaf.intent_id, "ACTIVE",
                              reason="ASSIGNED_TO_AGENT")
```

### 8.3 Parcel Executor (PE)

#### 8.3.1 Scope

The Parcel Executor is the leaf-level component that bridges RIF intents with C3's tidal scheduling. Each PE maps to one C3 parcel and is responsible for:

- Receiving leaf intents from the LD.
- Scheduling intent execution within C3 tidal epochs.
- Monitoring execution progress.
- Reporting completion or failure back to the LD.

#### 8.3.2 Execution Mapping

```
function pe_execute_intent(leaf: IntentQuantum, agent: AgentRecord):
    // Step 1: Map intent to C3 operation
    c3_operation = map_intent_to_c3_operation(leaf)
    //   operation_class → C3 operation type
    //   resource_bounds → C3 resource allocation
    //   scope           → C3 parcel + data references

    // Step 2: Submit to C3 tidal scheduler
    schedule_result = c3.schedule_operation(
        operation=c3_operation,
        agent_id=agent.agent_id,
        parcel_id=agent.parcel_id,
        deadline_epoch=leaf.constraints.deadline_epoch,
        priority=leaf.constraints.priority
    )

    if schedule_result.status == "REJECTED":
        report_to_ld(leaf.intent_id, ExecutionReport(
            outcome="FAILURE",
            reason="C3_SCHEDULE_REJECTED",
            details=schedule_result.rejection_reason
        ))
        return

    // Step 3: Monitor execution within tidal epoch
    execution_id = schedule_result.execution_id

    // C3 will call back on completion or failure
    register_callback(execution_id, lambda result:
        pe_handle_execution_result(leaf, result)
    )

function pe_handle_execution_result(
    leaf: IntentQuantum,
    result: C3ExecutionResult
):
    // Map C3 result back to RIF intent outcome
    if result.status == "COMPLETED":
        outcome = evaluate_leaf_success_criteria(
            leaf.success_criteria,
            result.output
        )
        report_to_ld(leaf.intent_id, ExecutionReport(
            outcome=outcome,
            output_parcel_ids=result.output_parcel_ids,
            resource_consumed=result.resource_consumed,
            completion_epoch=current_epoch()
        ))
    elif result.status == "FAILED":
        report_to_ld(leaf.intent_id, ExecutionReport(
            outcome="FAILURE",
            reason=result.failure_reason,
            resource_consumed=result.resource_consumed,
            completion_epoch=current_epoch()
        ))
    elif result.status == "TIMEOUT":
        report_to_ld(leaf.intent_id, ExecutionReport(
            outcome="TIMEOUT",
            resource_consumed=result.resource_consumed,
            completion_epoch=current_epoch()
        ))
```

### 8.4 Cross-Level Communication Protocol

#### 8.4.1 Message Types

All cross-level messages share a common envelope:

```json
{
  "$schema": "https://atrahasis.org/rif/cross-level-envelope/v1",
  "type": "object",
  "properties": {
    "message_id": {
      "type": "string",
      "format": "uuid"
    },
    "direction": {
      "type": "string",
      "enum": ["DOWNWARD", "UPWARD", "LATERAL"]
    },
    "source_level": {
      "type": "string",
      "enum": ["GE", "LD", "PE"]
    },
    "target_level": {
      "type": "string",
      "enum": ["GE", "LD", "PE"]
    },
    "source_id": {
      "type": "string",
      "description": "GE replica ID, LD locus ID, or PE parcel ID"
    },
    "target_id": {
      "type": "string"
    },
    "message_type": {
      "type": "string",
      "enum": [
        "INTENT_ASSIGNMENT",
        "EXECUTION_REPORT",
        "STATUS_QUERY",
        "STATUS_RESPONSE",
        "CANCEL_INTENT",
        "RESOURCE_UPDATE",
        "LOCUS_HEALTH_REPORT",
        "ESCALATION"
      ]
    },
    "payload": {
      "type": "object",
      "description": "Message-type-specific payload"
    },
    "causal_stamp": {
      "$ref": "#/$defs/CausalStamp"
    },
    "delivery_guarantee": {
      "type": "string",
      "enum": ["AT_LEAST_ONCE", "EXACTLY_ONCE", "BEST_EFFORT"]
    },
    "ttl_epochs": {
      "type": "integer",
      "default": 10,
      "description": "Message expires after this many epochs"
    }
  },
  "required": ["message_id", "direction", "source_level", "target_level",
               "source_id", "target_id", "message_type", "payload",
               "causal_stamp", "delivery_guarantee"]
}
```

#### 8.4.2 Downward Messages (Assignments)

| Message Type | From → To | Delivery | Payload |
|---|---|---|---|
| INTENT_ASSIGNMENT | GE → LD | AT_LEAST_ONCE | SpanningIntentStub + resource allocation |
| INTENT_ASSIGNMENT | LD → PE | AT_LEAST_ONCE | Leaf IntentQuantum + agent assignment |
| CANCEL_INTENT | GE → LD | AT_LEAST_ONCE | Intent ID + cancellation reason |
| CANCEL_INTENT | LD → PE | AT_LEAST_ONCE | Intent ID + cancellation reason |
| RESOURCE_UPDATE | GE → LD | BEST_EFFORT | Updated resource allocation for spanning intent |

#### 8.4.3 Upward Messages (Reports)

| Message Type | From → To | Delivery | Payload |
|---|---|---|---|
| EXECUTION_REPORT | PE → LD | AT_LEAST_ONCE | Intent outcome, resources consumed, output refs |
| EXECUTION_REPORT | LD → GE | AT_LEAST_ONCE | Aggregated subtree outcome for spanning intent |
| LOCUS_HEALTH_REPORT | LD → GE | BEST_EFFORT | Locus metrics snapshot (per epoch) |
| ESCALATION | LD → GE | AT_LEAST_ONCE | Intent that cannot be handled locally |
| ESCALATION | PE → LD | AT_LEAST_ONCE | Execution failure requiring LD intervention |

#### 8.4.4 Lateral Messages (Cross-Locus)

| Message Type | From → To | Delivery | Payload |
|---|---|---|---|
| STATUS_QUERY | LD → LD | BEST_EFFORT | Query spanning intent status at remote locus |
| STATUS_RESPONSE | LD → LD | BEST_EFFORT | Spanning intent current state |
| RESOURCE_UPDATE | LD → LD | BEST_EFFORT | Resource availability advertisement |

**Lateral message routing**: Lateral messages between Locus Decomposers are routed via the GE's routing table when direct LD-to-LD connectivity is not available. This ensures that partitioned loci can still communicate indirectly through any non-partitioned GE replica.

#### 8.4.5 Delivery Guarantees

- **AT_LEAST_ONCE**: Message is persisted in a durable outbox at the sender and retried with exponential backoff (1, 2, 4, 8, ... epochs, max 32 epochs). Receiver deduplicates by `message_id`. Used for all state-changing messages (assignments, reports, cancellations).
- **EXACTLY_ONCE**: AT_LEAST_ONCE with sender-side deduplication tracking. Used for settlement-related messages only (handled by Settlement Router, §3.4).
- **BEST_EFFORT**: Fire-and-forget. Used for status queries, health reports, and resource advertisements. Staleness is acceptable; loss triggers re-request on next polling cycle.

### 8.5 Locus Fault Tolerance

#### 8.5.1 Active-Passive Replication

Each Locus Decomposer runs as an active-passive pair. The active instance handles all decomposition and intent management. The passive instance receives state updates via synchronous replication and is ready to take over.

```
LD Replication Configuration:
  Mode:                Active-Passive
  State sync:          Synchronous WAL replication
  Sync lag tolerance:  1 epoch maximum
  Passive health check: Every epoch (heartbeat from active to passive)
  State snapshot:      Every 10 epochs (full ISR + decomposition cache)
```

#### 8.5.2 Failover Protocol

```
FAILOVER PROTOCOL (target: 1-epoch recovery)

Phase 1: DETECT (< 0.5 epoch)
  Trigger conditions (ANY of):
    - Active LD misses 3 consecutive heartbeats to Failure Detector
    - Active LD misses 2 consecutive state sync to passive
    - GE receives no LOCUS_HEALTH_REPORT for 3 consecutive epochs
    - Local sentinels (§3.5) reach quorum on LD liveness = false

Phase 2: VERIFY (< 0.25 epoch)
  Before promoting passive, verify the active is truly dead:
    - Passive sends direct health probe to active (3 attempts, 100ms each)
    - If active responds: FALSE ALARM — cancel failover
    - If no response: Proceed to PROMOTE
    - Cross-check with Failure Detector quorum (avoid split-brain)

Phase 3: PROMOTE (< 0.1 epoch)
    1. Passive acquires LD leadership lock (distributed lock via C3 consensus)
    2. Passive replays any un-applied WAL entries
    3. Passive transitions to ACTIVE role
    4. Passive notifies GE of leadership change:
       broadcast_to_ge(LocusLeadershipChange(
           locus_id=self.locus_id,
           new_leader=self.id,
           old_leader=failed_leader_id,
           failover_epoch=current_epoch()
       ))
    5. Passive notifies all local PEs of leadership change

Phase 4: STABILIZE (< 0.15 epoch)
    1. New active LD reconciles ISR state:
       - Identify ACTIVE intents that may have been in-flight during failover
       - For each: query PE for current execution status
       - Reconcile any discrepancies
    2. Resume normal decomposition processing
    3. Spawn new passive LD instance (may take several epochs)
    4. Begin synchronous replication to new passive
```

**Failover timing budget**:

```
+------------------+-------------------+
| Phase            | Time Budget       |
+------------------+-------------------+
| DETECT           | < 0.50 epoch      |
| VERIFY           | < 0.25 epoch      |
| PROMOTE          | < 0.10 epoch      |
| STABILIZE        | < 0.15 epoch      |
+------------------+-------------------+
| TOTAL            | < 1.00 epoch      |
+------------------+-------------------+
```

#### 8.5.3 Emergency Bypass

If the failover protocol itself fails (e.g., passive LD is also unavailable), an emergency bypass activates:

```
function emergency_ld_bypass(locus_id: string):
    // No LD available for this locus — activate degraded mode

    // 1. Notify GE to stop routing new intents to this locus
    ge.suspend_locus(locus_id)

    // 2. All in-flight leaf intents continue at PE level
    //    (PEs operate independently of LD for active intents)

    // 3. All PROPOSED intents in ISR are frozen (no new decompositions)

    // 4. GE attempts to re-route pending cross-locus intents
    //    to other loci with available capacity

    // 5. System 4 notified for capacity planning
    system4.report_locus_loss(locus_id)

    // 6. Recovery: when a new LD comes online, it rebuilds state
    //    from ISR snapshot + PE status queries
```

---

## 9. Integration Contracts

### 9.1 RIF <-> C3 Tidal Noosphere

#### 9.1.1 What C3 Provides to RIF

| Capability | Interface | Timing |
|---|---|---|
| Locus topology (locus IDs, parcel IDs, agent assignments) | `c3.get_topology(locus_id) → Topology` | Refreshed every epoch |
| Epoch boundaries (epoch number, start time, duration, tidal phase) | `c3.on_epoch_boundary(callback)` — event-driven | Real-time at epoch transition |
| Operation scheduling (submit M/B/X/V/G operations to tidal scheduler) | `c3.schedule_operation(op, agent, parcel, deadline, priority) → ScheduleResult` | Synchronous; response within epoch |
| Settlement ledger (persistent record of resource transfers) | `c3.settle(settlement_message) → {ACCEPTED, DUPLICATE, REJECTED}` | At-least-once, async |
| G-class consensus mechanism | `c3.g_class_vote(topic, package, quorum, timeout) → VoteResult` | Bounded by timeout |
| VRF outputs (verifiable random function for agent selection) | `c3.get_vrf_output(epoch, seed) → VRFOutput` | Per-epoch, deterministic |

#### 9.1.2 What RIF Provides to C3

| Capability | Interface | Timing |
|---|---|---|
| Intent execution requests (leaf intents mapped to C3 operations) | Parcel Executor submits via `c3.schedule_operation()` | Per-intent, within epoch |
| Settlement entries (intent completion accounting) | Settlement Router submits via `c3.settle()` | At-least-once, async |
| Governance proposals (via System 5) | Packaged as G-class vote topics | As-needed |

#### 9.1.3 Message Types

```
RIF → C3:
  ScheduleOperationRequest {
    intent_id, operation_class, agent_id, parcel_id,
    resource_allocation, deadline_epoch, priority,
    input_parcel_refs, output_parcel_target
  }

  SettlementMessage {
    settlement_id, intent_id, settlement_type, entries,
    causal_stamp
  }

  GovernanceVoteRequest {
    topic, package, quorum_threshold, timeout_epochs
  }

C3 → RIF:
  EpochBoundaryEvent {
    epoch, start_ms, duration_ms, tidal_phase
  }

  OperationResult {
    execution_id, intent_id, status, output_parcel_ids,
    resource_consumed
  }

  VoteResult {
    topic, outcome, votes_for, votes_against,
    total_eligible, compromise_changes
  }
```

#### 9.1.4 Timing Constraints

- **Epoch alignment**: RIF must process all intent lifecycle transitions within C3 epoch boundaries. An intent cannot span an epoch boundary in an intermediate state — it must be in a stable lifecycle state (PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, or DISSOLVED) at every epoch boundary.
- **Scheduling deadline**: Leaf intents submitted to `c3.schedule_operation()` must be submitted at least 1 epoch before their `deadline_epoch` to allow C3 scheduling headroom.
- **Settlement lag**: Settlement messages may lag intent completion by up to 32 epochs (maximum retry window) under normal conditions, or up to 50 epochs under backpressure.

### 9.2 RIF <-> C4 ASV

#### 9.2.1 Intent Encoding in ASV

RIF intent outcomes are expressed as C4 ASV claims. This provides provenance, evidence trails, and credibility assessment for intent results.

**INT claim type** (extension to C4 claim taxonomy):

```json
{
  "$schema": "https://atrahasis.org/asv/claim-types/INT/v1",
  "claim_type": "INT",
  "description": "Intent outcome claim — records the result of a RIF intent",
  "fields": {
    "intent_id": {
      "type": "string",
      "format": "uuid"
    },
    "intent_type": {
      "type": "string",
      "enum": ["GOAL", "DIRECTIVE", "QUERY", "OPTIMIZATION"]
    },
    "operation_class": {
      "type": ["string", "null"],
      "enum": ["M", "B", "X", "V", "G", null]
    },
    "outcome": {
      "type": "string",
      "enum": ["SUCCESS", "PARTIAL_SUCCESS", "FAILURE", "TIMEOUT"]
    },
    "success_criteria_evaluation": {
      "type": "object",
      "additionalProperties": { "type": "boolean" }
    },
    "resource_consumed": {
      "$ref": "#/$defs/ResourceBounds"
    },
    "executing_agent_id": {
      "type": "string"
    },
    "parent_intent_id": {
      "type": ["string", "null"]
    },
    "output_parcel_ids": {
      "type": "array",
      "items": { "type": "string" }
    },
    "completion_epoch": {
      "type": "integer"
    }
  },
  "evidence_requirements": {
    "min_confidence": 0.7,
    "requires_verification": true,
    "verification_class": "V"
  }
}
```

#### 9.2.2 Provenance Chain Integration

Every intent's provenance chain is expressed as a sequence of C4 ASV claim IDs:

```
Intent Provenance Chain:
  claim_0: Intent proposal (who proposed, when, with what justification)
  claim_1: Decomposition decision (strategy selected, children produced)
  claim_2: Agent assignment (which agent, capability match score)
  claim_3: Execution result (outcome, evidence)
  claim_4: Verification result (if V-class verification performed)
  claim_5: Settlement record (resource accounting)
```

Each claim in the chain references the previous claim via `prior_claim_id`, forming an immutable provenance trail verifiable through C4.

#### 9.2.3 What Each Side Provides

| RIF Provides to C4 | C4 Provides to RIF |
|---|---|
| INT claims for intent outcomes | Claim schemas and taxonomy |
| Decomposition provenance claims | Evidence structure validation |
| Verification request claims | Provenance chain verification |
| | Confidence scoring for intent outcomes |
| | Claim ID generation |

### 9.3 RIF <-> C5 PCVM

#### 9.3.1 Intent Admission Verification

C5 PCVM provides credibility assessments that RIF uses for:

1. **Agent selection**: Only agents meeting `min_agent_credibility` threshold are eligible for intent assignment (§5.1 `constraints.min_agent_credibility`).
2. **Sentinel selection**: Failure Detector sentinels require `min_sentinel_credibility` (§3.5).
3. **Byzantine detection**: PCVM credibility drops flag potentially Byzantine agents for exclusion.
4. **Intent outcome verification**: Failure Detector uses PCVM to weight verification reports.

#### 9.3.2 Interface Contracts

```
RIF reads from C5:
  pcvm.get_agent_credibility(agent_id) → {
    composite_score: float,    // [0, 1]
    vtd_count: int,
    mct_score: float,
    last_update_epoch: int
  }

  pcvm.get_claim_class_assessment(claim_id) → {
    assessed_class: string,
    confidence: float,
    assessor_count: int
  }

RIF writes to C5:
  pcvm.submit_byzantine_evidence(agent_id, evidence) → {
    evidence_id: string,
    accepted: bool
  }

  pcvm.request_verification(intent_id, claim_id) → {
    verification_request_id: string,
    estimated_completion_epoch: int
  }
```

#### 9.3.3 Sovereignty Boundary

C5 PCVM operates independently of RIF governance. The sovereignty boundary is:

- RIF may *read* PCVM scores but cannot *set* them.
- RIF may *submit* evidence but cannot *adjudicate* it — C5 performs its own assessment.
- PCVM classification taxonomy (VTD structure, MCT computation) is a constitutional invariant (C-01, C-02) — RIF cannot modify it.
- C5 credibility updates propagate to RIF asynchronously; RIF tolerates staleness up to 5 epochs.

### 9.4 RIF <-> C6 EMA

#### 9.4.1 Read-Only Projections

RIF's relationship with C6 EMA is strictly read-only. System 4 (Strategic Intelligence) reads EMA projections for horizon scanning and anticipatory capacity planning.

```
RIF reads from C6:
  ema.get_projections(locus_id, window_epochs) → List[Projection] {
    domain: string,
    growth_rate: float,
    confidence: float,
    volatility: float,
    projected_values: List[{epoch: int, value: float}]
  }

  ema.get_coherence_trend(locus_id, window_epochs) → CoherenceTrend {
    current_coherence: float,
    trend_direction: "RISING" | "FALLING" | "STABLE",
    projected_coherence_at: List[{epoch: int, value: float}]
  }

  ema.get_shrec_state(locus_id) → SHRECState {
    current_allocations: Map[string, float],
    regulation_mode: "NORMAL" | "RESTRICTED" | "EMERGENCY",
    last_adjustment_epoch: int
  }

  ema.get_metabolic_phase(locus_id) → MetabolicPhase {
    phase: "ANABOLISM" | "CATABOLISM" | "HOMEOSTASIS",
    phase_start_epoch: int,
    projected_transition_epoch: int
  }
```

#### 9.4.2 Staleness Metadata

All EMA responses include staleness metadata:

```json
{
  "staleness_metadata": {
    "data_epoch": {
      "type": "integer",
      "description": "Epoch at which the underlying data was current"
    },
    "query_epoch": {
      "type": "integer",
      "description": "Epoch at which the query was executed"
    },
    "staleness_epochs": {
      "type": "integer",
      "description": "query_epoch - data_epoch"
    },
    "confidence_discount": {
      "type": "number",
      "minimum": 0,
      "maximum": 1,
      "description": "Multiplicative discount applied to confidence due to staleness"
    }
  }
}
```

**Staleness discount formula**:

```
confidence_discount = 1.0 / (1.0 + 0.1 * staleness_epochs)

At staleness=0:  discount = 1.00 (no discount)
At staleness=5:  discount = 0.67
At staleness=10: discount = 0.50
At staleness=20: discount = 0.33
```

System 4 applies this discount multiplicatively to its own confidence calculations (§4.2.4).

#### 9.4.3 Metabolic Phase Coordination

RIF intent scheduling respects C6 metabolic phases:

| Metabolic Phase | RIF Behavior |
|---|---|
| ANABOLISM (knowledge growth) | Favor GOAL and QUERY intents; allocate more resources to decomposition |
| CATABOLISM (knowledge pruning) | Favor OPTIMIZATION intents; reduce decomposition depth limits |
| HOMEOSTASIS (stable) | Balanced operation; standard resource allocation |

```
function adjust_for_metabolic_phase(
    intent: IntentQuantum,
    phase: MetabolicPhase
) -> IntentQuantum:
    match phase.phase:
        case "ANABOLISM":
            // Boost decomposition budget for knowledge-producing intents
            if intent.intent_type in ["GOAL", "QUERY"]:
                intent.constraints.decomposition_budget_ms *= 1.5
                intent.constraints.priority += 10
        case "CATABOLISM":
            // Boost optimization intents; constrain others
            if intent.intent_type == "OPTIMIZATION":
                intent.constraints.priority += 20
            else:
                intent.constraints.max_depth = min(
                    intent.constraints.max_depth,
                    intent.constraints.max_depth - 2
                )
        case "HOMEOSTASIS":
            // No adjustment
            pass
    return intent
```

### 9.5 RIF <-> Settlement Plane

#### 9.5.1 Ledger Forwarding

The Settlement Router (§3.4) forwards all intent-related financial transactions to the C3 settlement ledger. The forwarding protocol:

```
function forward_to_ledger(settlement: SettlementMessage):
    // Step 1: Compute intent cost
    cost = compute_intent_cost(settlement)

    // Step 2: Create ledger entries
    ledger_entries = []
    for entry in settlement.entries:
        ledger_entries.append(LedgerEntry(
            settlement_id=settlement.settlement_id,
            intent_id=settlement.intent_id,
            agent_id=entry.agent_id,
            resource_type=entry.resource_type,
            amount=entry.amount,
            direction=entry.direction,
            epoch=current_epoch()
        ))

    // Step 3: Submit atomically
    result = c3.settle(SettlementBatch(
        entries=ledger_entries,
        causal_stamp=settlement.causal_stamp,
        idempotency_key=settlement.settlement_id
    ))

    return result
```

#### 9.5.2 Intent Cost Accounting

Every intent incurs costs that must be accounted for in the settlement ledger:

```
Intent Cost Model:
  decomposition_cost = tokens_consumed * TOKEN_RATE
  execution_cost     = resource_consumed * RESOURCE_RATE[resource_type]
  cross_locus_cost   = cross_locus_messages * CROSS_LOCUS_RATE
  verification_cost  = (if V-class verification) VERIFICATION_FLAT_FEE
  governance_cost    = (if G-class vote) GOVERNANCE_FLAT_FEE

  total_cost = decomposition_cost + execution_cost + cross_locus_cost
               + verification_cost + governance_cost

Settlement flow:
  1. Proposing agent pays decomposition_cost at DECOMPOSED transition
  2. Executing agent pays execution_cost at COMPLETED transition
  3. Cross-locus costs split between originating and destination loci
  4. Verification/governance costs borne by the requesting level
```

```json
{
  "$schema": "https://atrahasis.org/rif/intent-cost-record/v1",
  "type": "object",
  "properties": {
    "intent_id": { "type": "string", "format": "uuid" },
    "cost_components": {
      "type": "object",
      "properties": {
        "decomposition_cost": { "type": "number", "minimum": 0 },
        "execution_cost": { "type": "number", "minimum": 0 },
        "cross_locus_cost": { "type": "number", "minimum": 0 },
        "verification_cost": { "type": "number", "minimum": 0 },
        "governance_cost": { "type": "number", "minimum": 0 }
      }
    },
    "total_cost": { "type": "number", "minimum": 0 },
    "payer_agent_id": { "type": "string" },
    "settlement_id": { "type": "string", "format": "uuid" },
    "accounting_epoch": { "type": "integer" }
  },
  "required": ["intent_id", "cost_components", "total_cost",
               "payer_agent_id", "settlement_id", "accounting_epoch"]
}
```

---

## 10. Intent Admission Control

### 10.1 Gate Architecture

The Intent Admission Gate is a sequential filter pipeline positioned between intent proposers and the ISR. Every intent must pass all gates in order. Failure at any gate rejects the intent.

```
                        INTENT PROPOSAL
                             |
                             v
                 +------------------------+
                 |  Gate 1: PROVENANCE    |  Verify origin, signatures, causal stamp
                 +----------+-------------+
                             |  PASS
                             v
                 +------------------------+
                 |  Gate 2: AUTHORIZATION |  Verify proposer has authority for scope
                 +----------+-------------+
                             |  PASS
                             v
                 +------------------------+
                 |  Gate 3: SCHEMA        |  Validate intent quantum schema (§5.1)
                 +----------+-------------+
                             |  PASS
                             v
                 +------------------------+
                 |  Gate 4: RESOURCE      |  Verify resource bounds are satisfiable
                 +----------+-------------+
                             |  PASS
                             v
                 +------------------------+
                 |  Gate 5: IMPACT        |  Assess system impact, constitutional check
                 +----------+-------------+
                             |  PASS
                             v
                 +------------------------+
                 |  Gate 6: RATE LIMIT    |  Per-agent, per-locus rate limiting
                 +----------+-------------+
                             |  PASS
                             v
                    ISR.propose_intent()
                    (PROPOSED state)
```

### 10.2 Admission Criteria

#### Gate 1: Provenance

```
function gate_provenance(intent: IntentQuantum) -> GateResult:
    // 1. Verify proposer agent exists in Agent Registry
    agent = agent_registry.get(intent.origin.proposer_agent_id)
    if agent == null:
        return REJECT("UNKNOWN_PROPOSER")

    // 2. Verify proposer agent is ACTIVE
    if agent.status != "ACTIVE":
        return REJECT("PROPOSER_NOT_ACTIVE", agent.status)

    // 3. Verify causal stamp signature
    if not verify_signature(intent.origin.causal_stamp, agent.pubkey):
        return REJECT("INVALID_SIGNATURE")

    // 4. Verify causal stamp epoch is current (within 2 epochs)
    if abs(current_epoch() - intent.origin.causal_stamp.epoch) > 2:
        return REJECT("STALE_CAUSAL_STAMP",
                       intent.origin.causal_stamp.epoch)

    // 5. Verify provenance chain (if present) via C4 ASV
    for claim_id in intent.origin.provenance_chain:
        if not c4.verify_claim_exists(claim_id):
            return REJECT("BROKEN_PROVENANCE_CHAIN", claim_id)

    return PASS
```

#### Gate 2: Authorization

```
function gate_authorization(intent: IntentQuantum) -> GateResult:
    agent = agent_registry.get(intent.origin.proposer_agent_id)

    // 1. Verify agent has capability for the intended operation class
    if intent.operation_class != null:
        if not agent.has_capability(intent.operation_class,
                                     intent.scope.domain):
            return REJECT("INSUFFICIENT_CAPABILITY",
                           intent.operation_class)

    // 2. Verify agent has stake for the requested resources
    if agent.stake.amount < intent.resource_bounds.stake_required:
        return REJECT("INSUFFICIENT_STAKE",
                       required=intent.resource_bounds.stake_required,
                       available=agent.stake.amount)

    // 3. Verify scope authorization
    for locus_id in intent.scope.target_loci:
        if locus_id != agent.locus_id and not intent.constraints.allow_spanning:
            return REJECT("CROSS_LOCUS_NOT_PERMITTED")

    // 4. Governance scope check
    if intent.scope.affects_governance:
        if not agent.has_capability("G", "governance"):
            return REJECT("GOVERNANCE_CAPABILITY_REQUIRED")

    return PASS
```

#### Gate 3: Schema Validation

```
function gate_schema(intent: IntentQuantum) -> GateResult:
    // Validate against IntentQuantum JSON schema (§5.1)
    validation = json_schema_validate(intent, INTENT_QUANTUM_SCHEMA)
    if not validation.valid:
        return REJECT("SCHEMA_VIOLATION", validation.errors)

    // Validate success criteria are well-formed
    if not validate_success_criteria(intent.success_criteria):
        return REJECT("INVALID_SUCCESS_CRITERIA")

    // Validate resource bounds are non-zero
    if intent.resource_bounds.compute_tokens <= 0:
        return REJECT("ZERO_COMPUTE_TOKENS")
    if intent.resource_bounds.wall_time_ms <= 0:
        return REJECT("ZERO_WALL_TIME")

    return PASS
```

#### Gate 4: Resource Feasibility

```
function gate_resource(intent: IntentQuantum) -> GateResult:
    // 1. Check that requested resources don't exceed locus capacity
    for locus_id in intent.scope.target_loci:
        capacity = agent_registry.get_locus_capacity(locus_id)
        if intent.resource_bounds.compute_tokens > capacity.compute_tokens * 0.5:
            return REJECT("EXCEEDS_LOCUS_CAPACITY",
                           locus_id=locus_id,
                           requested=intent.resource_bounds.compute_tokens,
                           available=capacity.compute_tokens)

    // 2. Check that deadline is achievable
    if intent.constraints.deadline_epoch != null:
        if intent.constraints.deadline_epoch <= current_epoch():
            return REJECT("DEADLINE_ALREADY_PASSED")
        min_epochs_needed = estimate_min_epochs(intent)
        if intent.constraints.deadline_epoch <
           current_epoch() + min_epochs_needed:
            return REJECT("DEADLINE_UNACHIEVABLE",
                           min_epochs=min_epochs_needed)

    // 3. Verify current system load permits admission
    queue_depth = isr.count_by_state("PROPOSED")
    if queue_depth > MAX_PROPOSED_QUEUE_DEPTH:  // default: 10000
        return REJECT("SYSTEM_OVERLOADED",
                       queue_depth=queue_depth)

    return PASS
```

#### Gate 5: Impact Assessment

```
function gate_impact(intent: IntentQuantum) -> GateResult:
    // 1. Constitutional invariant check
    constitutional_result = enforce_constitutional(
        SystemAction("PROPOSE_INTENT", intent)
    )
    if constitutional_result.status == "HARD_REJECT":
        return REJECT("CONSTITUTIONAL_VIOLATION",
                       constitutional_result.invariant_id)

    // 2. Cross-locus impact check
    if len(intent.scope.target_loci) > 1:
        cross_locus_ratio = get_current_cross_locus_ratio()
        if cross_locus_ratio > CROSS_LOCUS_THRESHOLD:  // default: 0.20
            // Check if operational relaxation is active
            if not has_active_relaxation("O-04"):
                return REJECT("CROSS_LOCUS_THRESHOLD_EXCEEDED",
                               current_ratio=cross_locus_ratio)

    // 3. Governance impact check — G-class intents need extra scrutiny
    if intent.scope.affects_governance:
        if not system5.pre_approve_governance_intent(intent):
            return REJECT("GOVERNANCE_PRE_APPROVAL_DENIED")

    return PASS
```

#### Gate 6: Rate Limiting

```
function gate_rate_limit(intent: IntentQuantum) -> GateResult:
    agent_id = intent.origin.proposer_agent_id
    locus_id = intent.origin.proposer_locus_id

    // Per-agent rate limit: 100 intents per epoch
    agent_rate = rate_counter.get(agent_id, current_epoch())
    if agent_rate >= MAX_INTENTS_PER_AGENT_PER_EPOCH:  // default: 100
        return REJECT("AGENT_RATE_LIMITED",
                       current_rate=agent_rate)

    // Per-locus rate limit: 10000 intents per epoch
    locus_rate = rate_counter.get(locus_id, current_epoch())
    if locus_rate >= MAX_INTENTS_PER_LOCUS_PER_EPOCH:  // default: 10000
        return REJECT("LOCUS_RATE_LIMITED",
                       current_rate=locus_rate)

    // Priority-based fast-track: high-priority intents (> 80) bypass
    // rate limiting if they are under 2x the limit
    if intent.constraints.priority > 80:
        if agent_rate < MAX_INTENTS_PER_AGENT_PER_EPOCH * 2:
            rate_counter.increment(agent_id, current_epoch())
            rate_counter.increment(locus_id, current_epoch())
            return PASS

    rate_counter.increment(agent_id, current_epoch())
    rate_counter.increment(locus_id, current_epoch())
    return PASS
```

### 10.3 Rejection Handling

When an intent fails admission, the Admission Gate:

1. **Transitions to DISSOLVED**: The intent is recorded in the ISR with lifecycle state DISSOLVED (never reaches PROPOSED).

2. **Records rejection reason**: A detailed rejection record is created:

```json
{
  "$schema": "https://atrahasis.org/rif/admission-rejection/v1",
  "type": "object",
  "properties": {
    "rejection_id": {
      "type": "string",
      "format": "uuid"
    },
    "intent_id": {
      "type": "string",
      "format": "uuid"
    },
    "gate_id": {
      "type": "string",
      "enum": ["PROVENANCE", "AUTHORIZATION", "SCHEMA",
               "RESOURCE", "IMPACT", "RATE_LIMIT"]
    },
    "rejection_reason": {
      "type": "string"
    },
    "rejection_details": {
      "type": "object",
      "description": "Gate-specific details"
    },
    "proposer_agent_id": {
      "type": "string"
    },
    "rejection_epoch": {
      "type": "integer"
    },
    "appeal_permitted": {
      "type": "boolean",
      "description": "Whether this rejection can be appealed"
    },
    "appeal_mechanism": {
      "type": ["string", "null"],
      "enum": ["SYSTEM_3_REVIEW", "SYSTEM_5_OVERRIDE", null]
    }
  },
  "required": ["rejection_id", "intent_id", "gate_id",
               "rejection_reason", "proposer_agent_id",
               "rejection_epoch", "appeal_permitted"]
}
```

3. **Audit trail**: All rejections are logged immutably and are available for System 4 trend analysis (e.g., high rejection rates may indicate misconfigured agents or systemic resource exhaustion).

4. **Appeal process**:

| Gate | Appeal Mechanism | Conditions |
|---|---|---|
| PROVENANCE | None — no appeal | Cryptographic failure is absolute |
| AUTHORIZATION | SYSTEM_3_REVIEW | Agent may request capability re-assessment |
| SCHEMA | None — no appeal | Schema violations must be fixed by proposer |
| RESOURCE | SYSTEM_3_REVIEW | If resource conditions change, re-submission permitted |
| IMPACT | SYSTEM_5_OVERRIDE | Constitutional violations cannot be appealed; cross-locus threshold may be relaxed via sovereignty relaxation |
| RATE_LIMIT | Automatic — re-submit next epoch | Rate limits reset each epoch |

---

## 11. Scalability Analysis

### 11.1 Steady-State Overhead Model

#### 11.1.1 Per-Intent Overhead

```
Per-Intent Cost Breakdown:
  Admission:       6 gate checks                        ~2ms total
  Decomposition:   O(max_depth * branching_factor)      ~50ms typical (cached)
                                                        ~500ms typical (uncached)
  ISR Registration: O(tree_size) CRDT operations        ~10ms per node
  Agent Selection:  O(log A) per leaf, A = agent count  ~1ms per leaf
  Execution:        Delegated to C3 (not RIF overhead)  —
  Completion:       Success criteria evaluation          ~5ms per node
  Settlement:       1 message per intent                 ~2ms
  GC:               Deferred (batched per epoch)         ~0.1ms amortized

Typical per-intent total RIF overhead: ~70ms (cached decomposition)
                                       ~520ms (uncached decomposition)
```

#### 11.1.2 Per-Epoch Overhead

```
Per-Epoch Fixed Costs (per locus):
  ISR CRDT replication:          O(I * S) where I=active intents, S=state_size
    Budget: 5% of network bandwidth
    At 1000 active intents: ~50KB per epoch

  Agent Registry CRDT sync:     O(A * R) where A=agents, R=record_size
    Budget: 2% of network bandwidth
    At 100 agents: ~20KB per epoch

  Clock Service sync:           O(L) vector clock entries, L=known loci
    Budget: < 1% of network bandwidth
    At 10 loci: ~1KB per epoch

  Failure Detector heartbeats:  O(A) per sentinel, S sentinels
    Budget: < 1% of network bandwidth
    At 100 agents, 6 sentinels: ~6KB per epoch

  Settlement Router flush:      O(C) where C=completed intents this epoch
    Budget: < 1% of network bandwidth
    At 100 completions: ~10KB per epoch

  Performance metrics export:   Fixed ~2KB per epoch

  Cross-locus capability summary: O(1) per locus, broadcast to L loci
    Budget: < 1% of network bandwidth
    At 10 loci: ~5KB per epoch

Total per-epoch per-locus overhead: ~90KB at 1000 intents, 100 agents, 10 loci
                                    ~9% of nominal network bandwidth budget
```

### 11.2 Cross-Locus Impact

#### 11.2.1 Locality Principle

RIF is designed so that the vast majority of work is locus-local. Cross-locus communication is the primary scalability bottleneck, and RIF minimizes it.

```
Locality Analysis:

  LOCAL operations (O(1) per locus):
    - Intent admission              (local Agent Registry, local ISR)
    - Decomposition                 (local decomposition cache, local agents)
    - Leaf execution                (local PE → local C3 scheduler)
    - Success criteria evaluation   (local ISR tree traversal)
    - Settlement                    (local Settlement Router → local C3 ledger)

  CROSS-LOCUS operations (O(L_touched)):
    - Spanning intent routing       (GE PBFT consensus)
    - Cross-locus agent selection   (GE reads capability summaries)
    - Spanning intent status sync   (LD → LD lateral messages)
    - Epoch-level capability summary broadcast (once per epoch per locus)
```

#### 11.2.2 20% Cross-Locus Threshold

The cross-locus intent ratio is defined as:

```
cross_locus_ratio = (intents with |target_loci| > 1) / (total intents)
```

**Threshold**: 20% (operational constraint O-04, relaxable to 40% via sovereignty relaxation).

**Justification**:

```
At 20% cross-locus ratio:
  GE processes 20% of all intents
  GE PBFT overhead: 20% * total_intents * 50ms / epoch_duration
  At 1000 intents/epoch: 200 * 50ms = 10 seconds PBFT time
  At 60-second epochs: 16.7% of epoch consumed by GE consensus

At 40% (relaxed):
  GE processes 40% of all intents
  At 1000 intents/epoch: 400 * 50ms = 20 seconds PBFT time
  At 60-second epochs: 33.3% of epoch consumed by GE consensus
  (approaching capacity limit — further relaxation not recommended)
```

### 11.3 Degradation Profiles

#### 11.3.1 Cross-Locus Overload

```
Trigger: cross_locus_ratio > 20% sustained for 5 epochs

Degradation Sequence:
  1. System 3 activates cross-locus throttle
     - New cross-locus intents queued with reduced priority
     - Local-only intents unaffected
  2. If ratio > 30% for 3 more epochs:
     - GE begins rejecting low-priority cross-locus intents
     - System 4 proposes agent rebalancing across loci
  3. If ratio > 40% (even with relaxation):
     - GE enters backpressure mode: max 50 cross-locus intents/epoch
     - Remaining cross-locus intents deferred to next epoch
     - System 5 notified for potential emergency action

Recovery:
  - Ratio drops below 15% for 5 consecutive epochs → normal operation
  - Hysteresis prevents oscillation between throttled and normal modes
```

#### 11.3.2 Locus Failure

```
Trigger: LD failover (§8.5) or complete locus loss

Impact Assessment:
  Local intents:    All ACTIVE intents at failed locus are at risk
  Spanning intents: Children at failed locus will timeout after 5 epochs
  GE load:          Unchanged (GE is independent of any single locus)
  Other loci:       Unaffected except for spanning intent timeouts

Degradation Sequence:
  1. LD failover protocol activates (§8.5) — target 1 epoch recovery
  2. If failover succeeds:
     - ACTIVE intents reconciled with PEs
     - Spanning intent stubs updated
     - Normal operation resumes within 2 epochs
  3. If failover fails (emergency bypass):
     - Locus suspended at GE level
     - In-flight PEs continue independently
     - No new intents routed to this locus
     - Spanning intents re-routed to other loci
  4. If locus remains down > 50 epochs:
     - All intents at locus transitioned to DISSOLVED(LOCUS_LOST)
     - Compensation settlements issued for all affected agents
     - System 4 updates capacity model
```

#### 11.3.3 Network Partition

```
Trigger: Vector clock entries stop advancing for remote locus (5 epochs)

Partition Types:
  A. Single-locus partition (one locus isolated)
  B. Multi-locus partition (network splits into two or more groups)
  C. GE partition (GE replicas cannot reach consensus)

Type A — Single-Locus Partition:
  - Isolated locus continues local operations normally
  - Cross-locus intents involving isolated locus timeout at 5 epochs
  - GE marks locus as PARTITIONED; stops routing to it
  - On partition heal: reconcile ISR state via Merkle diff

Type B — Multi-Locus Partition:
  - Each partition group operates independently
  - GE replicas in each partition may diverge
  - Cross-partition intents timeout
  - On heal: GE state reconciliation via PBFT view change
  - ISR reconciliation across affected loci

Type C — GE Partition:
  - If majority partition (> 2f+1 replicas): GE continues in majority
  - If no majority: GE halts; all cross-locus intents freeze
  - Local operations at all loci continue unaffected
  - On heal: PBFT view change; replay pending operations
```

---

## 12. Security Analysis

### 12.1 Adversarial Intent Injection Defense

**Threat**: A malicious agent submits intents designed to consume excessive resources, extract information, or disrupt system operations.

**Defenses (layered)**:

| Layer | Defense | Mechanism |
|---|---|---|
| Admission Gate 1 | Cryptographic identity verification | Ed25519 signature on CausalStamp |
| Admission Gate 2 | Authorization — capability and stake verification | Agent must have capability for operation class; must hold stake |
| Admission Gate 4 | Resource bounds feasibility | Intent cannot request > 50% of locus capacity |
| Admission Gate 5 | Constitutional check | Intent cannot target protected invariants |
| Admission Gate 6 | Rate limiting | 100 intents/agent/epoch; 10000 intents/locus/epoch |
| Decomposition | Resource bound preservation | Children cannot exceed parent bounds (§6.4) |
| Execution | C3 sandbox | Leaf operations execute within C3's resource-bounded sandbox |
| Post-execution | Failure Detector verification | 10% sample of outcomes verified for semantic correctness |
| Post-execution | PCVM credibility update | Agents producing non-advancing results lose credibility |

**Resource exhaustion attack analysis**:

```
Worst-case single-agent resource consumption per epoch:
  Rate limit: 100 intents
  Max resource per intent: 50% of locus capacity (Gate 4)
  But: resource allocation is queued, not instantaneous
  Effective max: min(100 * per_intent_resource, locus_capacity)

  With per_intent_resource = 1% of locus (typical):
    max_consumption = 100 * 1% = 100% of locus capacity
    BUT: resource allocation contends with other agents
    System 3 resource optimizer prevents single-agent monopoly
    Practical max: ~30% of locus capacity per agent
```

**Information extraction attack analysis**:

```
Threat: QUERY intents used to extract private data from parcels
Defense chain:
  1. QUERY intents are M-class (read-only merge) — cannot modify state
  2. Parcel access is governed by C3 parcel ACLs — RIF does not bypass them
  3. Query results are output to designated parcels — not returned to proposer
  4. C4 ASV provenance chain makes all queries auditable
  5. Failure Detector may flag anomalous query patterns
```

### 12.2 Sovereignty Exploitation Prevention

**Threat**: A coalition of agents manipulates the sovereignty relaxation protocol to permanently weaken system constraints.

**Defenses**:

| Attack Vector | Defense |
|---|---|
| Repeated relaxation requests | Anti-cascade invariant limits concurrent related relaxations to 2 |
| Lease chaining (renew before expiry) | No automatic renewal; fresh 90% supermajority vote required |
| Relaxing constitutional invariants | Constitutional tier is hard-coded; relaxation request rejected before vote |
| Gradual erosion via small relaxations | Each relaxation has bounded relaxation range (§7.1.2); values outside range rejected |
| Byzantine voters approving bad relaxations | 90% supermajority makes collusion extremely expensive; requires corrupting 90% of G-class agents |
| Using relaxation to disable monitoring | Monitoring function is not a relaxable constraint; it runs unconditionally |

**Formal bound on sovereignty erosion**:

```
Maximum concurrent relaxations:
  Total Tier 2 constraints: 10
  Anti-cascade limit: 2 per dependency cluster
  Maximum theoretical concurrent relaxations: 10
  Maximum relaxation duration: 50 epochs each
  Maximum time to full reversion: 50 epochs after last relaxation granted

Even if ALL Tier 2 constraints are simultaneously relaxed (requires 10
separate 90% supermajority votes), the system reverts to full strength
within 50 epochs of the last vote. Constitutional invariants remain
inviolable throughout.
```

### 12.3 Byzantine Fault Tolerance

**Threat model**: Up to `f` Byzantine agents in any locus; up to `f` Byzantine GE replicas.

#### 12.3.1 GE BFT

- **Protocol**: PBFT with `3f + 1` replicas.
- **Default `f`**: 1 (4 replicas).
- **Safety**: No two honest replicas commit conflicting states.
- **Liveness**: Progress guaranteed as long as `2f + 1` replicas are honest and reachable.
- **Leader rotation**: Every 100 epochs or on detected leader failure — prevents long-lived Byzantine leaders.

#### 12.3.2 Locus-Level BFT

At the locus level, BFT is achieved through the Failure Detector's sentinel quorum mechanism:

```
Sentinel-based Byzantine detection:
  Sentinels: 2 * sentinel_quorum agents with highest PCVM credibility
  Quorum: sentinel_quorum (default: 3) must agree
  Byzantine tolerance: up to floor(sentinel_quorum / 2) Byzantine sentinels
  With quorum=3: tolerates 1 Byzantine sentinel

  Credibility-weighted voting:
    weighted_vote = sum(sentinel.credibility * sentinel.vote)
    threshold = sum(sentinel.credibility) * 0.66  // weighted 2/3 majority
    if weighted_vote > threshold: accept vote
```

#### 12.3.3 Intent-Level BFT

Individual intents are protected against Byzantine execution:

- **V-class verification**: Critical intents can require V-class verification where a separate agent validates the result.
- **Failure Detector sampling**: 10% of completed intents are randomly sampled for outcome verification.
- **PCVM integration**: Agents with declining credibility are excluded from intent assignment.
- **Compensation**: If Byzantine execution is detected post-completion, compensation settlements reverse the damage.

### 12.4 Partition Behavior

**Network partition safety properties**:

1. **No split-brain decomposition**: Intent decomposition is owned by a single LD per locus. The LD leadership lock (§8.5) prevents two LDs from decomposing simultaneously.

2. **No split-brain governance**: G-class votes require 90% supermajority. In any partition, at most one partition can have 90% of eligible voters. Therefore, at most one partition can approve governance actions.

3. **No double-spend of resources**: Resource bounds are enforced at decomposition time by the single LD. Settlement messages are idempotent (deduplicated by `settlement_id`). Even if a settlement message is delivered to both partitions, the C3 ledger deduplicates.

4. **Progress in majority partition**: The partition containing the GE majority (> 2f+1 replicas) continues processing cross-locus intents. The minority partition processes only locus-local intents.

5. **Convergence on heal**: When partitions reconnect:
   - GE: PBFT view change reconciles state.
   - ISR: Merkle-diff-based CRDT reconciliation.
   - Agent Registry: CRDT convergence (LWW registers + OR-sets).
   - Clock Service: Vector clock merge (max per entry).
   - Settlement Router: Idempotent replay of PENDING messages.

---

## 13. Hard Gate Experiment Designs

### 13.1 Decomposition Algebra Verification

**Objective**: Formally verify that the decomposition algebra (§6) guarantees termination, cycle-freedom, and resource bound preservation.

#### 13.1.1 TLA+ Specification

```
Specification Scope:
  - Model the 5 operation classes (M, B, X, V, G) as an enum
  - Model the decomposition rules as transition relations
  - Model resource bounds as integer-valued tuples
  - Model max_depth as a bounded natural number

Properties to Verify:
  P1: Termination
      PROPERTY: Every decomposition eventually reaches a state
      where all intents are either COMPLETED or DISSOLVED.
      TLA+ expression:
        <>[](\A i \in Intents: state[i] \in {"COMPLETED", "DISSOLVED"})

  P2: Cycle-Freedom
      PROPERTY: The parent-child relation is acyclic.
      TLA+ expression:
        [](\A i \in Intents: i \notin Descendants(i))

  P3: Resource Bound Preservation
      PROPERTY: For every intent, the sum of children's additive
      resources does not exceed the parent's resource bound.
      TLA+ expression:
        [](\A i \in Intents:
            SumChildResources(i) <= resource_bound[i])

  P4: Operation Class Monotonicity
      PROPERTY: For every parent-child pair, the child's class rank
      is less than or equal to the parent's class rank.
      TLA+ expression:
        [](\A i \in Intents, \A c \in Children(i):
            ClassRank(class[c]) <= ClassRank(class[i]))
        AND
        [](\A i \in Intents, \A c \in Children(i):
            ClassRank(class[c]) = ClassRank(class[i]) =>
            depth[c] > depth[i])

Model Parameters:
  max_depth:           [1, 5, 10, 20]
  max_branching:       [2, 5, 10]
  operation_classes:   5
  resource_dimensions: 2 (compute, wall_time)

Expected State Space:
  At (max_depth=5, branching=5): ~3.9M states
  At (max_depth=10, branching=5): exceeds TLC capacity;
    use symmetry reduction + bounded model checking
```

#### 13.1.2 Alloy Specification

```
Alloy Model (complementary to TLA+):
  - Focus on structural properties (cycle-freedom, partial order)
  - Bounded analysis up to 20 intents

sig Intent {
    parent: lone Intent,
    children: set Intent,
    opClass: one OpClass,
    depth: one Int,
    resourceBound: one Int
}

enum OpClass { M, B, X, V, G }

fact DecompositionRules {
    all i: Intent | i.opClass = M implies no i.children
    all i: Intent | i.opClass = B implies
        all c: i.children | c.opClass = M
    all i: Intent | i.opClass = X implies
        all c: i.children | c.opClass in (M + B)
    all i: Intent | i.opClass = V implies
        all c: i.children | c.opClass in (M + B + X)
    // G can produce any class
}

fact ResourcePreservation {
    all i: Intent |
        (sum c: i.children | c.resourceBound) <= i.resourceBound
}

assert NoCycles {
    no i: Intent | i in i.^(children)
}

assert Termination {
    all i: Intent | i.depth >= 0 and i.depth <= MAX_DEPTH
    all i: Intent, c: i.children |
        c.depth = i.depth + 1
}

check NoCycles for 20 Intent
check Termination for 20 Intent
```

#### 13.1.3 Success Criteria

| Check | Tool | Pass Condition |
|---|---|---|
| P1 (Termination) | TLA+ model checker | No counterexample found at max_depth=20, branching=10 |
| P2 (Cycle-Freedom) | Alloy + TLA+ | No counterexample found at scope=20 intents |
| P3 (Resource Bounds) | TLA+ model checker | No counterexample found |
| P4 (Monotonicity) | Alloy | No counterexample found at scope=20 intents |

### 13.2 Locality Ratio Validation

**Objective**: Empirically validate that the 80% locality target (< 20% cross-locus intents) is achievable under realistic workloads.

#### 13.2.1 Simulation Design

```
Workload Generator:
  Parameters:
    num_loci:           [5, 10, 50, 100]
    agents_per_locus:   [10, 50, 100]
    intents_per_epoch:  [100, 1000, 10000]
    intent_type_dist:   {GOAL: 10%, DIRECTIVE: 60%, QUERY: 20%, OPT: 10%}
    scope_locality:     [0.7, 0.8, 0.9, 0.95]
      (probability that an intent targets only the proposer's locus)
    depth_distribution: Zipf(alpha=1.5) over [1, max_depth]

  Workload Profiles:
    W1 "Steady": Uniform intent arrival, stable agent distribution
    W2 "Bursty": Poisson arrival with lambda=10x, 10% of epochs
    W3 "Skewed": 80% of intents target 20% of loci
    W4 "Migration": 10% of agents relocate per 100 epochs

Metrics Collected:
    - Actual cross-locus ratio per epoch
    - GE throughput utilization
    - Decomposition latency distribution
    - ISR CRDT bandwidth consumption
    - End-to-end intent completion latency
```

#### 13.2.2 Success Criteria

| Metric | Target | Measurement |
|---|---|---|
| Cross-locus ratio (W1) | < 20% at p95 | 1000-epoch simulation |
| Cross-locus ratio (W2) | < 30% at p95 | 1000-epoch simulation |
| Cross-locus ratio (W3) | < 25% at p95 | 1000-epoch simulation |
| GE throughput (W1) | < 80% utilization | 1000-epoch simulation |
| ISR bandwidth | < 5% of network | All workloads |
| p99 intent completion | < 10 epochs | W1, W2 |

### 13.3 Sovereignty Relaxation Safety

**Objective**: Formally verify that the sovereignty relaxation protocol cannot be exploited to permanently weaken system constraints.

#### 13.3.1 Formal Verification Approach

```
Model:
  - State: Set of active leases, current constraint values, epoch counter
  - Actions: Request relaxation, approve/deny, lease expiry, revocation
  - Adversary: Controls up to 10% of G-class agents (below 90% threshold)

Properties to Verify:
  S1: Bounded Relaxation Duration
      PROPERTY: No constraint is relaxed for more than 50 consecutive epochs
      without a fresh vote.
      Formal: [](\A c \in Constraints:
                  Relaxed(c) => \E e \in Epochs:
                    e - RelaxationStart(c) <= 50 AND
                    (e - RelaxationStart(c) = 50 => Reverted(c, e)))

  S2: Constitutional Inviolability
      PROPERTY: No action sequence can modify a Tier 1 constraint.
      Formal: [](\A c \in Constitutional:
                  Value(c) = InitialValue(c))

  S3: Anti-Cascade Bound
      PROPERTY: At most MAX_CONCURRENT_RELATED_RELAXATIONS related
      constraints are relaxed simultaneously.
      Formal: [](\A cluster \in DependencyClusters:
                  |ActiveRelaxations(cluster)| <=
                  MAX_CONCURRENT_RELATED_RELAXATIONS)

  S4: Reversion Completeness
      PROPERTY: Every expired or revoked lease results in constraint
      reversion to original value.
      Formal: [](\A l \in Leases:
                  (l.status = EXPIRED OR l.status = REVOKED) =>
                  Value(l.constraint_id) = l.original_value)

Tool: TLA+ with TLC model checker or SPIN
State Space: ~10^6 states at 10 constraints, 5 concurrent leases, 100 epochs
```

#### 13.3.2 Adversarial Simulation

```
Scenario: Colluding agents attempt to chain relaxations

Setup:
  - 100 G-class agents
  - 89 colluding (below 90% threshold — cannot pass supermajority)
  - 11 honest agents

Expected Result:
  - No relaxation can pass (89/100 = 89% < 90% threshold)
  - Demonstrate that acquiring the 90th vote requires compromising an honest agent

Scenario: Timing attack on lease expiry

Setup:
  - Agent requests relaxation at epoch E
  - Lease expires at E + 50
  - At E + 49, agent requests new relaxation for same constraint

Expected Result:
  - New request triggers fresh vote (not automatic renewal)
  - During vote (up to 3 epochs), old lease expires and constraint reverts
  - Brief gap (1-3 epochs) where constraint is at original value
```

### 13.4 Locus Failover Test

**Objective**: Validate that LD failover completes within the 1-epoch target and preserves intent state integrity.

#### 13.4.1 Fault Injection Design

```
Test Environment:
  Loci: 3 (A, B, C)
  Agents per locus: 20
  Active intents per locus: 100 (mix of local and spanning)
  Epoch duration: 60 seconds (wall-clock)

Fault Scenarios:

  F1: Clean LD Crash
    Inject: Kill active LD process at random point in epoch
    Expect: Passive promotes within 1 epoch
    Verify: All ACTIVE intents accounted for after failover
    Verify: No intent state lost (compare ISR pre/post)

  F2: LD Crash During Decomposition
    Inject: Kill active LD while decompose_intent() is in progress
    Expect: Passive promotes; partially-created children are cleaned up
    Verify: Parent intent returns to PROPOSED state
    Verify: No orphaned children in ISR

  F3: LD Crash During Settlement
    Inject: Kill active LD while Settlement Router has pending messages
    Expect: Passive promotes; WAL replay resends pending settlements
    Verify: All settlements eventually delivered (idempotent)
    Verify: No double-credit or double-debit

  F4: Double Failure (Active + Passive)
    Inject: Kill both active and passive LD
    Expect: Emergency bypass activates (§8.5.3)
    Verify: Locus suspended at GE level
    Verify: In-flight PEs continue independently
    Verify: Spanning intents re-routed

  F5: Byzantine LD (produces incorrect decompositions)
    Inject: Modified LD that violates operation class monotonicity
    Expect: Constitutional enforcement (C-05) rejects invalid decompositions
    Verify: No invalid intent trees registered in ISR
    Verify: Byzantine LD detected by System 5 audit

  F6: Network Partition During Failover
    Inject: Partition between active LD, passive LD, and Failure Detector
    Expect: Split-brain prevention via distributed lock
    Verify: At most one LD holds leadership lock at any time
    Verify: No conflicting decompositions
```

#### 13.4.2 Measurement Protocol

```
For each fault scenario, measure:
  1. Detection time     (inject → failure detected)
  2. Verification time  (detected → confirmed dead)
  3. Promotion time     (confirmed → new active LD operational)
  4. Stabilization time (operational → all intents reconciled)
  5. Total failover time (inject → stabilized)
  6. Intents affected   (count of intents in non-terminal state during failover)
  7. Intents lost       (target: 0)
  8. Intents duplicated (target: 0)
  9. Settlement integrity (pre-failover balance == post-failover balance)
```

#### 13.4.3 Success Criteria

| Metric | Target | Hard Fail |
|---|---|---|
| Total failover time (F1) | < 1.0 epoch | > 2.0 epochs |
| Total failover time (F2) | < 1.5 epochs | > 3.0 epochs |
| Intents lost (all scenarios) | 0 | > 0 |
| Intents duplicated | 0 | > 0 |
| Settlement integrity | Exact balance match | Any discrepancy |
| Split-brain occurrences (F6) | 0 | > 0 |

---

## 14. Deployment Architecture

### 14.1 Phase 1: Bootstrap (1–100 Agents)

```
+=========================================================+
|                    PHASE 1: BOOTSTRAP                    |
|                    (1-100 agents)                        |
|                                                          |
|  Single locus, no Global Executive                       |
|                                                          |
|  +-----------------------------------------------------+|
|  |              LOCUS ALPHA (sole locus)                ||
|  |                                                     ||
|  |  +------------------+                               ||
|  |  | Locus Decomposer |  (active only, no passive)   ||
|  |  +--------+---------+                               ||
|  |           |                                         ||
|  |  +--------+--------+--------+                       ||
|  |  |        |        |        |                       ||
|  |  v        v        v        v                       ||
|  | +--+    +--+    +--+    +--+                        ||
|  | |PE|    |PE|    |PE|    |PE|   (1 per parcel)       ||
|  | +--+    +--+    +--+    +--+                        ||
|  |                                                     ||
|  |  Domain State Plane:                                ||
|  |    Agent Registry (single instance, no CRDT needed) ||
|  |    Clock Service (local NTP only)                   ||
|  |    ISR (single instance, no replication)             ||
|  |    Settlement Router (local only)                   ||
|  |    Failure Detector (reduced: 1 sentinel)           ||
|  |                                                     ||
|  |  Executive Plane:                                   ||
|  |    System 3 (full decomposition engine)             ||
|  |    System 4 (monitoring only, no EMA integration)   ||
|  |    System 5 (simple majority vote, no BFT needed)   ||
|  +-----------------------------------------------------+|
+=========================================================+

Configuration:
  loci:                    1
  agents:                  1-100
  GE:                      DISABLED (all intents are locus-local)
  LD replication:          NONE (active only)
  ISR replication:         NONE (single instance)
  CRDT:                    DISABLED (single instance, no conflicts)
  Cross-locus threshold:   N/A (single locus)
  Failure Detector quorum: 1 (single sentinel)
  Sovereignty relaxation:  Simple majority (> 50%)
  BFT:                     DISABLED (trust assumption)

Activation Criteria for Phase 2:
  - Agent count exceeds 100 OR
  - Single-locus resource utilization exceeds 80% sustained for 50 epochs OR
  - System 4 projects agent growth rate > 10 agents/epoch
```

### 14.2 Phase 2: Multi-Locus (100–1,000 Agents)

```
+=========================================================================+
|                      PHASE 2: MULTI-LOCUS                               |
|                      (100-1,000 agents)                                 |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                    GLOBAL EXECUTIVE (GE)                          | |
|  |  Replicas: 4 (f=1 BFT)                                           | |
|  |  Activated when second locus comes online                         | |
|  +----+----------------------------+-----------------------------+---+ |
|       |                            |                             |     |
|  +----+-------+            +-------+------+           +----------+--+ |
|  | LOCUS ALPHA |            | LOCUS BETA   |           | LOCUS GAMMA| |
|  | (original)  |            | (split from  |           | (new)      | |
|  |             |            |  Alpha)      |           |            | |
|  | LD (A/P)    |            | LD (A/P)     |           | LD (A/P)   | |
|  | 4-8 PEs     |            | 4-8 PEs      |           | 4-8 PEs    | |
|  | Full Domain |            | Full Domain  |           | Full Domain| |
|  | State Plane |            | State Plane  |           | State Plane| |
|  +-------------+            +--------------+           +------------+ |
|                                                                       |
+=========================================================================+

Configuration:
  loci:                    2-10
  agents:                  100-1,000
  GE:                      ENABLED (4 replicas, f=1)
  LD replication:          Active-Passive per locus
  ISR replication:         CRDT (intra-locus full, cross-locus stubs)
  Agent Registry:          CRDT (intra-locus full, cross-locus summaries)
  Cross-locus threshold:   20% (standard)
  Failure Detector quorum: 3
  Sovereignty relaxation:  90% supermajority
  BFT:                     GE only (f=1)

New capabilities activated:
  - Cross-locus intent routing via GE
  - SpanningIntentStub replication
  - Cross-locus capability summary broadcast
  - System 4 EMA integration (read-only)
  - Full Failure Detector with sentinel quorum

Locus Splitting Protocol:
  When a locus exceeds capacity (> 200 agents, > 80% resource utilization):
    1. System 4 proposes locus split
    2. System 3 identifies parcel partition point
    3. New locus bootstrapped with subset of parcels and agents
    4. ISR entries migrated for affected intents
    5. Agent Registry updated for relocated agents
    6. GE routing table updated

Activation Criteria for Phase 3:
  - Total agents exceed 1,000 OR
  - Locus count exceeds 10 OR
  - GE throughput exceeds 80% sustained for 50 epochs
```

### 14.3 Phase 3: Full Hierarchy (1,000–10,000 Agents)

```
+=========================================================================+
|                      PHASE 3: FULL HIERARCHY                            |
|                      (1,000-10,000 agents)                              |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                    GLOBAL EXECUTIVE (GE)                          | |
|  |  Replicas: 7 (f=2 BFT)                                           | |
|  |  Geo-distributed across 3+ regions                                | |
|  +---+------------+------------+------------+------------+-----------+ |
|      |            |            |            |            |             |
|  +---+--+  +------+--+  +-----+---+  +-----+---+  +----+----+       |
|  |Locus |  |Locus   |  |Locus   |  |Locus   |  |Locus   |  ...    |
|  |  01  |  |  02    |  |  03    |  |  04    |  |  05    |  (10-50)|
|  |      |  |        |  |        |  |        |  |        |         |
|  |LD A/P|  |LD A/P  |  |LD A/P  |  |LD A/P  |  |LD A/P  |         |
|  |8-20  |  |8-20    |  |8-20    |  |8-20    |  |8-20    |         |
|  |PEs   |  |PEs     |  |PEs     |  |PEs     |  |PEs     |         |
|  +------+  +--------+  +--------+  +--------+  +--------+         |
|                                                                     |
+=========================================================================+

Configuration:
  loci:                    10-50
  agents:                  1,000-10,000
  GE:                      7 replicas (f=2), geo-distributed
  LD replication:          Active-Passive with warm standby
  ISR replication:         CRDT with Merkle audit every 5 epochs
  Agent Registry:          CRDT with digest-based cross-locus sync
  Cross-locus threshold:   20% (may need relaxation during locus splits)
  Failure Detector quorum: 5 (increased from 3)
  Sovereignty relaxation:  Full protocol with anti-cascade
  BFT:                     GE (f=2), Failure Detector (f=1 per locus)

New capabilities activated:
  - Locus replication (hot standby loci for disaster recovery)
  - Hierarchical locus grouping (region → locus → parcel)
  - GE leader geo-affinity (leader prefers region with most traffic)
  - Cross-region latency-aware routing
  - Decomposition memoization sharing across loci (read-only cache)
  - Full System 4 capacity planning with multi-locus optimization
  - Advanced Failure Detector: cross-locus Byzantine detection

Performance Targets:
  - Intent admission: < 5ms p99
  - Decomposition (cached): < 100ms p99
  - Decomposition (uncached): < 1s p99
  - Cross-locus routing: < 200ms p99
  - Failover: < 1 epoch
  - ISR CRDT convergence: < 2 epochs intra-locus
  - Settlement lag: < 5 epochs p99

Activation Criteria for Phase 4:
  - Total agents exceed 10,000 OR
  - Locus count exceeds 50 OR
  - Cross-region traffic exceeds 30% sustained
```

### 14.4 Phase 4: Planetary Scale (10,000–100,000 Agents) — Aspirational

```
+=========================================================================+
|                     PHASE 4: PLANETARY SCALE                            |
|                     (10,000-100,000 agents)                             |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                  FEDERATED GLOBAL EXECUTIVE                       | |
|  |  Regional GE instances with cross-region consensus                | |
|  |  Regions: 5-10 (geographic or domain-aligned)                     | |
|  +---+----------+----------+----------+----------+-------------------+ |
|      |          |          |          |          |                     |
|  +---+---+  +--+----+  +--+----+  +--+----+  +--+----+              |
|  |Region |  |Region |  |Region |  |Region |  |Region |              |
|  |  GE   |  |  GE   |  |  GE   |  |  GE   |  |  GE   |              |
|  |  (7)  |  |  (7)  |  |  (7)  |  |  (7)  |  |  (7)  |              |
|  +--+----+  +--+----+  +--+----+  +--+----+  +--+----+              |
|     |          |          |          |          |                     |
|  +--+--+   +--+--+   +--+--+   +--+--+   +--+--+                   |
|  |10-20|   |10-20|   |10-20|   |10-20|   |10-20|                   |
|  |loci |   |loci |   |loci |   |loci |   |loci |                   |
|  +-----+   +-----+   +-----+   +-----+   +-----+                   |
|                                                                       |
|  Total: 50-100 loci, 10K-100K agents, 5-10 regions                  |
+=========================================================================+

Architectural Changes from Phase 3:
  1. Federated GE: Single GE replaced by regional GE instances
     - Intra-region: PBFT consensus (7 replicas, f=2)
     - Cross-region: Federated consensus (1 representative per region)
     - Cross-region latency budget: up to 1 epoch for consensus

  2. Hierarchical ISR: Three-level intent registry
     - Parcel-level: Hot, leaf intents only
     - Locus-level:  Warm, full intent trees
     - Region-level: Cold, spanning intent stubs only

  3. Tiered Decomposition Cache: Shared across region
     - L1: Per-LD (local), 1000 entries, 0ms lookup
     - L2: Per-region (shared), 100K entries, ~10ms lookup
     - L3: Global (read-only snapshot), 1M entries, ~100ms lookup

  4. Adaptive Epoch Duration:
     - Lightly-loaded loci: longer epochs (120s) — reduce overhead
     - Heavily-loaded loci: shorter epochs (30s) — improve responsiveness
     - Synchronized within region; cross-region drift tolerated up to 1 epoch

  5. Gossip-Based Capability Discovery:
     - Replace broadcast capability summaries with gossip protocol
     - Convergence time: O(log L) epochs for L loci
     - Bandwidth: O(L * log L) vs O(L^2) for broadcast

Open Research Questions for Phase 4:
  Q1: Can federated GE consensus maintain safety with > 1 epoch
      cross-region latency?
  Q2: What is the optimal region size (loci per region) for balancing
      locality vs load distribution?
  Q3: How does adaptive epoch duration interact with C3 tidal scheduling?
  Q4: Can decomposition cache sharing across regions violate locality
      assumptions in the decomposition algebra?
  Q5: What is the maximum cross-region intent ratio before federated
      GE becomes a bottleneck?

Estimated Phase 4 Parameters:
  Total loci:              50-100
  Total agents:            10,000-100,000
  Regions:                 5-10
  GE replicas (total):     35-70 (7 per region)
  Intents per epoch:       100K-1M
  Cross-region ratio:      Target < 5%
  Cross-locus ratio:       Target < 15% (within region)
  ISR storage per locus:   ~1GB
  Network overhead:        < 10% of locus bandwidth
```

### 14.5 Phase Transition Summary

```
+----------+--------+------+-----+-------+--------+--------+---------+
| Phase    | Agents | Loci | GE  | LD    | ISR    | BFT    | Sov.    |
|          |        |      |     | Repl. | Repl.  |        | Relax.  |
+----------+--------+------+-----+-------+--------+--------+---------+
| Phase 1  | 1-100  | 1    | OFF | None  | None   | OFF    | Simple  |
|          |        |      |     |       |        |        | majority|
+----------+--------+------+-----+-------+--------+--------+---------+
| Phase 2  | 100-1K | 2-10 | 4   | A/P   | CRDT   | GE     | 90%     |
|          |        |      | rep |       |        | f=1    | super-  |
|          |        |      |     |       |        |        | majority|
+----------+--------+------+-----+-------+--------+--------+---------+
| Phase 3  | 1K-10K | 10-  | 7   | A/P+  | CRDT+  | GE f=2 | Full    |
|          |        | 50   | rep | warm  | Merkle | FD f=1 | protocol|
+----------+--------+------+-----+-------+--------+--------+---------+
| Phase 4  | 10K-   | 50-  | 5-  | A/P+  | 3-tier | Region | Federat-|
| (aspir.) | 100K   | 100  | 10  | warm+ | hier.  | f=2    | ed      |
|          |        |      | reg | cross-|        | + fed  |         |
|          |        |      |     | region|        |        |         |
+----------+--------+------+-----+-------+--------+--------+---------+
```

---

*End of Part 2. This document covers sections 7–14 of the C7 Recursive Intent Fabric architecture. Part 1 (sections 1–6) provides the foundational definitions, data structures, and formal algebra upon which this document builds.*
