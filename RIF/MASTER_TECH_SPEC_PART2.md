# Recursive Intent Fabric (RIF) — Master Technical Specification

## Part 2: Sections 9–15 and Appendices

**Invention:** C7 — Recursive Intent Fabric (RIF)
**Version:** 1.0
**Date:** 2026-03-10
**Status:** SPECIFICATION
**Continuity:** This document continues directly from Part 1 (sections 1–8). All section cross-references (e.g., §5.1, §6.2) refer to Part 1 unless prefixed with "Part 2."

---

## Table of Contents — Part 2

- 9. Graduated Sovereignty Model
- 10. Recursive Decomposition Hierarchy
- 11. Integration Contracts
- 12. Intent Admission Control
- 13. Scalability and Security
- 14. Deployment Roadmap
- 15. Conclusion
- Appendix A: Complete Intent Quantum JSON Schema
- Appendix B: Decomposition Algebra Formal Rules
- Appendix C: Sovereignty Invariant Catalog
- Appendix D: Message Type Catalog
- Appendix E: Parameter Reference
- Appendix F: Glossary
- Appendix G: Test Vectors

---

## 9. Graduated Sovereignty Model

### 9.1 The Sovereignty Deadlock Problem

Any orchestration layer that coordinates autonomous subsystems faces a fundamental paradox. The subsystems — C3 (Tidal Noosphere), C4 (ASV), C5 (PCVM), C6 (EMA) — were designed to operate with sovereignty over their internal state. C5 alone decides how claims are classified. C6 alone decides when to consolidate knowledge. C3 alone schedules its tidal epochs. If the orchestration layer can override these decisions, sovereignty is illusory; if it cannot, orchestration is impossible.

This is the sovereignty deadlock: absolute sovereignty prevents orchestration, and absolute orchestration destroys sovereignty.

RIF resolves this deadlock not by choosing one extreme but by stratifying the concept itself. Not all sovereignty protections carry the same weight. The immutability of PCVM's classification taxonomy (a property that defines what the system *is*) occupies a fundamentally different category from a preferred SHREC allocation ratio (a tunable parameter). Treating them identically — both inviolable, or both overridable — is the source of the deadlock.

Graduated sovereignty partitions every system parameter into one of three tiers, each with distinct authorization requirements, modification protocols, and reversion semantics.

### 9.2 Three-Tier Formal Specification

```
+=========================================================================+
|                     GRADUATED SOVEREIGNTY MODEL                         |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 1 — CONSTITUTIONAL (Immutable)                              | |
|  |  Authorization: NEVER modifiable at runtime                       | |
|  |  Reversion: N/A — cannot be changed                               | |
|  |  Enforcement: System 5 audit + hard-coded assertion               | |
|  |  Defines: What the system IS                                      | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 2 — OPERATIONAL (Governance-Relaxable)                      | |
|  |  Authorization: 90% G-class supermajority                         | |
|  |  Reversion: Auto-revert after lease (max 50 epochs)               | |
|  |  Enforcement: System 5 vote + lease monitor                       | |
|  |  Defines: How the system NORMALLY operates                        | |
|  +-------------------------------------------------------------------+ |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |  TIER 3 — COORDINATION (Advisory)                                 | |
|  |  Authorization: System 3 may override unilaterally                | |
|  |  Reversion: Continuous adjustment                                 | |
|  |  Enforcement: Performance monitoring + System 4 feedback          | |
|  |  Defines: What the system PREFERS                                 | |
|  +-------------------------------------------------------------------+ |
+=========================================================================+
```

#### 9.2.1 Tier 1 — Constitutional Invariants

Constitutional invariants define properties so fundamental that their violation would constitute a different system entirely. They cannot be relaxed, suspended, or overridden under any circumstances. Violation of a constitutional invariant triggers immediate rejection of the offending action, immutable audit logging, and — if the invariant was somehow bypassed — system halt and rollback.

| ID | Invariant | Description | Cross-Reference | Enforcement |
|---|---|---|---|---|
| C-01 | PCVM Classification Integrity | Claim classification taxonomy immutable at runtime | C5 PCVM §3.1 | System 5 audit; ISR rejects targeting intents |
| C-02 | VTD Immutability | Verified Trust Documents are append-only; no mutation | C5 PCVM §4.2 | Admission Gate §12; ISR hard-reject |
| C-03 | EMA Canonical Source | EMA is sole authority for epistemic quanta; RIF reads only | C6 EMA §2.1 | System 4 interface read-only by construction |
| C-04 | Decomposition Termination | All decompositions terminate in finite steps; max_depth hard cap 20 | §6.2 | System 3 depth guard (hard-coded) |
| C-05 | Operation Class Monotonicity | Children have equal or lower class rank than parent | §6.1 | System 3 assertion in decompose_intent() |
| C-06 | Resource Bound Integrity | Children cannot exceed parent resource envelopes | §6.4 | System 3 validate_resource_partition() |
| C-07 | Provenance Chain Completeness | Every intent transition carries valid CausalStamp traceable via C4 ASV | §3.2, §3.3 | ISR rejects transitions without CausalStamp |
| C-08 | Settlement Completeness | Every COMPLETED intent produces a settlement entry in C3 ledger | §3.4 | Settlement Router at-least-once guarantee |

**Constitutional enforcement pseudocode:**

```
function enforce_constitutional(action: SystemAction) -> EnforcementResult:
    for invariant in CONSTITUTIONAL_INVARIANTS:
        violation = invariant.check(action)
        if violation != null:
            // Log immutably — this attempt is recorded regardless of outcome
            audit_log.append(ConstitutionalViolationAttempt(
                invariant_id = invariant.id,
                action       = action,
                epoch        = current_epoch(),
                violation    = violation
            ))
            // Hard reject — no appeal, no override, no governance vote
            return EnforcementResult.HARD_REJECT(
                invariant_id = invariant.id,
                reason       = violation.description
            )
    return EnforcementResult.PASS
```

The critical design choice is that constitutional enforcement is *two-layered*: the `enforce_constitutional()` function runs inline on every system action (prevention), and System 5 runs a continuous background audit against all ISR state (detection). Even if one layer has a bug, the other catches violations. This defense-in-depth is what makes the "NEVER" guarantee credible rather than aspirational.

#### 9.2.2 Tier 2 — Operational Constraints

Operational constraints govern resource allocations, composition rules, and timing parameters. They represent the system's normal operating envelope — sensible defaults that should hold under typical conditions but may need temporary adjustment during exceptional circumstances.

| ID | Constraint | Default | Relaxation Bounds | Cross-Reference |
|---|---|---|---|---|
| O-01 | VRF Composition Rules | Standard C3 VRF composition | Expanded composition sets | C3 §5.3 |
| O-02 | Metabolic Timing Windows | C6-defined epoch boundaries | Extend/contract up to 2x | C6 §4.1 |
| O-03 | SHREC Allocation Ratios | C6 defaults | Shift within +/-20% | C6 §6.2 |
| O-04 | Cross-Locus Intent Threshold | 20% of locus traffic | Increase to 40% max | §13.2 |
| O-05 | Decomposition Depth Soft Limit | 10 levels | Increase to 15 (hard max 20 per C-04) | §6.5 |
| O-06 | Memoization Cache TTL | 50 epochs | Extend to 100 epochs | §6.6 |
| O-07 | Agent Credibility Floor | 0.5 PCVM score | Lower to 0.3 during capacity shortage | §5.1 |
| O-08 | Settlement Retry Limit | 10 attempts | Increase to 20 during congestion | §3.4 |
| O-09 | Failure Detector Quorum | 3 sentinels | Reduce to 2 during low-agent conditions | §3.5 |
| O-10 | ISR Bandwidth Cap | 5% of locus network | Increase to 8% during high-intent periods | §3.3 |

Each operational constraint has a well-defined relaxation range. The requested relaxed value must fall within this range; requests exceeding the bounds are rejected before reaching the vote. This prevents "relaxation creep" — the gradual widening of bounds through repeated requests.

#### 9.2.3 Tier 3 — Coordination Parameters

Coordination parameters are advisory hints that System 3 may override unilaterally based on operational needs. No governance vote is required. These parameters express preferences, not requirements.

| ID | Parameter | Default | Override Authority |
|---|---|---|---|
| A-01 | Agent Workload Preferences | Agent-declared | System 3 intent assignment |
| A-02 | Preferred Decomposition Strategy | Intent-declared | System 3 strategy selector |
| A-03 | Locus Affinity Hints | Agent-declared | System 3 cross-locus routing |
| A-04 | Priority Boost Requests | Proposer-declared | System 3 queue management |
| A-05 | Output Format Preferences | Intent-declared | Parcel Executor normalization |
| A-06 | Monitoring Verbosity | Locus-default | System 3 performance monitor |

### 9.3 Sovereignty Relaxation Protocol

When operational conditions require temporary deviation from Tier 2 constraints, the Sovereignty Relaxation Protocol activates. The protocol has five phases: Request, Vote, Activation, Monitoring, and Termination.

#### 9.3.1 Request Phase

System 3 or System 4 identifies an operational condition that would benefit from temporarily relaxing a Tier 2 constraint. The requester constructs a formal relaxation request:

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-relaxation-request/v1",
  "type": "object",
  "properties": {
    "request_id":               { "type": "string", "format": "uuid" },
    "requester":                { "type": "string", "enum": ["SYSTEM_3", "SYSTEM_4"] },
    "request_epoch":            { "type": "integer" },
    "constraint_id":            { "type": "string", "description": "O-01 through O-10" },
    "current_value":            { "description": "Current enforced value" },
    "requested_value":          { "description": "Proposed relaxed value" },
    "justification": {
      "type": "object",
      "properties": {
        "trigger_condition":    { "type": "string" },
        "supporting_metrics":   { "type": "array", "items": {
          "type": "object",
          "properties": {
            "metric_name":      { "type": "string" },
            "current_value":    { "type": "number" },
            "threshold_value":  { "type": "number" },
            "window_epochs":    { "type": "integer" }
          }
        }},
        "impact_assessment":    { "type": "string" },
        "risk_if_denied":       { "type": "string" }
      },
      "required": ["trigger_condition", "supporting_metrics",
                    "impact_assessment", "risk_if_denied"]
    },
    "requested_lease_epochs":   { "type": "integer", "minimum": 1, "maximum": 50 },
    "anti_cascade_declaration": {
      "type": "object",
      "properties": {
        "dependent_constraints": { "type": "array", "items": { "type": "string" } },
        "cascade_risk":          { "type": "string", "enum": ["NONE","LOW","MEDIUM","HIGH"] },
        "mitigation":            { "type": "string" }
      },
      "required": ["dependent_constraints", "cascade_risk"]
    }
  },
  "required": ["request_id", "requester", "request_epoch", "constraint_id",
               "current_value", "requested_value", "justification",
               "requested_lease_epochs", "anti_cascade_declaration"]
}
```

#### 9.3.2 Vote Phase

The request undergoes three pre-validation checks before reaching the G-class vote:

```
function process_relaxation_request(
    request: SovereigntyRelaxationRequest
) -> RelaxationOutcome:

    // PRE-CHECK 1: Constitutional guard
    if request.constraint_id in CONSTITUTIONAL_INVARIANTS:
        return DENIED("CONSTITUTIONAL_INVIOLABLE")

    // PRE-CHECK 2: Relaxation bounds
    bounds = OPERATIONAL_CONSTRAINTS[request.constraint_id].relaxation_bounds
    if not bounds.contains(request.requested_value):
        return DENIED("EXCEEDS_RELAXATION_BOUNDS", max=bounds.max)

    // PRE-CHECK 3: Anti-cascade
    active = get_active_relaxations()
    cascade_count = count_related(
        request.anti_cascade_declaration.dependent_constraints, active
    )
    if cascade_count >= MAX_CONCURRENT_RELATED_RELAXATIONS:  // default: 2
        return DENIED("ANTI_CASCADE_LIMIT", active_related=cascade_count)

    // G-CLASS VOTE: 90% supermajority, 3-epoch timeout
    vote_result = c3.g_class_vote(
        topic     = "SOVEREIGNTY_RELAXATION",
        package   = RelaxationVotePackage(request, active, system_health()),
        quorum    = 0.90,
        timeout   = 3  // epochs
    )

    if not vote_result.supermajority_met:
        return DENIED("SUPERMAJORITY_NOT_MET",
                       for=vote_result.votes_for,
                       against=vote_result.votes_against)

    // ACTIVATE LEASE
    lease = SovereigntyLease(
        relaxation_id  = request.request_id,
        constraint_id  = request.constraint_id,
        original_value = request.current_value,
        relaxed_value  = request.requested_value,
        start_epoch    = current_epoch(),
        expiry_epoch   = current_epoch() + request.requested_lease_epochs,
        vote_record    = vote_result,
        status         = "ACTIVE"
    )
    activate_lease(lease)
    return APPROVED(lease)
```

#### 9.3.3 Lease Structure and Lifecycle

Every approved relaxation creates a time-bounded lease. The lease stores the original value immutably — guaranteeing that reversion restores the exact pre-relaxation state.

```json
{
  "$schema": "https://atrahasis.org/rif/sovereignty-lease/v1",
  "type": "object",
  "properties": {
    "relaxation_id":    { "type": "string", "format": "uuid" },
    "constraint_id":    { "type": "string" },
    "original_value":   { "description": "Value to revert to on expiry" },
    "relaxed_value":    { "description": "Currently active relaxed value" },
    "start_epoch":      { "type": "integer" },
    "expiry_epoch":     { "type": "integer" },
    "vote_record": {
      "type": "object",
      "properties": {
        "votes_for":      { "type": "integer" },
        "votes_against":  { "type": "integer" },
        "total_eligible": { "type": "integer" },
        "vote_epoch":     { "type": "integer" }
      }
    },
    "monitoring": {
      "type": "object",
      "properties": {
        "health_check_interval_epochs": { "type": "integer", "default": 5 },
        "revocation_trigger_metric":    { "type": "string" },
        "revocation_threshold":         { "type": "number" }
      }
    },
    "status": { "type": "string", "enum": ["ACTIVE","EXPIRED","REVOKED","SUPERSEDED"] }
  }
}
```

#### 9.3.4 Monitoring and Automatic Reversion

System 5 monitors all active leases every epoch. Three conditions trigger reversion:

```
function monitor_active_leases():
    for lease in get_active_leases():

        // CONDITION 1: Lease expiry (temporal bound)
        if current_epoch() >= lease.expiry_epoch:
            revert_constraint(lease.constraint_id, lease.original_value)
            lease.status = "EXPIRED"
            continue

        // CONDITION 2: Health degradation (operational bound)
        if lease.monitoring.revocation_trigger_metric != null:
            val = get_metric(lease.monitoring.revocation_trigger_metric)
            if val > lease.monitoring.revocation_threshold:
                revert_constraint(lease.constraint_id, lease.original_value)
                lease.status = "REVOKED"
                lease.revocation_reason = "Health metric exceeded threshold"

        // CONDITION 3: Cascade revocation (dependency bound)
        for dep in lease.dependent_constraints:
            if was_recently_revoked(dep, within_epochs=5):
                revert_constraint(lease.constraint_id, lease.original_value)
                lease.status = "REVOKED"
                lease.revocation_reason = "Dependent relaxation revoked"
```

#### 9.3.5 Anti-Cascade Invariant

The anti-cascade invariant prevents sovereignty relaxations from amplifying into unbounded constraint erosion.

**Formal statement:** At any epoch *e*, for all pairs (L1, L2) of active leases, if L1.dependent_constraints intersects L2.dependent_constraints is non-empty, the count of active leases in that overlapping cluster must not exceed `MAX_CONCURRENT_RELATED_RELAXATIONS` (default: 2).

This is enforced at request time (pre-check 3 in §9.3.2) and again at monitoring time (condition 3 in §9.3.4). The request-time check prevents new relaxations from creating oversized clusters. The monitoring-time check revokes existing relaxations if a related relaxation is revoked, preventing orphaned relaxations from persisting in a now-unstable cluster.

### 9.4 Safety Guarantees

#### 9.4.1 No Permanent Sovereignty Loss

**Claim:** No sovereignty relaxation can permanently alter a Tier 2 constraint.

**Proof sketch:**

1. Every approved relaxation creates a lease with `expiry_epoch = start_epoch + requested_lease_epochs`.
2. `requested_lease_epochs` has hard maximum 50 (enforced at request validation).
3. `monitor_active_leases()` runs every epoch; reverts any lease where `current_epoch() >= expiry_epoch`.
4. Lease renewal requires a *fresh* 90% supermajority vote — no automatic renewal exists.
5. `original_value` is stored immutably at lease creation.
6. Even if monitoring experiences transient failure (delayed by *k* epochs), the Failure Detector detects monitor failure within 3 epochs (§3.5), bounding maximum overshoot to `50 + 3 = 53` epochs. No permanent alteration is possible. QED.

#### 9.4.2 No Cascade Amplification

**Claim:** Sovereignty relaxations cannot cascade into unbounded constraint erosion.

**Proof sketch:** The anti-cascade invariant (§9.3.5) bounds cluster size at `MAX_CONCURRENT_RELATED_RELAXATIONS`. With 10 Tier 2 constraints and a cluster limit of 2, the maximum concurrent relaxations is 10 (all constraints relaxed independently). Each has a 50-epoch maximum lease. Full reversion occurs within 50 epochs of the last granted lease. QED.

#### 9.4.3 Constitutional Inviolability

**Claim:** No runtime action can violate a Tier 1 constitutional invariant.

**Proof sketch:** (1) `enforce_constitutional()` runs on every system action before execution. (2) If any constitutional invariant check fails, the action receives HARD_REJECT with no appeal mechanism. (3) The relaxation protocol explicitly rejects requests targeting constitutional IDs before reaching the vote. (4) The invariant set is defined at compile time in an immutable data structure. (5) System 5 continuously audits constitutional compliance independently. Two-layer defense (inline enforcement + background audit) ensures that even a single-layer bug is caught. QED.

---

## 10. Recursive Decomposition Hierarchy

### 10.1 Overview

The three-level decomposition hierarchy maps the logical structure of intent decomposition onto the physical structure of the C3 locus network. Each level has a distinct scope, replication strategy, and failure model.

```
+=========================================================================+
|                   RECURSIVE DECOMPOSITION HIERARCHY                     |
|                                                                         |
|  +-------------------------------------------------------------------+ |
|  |                    GLOBAL EXECUTIVE (GE)                          | |
|  |  Scope: Cross-locus intents + G-class governance                  | |
|  |  Instances: 1 logical (BFT-replicated, 3f+1 nodes)               | |
|  |  Throughput: 100 cross-locus intents/epoch                        | |
|  +----+---------------------------+----------------------------+-----+ |
|       |                           |                            |       |
|       v                           v                            v       |
|  +-----------+             +-----------+              +-----------+    |
|  | Locus     |             | Locus     |              | Locus     |    |
|  | Decomposer|             | Decomposer|              | Decomposer|    |
|  | (LD-A)    |             | (LD-B)    |              | (LD-C)    |    |
|  +-----+-----+             +-----+-----+              +-----+-----+    |
|        |                         |                           |         |
|   +----+----+              +-----+-----+               +----+----+    |
|   v    v    v              v     v     v               v    v    v    |
|  +--+ +--+ +--+          +--+ +--+ +--+             +--+ +--+ +--+  |
|  |PE| |PE| |PE|          |PE| |PE| |PE|             |PE| |PE| |PE|  |
|  +--+ +--+ +--+          +--+ +--+ +--+             +--+ +--+ +--+  |
|  Parcel Executors         Parcel Executors            Parcel Executors |
+=========================================================================+
```

### 10.2 Global Executive (GE)

#### 10.2.1 Scope and Responsibilities

The Global Executive handles only intents that *must* span loci. Specifically:

- **Cross-locus intents:** Any intent whose `scope.target_loci` contains more than one locus ID.
- **G-class intents:** Any intent with `operation_class = G` (governance operations).
- **System 4 adaptation proposals** affecting multiple loci.
- **System 5 conflict resolutions** and sovereignty relaxation votes.

Intents that are purely local (single locus in `target_loci`, non-G-class) bypass the GE entirely. This is the key to sub-linear scaling: if 80%+ of intents are locus-local, 80%+ of the system's work never touches the GE.

#### 10.2.2 BFT Replication

The GE is a single logical instance replicated across `3f + 1` nodes using Practical Byzantine Fault Tolerance (PBFT), where `f` is the maximum tolerated Byzantine failures.

```
GE Replication Configuration:
  f                  = 1 (default; tolerates 1 Byzantine node)
  replicas           = 3f + 1 = 4
  consensus          = PBFT
  leader_rotation    = Every 100 epochs or on leader failure
  state_sync         = Merkle-diff, every 10 epochs
  checkpoint         = Every 50 epochs; 2 retained
```

**GE replicated state includes:** active cross-locus intents, pending governance votes, locus capability summaries, routing table (locus health scores, available capacity), current epoch, and leader ID.

#### 10.2.3 Throughput Model

```
GE Throughput Budget:
  Target:     100 cross-locus intents per epoch
  Hard limit: 200 (backpressure above this)
  Per-intent: ~5ms routing decision + ~50ms PBFT consensus round
  At f=1 (4 replicas): 16 messages per consensus round
  At f=2 (7 replicas): 49 messages per consensus round

Routing Decision for cross-locus intent:
  1. Read locus capability summaries     O(L)       L = target loci
  2. Select optimal locus assignment     O(L*logA)  A = agents
  3. Produce SpanningIntentStubs         O(L)
  4. Commit via PBFT                     O(n^2)     n = replicas
```

### 10.3 Locus Decomposer (LD)

#### 10.3.1 Scope

The Locus Decomposer is the workhorse of the hierarchy. Each C3 locus has exactly one LD instance (with active-passive failover per §10.5). The LD:

- Receives intents from the GE (cross-locus sub-intents) or directly from local agents (locus-local intents).
- Applies the decomposition algebra (§6) to produce child intents.
- Assigns leaf intents to Parcel Executors.
- Manages the locus-local Intent State Registry.
- Reports completion/failure upward to the GE (for spanning intents) or evaluates parent success criteria directly (for locus-local intents).

#### 10.3.2 Domain Knowledge

Each LD maintains domain-specific knowledge for efficient decomposition: a local agent capability index, a memoization cache (§6.6), the C3 parcel topology, historical decomposition statistics (average depth, branching factor, failure rates by operation class), and current throughput metrics. This domain knowledge is what enables locus-local intents to be decomposed without touching the GE.

#### 10.3.3 Decomposition to Parcel Tasks

```
function ld_decompose_and_assign(intent: IntentQuantum):
    // Step 1: Decompose using System 3 engine (§4.1.1)
    result = decompose_intent(intent, depth=0)
    if result.is_failure():
        handle_decomposition_failure(intent, result)
        return

    // Step 2: Assign each leaf intent to a Parcel Executor
    for leaf in result.plan.leaves():
        agent = agent_registry.query_capable_agents(
            operation_class = leaf.operation_class,
            domain          = leaf.scope.domain,
            min_capacity    = leaf.resource_bounds.compute_tokens
        )
        if agent == null:
            if intent.constraints.allow_spanning:
                escalate_to_ge(leaf)    // Cross-locus escalation
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

### 10.4 Parcel Executor (PE)

#### 10.4.1 Scope

The Parcel Executor bridges RIF intents with C3's tidal scheduling. Each PE maps 1:1 to a C3 parcel and handles:

- Receiving leaf intents from the LD.
- Scheduling execution within C3 tidal epochs via `c3.schedule_operation()`.
- Monitoring execution progress via C3 callbacks.
- Reporting completion or failure back to the LD.

#### 10.4.2 Execution Mapping

```
function pe_execute_intent(leaf: IntentQuantum, agent: AgentRecord):
    // Map intent to C3 operation
    c3_op = map_intent_to_c3_operation(leaf)

    // Submit to tidal scheduler
    result = c3.schedule_operation(
        operation = c3_op,
        agent_id  = agent.agent_id,
        parcel_id = agent.parcel_id,
        deadline  = leaf.constraints.deadline_epoch,
        priority  = leaf.constraints.priority
    )

    if result.status == "REJECTED":
        report_to_ld(leaf.intent_id, ExecutionReport(
            outcome = "FAILURE",
            reason  = "C3_SCHEDULE_REJECTED",
            details = result.rejection_reason
        ))
        return

    // Register callback — C3 notifies PE on completion
    register_callback(result.execution_id, lambda res:
        pe_handle_result(leaf, res))

function pe_handle_result(leaf: IntentQuantum, result: C3ExecutionResult):
    match result.status:
        case "COMPLETED":
            outcome = evaluate_leaf_success_criteria(
                leaf.success_criteria, result.output
            )
            report_to_ld(leaf.intent_id, ExecutionReport(
                outcome            = outcome,
                output_parcel_ids  = result.output_parcel_ids,
                resource_consumed  = result.resource_consumed,
                completion_epoch   = current_epoch()
            ))
        case "FAILED":
            report_to_ld(leaf.intent_id, ExecutionReport(
                outcome           = "FAILURE",
                reason            = result.failure_reason,
                resource_consumed = result.resource_consumed
            ))
        case "TIMEOUT":
            report_to_ld(leaf.intent_id, ExecutionReport(
                outcome           = "TIMEOUT",
                resource_consumed = result.resource_consumed
            ))
```

### 10.5 Cross-Level Communication Protocol

All messages between hierarchy levels share a common envelope:

```json
{
  "$schema": "https://atrahasis.org/rif/cross-level-envelope/v1",
  "properties": {
    "message_id":          { "type": "string", "format": "uuid" },
    "direction":           { "enum": ["DOWNWARD", "UPWARD", "LATERAL"] },
    "source_level":        { "enum": ["GE", "LD", "PE"] },
    "target_level":        { "enum": ["GE", "LD", "PE"] },
    "source_id":           { "type": "string" },
    "target_id":           { "type": "string" },
    "message_type":        { "enum": [
      "INTENT_ASSIGNMENT", "EXECUTION_REPORT", "STATUS_QUERY",
      "STATUS_RESPONSE", "CANCEL_INTENT", "RESOURCE_UPDATE",
      "LOCUS_HEALTH_REPORT", "ESCALATION"
    ]},
    "payload":             { "type": "object" },
    "causal_stamp":        { "$ref": "#/$defs/CausalStamp" },
    "delivery_guarantee":  { "enum": ["AT_LEAST_ONCE","EXACTLY_ONCE","BEST_EFFORT"] },
    "ttl_epochs":          { "type": "integer", "default": 10 }
  }
}
```

**Delivery guarantees:**

- **AT_LEAST_ONCE:** Persisted in durable outbox, retried with exponential backoff (1, 2, 4, 8, ... epochs, max 32). Receiver deduplicates by `message_id`. Used for all state-changing messages.
- **EXACTLY_ONCE:** AT_LEAST_ONCE with sender-side deduplication tracking. Used for settlement messages only.
- **BEST_EFFORT:** Fire-and-forget. Used for status queries, health reports, and resource advertisements. Staleness is acceptable.

**Lateral messages** between Locus Decomposers route via the GE's routing table when direct LD-to-LD connectivity is unavailable, ensuring partitioned loci can communicate indirectly through any non-partitioned GE replica.

### 10.6 Locus Fault Tolerance

#### 10.6.1 Active-Passive Replication

Each LD runs as an active-passive pair. The active instance handles all decomposition. The passive receives state updates via synchronous WAL replication (sync lag tolerance: 1 epoch maximum; full ISR snapshot every 10 epochs).

#### 10.6.2 Failover Protocol

```
FAILOVER PROTOCOL (target: 1-epoch total recovery)

Phase 1: DETECT (< 0.5 epoch)
  Trigger (ANY of):
    - Active LD misses 3 consecutive heartbeats
    - Active LD misses 2 consecutive state syncs to passive
    - GE receives no LOCUS_HEALTH_REPORT for 3 epochs
    - Local sentinels reach quorum on LD liveness = false

Phase 2: VERIFY (< 0.25 epoch)
    - Passive sends 3 direct health probes (100ms each) to active
    - If active responds: FALSE ALARM — cancel failover
    - If no response: cross-check with Failure Detector quorum
    - Proceed to PROMOTE only if quorum confirms

Phase 3: PROMOTE (< 0.1 epoch)
    1. Passive acquires LD leadership lock (distributed lock via C3)
    2. Replay un-applied WAL entries
    3. Transition to ACTIVE role
    4. Notify GE of leadership change
    5. Notify all local PEs of leadership change

Phase 4: STABILIZE (< 0.15 epoch)
    1. Reconcile ISR state (query PEs for in-flight intent status)
    2. Resume normal decomposition
    3. Spawn new passive LD instance (may take several epochs)
    4. Begin synchronous replication to new passive
```

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

#### 10.6.3 Emergency Bypass

If both active and passive LD are unavailable, emergency bypass activates:

1. GE suspends the affected locus (no new intents routed to it).
2. In-flight leaf intents continue at PE level (PEs operate independently for active intents).
3. All PROPOSED intents are frozen (no new decompositions).
4. GE re-routes pending cross-locus intents to other loci with available capacity.
5. System 4 is notified for capacity planning.
6. When a new LD comes online, it rebuilds state from ISR snapshot + PE status queries.

---

## 11. Integration Contracts

RIF is a coordination layer, not a self-contained system. It delegates scheduling to C3, provenance to C4, credibility to C5, and knowledge metabolism to C6. This section specifies the bidirectional contracts that make those delegations precise.

### 11.1 RIF <-> C3 Tidal Noosphere

#### 11.1.1 What C3 Provides to RIF

| Capability | Interface | Timing |
|---|---|---|
| Locus topology | `c3.get_topology(locus_id) -> Topology` | Refreshed every epoch |
| Epoch boundaries | `c3.on_epoch_boundary(callback)` — event-driven | Real-time |
| Operation scheduling | `c3.schedule_operation(op, agent, parcel, deadline, priority)` | Synchronous within epoch |
| Settlement ledger | `c3.settle(msg) -> {ACCEPTED, DUPLICATE, REJECTED}` | At-least-once, async |
| G-class consensus | `c3.g_class_vote(topic, package, quorum, timeout) -> VoteResult` | Bounded by timeout |
| VRF outputs | `c3.get_vrf_output(epoch, seed) -> VRFOutput` | Per-epoch, deterministic |

#### 11.1.2 What RIF Provides to C3

| Capability | Interface | Timing |
|---|---|---|
| Leaf intent execution | PE submits via `c3.schedule_operation()` | Per-intent |
| Settlement entries | Settlement Router via `c3.settle()` | At-least-once |
| Governance proposals | Packaged as G-class vote topics | As-needed |

#### 11.1.3 Timing Constraints

- **Epoch alignment:** RIF must complete all intent lifecycle transitions before epoch boundaries. An intent must be in a stable lifecycle state (PROPOSED, DECOMPOSED, ACTIVE, COMPLETED, or DISSOLVED) at every epoch boundary.
- **Scheduling deadline:** Leaf intents must be submitted at least 1 epoch before their `deadline_epoch` to allow C3 scheduling headroom.
- **Settlement lag:** Settlement messages may lag intent completion by up to 32 epochs (normal) or 50 epochs (backpressure).

#### 11.1.4 Message Types

```
RIF -> C3:
  ScheduleOperationRequest { intent_id, operation_class, agent_id,
    parcel_id, resource_allocation, deadline_epoch, priority,
    input_parcel_refs, output_parcel_target }
  SettlementMessage { settlement_id, intent_id, settlement_type,
    entries, causal_stamp }
  GovernanceVoteRequest { topic, package, quorum_threshold, timeout_epochs }

C3 -> RIF:
  EpochBoundaryEvent { epoch, start_ms, duration_ms, tidal_phase }
  OperationResult { execution_id, intent_id, status, output_parcel_ids,
    resource_consumed }
  VoteResult { topic, outcome, votes_for, votes_against,
    total_eligible, compromise_changes }
```

### 11.2 RIF <-> C4 ASV

#### 11.2.1 Intent Encoding in ASV

RIF intent outcomes are expressed as C4 ASV claims via the INT claim type extension:

```json
{
  "$schema": "https://atrahasis.org/asv/claim-types/INT/v1",
  "claim_type": "INT",
  "description": "Intent outcome claim",
  "fields": {
    "intent_id":                     { "type": "string", "format": "uuid" },
    "intent_type":                   { "enum": ["GOAL","DIRECTIVE","QUERY","OPTIMIZATION"] },
    "operation_class":               { "enum": ["M","B","X","V","G", null] },
    "outcome":                       { "enum": ["SUCCESS","PARTIAL_SUCCESS","FAILURE","TIMEOUT"] },
    "success_criteria_evaluation":   { "type": "object", "additionalProperties": { "type": "boolean" } },
    "resource_consumed":             { "$ref": "#/$defs/ResourceBounds" },
    "executing_agent_id":            { "type": "string" },
    "parent_intent_id":              { "type": ["string", "null"] },
    "output_parcel_ids":             { "type": "array", "items": { "type": "string" } },
    "completion_epoch":              { "type": "integer" }
  },
  "evidence_requirements": {
    "min_confidence": 0.7,
    "requires_verification": true,
    "verification_class": "V"
  }
}
```

#### 11.2.2 Provenance Chain Integration

Every intent's provenance chain is a sequence of C4 ASV claim IDs, forming an immutable audit trail:

```
Intent Provenance Chain:
  claim_0: Intent proposal     (who proposed, when, justification)
  claim_1: Decomposition       (strategy selected, children produced)
  claim_2: Agent assignment    (which agent, capability match score)
  claim_3: Execution result    (outcome, evidence)
  claim_4: Verification        (if V-class verification performed)
  claim_5: Settlement record   (resource accounting)
```

Each claim references the previous via `prior_claim_id`, and the full chain is verifiable through C4's provenance verification interface.

### 11.3 RIF <-> C5 PCVM

#### 11.3.1 Intent Admission Verification

C5 PCVM provides credibility assessments that RIF uses for agent selection (min 0.5 score, §5.1), sentinel selection for the Failure Detector (min sentinel credibility, §3.5), Byzantine detection (credibility drops flag agents for exclusion), and intent outcome verification (credibility-weighted reporting).

#### 11.3.2 Interface Contracts

```
RIF reads from C5:
  pcvm.get_agent_credibility(agent_id) -> {
    composite_score, vtd_count, mct_score, last_update_epoch }
  pcvm.get_claim_class_assessment(claim_id) -> {
    assessed_class, confidence, assessor_count }

RIF writes to C5:
  pcvm.submit_byzantine_evidence(agent_id, evidence) -> {
    evidence_id, accepted }
  pcvm.request_verification(intent_id, claim_id) -> {
    verification_request_id, estimated_completion_epoch }
```

#### 11.3.3 Sovereignty Boundary

The sovereignty boundary between RIF and C5 is precise: RIF may *read* PCVM scores but cannot *set* them. RIF may *submit* evidence but cannot *adjudicate* it — C5 performs its own assessment. The PCVM classification taxonomy (VTD structure, MCT computation) is constitutional invariant C-01/C-02. C5 credibility updates propagate asynchronously; RIF tolerates staleness up to 5 epochs.

### 11.4 RIF <-> C6 EMA

#### 11.4.1 Read-Only Projections

RIF's relationship with C6 EMA is strictly read-only. System 4 reads EMA projections for horizon scanning and anticipatory capacity planning:

```
RIF reads from C6:
  ema.get_projections(locus_id, window_epochs) -> List[Projection]
  ema.get_coherence_trend(locus_id, window_epochs) -> CoherenceTrend
  ema.get_shrec_state(locus_id) -> SHRECState
  ema.get_metabolic_phase(locus_id) -> MetabolicPhase
```

#### 11.4.2 Staleness Metadata and Discounting

All EMA responses include staleness metadata. System 4 applies a multiplicative confidence discount:

```
confidence_discount = 1.0 / (1.0 + 0.1 * staleness_epochs)

  staleness=0:   discount = 1.00  (fresh)
  staleness=5:   discount = 0.67
  staleness=10:  discount = 0.50
  staleness=20:  discount = 0.33
```

This discount propagates through all System 4 confidence calculations (§4.2.4), ensuring that stale data automatically receives less weight in strategic decisions.

#### 11.4.3 Metabolic Phase Coordination

RIF intent scheduling respects C6 metabolic phases:

| Phase | RIF Behavior |
|---|---|
| ANABOLISM (growth) | Favor GOAL/QUERY intents; boost decomposition budgets by 1.5x |
| CATABOLISM (pruning) | Favor OPTIMIZATION intents; reduce decomposition depth limits by 2 |
| HOMEOSTASIS (stable) | Balanced operation; standard resource allocation |

This coordination ensures that RIF's intent processing aligns with the broader epistemic metabolism of the system, avoiding situations where RIF aggressively decomposes knowledge-producing goals during a catabolism phase when the system is actively pruning.

### 11.5 RIF <-> Settlement Plane

#### 11.5.1 Intent Cost Accounting

Every intent incurs costs that must be accounted for:

```
Intent Cost Model:
  decomposition_cost = tokens_consumed * TOKEN_RATE
  execution_cost     = resource_consumed * RESOURCE_RATE[type]
  cross_locus_cost   = cross_locus_messages * CROSS_LOCUS_RATE
  verification_cost  = (if V-class) VERIFICATION_FLAT_FEE
  governance_cost    = (if G-class) GOVERNANCE_FLAT_FEE
  total_cost         = sum of all components

Settlement Flow:
  1. Proposing agent pays decomposition_cost at DECOMPOSED transition
  2. Executing agent pays execution_cost at COMPLETED transition
  3. Cross-locus costs split between originating and destination loci
  4. Verification/governance costs borne by requesting level
```

The Settlement Router forwards all intent-related transactions to the C3 settlement ledger atomically, using `settlement_id` as idempotency key to guarantee exactly-once accounting.

---

## 12. Intent Admission Control

### 12.1 Gate Architecture

The Intent Admission Gate is a sequential filter pipeline positioned between intent proposers and the ISR. Every intent must pass all six gates in order. Failure at any gate rejects the intent immediately.

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
                |  Gate 2: AUTHORIZATION |  Verify proposer authority for scope
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 3: SCHEMA        |  Validate IntentQuantum schema
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 4: RESOURCE      |  Verify resource bounds are satisfiable
                +----------+-------------+
                            |  PASS
                            v
                +------------------------+
                |  Gate 5: IMPACT        |  Constitutional check + cross-locus check
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

### 12.2 Admission Criteria

**Gate 1 — Provenance:** Verifies proposer exists in Agent Registry and is ACTIVE, validates Ed25519 signature on CausalStamp, checks CausalStamp epoch is within 2 of current, and verifies provenance chain via C4 ASV.

**Gate 2 — Authorization:** Verifies agent has capability for the intended operation class, confirms sufficient stake for requested resources, checks scope authorization (cross-locus requires explicit `allow_spanning`), and verifies G-class capability for governance-affecting intents.

**Gate 3 — Schema:** Validates intent against the IntentQuantum JSON schema (§5.1), verifies success criteria are well-formed and machine-evaluable, and confirms resource bounds are non-zero.

**Gate 4 — Resource Feasibility:** Checks requested resources do not exceed 50% of any target locus capacity, verifies deadline is achievable given estimated minimum epochs, and confirms current system load (PROPOSED queue depth) is below `MAX_PROPOSED_QUEUE_DEPTH` (default: 10,000).

**Gate 5 — Impact Assessment:** Runs `enforce_constitutional()` to check all constitutional invariants, checks cross-locus ratio against threshold (O-04), and requires System 5 pre-approval for governance-affecting intents.

**Gate 6 — Rate Limiting:** Per-agent: 100 intents/epoch. Per-locus: 10,000 intents/epoch. High-priority intents (priority > 80) get a 2x fast-track allowance.

### 12.3 Security Properties

The six-gate pipeline provides the following security properties:

1. **Identity assurance:** No intent can enter the system without cryptographic proof of origin (Gate 1).
2. **Capability enforcement:** An agent cannot propose work beyond its authorized capabilities (Gate 2).
3. **Well-formedness:** Malformed intents are caught before consuming decomposition resources (Gate 3).
4. **Resource bounding:** No single intent can monopolize locus capacity (Gate 4).
5. **Constitutional protection:** Intents targeting protected invariants are rejected before admission (Gate 5).
6. **Fairness:** Rate limiting prevents any single agent or locus from flooding the system (Gate 6).

### 12.4 Rejection and Appeal

When an intent fails admission, it is recorded in the ISR as DISSOLVED (it never reaches PROPOSED). A detailed rejection record is created including the gate ID, rejection reason, proposer agent ID, epoch, and whether appeal is permitted.

| Gate | Appeal Mechanism | Conditions |
|---|---|---|
| PROVENANCE | None | Cryptographic failure is absolute |
| AUTHORIZATION | SYSTEM_3_REVIEW | Agent may request capability re-assessment |
| SCHEMA | None | Must be fixed by proposer |
| RESOURCE | SYSTEM_3_REVIEW | Re-submission permitted if conditions change |
| IMPACT | SYSTEM_5_OVERRIDE | Constitutional violations: no appeal. Cross-locus: sovereignty relaxation possible |
| RATE_LIMIT | Automatic | Rate limits reset each epoch; re-submit next epoch |

All rejections are logged immutably and available for System 4 trend analysis (e.g., high rejection rates may signal misconfigured agents or systemic resource exhaustion).

---

## 13. Scalability and Security

### 13.1 Overhead Model

#### 13.1.1 Per-Intent Overhead

```
Per-Intent Cost Breakdown:
  Admission (6 gates):                      ~2ms total
  Decomposition (cached):                   ~50ms typical
  Decomposition (uncached):                 ~500ms typical
  ISR Registration (CRDT per tree node):    ~10ms per node
  Agent Selection (per leaf):               ~1ms per leaf
  Execution:                                Delegated to C3
  Success Criteria Evaluation:              ~5ms per node
  Settlement:                               ~2ms per intent
  GC (deferred, batched):                   ~0.1ms amortized

Typical per-intent total RIF overhead:
  Cached decomposition:    ~70ms
  Uncached decomposition:  ~520ms
```

#### 13.1.2 Per-Epoch Overhead (Per Locus)

```
At 1000 active intents, 100 agents, 10 loci:
  ISR CRDT replication:               ~50KB   (5% network budget)
  Agent Registry CRDT sync:           ~20KB   (2% network budget)
  Clock Service sync:                 ~1KB    (<1% network budget)
  Failure Detector heartbeats:        ~6KB    (<1% network budget)
  Settlement Router flush:            ~10KB   (<1% network budget)
  Performance metrics export:         ~2KB    (fixed)
  Cross-locus capability summary:     ~5KB    (<1% network budget)
  ───────────────────────────────────────────────────────────
  Total:                              ~90KB   (~9% of bandwidth)
```

### 13.2 Cross-Locus Bottleneck Analysis

The cross-locus intent ratio is the primary scalability metric:

```
cross_locus_ratio = intents with |target_loci| > 1 / total intents
```

**Threshold:** 20% (operational constraint O-04; relaxable to 40%).

```
At 20% cross-locus (nominal):
  GE processes 200 of 1000 intents/epoch
  PBFT time: 200 * 50ms = 10s
  At 60s epochs: 16.7% of epoch consumed → comfortable

At 40% cross-locus (relaxed maximum):
  GE processes 400 of 1000 intents/epoch
  PBFT time: 400 * 50ms = 20s
  At 60s epochs: 33.3% of epoch consumed → approaching capacity

At >40%:
  System enters degradation mode (§13.3)
```

The locality principle ensures sub-linear scaling: if 80%+ of intents are locus-local, adding loci increases total capacity without proportionally increasing GE load. The system scales as O(L) in total throughput but O(1) in per-locus overhead, as long as the locality assumption holds.

### 13.3 Degradation Profiles

#### 13.3.1 Cross-Locus Overload

```
Trigger: cross_locus_ratio > 20% sustained 5 epochs

Sequence:
  1. System 3 activates cross-locus throttle
     - New cross-locus intents queued at reduced priority
     - Local intents unaffected
  2. If ratio > 30% for 3 more epochs:
     - GE rejects low-priority cross-locus intents
     - System 4 proposes agent rebalancing
  3. If ratio > 40% (even with relaxation):
     - GE enters backpressure: max 50 cross-locus intents/epoch
     - Remaining deferred to next epoch
     - System 5 notified for emergency action

Recovery: ratio drops below 15% for 5 consecutive epochs
Hysteresis: prevents oscillation between throttled/normal modes
```

#### 13.3.2 Locus Failure

```
Trigger: LD failover or complete locus loss

Impact:
  Local intents:     All ACTIVE at failed locus are at risk
  Spanning intents:  Children at failed locus timeout after 5 epochs
  GE load:           Unchanged
  Other loci:        Unaffected except for spanning intent timeouts

Sequence:
  1. LD failover activates (target: 1 epoch)
  2. If failover succeeds: reconcile within 2 epochs
  3. If failover fails: emergency bypass (§10.6.3)
  4. If locus down > 50 epochs: all intents DISSOLVED(LOCUS_LOST),
     compensation settlements issued
```

#### 13.3.3 Network Partition

Three partition types, each with distinct behavior:

- **Single-locus partition:** Isolated locus continues local operations normally. Cross-locus intents involving it timeout at 5 epochs. GE marks locus as PARTITIONED. On heal: ISR reconciliation via Merkle diff.

- **Multi-locus partition:** Each partition group operates independently. GE replicas may diverge between partitions. On heal: PBFT view change + ISR reconciliation.

- **GE partition:** If majority partition (> 2f+1 replicas): GE continues in majority. If no majority: GE halts, all cross-locus intents freeze. Local operations at all loci continue unaffected. On heal: PBFT view change + pending operation replay.

### 13.4 Adversarial Defenses

#### 13.4.1 Intent Injection

A malicious agent submitting intents designed to consume resources, extract information, or disrupt operations faces nine layers of defense:

| Layer | Defense | Mechanism |
|---|---|---|
| Gate 1 | Identity verification | Ed25519 on CausalStamp |
| Gate 2 | Capability + stake | Must hold stake, have capability |
| Gate 4 | Resource cap | Cannot request > 50% locus capacity |
| Gate 5 | Constitutional guard | Cannot target protected invariants |
| Gate 6 | Rate limit | 100/agent/epoch; 10K/locus/epoch |
| Decomposition | Resource preservation | Children cannot exceed parent |
| Execution | C3 sandbox | Resource-bounded execution |
| Post-execution | Failure Detector | 10% sample verification |
| Post-execution | PCVM update | Bad actors lose credibility |

**Worst-case single-agent resource consumption per epoch:** Rate limit of 100 intents, but System 3's resource optimizer prevents single-agent monopoly. Practical maximum: ~30% of locus capacity per agent.

#### 13.4.2 Sovereignty Exploitation

A coalition attempting to permanently weaken constraints faces:

- **Anti-cascade invariant:** Limits concurrent related relaxations to 2.
- **No automatic renewal:** Fresh 90% vote required for each lease.
- **Constitutional hard-coding:** Tier 1 invariants rejected before vote.
- **Bounded relaxation ranges:** Values outside defined range rejected.
- **Supermajority barrier:** Corrupting 90% of G-class agents is extremely expensive.
- **Monitoring independence:** Monitoring function is not a relaxable constraint.

**Formal bound:** Even if ALL 10 Tier 2 constraints are simultaneously relaxed (requiring 10 separate 90% supermajority votes), full reversion occurs within 50 epochs of the last granted lease. Constitutional invariants remain inviolable throughout.

### 13.5 Byzantine Tolerance

#### 13.5.1 GE Level

PBFT with `3f+1` replicas (default f=1, 4 replicas). Safety: no two honest replicas commit conflicting states. Liveness: progress guaranteed with `2f+1` honest and reachable replicas. Leader rotation every 100 epochs prevents long-lived Byzantine leaders.

#### 13.5.2 Locus Level

Sentinel-based detection via the Failure Detector. Sentinels are `2 * sentinel_quorum` agents with highest PCVM credibility. Quorum of 3 (default) tolerates 1 Byzantine sentinel. Credibility-weighted voting with 2/3 weighted majority threshold.

#### 13.5.3 Intent Level

Critical intents use V-class verification (separate agent validates result). 10% of completed intents are randomly sampled for outcome verification. Agents with declining PCVM credibility are excluded from assignment. Compensation settlements reverse damage from detected Byzantine execution.

### 13.6 Partition Safety Properties

1. **No split-brain decomposition:** LD leadership lock prevents two LDs from decomposing simultaneously.
2. **No split-brain governance:** 90% supermajority means at most one partition can approve governance actions.
3. **No double-spend:** Resource bounds enforced at decomposition by single LD; settlement messages idempotent.
4. **Progress in majority partition:** GE majority continues cross-locus processing; minority processes locus-local only.
5. **Convergence on heal:** GE via PBFT view change; ISR via Merkle-diff CRDT; Agent Registry via CRDT convergence; Clock Service via vector clock merge; Settlement Router via idempotent replay.

---

## 14. Deployment Roadmap

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
|  |  Locus Decomposer (active only, no passive)         ||
|  |  4 Parcel Executors                                  ||
|  |  Domain State Plane:                                 ||
|  |    Agent Registry (single instance, no CRDT)         ||
|  |    Clock Service (local NTP only)                    ||
|  |    ISR (single instance, no replication)             ||
|  |    Settlement Router (local only)                    ||
|  |    Failure Detector (1 sentinel)                     ||
|  |  Executive Plane:                                    ||
|  |    System 3 (full decomposition engine)              ||
|  |    System 4 (monitoring only, no EMA integration)    ||
|  |    System 5 (simple majority, no BFT)                ||
|  +-----------------------------------------------------+|
+=========================================================+

Configuration:
  GE:                     DISABLED
  LD replication:         NONE
  ISR replication:        NONE
  BFT:                    DISABLED
  Sovereignty relaxation: Simple majority (>50%)
```

**Activation criteria for Phase 2:** Agent count exceeds 100, OR single-locus utilization exceeds 80% sustained for 50 epochs, OR System 4 projects growth rate > 10 agents/epoch.

### 14.2 Phase 2: Multi-Locus (100–1,000 Agents)

```
+=========================================================================+
|                      PHASE 2: MULTI-LOCUS                               |
|  +-------------------------------------------------------------------+ |
|  |  GLOBAL EXECUTIVE (4 replicas, f=1 BFT)                          | |
|  +----+----------------------------+-----------------------------+---+ |
|       |                            |                             |     |
|  +----+-------+            +-------+------+           +----------+-+  |
|  | LOCUS ALPHA |            | LOCUS BETA   |           | LOCUS GAMMA| |
|  | LD (A/P)    |            | LD (A/P)     |           | LD (A/P)   | |
|  | 4-8 PEs     |            | 4-8 PEs      |           | 4-8 PEs    | |
|  | Full Domain |            | Full Domain  |           | Full Domain| |
|  | State Plane |            | State Plane  |           | State Plane| |
|  +-------------+            +--------------+           +------------+ |
+=========================================================================+

New capabilities:
  - Cross-locus intent routing via GE
  - SpanningIntentStub replication
  - System 4 EMA integration (read-only)
  - Full Failure Detector with sentinel quorum (3)
  - ISR CRDT (intra-locus full, cross-locus stubs)
  - 90% supermajority sovereignty relaxation

Locus Splitting Protocol:
  1. System 4 proposes split when locus > 200 agents or > 80% utilization
  2. System 3 identifies parcel partition point
  3. New locus bootstrapped with subset of parcels and agents
  4. ISR entries migrated; Agent Registry updated; GE routing table updated
```

**Activation criteria for Phase 3:** Total agents exceed 1,000, OR locus count exceeds 10, OR GE throughput exceeds 80% sustained for 50 epochs.

### 14.3 Phase 3: Full Hierarchy (1,000–10,000 Agents)

```
Configuration:
  Loci:                   10-50
  GE:                     7 replicas (f=2), geo-distributed
  LD replication:         Active-Passive with warm standby
  ISR:                    CRDT + Merkle audit every 5 epochs
  Failure Detector:       Quorum 5
  BFT:                    GE f=2, FD f=1 per locus

Performance Targets:
  Intent admission:            < 5ms p99
  Decomposition (cached):     < 100ms p99
  Decomposition (uncached):   < 1s p99
  Cross-locus routing:        < 200ms p99
  Failover:                   < 1 epoch
  ISR CRDT convergence:       < 2 epochs intra-locus
  Settlement lag:              < 5 epochs p99

New capabilities:
  - Hierarchical locus grouping (region -> locus -> parcel)
  - GE leader geo-affinity
  - Cross-region latency-aware routing
  - Decomposition memoization sharing across loci (read-only)
  - Advanced Failure Detector: cross-locus Byzantine detection
```

**Activation criteria for Phase 4:** Total agents exceed 10,000, OR locus count exceeds 50, OR cross-region traffic exceeds 30% sustained.

### 14.4 Phase 4: Planetary Scale (10,000–100,000 Agents) — Aspirational

```
+=========================================================================+
|  FEDERATED GLOBAL EXECUTIVE                                             |
|  5-10 regional GE instances, each 7 replicas (f=2)                     |
|  Cross-region: federated consensus (1 representative per region)        |
+---+----------+----------+----------+----------+------------------------+
    |          |          |          |          |
 Region A   Region B   Region C   Region D   Region E
 10-20 loci 10-20 loci 10-20 loci 10-20 loci 10-20 loci
+=========================================================================+

Architectural Changes:
  1. Federated GE (regional PBFT + cross-region federation)
  2. Hierarchical ISR (parcel/locus/region tiers)
  3. Tiered decomposition cache (L1 local, L2 regional, L3 global)
  4. Adaptive epoch duration (30-120s based on load)
  5. Gossip-based capability discovery (O(L*logL) vs O(L^2))

Estimated Parameters:
  Total loci:            50-100
  Total agents:          10K-100K
  Regions:               5-10
  Intents per epoch:     100K-1M
  Cross-region ratio:    Target < 5%
  ISR storage per locus: ~1GB
  Network overhead:      < 10% of locus bandwidth
```

### 14.5 Hard Gate Experiment Designs

Before progressing from SPECIFICATION to full implementation, four hard gates must be cleared:

**Gate 1: Decomposition Algebra Verification.** TLA+ and Alloy models must prove termination (P1), cycle-freedom (P2), resource bound preservation (P3), and operation class monotonicity (P4). Target state space: up to max_depth=20, branching=10 in TLA+; up to 20 intents in Alloy.

**Gate 2: Locality Ratio Validation.** Simulation across four workload profiles (Steady, Bursty, Skewed, Migration) must demonstrate cross-locus ratio < 20% at p95 under steady workload and < 30% under burst. GE throughput must remain below 80% utilization.

**Gate 3: Sovereignty Relaxation Safety.** Formal verification (TLA+ or SPIN) must prove bounded relaxation duration (S1), constitutional inviolability (S2), anti-cascade bound (S3), and reversion completeness (S4). Adversarial simulation must show that 89% collusion fails to pass the 90% supermajority threshold.

**Gate 4: Locus Failover Latency.** Fault injection across six scenarios (clean crash, crash during decomposition, crash during settlement, double failure, Byzantine LD, partition during failover) must demonstrate total failover time < 1 epoch for clean crash, zero intent loss, zero duplicates, exact settlement balance, and zero split-brain occurrences.

### 14.6 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Cross-locus ratio exceeds 20% | Medium | High | Monitoring flag; agent rebalancing; sovereignty relaxation to 40% |
| Decomposition depth explosion | Low | High | Hard max_depth=20 (constitutional); decomposition budget (time+compute) |
| System 3/4 oscillation | Medium | Medium | Cool-down (5 epochs); similarity detection; 3 stable epochs gate |
| Locus failure cascade | Low | Critical | Active-passive LD; emergency bypass; GE rerouting |
| Byzantine coalition | Very Low | Critical | 90% supermajority; PCVM credibility; two-layer enforcement |
| EMA projection staleness | Medium | Low | Staleness metadata; confidence discounting; volatility awareness |

### 14.7 Phase Transition Summary

```
+--------+--------+------+------+--------+--------+--------+-----------+
| Phase  | Agents | Loci | GE   | LD     | ISR    | BFT    | Sov.      |
|        |        |      |      | Repl.  | Repl.  |        | Relax.    |
+--------+--------+------+------+--------+--------+--------+-----------+
| 1      | 1-100  | 1    | OFF  | None   | None   | OFF    | >50%      |
| 2      | 100-1K | 2-10 | 4rep | A/P    | CRDT   | GE f=1 | 90% super |
| 3      | 1K-10K | 10-50| 7rep | A/P+   | CRDT+  | GE f=2 | Full      |
|        |        |      |      | warm   | Merkle | FD f=1 | protocol  |
| 4*     | 10K+   | 50+  | Fed  | A/P+   | 3-tier | Reg.   | Federated |
|        |        |      | 5-10 | cross- | hier.  | f=2    |           |
|        |        |      | reg  | region |        | + fed  |           |
+--------+--------+------+------+--------+--------+--------+-----------+
* Phase 4 is aspirational; open research questions remain (§15.2).
```

---

## 15. Conclusion

### 15.1 Summary of Contributions

The Recursive Intent Fabric introduces six architectural contributions to the Atrahasis agent system:

**1. Intent Quantum as First-Class Object.** By elevating intents from ephemeral messages to persistent, typed objects with a 5-state lifecycle, RIF makes goals, their decomposition, their execution, and their outcomes all first-class citizens of the system. This enables provenance tracking, resource accounting, and formal reasoning about system behavior — none of which are possible with message-passing orchestration.

**2. Formal Decomposition Algebra.** The operation-class-aware decomposition rules (G->any, V->M/B/X, X->M/B, B->M, M->terminal) with monotonic descent, bounded depth, and resource preservation provide mathematically grounded termination guarantees. This is not a soft claim — it is verifiable via TLA+ and Alloy model checking.

**3. Two-Plane Separation.** By separating domain-scoped infrastructure (replicated per-locus) from executive functions (spanning loci as needed), RIF achieves the critical property that most work is local. The Domain-Scoped State Plane keeps agent registries, intent states, and settlement routing close to where work happens. The Executive Plane (Systems 3/4/5) provides operational control, strategic intelligence, and governance without centralized bottlenecks.

**4. Graduated Sovereignty.** The three-tier sovereignty model resolves the fundamental paradox between subsystem autonomy and orchestration effectiveness. Constitutional invariants are absolutely inviolable. Operational constraints are temporarily relaxable via governance supermajority with bounded leases and automatic reversion. Coordination parameters are advisory. This is more nuanced and more rigorous than either absolute sovereignty or absolute override.

**5. VSM-Aligned Executive.** Mapping System 3 (operational), System 4 (strategic), and System 5 (governance) onto Stafford Beer's Viable System Model provides a theoretically grounded framework for managing the inherent tension between operational efficiency and strategic adaptation. The oscillation dampening mechanisms (cool-down, similarity detection, stability gating) prevent the System 3/4 feedback loop from becoming unstable.

**6. Substrate-Aware Integration.** RIF does not reinvent what the Atrahasis subsystems already provide. It delegates scheduling to C3, provenance to C4, credibility to C5, and knowledge metabolism to C6 — with precisely defined integration contracts, sovereignty boundaries, and staleness handling. This makes RIF a *coordination layer*, not a replacement for any existing subsystem.

### 15.2 Open Research Questions

Several questions remain open for future investigation:

**Q1: Federated GE Consensus Latency.** Can the federated Global Executive (Phase 4) maintain safety properties with cross-region latency exceeding one epoch? The PBFT model assumes bounded network delay, and planetary-scale deployment may violate this assumption.

**Q2: Optimal Region Sizing.** What is the optimal number of loci per region for balancing locality (keeping intents within a region) against load distribution (spreading work across regions)? This is likely workload-dependent and may require adaptive region boundaries.

**Q3: Adaptive Epoch Interaction.** How does adaptive epoch duration (Phase 4) interact with C3's tidal scheduling, which assumes fixed epoch boundaries? Variable epoch lengths may create synchronization challenges at the RIF-C3 boundary.

**Q4: Cross-Region Cache Coherence.** Can decomposition memoization sharing across regions violate locality assumptions in the decomposition algebra? If a cached decomposition plan references agents that exist only in the originating region, the plan may be invalid in the consuming region.

**Q5: Empirical Locality Validation.** The 80% locality assumption (< 20% cross-locus intents) is theoretically motivated but empirically unvalidated. Real workload characterization studies are needed to confirm or refine this target.

**Q6: Compensation Protocol Completeness.** The saga-style compensation protocols for partial decomposition failure require formal verification that compensation actions themselves cannot fail in ways that leave the system in an inconsistent state.

**Q7: Long-Term Sovereignty Dynamics.** While individual sovereignty relaxations are proven bounded, the long-term statistical dynamics of repeated relaxation-reversion cycles have not been analyzed. Could the system develop "relaxation habits" that, while individually safe, collectively shift its operating point?

### 15.3 Relationship to Broader Atrahasis Vision

RIF occupies a specific niche in the Atrahasis architecture: it is the *intent translation layer* that converts high-level goals into concrete, schedulable, accountable work assignments. It sits between the human-facing goal specification interface (above RIF) and the substrate systems that actually execute work (below RIF).

The broader Atrahasis vision — planetary-scale AI coordination with formal governance — requires all seven layers to function in concert: C3 provides the tidal scheduling substrate, C4 provides semantic versioning and provenance, C5 provides credibility assessment, C6 provides epistemic metabolism, and RIF (C7) provides the recursive intent orchestration that ties them together. The remaining inventions in the pipeline will address the layers above and below RIF, completing the full stack.

RIF's graduated sovereignty model, in particular, establishes a pattern that may generalize beyond intent orchestration. Any system that must coordinate autonomous subsystems faces the sovereignty deadlock. The three-tier approach — immutable constitution, governance-relaxable operations, advisory coordination — offers a principled resolution that other Atrahasis components may adopt.

---

## Appendix A: Complete Intent Quantum JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.org/rif/intent-quantum/v1",
  "title": "IntentQuantum",
  "description": "First-class typed object representing a goal, directive, query, or optimization with lifecycle management, decomposition constraints, and resource bounds.",
  "type": "object",
  "properties": {
    "intent_id": {
      "type": "string",
      "description": "Globally unique 256-bit identifier",
      "pattern": "^[0-9a-f]{64}$"
    },
    "intent_type": {
      "type": "string",
      "enum": ["GOAL", "DIRECTIVE", "QUERY", "OPTIMIZATION"],
      "description": "GOAL=open-ended objective, DIRECTIVE=specific instruction, QUERY=information request, OPTIMIZATION=improve existing state"
    },
    "content": {
      "type": "string",
      "description": "Structured intent specification in natural language or domain-specific format"
    },
    "scope": {
      "type": "object",
      "properties": {
        "target_loci":       { "type": "array", "items": { "type": "string" }, "minItems": 1 },
        "domain":            { "type": "string" },
        "affects_governance": { "type": "boolean", "default": false }
      },
      "required": ["target_loci", "domain"]
    },
    "origin": {
      "type": "object",
      "properties": {
        "proposer_agent_id": { "type": "string" },
        "proposer_locus_id": { "type": "string" },
        "causal_stamp": {
          "type": "object",
          "properties": {
            "epoch":          { "type": "integer" },
            "vector_clock":   { "type": "object", "additionalProperties": { "type": "integer" } },
            "signature":      { "type": "string", "description": "Ed25519 signature" }
          },
          "required": ["epoch", "vector_clock", "signature"]
        },
        "provenance_chain":  { "type": "array", "items": { "type": "string" } }
      },
      "required": ["proposer_agent_id", "proposer_locus_id", "causal_stamp"]
    },
    "authorization": {
      "type": ["object", "null"],
      "description": "GovernanceToken; required for cross-locus and G-class intents"
    },
    "decomposition_strategy": {
      "type": "string",
      "enum": ["RECURSIVE", "PARALLEL", "SEQUENTIAL", "CONDITIONAL"],
      "default": "RECURSIVE"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_depth":                { "type": "integer", "minimum": 1, "maximum": 20 },
        "decomposition_budget_ms":  { "type": "integer", "minimum": 100 },
        "decomposition_budget_tokens": { "type": "integer", "minimum": 1 },
        "deadline_epoch":           { "type": ["integer", "null"] },
        "priority":                 { "type": "integer", "minimum": 0, "maximum": 100, "default": 50 },
        "allow_spanning":           { "type": "boolean", "default": false },
        "min_agent_credibility":    { "type": "number", "minimum": 0, "maximum": 1, "default": 0.5 }
      },
      "required": ["max_depth", "decomposition_budget_ms"]
    },
    "resource_bounds": {
      "type": "object",
      "properties": {
        "compute_tokens":   { "type": "integer", "minimum": 1 },
        "wall_time_ms":     { "type": "integer", "minimum": 1 },
        "storage_bytes":    { "type": "integer", "minimum": 0 },
        "network_bytes":    { "type": "integer", "minimum": 0 },
        "stake_required":   { "type": "number", "minimum": 0 }
      },
      "required": ["compute_tokens", "wall_time_ms"]
    },
    "success_criteria": {
      "type": "object",
      "properties": {
        "predicates": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "predicate_id":   { "type": "string" },
              "expression":     { "type": "string", "description": "Machine-evaluable predicate" },
              "weight":         { "type": "number", "minimum": 0, "maximum": 1, "default": 1.0 },
              "required":       { "type": "boolean", "default": true }
            },
            "required": ["predicate_id", "expression"]
          },
          "minItems": 1
        },
        "aggregation": {
          "type": "string",
          "enum": ["ALL_REQUIRED", "WEIGHTED_THRESHOLD", "ANY_REQUIRED"],
          "default": "ALL_REQUIRED"
        },
        "threshold": {
          "type": "number",
          "minimum": 0, "maximum": 1,
          "description": "For WEIGHTED_THRESHOLD: minimum weighted sum"
        }
      },
      "required": ["predicates"]
    },
    "lifecycle_state": {
      "type": "string",
      "enum": ["PROPOSED", "DECOMPOSED", "ACTIVE", "COMPLETED", "DISSOLVED"]
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
    "operation_class": {
      "type": ["string", "null"],
      "enum": ["M", "B", "X", "V", "G", null],
      "description": "DERIVED by decomposition, not assigned by proposer"
    },
    "provenance": {
      "type": "object",
      "description": "W3C PROV compatible provenance record"
    },
    "compensation": {
      "type": ["object", "null"],
      "properties": {
        "strategy":          { "type": "string", "enum": ["SAGA_ROLLBACK", "COMPENSATING_INTENT", "ABANDON"] },
        "compensation_intents": { "type": "array", "items": { "type": "string" } },
        "timeout_epochs":    { "type": "integer" }
      },
      "description": "Rollback procedure for partial failure; null if no compensation needed"
    }
  },
  "required": ["intent_id", "intent_type", "content", "scope", "origin",
               "constraints", "resource_bounds", "success_criteria",
               "lifecycle_state"]
}
```

---

## Appendix B: Decomposition Algebra Formal Rules

| Parent Class | Permitted Child Classes | Terminal? | Notes |
|---|---|---|---|
| G (Governance) | G, V, X, B, M | No | May produce any class; only class that can produce G children |
| V (Verification) | M, B, X | No | Cannot produce G or V children |
| X (Cross-reference) | M, B | No | Cannot produce V, X, or G children |
| B (Branch) | M | No | Can only produce terminal M children |
| M (Merge) | — | Yes | Terminal; cannot be decomposed further |

**Class rank ordering:** G(4) > V(3) > X(2) > B(1) > M(0)

**Monotonicity rule:** For every parent-child pair, `ClassRank(child) <= ClassRank(parent)`. If `ClassRank(child) == ClassRank(parent)`, then `depth(child) > depth(parent)` (strict depth increase ensures progress).

**Termination guarantees:**
1. `max_depth` hard cap (constitutional invariant C-04, maximum 20).
2. `decomposition_budget` (wall-clock ms + compute tokens) limits decomposition time.
3. Monotonic class descent ensures finite decomposition paths.

**Resource preservation rule:** For any intent `i` with children `{c_1, ..., c_n}`:
```
sum(c_j.resource_bounds.compute_tokens for j in 1..n) + decomposition_overhead
    <= i.resource_bounds.compute_tokens

sum(c_j.resource_bounds.wall_time_ms for j in 1..n) + decomposition_overhead
    <= i.resource_bounds.wall_time_ms
```

Unused resource margins are returned to the parent upon child completion.

---

## Appendix C: Sovereignty Invariant Catalog

### C.1 Constitutional Invariants (Tier 1)

| ID | Invariant | Enforcement | Cross-Ref |
|---|---|---|---|
| C-01 | PCVM Classification Integrity | System 5 audit + ISR reject | C5 §3.1 |
| C-02 | VTD Immutability | Admission Gate + ISR reject | C5 §4.2 |
| C-03 | EMA Canonical Source | Read-only interface by construction | C6 §2.1 |
| C-04 | Decomposition Termination | Hard-coded depth guard (max 20) | §6.2 |
| C-05 | Operation Class Monotonicity | System 3 assertion | §6.1 |
| C-06 | Resource Bound Integrity | System 3 validation | §6.4 |
| C-07 | Provenance Chain Completeness | ISR rejects without CausalStamp | §3.2 |
| C-08 | Settlement Completeness | Settlement Router ALO guarantee | §3.4 |

### C.2 Operational Constraints (Tier 2)

| ID | Constraint | Default | Relaxation Range | Max Lease |
|---|---|---|---|---|
| O-01 | VRF Composition | Standard | Expanded sets | 50 epochs |
| O-02 | Metabolic Timing | C6 default | 0.5x - 2x | 50 epochs |
| O-03 | SHREC Ratios | C6 default | +/-20% | 50 epochs |
| O-04 | Cross-Locus Threshold | 20% | 20-40% | 50 epochs |
| O-05 | Decomp Depth Soft Limit | 10 | 10-15 | 50 epochs |
| O-06 | Memo Cache TTL | 50 epochs | 50-100 | 50 epochs |
| O-07 | Credibility Floor | 0.5 | 0.3-0.5 | 50 epochs |
| O-08 | Settlement Retry | 10 | 10-20 | 50 epochs |
| O-09 | FD Quorum | 3 | 2-3 | 50 epochs |
| O-10 | ISR Bandwidth Cap | 5% | 5-8% | 50 epochs |

### C.3 Coordination Parameters (Tier 3)

| ID | Parameter | Default | Override By |
|---|---|---|---|
| A-01 | Agent Workload Preferences | Agent-declared | System 3 |
| A-02 | Preferred Decomposition Strategy | Intent-declared | System 3 |
| A-03 | Locus Affinity Hints | Agent-declared | System 3 |
| A-04 | Priority Boost Requests | Proposer-declared | System 3 |
| A-05 | Output Format Preferences | Intent-declared | PE |
| A-06 | Monitoring Verbosity | Locus-default | System 3 |

---

## Appendix D: Message Type Catalog

### D.1 Cross-Level Messages

| Type | Direction | From | To | Delivery | Purpose |
|---|---|---|---|---|---|
| INTENT_ASSIGNMENT | Down | GE | LD | ALO | Assign spanning intent sub-task |
| INTENT_ASSIGNMENT | Down | LD | PE | ALO | Assign leaf intent to parcel |
| CANCEL_INTENT | Down | GE | LD | ALO | Cancel spanning intent |
| CANCEL_INTENT | Down | LD | PE | ALO | Cancel leaf intent |
| RESOURCE_UPDATE | Down | GE | LD | BE | Updated resource allocation |
| EXECUTION_REPORT | Up | PE | LD | ALO | Leaf execution outcome |
| EXECUTION_REPORT | Up | LD | GE | ALO | Aggregated subtree outcome |
| LOCUS_HEALTH_REPORT | Up | LD | GE | BE | Locus metrics per epoch |
| ESCALATION | Up | LD | GE | ALO | Intent cannot be handled locally |
| ESCALATION | Up | PE | LD | ALO | Execution failure requiring intervention |
| STATUS_QUERY | Lateral | LD | LD | BE | Query spanning intent status |
| STATUS_RESPONSE | Lateral | LD | LD | BE | Return spanning intent state |

### D.2 Integration Messages

| Type | From | To | Delivery | Purpose |
|---|---|---|---|---|
| ScheduleOperationRequest | RIF (PE) | C3 | Sync | Submit leaf to tidal scheduler |
| OperationResult | C3 | RIF (PE) | Callback | Execution outcome |
| EpochBoundaryEvent | C3 | RIF | Event | Epoch transition notification |
| SettlementMessage | RIF (SR) | C3 | ALO | Intent cost accounting |
| GovernanceVoteRequest | RIF (S5) | C3 | Sync | Submit G-class vote |
| VoteResult | C3 | RIF (S5) | Sync | Vote outcome |
| INT Claim | RIF | C4 | ALO | Intent outcome provenance |
| CredibilityQuery | RIF | C5 | Sync | Agent credibility lookup |
| ByzantineEvidence | RIF (FD) | C5 | ALO | Report Byzantine behavior |
| ProjectionQuery | RIF (S4) | C6 | Sync | EMA projections read |
| MetabolicPhaseQuery | RIF (S3) | C6 | Sync | Current metabolic state |

*ALO = At-Least-Once, BE = Best-Effort, Sync = Synchronous request-response*

### D.3 Sovereignty Protocol Messages

| Type | From | To | Delivery | Purpose |
|---|---|---|---|---|
| RelaxationRequest | S3/S4 | S5 | ALO | Request Tier 2 relaxation |
| RelaxationVotePackage | S5 | C3 (G-class) | Sync | Submit to governance vote |
| RelaxationOutcome | S5 | S3/S4 | ALO | Vote result + lease (if approved) |
| LeaseExpiry | S5 (monitor) | S3 | ALO | Constraint reverted to original |
| LeaseRevocation | S5 (monitor) | S3 | ALO | Lease revoked early (health/cascade) |

---

## Appendix E: Parameter Reference

| Parameter | Default | Range | Location | Description |
|---|---|---|---|---|
| MAX_DEPTH_HARD | 20 | Fixed (C-04) | System 3 | Absolute maximum decomposition depth |
| MAX_DEPTH_SOFT | 10 | 10-15 (O-05) | System 3 | Default decomposition depth limit |
| DECOMP_BUDGET_MS | 5000 | 100-60000 | Per-intent | Wall-clock budget for decomposition |
| CROSS_LOCUS_THRESHOLD | 0.20 | 0.20-0.40 (O-04) | GE | Max cross-locus intent ratio |
| AGENT_CREDIBILITY_FLOOR | 0.5 | 0.3-0.5 (O-07) | Agent Registry | Min PCVM score for assignment |
| SENTINEL_QUORUM | 3 | 2-3 (O-09) | Failure Detector | Min sentinels for liveness quorum |
| ISR_BANDWIDTH_CAP | 0.05 | 0.05-0.08 (O-10) | ISR | Max network fraction for replication |
| ISR_GC_TTL_EPOCHS | 100 | 50-200 | ISR | Epochs before DISSOLVED intent GC |
| MEMO_CACHE_TTL | 50 | 50-100 (O-06) | System 3 | Decomposition cache entry lifetime |
| SETTLEMENT_RETRY_MAX | 10 | 10-20 (O-08) | Settlement Router | Max settlement delivery attempts |
| GE_REPLICAS | 4 | 4-70 | GE | PBFT replica count (3f+1) |
| GE_LEADER_ROTATION | 100 | 50-200 | GE | Epochs between leader rotations |
| GE_CHECKPOINT_INTERVAL | 50 | 25-100 | GE | Epochs between state checkpoints |
| GE_THROUGHPUT_TARGET | 100 | 50-200 | GE | Cross-locus intents/epoch target |
| GE_THROUGHPUT_HARD | 200 | 100-400 | GE | Backpressure threshold |
| LD_HEARTBEAT_MISS_THRESHOLD | 3 | 2-5 | Failure Detector | Missed heartbeats before failover |
| LD_STATE_SYNC_INTERVAL | 1 | 1 | LD | Epochs between passive sync |
| LD_SNAPSHOT_INTERVAL | 10 | 5-20 | LD | Epochs between full snapshots |
| RATE_LIMIT_AGENT_EPOCH | 100 | 50-500 | Admission Gate | Max intents per agent per epoch |
| RATE_LIMIT_LOCUS_EPOCH | 10000 | 5000-50000 | Admission Gate | Max intents per locus per epoch |
| MAX_PROPOSED_QUEUE | 10000 | 5000-50000 | ISR | Max PROPOSED intents before overload |
| SOVEREIGNTY_SUPERMAJORITY | 0.90 | Fixed | System 5 | Required vote fraction for relaxation |
| SOVEREIGNTY_LEASE_MAX | 50 | Fixed | System 5 | Max lease duration in epochs |
| MAX_CONCURRENT_RELAXATIONS | 2 | Fixed | System 5 | Anti-cascade cluster limit |
| VOTE_TIMEOUT_EPOCHS | 3 | 2-5 | System 5 | G-class vote timeout |
| S4_COOLDOWN_EPOCHS | 5 | 3-10 | System 4 | Min epochs between S4 proposals |
| S4_STABILITY_GATE | 3 | 2-5 | System 4 | Consecutive stable epochs for adaptation |
| STALENESS_DECAY_RATE | 0.1 | 0.05-0.2 | System 4 | EMA staleness discount coefficient |
| PARTITION_DETECT_EPOCHS | 5 | 3-10 | Clock Service | Epochs without clock advance = partition |
| MESSAGE_TTL_EPOCHS | 10 | 5-32 | Cross-level | Default message expiry |
| MESSAGE_RETRY_MAX_EPOCHS | 32 | 16-64 | Cross-level | Max retry backoff |

---

## Appendix F: Glossary

| Term | Definition |
|---|---|
| Agent | An autonomous computational entity registered in a C3 locus, capable of executing operations |
| ASV | Adversarial Semantic Versioning (C4); provides provenance and credibility for claims |
| BFT | Byzantine Fault Tolerance; ability to function correctly with up to f malicious participants |
| CausalStamp | Cryptographically signed record of epoch, vector clock, and agent identity attached to every state transition |
| Constitutional Invariant | A Tier 1 system property that cannot be modified under any circumstances at runtime |
| CRDT | Conflict-free Replicated Data Type; data structure that converges across replicas without coordination |
| Decomposition Algebra | The formal rules governing how intents of each operation class may be decomposed into children |
| DISSOLVED | Terminal lifecycle state for intents that were rejected, timed out, or explicitly cancelled |
| EMA | Epistemic Metabolism Architecture (C6); manages knowledge growth, consolidation, and pruning |
| Epoch | A discrete time interval in C3's tidal scheduling system; the fundamental unit of time in Atrahasis |
| GE | Global Executive; the top level of the decomposition hierarchy handling cross-locus intents |
| G-class | Governance operation class; requires G-class consensus (via C3) for execution |
| Intent Quantum | The fundamental unit of work in RIF; a self-describing goal with lifecycle, resources, and provenance |
| ISR | Intent State Registry; locus-local CRDT-replicated registry tracking all intent lifecycle states |
| LD | Locus Decomposer; handles intent decomposition within a single C3 locus |
| Lease | A time-bounded authorization for temporary relaxation of a Tier 2 operational constraint |
| Locus | A logical partition in C3's topology containing agents, parcels, and local infrastructure |
| MCT | Multi-Criteria Trust score computed by C5 PCVM |
| Metabolic Phase | One of ANABOLISM, CATABOLISM, or HOMEOSTASIS as defined by C6 EMA |
| Operation Class | One of M (Merge), B (Branch), X (Cross-reference), V (Verification), G (Governance) |
| Parcel | A data unit in C3's storage model; the smallest addressable unit of state |
| PBFT | Practical Byzantine Fault Tolerance; consensus protocol tolerating f Byzantine nodes with 3f+1 replicas |
| PCVM | Proof-Carrying Verifiable Merit (C5); credibility and trust assessment system |
| PE | Parcel Executor; leaf-level component bridging RIF intents with C3 tidal scheduling |
| Provenance | An immutable chain of C4 ASV claims recording the full history of an intent's lifecycle |
| RIF | Recursive Intent Fabric (C7); this system |
| Settlement Router | Domain State Plane component that forwards intent cost accounting to C3's settlement ledger |
| SHREC | Resource allocation mechanism in C6 EMA |
| Sovereignty Relaxation | Temporary, governance-approved modification of a Tier 2 operational constraint |
| SpanningIntentStub | A lightweight reference to a cross-locus intent, stored in remote loci for tracking |
| Tidal Noosphere | C3; provides locus topology, epoch scheduling, settlement, and VRF |
| VRF | Verifiable Random Function; used for agent selection and committee composition |
| VSM | Viable System Model (Stafford Beer); theoretical foundation for the Executive Plane |
| VTD | Verified Trust Document; append-only credential in C5 PCVM |
| WAL | Write-Ahead Log; used for synchronous LD replication to passive instance |

---

## Appendix G: Test Vectors

### G.1 Simple Locus-Local Decomposition

This test vector traces a GOAL intent through decomposition, execution, and settlement within a single locus.

```
INPUT:
  IntentQuantum {
    intent_id:    "a1b2c3d4...0001"
    intent_type:  GOAL
    content:      "Analyze dataset-42 and produce summary report"
    scope:        { target_loci: ["locus-alpha"], domain: "analytics" }
    origin:       { proposer_agent_id: "agent-007", proposer_locus_id: "locus-alpha" }
    constraints:  { max_depth: 5, decomposition_budget_ms: 3000 }
    resource_bounds: { compute_tokens: 1000, wall_time_ms: 60000 }
    success_criteria: {
      predicates: [
        { predicate_id: "p1", expression: "output.report != null", required: true },
        { predicate_id: "p2", expression: "output.report.sections >= 3", required: true }
      ],
      aggregation: "ALL_REQUIRED"
    }
    lifecycle_state: PROPOSED
  }

ADMISSION (6 gates): ALL PASS
  Gate 1: agent-007 exists, ACTIVE, signature valid, epoch current
  Gate 2: agent-007 has X-class capability in analytics domain
  Gate 3: Schema valid
  Gate 4: 1000 tokens < 50% of locus-alpha capacity (10000)
  Gate 5: No constitutional violation; single locus (no cross-locus check)
  Gate 6: agent-007 at 3 intents this epoch (< 100 limit)

DECOMPOSITION (by LD-alpha, System 3):
  Depth 0: GOAL -> operation_class derived as X (cross-reference)
    Strategy: SEQUENTIAL
    Child 1: DIRECTIVE "Load dataset-42"
      operation_class: M (terminal)
      resource_bounds: { compute: 200, wall: 10000 }
    Child 2: DIRECTIVE "Run analysis pipeline on loaded data"
      operation_class: B (branch)
      resource_bounds: { compute: 500, wall: 30000 }
    Child 3: DIRECTIVE "Format results as summary report"
      operation_class: M (terminal)
      resource_bounds: { compute: 200, wall: 15000 }
    Decomposition overhead: 100 tokens (total children + overhead = 1000)

  Depth 1: B-class child 2 decomposes further
    Child 2a: DIRECTIVE "Statistical summary"
      operation_class: M (terminal)
      resource_bounds: { compute: 250, wall: 15000 }
    Child 2b: DIRECTIVE "Anomaly detection"
      operation_class: M (terminal)
      resource_bounds: { compute: 200, wall: 12000 }
    Decomposition overhead: 50 tokens

FINAL INTENT TREE:
  a1b2...0001 (GOAL, X, depth=0)
    +-- child-01 (DIRECTIVE, M, depth=1) "Load dataset-42"
    +-- child-02 (DIRECTIVE, B, depth=1) "Run analysis pipeline"
    |     +-- child-02a (DIRECTIVE, M, depth=2) "Statistical summary"
    |     +-- child-02b (DIRECTIVE, M, depth=2) "Anomaly detection"
    +-- child-03 (DIRECTIVE, M, depth=1) "Format report"

EXECUTION SEQUENCE (sequential strategy):
  Epoch E:    child-01 assigned to PE-3, agent-012 -> COMPLETED (success)
  Epoch E+1:  child-02a assigned to PE-1, agent-003 -> COMPLETED (success)
              child-02b assigned to PE-2, agent-009 -> COMPLETED (success)
              child-02 -> COMPLETED (both children succeeded)
  Epoch E+2:  child-03 assigned to PE-3, agent-012 -> COMPLETED (success)

SUCCESS CRITERIA EVALUATION:
  p1: output.report != null -> TRUE (report produced by child-03)
  p2: output.report.sections >= 3 -> TRUE (4 sections)
  Aggregation: ALL_REQUIRED -> PASS

LIFECYCLE TRANSITIONS:
  E-1:  PROPOSED -> DECOMPOSED (admission passed, decomposition complete)
  E:    DECOMPOSED -> ACTIVE (all children accepted by executors)
  E+2:  ACTIVE -> COMPLETED (success criteria met)
  E+3:  COMPLETED -> (GC after 100 epochs) -> DISSOLVED

SETTLEMENT:
  decomposition_cost: 150 tokens * TOKEN_RATE = 0.15 credits
  execution_cost:     850 tokens * RESOURCE_RATE = 0.85 credits
  cross_locus_cost:   0 (single locus)
  total_cost:         1.00 credits, charged to agent-007
```

### G.2 Cross-Locus Spanning Intent

```
INPUT:
  IntentQuantum {
    intent_id:    "a1b2c3d4...0002"
    intent_type:  QUERY
    content:      "Find all references to 'quantum coherence' across all loci"
    scope:        { target_loci: ["locus-alpha", "locus-beta", "locus-gamma"],
                    domain: "search" }
    constraints:  { max_depth: 3, allow_spanning: true }
    resource_bounds: { compute_tokens: 3000, wall_time_ms: 120000 }
  }

ROUTING (GE):
  Cross-locus intent detected (3 loci)
  GE decomposes into 3 per-locus sub-intents:
    sub-alpha: { target_loci: ["locus-alpha"], compute: 1000 }
    sub-beta:  { target_loci: ["locus-beta"],  compute: 1000 }
    sub-gamma: { target_loci: ["locus-gamma"], compute: 900 }
    GE overhead: 100 tokens
  SpanningIntentStubs broadcast to all 3 loci

EXECUTION:
  Each sub-intent decomposes locally at its LD into M-class queries
  Results propagate: PE -> LD -> GE
  GE aggregates results and evaluates parent success criteria

SETTLEMENT:
  cross_locus_cost: 3 messages * CROSS_LOCUS_RATE = 0.03 credits
  (split between locus-alpha as originator and beta/gamma as destinations)
```

### G.3 Sovereignty Relaxation Trace

```
TRIGGER: cross_locus_ratio = 0.25 for 5 consecutive epochs (exceeds O-04 = 0.20)

REQUEST:
  System 3 submits SovereigntyRelaxationRequest:
    constraint_id:           "O-04"
    current_value:           0.20
    requested_value:         0.35
    justification:
      trigger_condition:     "Sustained cross-locus ratio above threshold"
      supporting_metrics:    [{ metric: "cross_locus_ratio", current: 0.25,
                                threshold: 0.20, window: 5 }]
      impact_assessment:     "Allow GE to process additional 15% cross-locus traffic"
      risk_if_denied:        "Increasing rejection rate for cross-locus intents"
    requested_lease_epochs:  20
    anti_cascade:            { dependent: ["O-10"], cascade_risk: "LOW" }

PRE-VALIDATION:
  Check 1: O-04 is Tier 2 (not constitutional) -> PASS
  Check 2: 0.35 within relaxation bounds [0.20, 0.40] -> PASS
  Check 3: No active relaxations on O-10 -> cascade count = 0 < 2 -> PASS

G-CLASS VOTE:
  Eligible voters: 50 G-class agents
  Votes for:       47 (94%)
  Votes against:   3 (6%)
  Supermajority:   94% >= 90% -> PASS

LEASE CREATED:
  relaxation_id:  "rel-001"
  constraint_id:  "O-04"
  original_value: 0.20
  relaxed_value:  0.35
  start_epoch:    1000
  expiry_epoch:   1020
  status:         ACTIVE

MONITORING (every epoch):
  Epoch 1005: cross_locus_ratio = 0.28 -> within relaxed threshold -> OK
  Epoch 1010: cross_locus_ratio = 0.22 -> trending down -> OK
  Epoch 1015: cross_locus_ratio = 0.18 -> below original threshold -> OK
  Epoch 1020: LEASE EXPIRED -> revert O-04 to 0.20
  Epoch 1020+: normal operation resumes at 0.20 threshold
```

---

*End of Part 2. This document covers sections 9–15 and Appendices A–G of the C7 Recursive Intent Fabric Master Technical Specification. Part 1 (sections 1–8) provides the foundational definitions, data structures, formal algebra, Domain-Scoped State Plane, and Executive Plane upon which this document builds.*
