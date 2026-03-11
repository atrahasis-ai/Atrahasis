
# AIChain Master Protocol Specification
## Atrahasis Coordination Substrate — Singular Master Document
**Document status:** Draft master specification  
**Version:** 0.9  
**Date:** 2026-03-09  
**Project:** Atrahasis  
**Supersedes:** HEF concept note and prior AIChain blockchain-style assumptions  
**Working substrate name:** **Locus Fabric** (AIChain coordination layer)  

---

## Table of Contents

1. [Purpose and scope](#1-purpose-and-scope)  
2. [System design overview](#2-system-design-overview)  
3. [Formal core: primitives, state, and agreement modes](#3-formal-core-primitives-state-and-agreement-modes)  
4. [Embedded file: `BiTimescale_Parcel_Controller.md`](#4-embedded-file-bitimescale_parcel_controllermd)  
5. [Embedded file: `Capsule_Epoch_Protocol.md`](#5-embedded-file-capsule_epoch_protocolmd)  
6. [Embedded file: `Capsule_Epoch_Protocol.tla`](#6-embedded-file-capsule_epoch_protocoltla)  
7. [Embedded file: `Capsule_Epoch_ProofPlan.md`](#7-embedded-file-capsule_epoch_proofplanmd)  
8. [Embedded file: `Contestable_Reliance_Membrane.md`](#8-embedded-file-contestable_reliance_membranemd)  
9. [Embedded file: `Heuristic_Family_Argumentation_Engine.md`](#9-embedded-file-heuristic_family_argumentation_enginemd)  
10. [Embedded directory spec: `Parcel_Controller_Simulator/`](#10-embedded-directory-spec-parcel_controller_simulator)  
11. [Integrated implementation roadmap](#11-integrated-implementation-roadmap)  
12. [Open unresolved research questions](#12-open-unresolved-research-questions)  
13. [References and design antecedents](#13-references-and-design-antecedents)  

---

## 1. Purpose and scope

This document is the **singular master protocol specification** for the current redesign of Atrahasis AIChain.

It integrates, in one file:

- the current end-to-end system design,
- the formal core of the AIChain replacement architecture,
- the requested controller, capsule, membrane, and argumentation specifications,
- the initial TLA+ seed for the capsule protocol,
- the simulation harness specification needed to test the unstable parts.

### 1.1 Architectural decision

AIChain is no longer specified as a universal blockchain, DAG ledger, distributed log, or Kafka-style stream.  
AIChain is specified as a **mixed-consistency, verification-gated coordination fabric**.

The current architecture name is:

> **Locus Fabric**

This is the current best protocol form of the earlier HEF direction. The key architectural shift is:

> **replace global event ordering with scoped, typed, verification-gated state coordination.**

### 1.2 Relationship to the Atrahasis stack

This specification assumes the broader Atrahasis system contains:

- **CIOS** — orchestration and planning layer,
- **AIChain / Locus Fabric** — live coordination substrate,
- **Verichain** — verification membrane and verifier network,
- **Knowledge Cortex** — durable knowledge graph / memory system,
- **Artifact Plane** — large artifact storage / availability layer,
- **Settlement Plane** — exact arithmetic, slashing, treasury, governance checkpoints,
- **Planetary Compute Infrastructure** — execution, routing, GPU/CPU/memory/network resources,
- **AASL / AACP** — canonical semantic language and communication protocol.

### 1.3 What this document is and is not

This document **is**:

- a master systems design specification,
- a protocol continuation paper,
- an implementation-facing architecture baseline,
- a proof-planning and simulation-planning document.

This document **is not**:

- a finished production spec,
- a completed formal proof,
- a full governance constitution,
- a performance benchmark report.

### 1.4 Normative language

The words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are used in the normative sense common to protocol specifications.

---

## 2. System design overview

### 2.1 Executive summary

Locus Fabric is designed for Atrahasis, where the primary workload is not token transfer but:

- distributed reasoning,
- task decomposition and orchestration,
- claim generation,
- verification,
- artifact production,
- memory admission,
- resource reservation,
- economic settlement,
- governance escalation.

The primary replicated unit is therefore **not a transaction history**. It is a **typed coordination state object** attached to a logical domain.

This specification distinguishes sharply between:

- **logical coordination domains** (**Loci**),
- **physical execution/load balancing units** (**Parcels**).

This separation is one of the most important corrections to earlier HEF drafts.

### 2.2 Design principles

1. **Local by default**  
   The system MUST coordinate within the smallest domain that actually contends.

2. **Verification before durable admission**  
   Durable shared knowledge MUST pass through Verichain and the membrane protocol.

3. **Ephemeral coordination, durable knowledge**  
   Most live coordination traces SHOULD expire; durable memory SHOULD store distilled bundles, not raw chatter.

4. **Mixed consistency, not single-mode consensus**  
   Different operation classes MUST use different agreement modes.

5. **Separation of control plane and artifact plane**  
   Control messages MUST remain small and typed; large artifacts MUST travel through a separate availability system.

6. **AI-native semantics**  
   Internal protocol payloads SHOULD be represented in AASL carried by AACP envelopes.

7. **Formal safety where exclusivity exists**  
   Shared exclusive mutation, settlement, and constitutional changes MUST be handled by explicitly safe protocols.

8. **Do not hide sharded consensus inside metaphors**  
   Any subsystem that behaves like distributed transaction coordination MUST be specified as such and constrained.

### 2.3 Threat and workload model

The substrate MUST tolerate:

- millions of agents initially,
- billions to trillions later,
- Byzantine or arbitrarily faulty agents,
- colluding verifier/operator/provider groups,
- partitions and regional outages,
- artifact withholding,
- message delay, duplication, and reordering,
- hotspot migration and workload non-stationarity,
- adversarial attempts to induce repartition churn,
- contradictory high-confidence claims.

The substrate MAY assume, depending on subsystem:

- cryptographic signatures are unforgeable,
- hash functions are collision-resistant,
- node clocks are only loosely synchronized,
- witness quorums are eventually available in non-catastrophic conditions.

### 2.4 Layered architecture

#### 2.4.1 Intent and routing plane

CIOS converts user goals and system goals into typed intents expressed in AASL and carried over AACP. It computes initial loci, resource budgets, risk classes, and decomposition trees.

#### 2.4.2 Locus router plane

Locus routers host the **Locus State Object** for each active locus. They manage:

- mergeable state,
- bounded-resource state,
- exclusive state,
- claim families and contradiction structure,
- metrics and control variables,
- witness and recovery metadata.

#### 2.4.3 Parcel execution plane

Parcels are the physical execution containers that own hot subsets of locus state. Parcels MAY split, merge, migrate, replicate, and cool down without changing locus semantics.

#### 2.4.4 Artifact plane

Large artifacts move through an availability subsystem with chunking, retrievability proofs, retention classes, and withholding penalties.

#### 2.4.5 Verification membrane

Verichain provides verifier allocation, challenge handling, contradiction tracking, and **Membrane Certificates** for durable admission.

#### 2.4.6 Knowledge and settlement plane

The **Knowledge Cortex** stores admitted bundles, claim family graphs, supersession edges, and reusable blueprints.  
The **Settlement Plane** tracks AIC-denominated economic state, slashing, treasury, governance checkpoints, and narrow exact-consensus tasks.

### 2.5 Locus vs Parcel

#### 2.5.1 Locus

A **Locus** is a stable logical coordination domain defined by:

- selector / namespace,
- invariant set,
- safety class,
- claim-family namespace,
- access-control membrane,
- locality hints,
- epoch class.

A locus SHOULD change rarely. A locus split or merge is a semantic event.

#### 2.5.2 Parcel

A **Parcel** is a physical execution pack defined by:

- current hot object subset,
- open leases and active capsules touching that subset,
- current replica set,
- routing weights,
- current queue / load / verifier spillover statistics.

Parcels MAY change frequently. A parcel split or migration is an operational event.

### 2.6 Core mechanisms that define the current design

The current design is built around the following mechanisms:

- **Locus State Objects (LSOs)** — canonical typed replicated state objects,
- **Bi-timescale parcel controller** — slow loop for repartition, fast loop for routing/replication/placement,
- **Certified Slice Objects (CSOs)** — proof-carrying bounded resource objects,
- **Fusion Capsules implemented by Capsule Epoch Protocol (CEP)** — primary multi-parcel exclusive execution path,
- **Cut Commit fallback** — narrow last-resort protocol, not the normal path,
- **Witness Ladder** — snapshot + delta + witness seal recovery model,
- **Orthogonal Sortition** — verifier committee selection across correlated-failure domains,
- **Contestable Reliance Membrane (CRM)** — separate epistemic status from reliance status,
- **Heuristic Family Argumentation Engine (HFAE)** — operational canon in truth-sparse domains.

### 2.7 Operation classes

Every operation MUST be classified into one of five classes:

- **M-class** — mergeable / monotone / coordination-free after authenticated anti-entropy,
- **B-class** — bounded / escrowable / CSO-compatible,
- **X-class** — exclusive, non-escrowable shared mutation,
- **V-class** — verification-state and membrane-state transitions,
- **G-class** — global constitutional or settlement operations.

The classification is normative. Misclassification is a correctness bug.

### 2.8 Resource and economic model

The architecture uses a three-budget system:

- **Sponsor Budget (SB)** — AIC-backed spend authorization for compute/storage/verification,
- **Protocol Credits (PC)** — non-transferable control-plane budget for emits, subscriptions, challenges, and routing pressure,
- **Capacity Slices (CS)** — locus-local reservation rights over scarce compute, storage bandwidth, verifier slots, and similar resources.

Not every resource is CSO-compatible. Only resources with explicit conservation or enforceable local rights MAY use CSO semantics.

### 2.9 Durable vs ephemeral memory

#### 2.9.1 Ephemeral

- open intents,
- live offers,
- in-flight cells,
- active capsules,
- temporary challenges,
- soft routing weights,
- unsealed delta journals.

#### 2.9.2 Durable

- identity and stake registry,
- locus registry and ancestry,
- active lease table,
- admitted bundles,
- claim family graphs,
- membrane certificates,
- witness seals and snapshots,
- settlement and slashing state,
- reliance permits.

### 2.10 End-to-end flow

1. A requester escrows Sponsor Budget.
2. CIOS emits typed intents to target loci.
3. Mergeable coordination state converges.
4. The parcel controller allocates workers, routing, and capacity.
5. Cells execute; artifacts are published to the artifact plane.
6. Claims enter Verichain.
7. Deterministic, empirical, statistical, or heuristic membrane rules apply.
8. If admitted, the result is wrapped in a Bundle + Membrane Certificate.
9. Knowledge Cortex stores the admitted bundle.
10. Settlement releases rewards, slashes faults, and updates credit balances.
11. Witness seals preserve recovery and auditability without universal replay.

### 2.11 What has been deliberately constrained

The architecture explicitly constrains three failure-prone areas:

- **Repartitioning** is constrained by a bi-timescale controller with hysteresis, shadow planning, and churn budgets.
- **Exclusive cross-parcel execution** is constrained by Capsule Epoch Protocol; Cut Commit is only a fallback.
- **Heuristic canonicalization** is constrained by the Contestable Reliance Membrane; heuristic families do not become timeless truth merely because they are useful.

### 2.12 Orthogonal Sortition

Verifier allocation is not random in a naive sense.

The system uses **Orthogonal Sortition** for V-class work. Committee selection MUST aim for diversity across at least:

- operator identity,
- model family,
- training provenance lineage,
- region,
- infrastructure provider.

The committee constructor SHOULD enforce:
- minimum distinct operator count,
- minimum distinct region count,
- minimum distinct provider count,
- maximum stake concentration by any one failure domain.

This does not eliminate hidden common control, but it reduces obvious correlated-failure concentration.

### 2.13 Certified Slice Objects (CSOs)

CSOs are the formal replacement for vague “invariant slices.”

A resource MAY use CSO semantics only if:

- the resource has a clear conservation law or hard bound,
- local operations can be expressed within locally owned rights,
- transfer, expiry, and reclaim can be made explicit,
- merge and reconciliation preserve the invariant.

CSOs MUST satisfy:

1. conservation,
2. local non-negativity,
3. no double-spend of slice rights,
4. single-claim transfer or safe expiry,
5. deterministic reconciliation.

Resources that do not satisfy these constraints MUST NOT be placed on the CSO path.

### 2.14 Sentinel graph

The security plane maintains a **Sentinel Graph** of anomaly edges:

```text
SentinelEdge =
  <subject_a, subject_b, relation_type, evidence_ref, confidence, epoch>
```

Examples of `relation_type`:

- collusion suspicion,
- artifact withholding,
- replay anomaly,
- identity churn anomaly,
- verification drift,
- routing manipulation suspicion.

Sentinel state feeds into:

- verifier depth,
- challenge priority,
- committee exclusions,
- reliance downgrade pressure,
- rate limits and slashing review.

### 2.15 Witness ladder details

The Witness Ladder is the recovery backbone.

For each active locus, maintain:

- snapshot root,
- delta journal root,
- lease frontier,
- claim frontier,
- admitted bundle frontier,
- capsule frontier.

A witness seal MUST bind the frontiers needed to recover both:
- ordinary locus activity,
- in-flight or recently committed capsules.

### 2.16 Knowledge promotion lanes

The membrane has four operational lanes:

1. **Deterministic lane**  
   proof / replay / checker validated.

2. **Empirical lane**  
   rerun / benchmark replication / cross-provider reproduction.

3. **Statistical lane**  
   distributional validity, interval validity, scoring, calibration.

4. **Heuristic lane**  
   argumentation, assumption stability, challenge pressure, reliance permits.

The system SHOULD NOT force these lanes into one universal notion of truth.

---

## 3. Formal core: primitives, state, and agreement modes

### 3.1 Core primitives

```text
Identity I =
  <pubkey, operator_id, model_hash, training_hash, region, provider,
   reputation, stake, safety_clearance>

Locus L =
  <locus_id, selector, invariant_set, safety_class,
   namespace, locality_hint, epoch_class>

Parcel P =
  <parcel_id, locus_id, object_subset, replica_set,
   routing_weight, status, min_lifetime, churn_budget_ref>

Intent T =
  <intent_id, locus_id, issuer, kind, refs, ttl_epoch, priority, sig>

Claim C =
  <claim_id, family_id, claim_class, subject, predicate, object,
   evidence_refs, provenance_refs, confidence, issuer, sig>

VerifierCommittee VC =
  <committee_id, locus_id, family_id, member_set,
   diversity_vector, policy_ref, epoch>

Lease R =
  <lease_id, locus_id, resource_set, holder, ttl_epoch, status>

ArtifactCert A =
  <artifact_id, namespace, chunk_root, availability_cert,
   retention_class, withholding_policy>

Bundle B =
  <bundle_id, locus_id, claim_ids, artifact_ids, supersedes,
   membrane_cert, witness_ref>

MembraneCert MC =
  <schema_root, availability_root, verifier_cert, contradiction_root,
   lineage_root, policy_version, retention_policy, privacy_policy>

WitnessSeal W =
  <locus_id, seal_seq, snapshot_root, delta_root,
   frontier_root, qc>

CertifiedSliceObject CSO =
  <cso_id, resource_type, total_supply,
   alloc_map, pending_transfers, spent_frontier, epoch, proof_hash>

Capsule K =
  <capsule_id, locus_id, touched_set, exec_host,
   grant_map, expiry_epoch, state, witness_ref>

ReliancePermit RP =
  <family_id, context, horizon, risk_class, ttl_epoch,
   reliance_status, rationale_root, approver_set, revocation_rule>

SentinelEdge S =
  <subject_a, subject_b, relation_type, evidence_ref, confidence, epoch>
```

### 3.2 Locus State Object

```text
LSO(L) = {
  meta_state,
  merge_state,        // M-class
  slice_state,        // B-class / CSO-compatible resources
  exclusive_state,    // X-class object versions and lease fronts
  claim_state,        // claim families, support/attack graph, status pointers
  control_state,      // arrival, service, contention, entropy, risk, utilization
  recovery_state      // snapshot ref, delta frontier, witness seals
}
```

### 3.3 Legal state transitions

#### Intent

```text
open -> matched -> consumed
open -> expired
open -> cancelled
```

#### Lease

```text
requested -> prepared -> granted -> renewed
granted -> expired
granted -> revoked
```

#### Claim

```text
submitted -> admissible -> under_review
under_review -> verified
under_review -> rejected
under_review -> contested
verified -> canonical            // deterministic / empirical / calibrated statistical only
verified -> operational_champion // heuristic families
verified -> superseded
```

#### Bundle

```text
assembled -> membrane_checked -> admitted -> canonicalized -> compacted
```

#### Capsule

```text
created -> grants_partial -> armed -> committed -> installed
created -> expired
grants_partial -> expired
armed -> expired
committed -> recovered_install
```

#### Reliance Permit

```text
draft -> advisory -> bounded_operational -> ratified
advisory -> downgraded
bounded_operational -> expired
ratified -> revoked
```

### 3.4 Agreement modes

#### M-class: merge / converge

Used for:

- needs,
- offers,
- lineage references,
- support edges,
- low-risk routing metadata,
- nonexclusive coordination state.

Requires:
- authenticated anti-entropy,
- deterministic merge law,
- bounded retention.

#### B-class: bounded local commit

Used when a resource can be represented by a Certified Slice Object.  
Local operations are legal only within local rights. Slice transfer and epoch reconciliation are separate protocols.

#### X-class: exclusive mutation

Preferred order of execution:

1. single-parcel local serial execution,
2. CSO reduction if possible,
3. Capsule Epoch Protocol,
4. Cut Commit fallback.

#### V-class: verification-state transitions

Used for:

- verifier selection,
- challenge deadlines,
- contradiction resolution state,
- membrane certificate issuance,
- reliance permit changes.

#### G-class: global settlement / governance

Used only for:

- AIC settlement,
- slashing,
- treasury updates,
- randomness beacon,
- constitutional parameter changes,
- governance ratification paths.

### 3.5 Recovery model

Recovery is based on the **Witness Ladder**:

1. periodic snapshot,
2. bounded delta journal,
3. quorum-signed witness seal,
4. optional anchoring in settlement plane.

A recovering node or parcel reconstructs state by:

1. loading the latest verified snapshot,
2. pulling missing deltas,
3. replaying to frontier,
4. verifying roots against the latest witness seal,
5. resuming service.

### 3.6 Verification membrane

Durable knowledge admission requires a **Membrane Certificate**.  
A bundle MUST NOT become admitted durable knowledge unless the certificate includes:

- schema-valid AASL content,
- artifact availability proof,
- verifier committee certificate,
- contradiction graph root,
- provenance root,
- privacy/retention policy binding.

### 3.7 Heuristic families

Heuristic claim families are special. They do not receive timeless canonical status by default. They participate in the Contestable Reliance Membrane, where:

- **TruthStatus** captures epistemic standing,
- **RelianceStatus** captures what the system is permitted to do with the claim in context.

---

## 4. Embedded file: `BiTimescale_Parcel_Controller.md`

# BiTimescale Parcel Controller

## 4.1 Purpose

The parcel controller manages physical execution placement without destabilizing logical semantics.

Its job is to decide:

- when to keep the current parcelization,
- when to adjust routing and replication only,
- when to split or merge parcels,
- when to migrate parcel ownership,
- when to reject a proposed repartition because the cure is worse than the disease.

The parcel controller MUST NOT alter locus semantics. It operates under a fixed locus boundary unless an explicit, rare locus redefinition event occurs.

## 4.2 Why this subsystem exists

Earlier HEF drafts treated "scope" as both a correctness boundary and a load-balancing boundary. That was unsafe. The parcel controller exists because logical boundaries and physical placement must be separate.

Design antecedents include workload-driven partitioning (Schism), online fine-grained adaptive partitioning (Clay), live repartitioning (Squall), and dynamic locality-aware object motion (Zeus). See references [R1]-[R4].

## 4.3 Controller model

The controller is bi-timescale:

### Fast loop

Runs frequently and changes:

- routing weights,
- worker counts,
- replica factor,
- verifier slot assignment,
- subscription fanout,
- queue pressure damping.

The fast loop MUST NOT change parcel boundaries.

### Slow loop

Runs less frequently and MAY change:

- parcel split / merge plan,
- object-to-parcel mapping,
- replica placement,
- parcel ownership,
- cold parcel archival.

The slow loop MUST respect hysteresis and churn budgets.

## 4.4 State observed by the controller

For each parcel `p` and locus `L`, maintain at least:

```text
arrival_rate[p]
service_rate[p]
queue_delay[p]
verifier_spillover[p]
remote_x_rate[p]
remote_v_rate[p]
capsule_rate[p]
artifact_backpressure[p]
recovery_surface[p]
migration_bytes_recent[p]
parcel_age[p]
replica_cost[p]
```

And maintain a rolling access/conflict hypergraph:

```text
H_W = (O, E, w)
O = objects / claim families / lease subjects
E = operation footprints over window W
w = weighted by frequency, latency penalty, and conflict cost
```

## 4.5 Objective `J(P)`

Let `P` be a parcelization plan and `P_t` the active plan at time `t`.

The controller minimizes:

```text
J(P) =
  w1 * RemoteXRate(P) +
  w2 * QueueDelay(P) +
  w3 * VerifierSpillover(P) +
  w4 * MigrationBytes(P) +
  w5 * ParcelChurn(P) +
  w6 * RecoverySurface(P) +
  w7 * ReplicaCost(P) +
  w8 * ArtifactBackpressure(P) +
  w9 * CapsuleOveruse(P)
```

Where:

- `RemoteXRate` = fraction of X-class operations whose touched set spans multiple parcels,
- `QueueDelay` = weighted mean queue latency,
- `VerifierSpillover` = verification activity that escapes intended locality,
- `MigrationBytes` = data and state transferred by reconfiguration,
- `ParcelChurn` = rate of boundary changes,
- `RecoverySurface` = cost to recover after faults,
- `ReplicaCost` = standing cost of the placement,
- `ArtifactBackpressure` = control-plane slowdown due to artifact availability bottlenecks,
- `CapsuleOveruse` = proportion of X-class volume requiring capsules beyond a policy threshold.

The optimization is not purely greedy. A candidate plan MUST beat the current plan by more than a policy threshold after accounting for migration debt and control variance.

## 4.6 Acceptance rule for candidate parcelization

For candidate plan `P'`, define:

```text
Δ(P -> P') = J(P) - J(P')
```

A candidate plan MAY be accepted only if all conditions hold:

```text
Δ(P -> P') > θ_enter
for k consecutive slow-loop windows
variance_estimate(P') < σ_max
migration_cost(P -> P') < budget_epoch_remaining
predicted_remote_x(P') <= x_cap
```

## 4.7 Hysteresis

To prevent thrash:

- `θ_exit < θ_enter`
- merge / rollback decisions use `k' > k`
- parcel lifetime MUST exceed `τ_min` before being eligible for another structural change
- each parcel SHOULD observe a cooldown `τ_cool` after split/merge/migration
- each locus has a per-epoch churn budget `β_epoch`

This means the controller resists oscillation even when the workload fluctuates.

## 4.8 Shadow planning

No candidate parcelization MAY be applied directly.

Every candidate `P'` MUST pass a shadow-planning stage:

1. Generate candidate from `H_W` and recent metrics.
2. Run the routing layer in **shadow mode** for `s` windows:
   - no data moves,
   - no ownership changes,
   - only virtual route decisions and cost estimates.
3. Estimate:
   - mean `J(P')`,
   - variance of `J(P')`,
   - predicted migration debt,
   - expected remote X-class reduction,
   - expected verifier spillover reduction.
4. Reject if:
   - variance increases materially,
   - expected recovery surface increases above threshold,
   - capsule rate increases above threshold,
   - the workload appears phase-transient rather than structurally persistent.

Shadow mode is mandatory because non-stationary AI workloads can create false positives for repartitioning.

## 4.9 Split / merge rules

### Split eligibility

A parcel MAY split only if:

- conflict/co-access clustering quality exceeds `q_split`,
- predicted local execution gain exceeds `g_split`,
- active capsule count on affected objects is zero,
- no open X-class lease blocks the move,
- projected post-split parcel sizes stay within `size_min .. size_max`,
- split does not violate the locus churn budget.

### Merge eligibility

A parcel pair or set MAY merge only if:

- access overlap stays high for `k'` windows,
- combined parcel remains within `size_max`,
- projected remote X-class count decreases or stays flat,
- merge does not create a verifier hotspot,
- merge does not increase recovery surface unacceptably.

## 4.10 Rollback rules

Rollback applies only to structural parcel changes, not to fast-loop parameter changes.

A recent change MAY roll back if:

```text
J(P_active) - J(P_prev) > θ_rollback
for r consecutive windows
and no active capsule or open exclusive lease blocks restoration
```

Rollback MUST occur only at an epoch boundary and only from a **reconfig checkpoint** that contains:

- previous object-to-parcel mapping,
- previous replica assignments,
- previous routing weights,
- witness seal reference,
- migration frontier.

Rollback MUST be idempotent.

If full rollback is unsafe, the controller MAY perform partial rollback:
- undo latest split only,
- restore previous replica layout,
- restore previous routing only.

## 4.11 Adversarial workload suite

The simulator and controller evaluation MUST include at least the following scenarios.

### A. Hotspot drift
A hotspot moves gradually across the object space.

### B. Toggle hotspot
A hotspot alternates between two disjoint regions faster than the slow loop can safely react.

### C. Flash crowd
A sudden burst targets one claim family or resource set.

### D. Anti-locality attack
Requests are deliberately shaped to maximize cross-parcel footprints.

### E. Repartition churn attack
Adversaries create temporary co-access patterns to bait the controller into expensive migration.

### F. Capsule flood
A workload forces frequent exclusive cross-parcel operations to test whether the controller reduces capsule demand or amplifies it.

### G. Verifier storm
A spike in contested claims creates sustained verification spillover.

### H. Artifact withholding backpressure
Artifact retrieval failures create control-plane blocking and delayed admission.

### I. Regional partition loss
Replica sets are disrupted and controller decisions must respect degraded topology.

### J. Mixed-stakes interference
Low-risk, high-volume traffic attempts to starve high-risk, low-volume loci.

## 4.12 Controller outputs

The controller produces:

- `routing_update`
- `replica_factor_update`
- `worker_target_update`
- `candidate_repartition_plan`
- `approved_repartition_plan`
- `rollback_plan`
- `do_nothing`

## 4.13 Slow-loop pseudocode

```text
for each slow window W:
    metrics <- summarize_recent_metrics()
    H_W <- build_access_conflict_hypergraph(W)
    P_candidates <- generate_candidate_parcelizations(H_W, metrics)

    for each P' in P_candidates:
        if violates_hard_guards(P'):
            reject(P')
            continue

        shadow <- run_shadow_plan(P', s_windows)
        if not passes_shadow(shadow):
            reject(P')
            continue

        if improvement(P_current, P') > θ_enter for k windows:
            approve_epoch_cutover(P')
            checkpoint_current_plan()
            apply(P')
            break
```

## 4.14 Hard guards

A candidate plan MUST be rejected if any of the following hold:

- active capsule on moved object set,
- open X-class lease on moved object set,
- parcel lifetime below `τ_min`,
- churn budget exhausted,
- predicted remote X-class fraction above `x_cap`,
- recovery surface above `r_cap`,
- witness seal gap too large.

## 4.15 Acceptance criteria for this subsystem

This subsystem is considered acceptable only if, under simulation:

- parcel churn stays below policy budget,
- remote X-class rate falls materially relative to baseline,
- rollback remains rare,
- controller-induced outages are zero,
- latency variance does not materially exceed baseline,
- capsule usage remains bounded,
- verifier spillover stays within policy bounds.

---

## 5. Embedded file: `Capsule_Epoch_Protocol.md`

# Capsule Epoch Protocol (CEP)

## 5.1 Purpose

Capsule Epoch Protocol is the primary mechanism for rare but necessary exclusive cross-parcel execution.

CEP exists because:

- arbitrary multi-parcel X-class mutation is unsafe if left informal,
- general distributed commit should not be the default path,
- many multi-object operations can be reduced to temporary exclusive handoff plus local serial execution.

CEP formalizes the earlier "Fusion Capsule" idea.

## 5.2 Design goal

Turn a hard multi-parcel exclusive update into three smaller problems:

1. exclusive **prepare grants** from current owners,
2. local serial execution inside a temporary capsule,
3. idempotent **install** of the committed result.

The design goal is to ensure:

- no double authority,
- no stale install,
- safe timeout and reversion,
- idempotent recovery.

## 5.3 Non-goals

CEP does **not** attempt to optimize:

- large fanout transactions over arbitrary loci,
- long-running workflows spanning unrelated domains,
- normative governance decisions,
- resources that can be reduced to CSO semantics.

If a workflow is long-running, it SHOULD use saga semantics, not CEP.

## 5.4 State objects

### 5.4.1 Per-object authority state

```text
ObjAuth[o] =
  <owner,
   auth_epoch,
   prepared_capsule | null,
   install_frontier,
   last_commit_root>
```

### 5.4.2 Per-capsule state

```text
Capsule[c] =
  <capsule_id,
   locus_id,
   touched_set,
   exec_host,
   grant_map,          // object -> proposed epoch
   grant_state_hashes, // object -> state hash at prepare time
   private_versions,
   expiry_epoch,
   status,
   witness_ref>
```

### 5.4.3 Commit record

```text
CommitRecord[c] =
  <capsule_id,
   locus_id,
   touched_root,
   grant_root,
   input_state_root,
   delta_root,
   install_seq,
   exec_trace_hash,
   artifact_roots,
   sponsor_ref,
   verifier_policy_ref,
   signatures>
```

## 5.5 Capsule states

```text
created
grants_partial
armed
committed
installed
expired
aborted
```

## 5.6 Message types

- `PrepareGrantRequest`
- `PrepareGrantResponse`
- `ArmNotice`
- `CommitRecord`
- `InstallNotice`
- `InstallAck`
- `ExpireNotice`
- `RecoveryQuery`
- `RecoveryResponse`

## 5.7 Protocol flow

### Step 0 — Eligibility

An X-class operation MAY use CEP only if:

- it cannot be executed locally in one parcel,
- it cannot be reduced to a CSO-compatible operation,
- its touched set is bounded by `capsule_touch_max`,
- its predicted runtime fits within `capsule_ttl_max`,
- policy permits capsule use for the relevant safety class.

Otherwise:
- use local execution,
- use CSO,
- use Cut Commit fallback,
- or reject.

### Step 1 — Capsule creation

The initiator computes:

- exact write footprint,
- exact read dependencies that must be fenced,
- candidate execution host,
- expiry epoch.

The capsule is created in `created` state.

### Step 2 — Prepare grants

For each object `o` in the touched set, the current parcel owner MAY issue:

```text
Grant(o, c, auth_epoch(o)+1, expiry_epoch, state_hash(o))
```

Local rules:

- a parcel MUST NOT issue a grant if `prepared_capsule != null`,
- a parcel MUST freeze external write authority for `o` once it issues the grant,
- a parcel MAY continue to serve safe reads under the read policy,
- a parcel MUST record the proposed epoch and prepared capsule ID durably before responding success.

After at least one but not all grants arrive, capsule state is `grants_partial`.

### Step 3 — Arm

The capsule becomes `armed` only when it holds a valid grant for every object in the touched set.

No execution may start before the full touched set is armed.

### Step 4 — Private execution

The capsule executes on private copies only.

Rules:

- no externally visible writes before commit,
- private execution uses the exact prepared input state roots,
- execution MUST be deterministic within the capsule runtime model,
- artifacts produced during execution MUST be content-addressed.

### Step 5 — Commit record

If execution succeeds, the capsule writes a `CommitRecord` to the witness path.

A valid commit record MUST bind:

- touched set,
- grant map,
- input state root,
- output delta root,
- install sequence,
- execution trace hash,
- any artifact roots,
- signer set / quorum.

After commit record durability is confirmed, capsule state becomes `committed`.

### Step 6 — Install

Each source parcel installs the result independently but idempotently.

Install acceptance rules for object `o`:

- `prepared_capsule(o) == capsule_id`,
- `grant_epoch(o) == auth_epoch(o) + 1`,
- `install_seq > install_frontier(o)`,
- commit record verifies,
- object state hash at prepare matches the capsule grant record, unless a recovery path explicitly handles divergence.

If valid, the parcel:

- applies the delta,
- sets `auth_epoch := auth_epoch + 1`,
- updates owner if the new owner changes,
- clears `prepared_capsule`,
- sets `install_frontier := install_seq`,
- updates `last_commit_root`.

After all touched objects install, capsule state becomes `installed`.

### Step 7 — Expiry / reversion

If a valid commit record does not appear before expiry:

- all prepare grants expire,
- `prepared_capsule` is cleared,
- write authority reverts to the pre-capsule owner,
- no rollback of externally visible writes is needed because no install occurred.

This is a major design simplification: **tentative authority is not globally real authority**.

## 5.8 Safety invariants

CEP MUST satisfy the following invariants.

### I1. No double authority
For any object and epoch, at most one prepared capsule may hold a valid grant.

### I2. Monotone authority epoch
`auth_epoch` increases only by install, never by prepare.

### I3. No stale install
An install with stale epoch or stale install sequence MUST be rejected.

### I4. No early visibility
No capsule result becomes externally visible before a valid commit record exists and install succeeds.

### I5. Idempotent install
Reapplying the same valid install after crash/restart MUST converge to the same state.

### I6. Expiry safety
If a commit record does not materialize before expiry, the previous owner remains authoritative.

### I7. Prepare durability
A parcel MUST durably record prepare state before returning a successful grant.

### I8. Install fence
While prepared, external writes to the fenced object set MUST NOT proceed.

## 5.9 Read policy during prepare

The read policy is configurable by safety class:

- **strict**: reads blocked or redirected,
- **snapshot**: reads served from pre-prepare state with explicit staleness annotation,
- **optimistic**: reads allowed only if the object type permits stale observation.

Safety classes MUST define which read mode is legal.

## 5.10 Expiry semantics

Capsule expiry is epoch-based.

Each grant contains:
- `grant_epoch`,
- `expiry_epoch`.

Rules:

- the execution host MUST stop work after `expiry_epoch`,
- parcels MUST reject late installs after expiry unless the commit record was durably witnessed before expiry and only delivery is delayed,
- expiry MUST be monotone and checkable against witness time or agreed epoch progression.

## 5.11 Witness record format

CEP relies on a witness path.

### Witness capsule record

```text
WitnessCapsuleRecord =
  <capsule_id,
   locus_id,
   touched_root,
   grant_root,
   input_state_root,
   delta_root,
   install_seq,
   exec_trace_hash,
   artifact_root_set,
   created_epoch,
   commit_epoch,
   expiry_epoch,
   signer_bitmap,
   quorum_sig>
```

This record is sufficient to:

- prove a capsule committed,
- replay install,
- reject stale installs,
- audit touched state.

## 5.12 Recovery path

Recovery has three principal cases.

### Case A — Parcel crashed after prepare, before commit

On restart:
- reload durable `prepared_capsule`,
- query witness path for a matching commit record,
- if none exists and expiry passed, clear prepare,
- if commit exists, proceed to install.

### Case B — Commit exists, some parcels installed, others did not

On restart or query:
- fetch witness capsule record,
- verify install sequence and grant map,
- perform idempotent install on missing parcels,
- mark installed.

### Case C — Capsule host crashed before commit

If no commit record exists and expiry passes:
- grants lapse,
- state returns to normal,
- capsule is marked expired or aborted.

## 5.13 Failure handling

CEP MUST handle:

- duplicated grant messages,
- duplicated install notices,
- delayed commit delivery,
- parcel crash after grant durability,
- parcel crash after partial install,
- execution host crash,
- replay attack on stale commit records,
- conflicting capsule initiation.

## 5.14 Fallback criteria

CEP SHOULD NOT be used when:

- touched set is too large,
- TTL cannot be bounded safely,
- objects are already widely contended shared state,
- safety class requires a broader consensus surface.

In those cases the system MAY use Cut Commit fallback. That fallback MUST be observable, metered, and auditable. If Cut Commit becomes common, parcelization or object modeling is wrong.

## 5.15 Acceptance criteria for this subsystem

CEP is acceptable only if formal and simulation work support:

- no double authority,
- no stale install,
- idempotent recovery,
- safe expiry,
- bounded lockout window,
- strictly lower frequency than ordinary X-class volume.

---

## 6. Embedded file: `Capsule_Epoch_Protocol.tla`

# Capsule Epoch Protocol — TLA+ Seed Module

The following is a **seed TLA+ model** for CEP. It is intentionally small enough to model check, but rich enough to express the core safety invariants. It is not the final refinement proof.

```tla
----------------------------- MODULE CapsuleEpochProtocol -----------------------------
EXTENDS Naturals, FiniteSets, Sequences, TLC

CONSTANTS OBJECTS, CAPSULES, HOSTS, NullCapsule, NullOwner

VARIABLES
    owner,            \* [OBJECTS -> HOSTS \cup {NullOwner}]
    authEpoch,        \* [OBJECTS -> Nat]
    prepared,         \* [OBJECTS -> CAPSULES \cup {NullCapsule}]
    installFrontier,  \* [OBJECTS -> Nat]
    lastCommitRoot,   \* [OBJECTS -> Nat]
    capState,         \* [CAPSULES -> {"created","grants_partial","armed","committed","installed","expired","aborted"}]
    capTouched,       \* [CAPSULES -> SUBSET OBJECTS]
    capHost,          \* [CAPSULES -> HOSTS]
    capExpiry,        \* [CAPSULES -> Nat]
    grantEpoch,       \* [CAPSULES -> [OBJECTS -> Nat]]
    committed,        \* [CAPSULES -> BOOLEAN]
    commitSeq,        \* [CAPSULES -> Nat]
    installedSet,     \* [CAPSULES -> SUBSET OBJECTS]
    now               \* Nat

Vars ==
    << owner, authEpoch, prepared, installFrontier, lastCommitRoot,
       capState, capTouched, capHost, capExpiry, grantEpoch,
       committed, commitSeq, installedSet, now >>

TypeOK ==
    /\ owner \in [OBJECTS -> (HOSTS \cup {NullOwner})]
    /\ authEpoch \in [OBJECTS -> Nat]
    /\ prepared \in [OBJECTS -> (CAPSULES \cup {NullCapsule})]
    /\ installFrontier \in [OBJECTS -> Nat]
    /\ lastCommitRoot \in [OBJECTS -> Nat]
    /\ capState \in [CAPSULES -> {"created","grants_partial","armed","committed","installed","expired","aborted"}]
    /\ capTouched \in [CAPSULES -> SUBSET OBJECTS]
    /\ capHost \in [CAPSULES -> HOSTS]
    /\ capExpiry \in [CAPSULES -> Nat]
    /\ grantEpoch \in [CAPSULES -> [OBJECTS -> Nat]]
    /\ committed \in [CAPSULES -> BOOLEAN]
    /\ commitSeq \in [CAPSULES -> Nat]
    /\ installedSet \in [CAPSULES -> SUBSET OBJECTS]
    /\ now \in Nat

Init ==
    /\ owner \in [OBJECTS -> (HOSTS \cup {NullOwner})]
    /\ authEpoch = [o \in OBJECTS |-> 0]
    /\ prepared = [o \in OBJECTS |-> NullCapsule]
    /\ installFrontier = [o \in OBJECTS |-> 0]
    /\ lastCommitRoot = [o \in OBJECTS |-> 0]
    /\ capState \in [CAPSULES -> {"created"}]
    /\ capTouched \in [CAPSULES -> SUBSET OBJECTS]
    /\ capHost \in [CAPSULES -> HOSTS]
    /\ capExpiry \in [CAPSULES -> Nat]
    /\ grantEpoch = [c \in CAPSULES |-> [o \in OBJECTS |-> 0]]
    /\ committed = [c \in CAPSULES |-> FALSE]
    /\ commitSeq = [c \in CAPSULES |-> 0]
    /\ installedSet = [c \in CAPSULES |-> {}]
    /\ now = 0

CanGrant(c, o) ==
    /\ c \in CAPSULES
    /\ o \in capTouched[c]
    /\ prepared[o] = NullCapsule
    /\ capState[c] \in {"created","grants_partial"}
    /\ now < capExpiry[c]

Grant(c, o) ==
    /\ CanGrant(c, o)
    /\ prepared' = [prepared EXCEPT ![o] = c]
    /\ grantEpoch' = [grantEpoch EXCEPT ![c][o] = authEpoch[o] + 1]
    /\ capState' =
        [capState EXCEPT
            ![c] = IF \A x \in capTouched[c] : (x = o) \/ prepared[x] = c
                   THEN "armed"
                   ELSE "grants_partial"]
    /\ UNCHANGED << owner, authEpoch, installFrontier, lastCommitRoot,
                    capTouched, capHost, capExpiry, committed, commitSeq,
                    installedSet, now >>

AllGranted(c) ==
    \A o \in capTouched[c] : prepared[o] = c /\ grantEpoch[c][o] = authEpoch[o] + 1

Arm(c) ==
    /\ c \in CAPSULES
    /\ capState[c] = "grants_partial"
    /\ AllGranted(c)
    /\ capState' = [capState EXCEPT ![c] = "armed"]
    /\ UNCHANGED << owner, authEpoch, prepared, installFrontier, lastCommitRoot,
                    capTouched, capHost, capExpiry, grantEpoch, committed,
                    commitSeq, installedSet, now >>

WriteCommit(c) ==
    /\ c \in CAPSULES
    /\ capState[c] = "armed"
    /\ now < capExpiry[c]
    /\ committed' = [committed EXCEPT ![c] = TRUE]
    /\ commitSeq' = [commitSeq EXCEPT ![c] = commitSeq[c] + 1]
    /\ capState' = [capState EXCEPT ![c] = "committed"]
    /\ UNCHANGED << owner, authEpoch, prepared, installFrontier, lastCommitRoot,
                    capTouched, capHost, capExpiry, grantEpoch, installedSet, now >>

CanInstall(c, o) ==
    /\ c \in CAPSULES
    /\ o \in capTouched[c]
    /\ capState[c] = "committed"
    /\ committed[c] = TRUE
    /\ prepared[o] = c
    /\ grantEpoch[c][o] = authEpoch[o] + 1
    /\ commitSeq[c] > installFrontier[o]

Install(c, o) ==
    /\ CanInstall(c, o)
    /\ authEpoch' = [authEpoch EXCEPT ![o] = @ + 1]
    /\ prepared' = [prepared EXCEPT ![o] = NullCapsule]
    /\ installFrontier' = [installFrontier EXCEPT ![o] = commitSeq[c]]
    /\ lastCommitRoot' = [lastCommitRoot EXCEPT ![o] = commitSeq[c]]
    /\ installedSet' = [installedSet EXCEPT ![c] = @ \cup {o}]
    /\ capState' =
        [capState EXCEPT
            ![c] = IF installedSet[c] \cup {o} = capTouched[c]
                   THEN "installed"
                   ELSE "committed"]
    /\ UNCHANGED << owner, capTouched, capHost, capExpiry,
                    grantEpoch, committed, commitSeq, now >>

ExpirePrepared(c, o) ==
    /\ c \in CAPSULES
    /\ o \in capTouched[c]
    /\ prepared[o] = c
    /\ now >= capExpiry[c]
    /\ committed[c] = FALSE
    /\ prepared' = [prepared EXCEPT ![o] = NullCapsule]
    /\ capState' =
        [capState EXCEPT
            ![c] = IF \A x \in capTouched[c] : (x = o) \/ prepared[x] # c
                   THEN "expired"
                   ELSE capState[c]]
    /\ UNCHANGED << owner, authEpoch, installFrontier, lastCommitRoot,
                    capTouched, capHost, capExpiry, grantEpoch, committed,
                    commitSeq, installedSet, now >>

Tick ==
    /\ now' = now + 1
    /\ UNCHANGED << owner, authEpoch, prepared, installFrontier, lastCommitRoot,
                    capState, capTouched, capHost, capExpiry, grantEpoch,
                    committed, commitSeq, installedSet >>

Next ==
    \/ \E c \in CAPSULES, o \in OBJECTS : Grant(c, o)
    \/ \E c \in CAPSULES : Arm(c)
    \/ \E c \in CAPSULES : WriteCommit(c)
    \/ \E c \in CAPSULES, o \in OBJECTS : Install(c, o)
    \/ \E c \in CAPSULES, o \in OBJECTS : ExpirePrepared(c, o)
    \/ Tick

NoDoubleAuthority ==
    \A o \in OBJECTS :
        Cardinality({ c \in CAPSULES : prepared[o] = c }) <= 1

PreparedImpliesNextEpoch ==
    \A c \in CAPSULES :
        \A o \in capTouched[c] :
            prepared[o] = c => grantEpoch[c][o] = authEpoch[o] + 1

CommittedRequiresArmedHistory ==
    \A c \in CAPSULES :
        committed[c] => capState[c] \in {"committed","installed"}

InstalledImpliesCommitted ==
    \A c \in CAPSULES :
        capState[c] = "installed" => committed[c] = TRUE

FrontierMonotone ==
    \A o \in OBJECTS : installFrontier[o] <= lastCommitRoot[o]

Safety ==
    TypeOK /\ NoDoubleAuthority /\ PreparedImpliesNextEpoch
            /\ CommittedRequiresArmedHistory /\ InstalledImpliesCommitted
            /\ FrontierMonotone

Spec ==
    Init /\ [][Next]_Vars

=============================================================================
```

### 6.1 Notes on the TLA+ seed

This module is intentionally a **seed**, not the final proof artifact.

It omits, for tractability:

- quorum certificate internals,
- artifact root details,
- read modes,
- external ownership transfer semantics,
- witness anchoring,
- Byzantine signer modeling.

Those belong in later refinement stages.

### 6.2 Model checking goals

The initial TLC / Apalache model checking goal is to establish small-model evidence for:

- no double prepared authority,
- no stale install frontier regressions,
- commit-before-install,
- expiry safety,
- install idempotence across interleavings.

---

## 7. Embedded file: `Capsule_Epoch_ProofPlan.md`

# Capsule Epoch Proof Plan

## 7.1 Objective

This document defines the proof strategy for CEP. The goal is not merely testing. The goal is a staged assurance ladder from abstract safety to implementation-critical correctness.

## 7.2 Assurance ladder

### Stage 1 — Abstract protocol model

Use TLA+ to model:

- prepare,
- arm,
- commit,
- install,
- expiry,
- recovery interleavings.

Tooling:
- TLC for finite-state exploration,
- Apalache or equivalent symbolic/state-space assistance where useful.

Deliverables:
- checked invariants,
- counterexample traces for violated properties,
- minimized state machine before code.

### Stage 2 — Refinement model

Refine the abstract CEP model into:

- message handlers,
- durable storage writes,
- witness log writes,
- restart recovery behavior.

Prove or check that the refinement preserves abstract safety obligations.

### Stage 3 — Implementation-critical proof track

For components with the highest blast radius, produce stronger proofs over executable or near-executable logic.

Recommended target set:

1. **Authority Manager**
   - prepare durability,
   - no double authority,
   - epoch monotonicity.

2. **Install Worker**
   - stale install rejection,
   - idempotent install,
   - crash-safe replay.

3. **Witness Record Validator**
   - commit record binding correctness,
   - touched-set / grant-root / delta-root consistency.

4. **Recovery Coordinator**
   - safe case distinction between:
     - expired-no-commit,
     - commit-partial-install,
     - already-installed.

Suggested methods:
- Dafny / F* / Ivy / Coq depending on implementation language and team capability.
- The principle is refinement from protocol state machine to implementation, following the general assurance style seen in AWS TLA+ practice, IronFleet, and Verdi [R11]-[R13].

## 7.3 Safety properties to prove

The following are non-negotiable.

### P1. No double authority
No two distinct capsules hold valid prepared authority for the same object and next epoch.

### P2. Prepare durability
A successful grant response implies that prepare state will survive crash/restart.

### P3. Commit before visibility
No write becomes externally visible unless the corresponding commit record exists and install conditions hold.

### P4. No stale install
Install is rejected if:
- epoch is stale,
- commit sequence is stale,
- prepared capsule mismatches,
- touched-set membership mismatches.

### P5. Idempotent recovery
Repeated recovery/install actions produce the same stable state.

### P6. Expiry safety
If commit is absent at expiry, prepared state eventually clears and old ownership remains authoritative.

### P7. Fence safety
While an object is prepared, conflicting writes are rejected or blocked according to policy.

## 7.4 Liveness assumptions

Liveness proofs MUST be conditional on explicit assumptions, including:

- eventually stable communication between some quorum/witness path,
- bounded witness persistence failure,
- bounded clock/epoch skew or a well-defined logical epoch progression,
- non-Byzantine local storage in correct replicas,
- fair scheduling for recovery retries.

The proof plan MUST distinguish between:
- unconditional safety,
- assumption-dependent liveness.

## 7.5 Proof decomposition

The proof plan SHOULD decompose CEP into modules:

1. **Local object authority module**
2. **Capsule orchestration module**
3. **Witness durability module**
4. **Install/recovery module**
5. **Network wrapper / retry semantics**
6. **Cryptographic authenticity assumptions**

This reduces proof surface and supports independent verification.

## 7.6 Fault injection and differential testing

Formal work MUST be complemented by fault injection:

- duplicate messages,
- reordered messages,
- dropped install notices,
- crash after durable prepare,
- crash after durable commit,
- restart during partial install,
- delayed expiry notifications,
- replayed stale commit records.

Differential testing SHOULD compare:
- reference implementation,
- model oracle,
- randomized adversarial scheduler.

## 7.7 Implementation guidance

The production implementation SHOULD:

- make durable state explicit,
- avoid hidden side effects during prepare/install,
- separate pure validation from mutation,
- log enough structured metadata to reconstruct proof-relevant transitions.

## 7.8 Exit criteria

CEP is not implementation-ready until:

- abstract TLA+ safety checks pass,
- refinement artifacts exist,
- implementation-critical modules have stronger proof coverage,
- fault-injection and simulation results align with the model.

---

## 8. Embedded file: `Contestable_Reliance_Membrane.md`

# Contestable Reliance Membrane (CRM)

## 8.1 Purpose

The membrane governs how provisional work becomes durable shared knowledge and how claims become safe to rely on.

The key correction in this architecture is:

> heuristic claims are not failed deterministic claims.

Therefore the membrane MUST separate:

- **epistemic status** — what the system believes about the claim,
- **reliance status** — what the system is allowed to do with that claim.

## 8.2 Core split

### TruthStatus

```text
submitted
admissible
preferred
verified
contested
rejected
retired
```

### RelianceStatus

```text
sandbox
advisory
bounded_operational
ratified
revoked
expired
```

A claim family MAY have high TruthStatus and low RelianceStatus, or vice versa only under explicit policy.

## 8.3 Claim classes

The membrane applies different rules by class.

### Deterministic
Proof, replay, formal check, exact invariant validation.

### Empirical
Replication, rerun, benchmark reproduction, cross-provider reproduction.

### Statistical
Calibration, interval validity, proper score history, sample-size policy.

### Heuristic
Argumentation structure, challenge history, assumption stability, context matching, delayed truth if available.

### Normative
Human/governance policy. Verichain may validate process integrity, but policy ratification cannot be fully automated.

## 8.4 Why CRM exists

Without CRM, the system risks either:
- over-canonizing weak claims,
- or refusing to operationalize useful but imperfect claims.

CRM allows bounded operational use without pretending timeless truth.

## 8.5 Reliance Permit schema

```text
ReliancePermit =
  <family_id,
   context,
   horizon,
   risk_class,
   ttl_epoch,
   truth_status,
   reliance_status,
   rationale_root,
   approver_set,
   downgrade_rules,
   revocation_rule,
   policy_version>
```

A reliance permit is the durable authorization object for using a family in planning, execution, routing, or governance.

## 8.6 Promotion rules

### submitted -> admissible
Requires:
- schema-valid claim,
- identity and provenance check,
- evidence references present,
- family linkage valid.

### admissible -> preferred
Requires:
- argumentation engine finds membership in at least one preferred set,
- no immediate disqualifying contradiction,
- policy checks pass.

### preferred -> verified
Applies only where the claim class supports actual verification rules.

### advisory reliance
Requires:
- admissible or preferred truth status,
- low risk class,
- bounded TTL,
- no active high-confidence challenge.

### bounded_operational reliance
Requires:
- context and horizon specified,
- risk budget available,
- challenge window satisfied,
- margin over competing family members exceeds policy threshold,
- downgrade rules present,
- approval path satisfied for the risk class.

### ratified reliance
Requires governance or policy ratification where the risk class or domain demands it.

## 8.7 Downgrade rules

CRM MUST support automatic downgrade.

Triggers include:

- accepted challenge,
- invalidated assumption,
- artifact retrieval failure,
- verifier collusion evidence,
- calibration collapse,
- policy version invalidation,
- expiration of TTL,
- appearance of stronger family member or superseding bundle.

Automatic downgrade is a core safety feature.

## 8.8 Governance hooks

Governance enters in three places:

1. **High-risk operationalization**
   - medical, safety-critical, constitutional, or treasury-impacting families MAY require human or delegate ratification.

2. **Normative claim families**
   - truth is not enough; authority is required.

3. **Persistent contestation**
   - if a family remains contested beyond policy limits, governance MAY:
     - ratify one operational policy,
     - keep all candidates advisory only,
     - require human review,
     - demand further evidence generation.

## 8.9 Membrane certificate integration

For a bundle to be admitted, its membrane certificate MUST bind:

- claim family roots,
- contradiction roots,
- verifier certificate,
- artifact availability certificate,
- privacy and retention policy.

For heuristic families, the certificate MUST additionally bind:
- argumentation graph root,
- assumption graph root,
- reliance permit reference if any.

## 8.10 Sparse-ground-truth policy

When delayed truth is scarce or absent:

- calibration history is weak,
- score history is incomplete,
- argumentation structure matters more,
- governance or human review may be necessary.

CRM explicitly handles this by allowing:
- `preferred` truth status without operational ratification,
- `advisory` reliance without pretending canon,
- short-lived `bounded_operational` permits with tight downgrade rules.

## 8.11 Safety rules for CRM

1. A claim family MUST NOT receive ratified reliance without a named policy path.
2. Bounded operational reliance MUST always expire unless renewed.
3. Heuristic families MUST NOT be labeled timelessly canonical by default.
4. Revocation MUST be faster than initial ratification for high-risk domains.
5. Every reliance permit MUST name:
   - context,
   - horizon,
   - risk class,
   - downgrade triggers.

## 8.12 Acceptance criteria

CRM is acceptable if it prevents both:

- reckless operational canon,
- and useless paralysis.

---

## 9. Embedded file: `Heuristic_Family_Argumentation_Engine.md`

# Heuristic Family Argumentation Engine (HFAE)

## 9.1 Purpose

HFAE manages claim families where truth is uncertain, partially observable, delayed, or context-sensitive.

It provides:

- admissibility,
- preferred-set computation,
- graded ranking,
- challenge handling,
- assumption graph integration,
- champion selection for CRM.

HFAE is how Atrahasis reasons under uncertainty without collapsing into either binary truth or arbitrary opinion.

## 9.2 Family object

```text
HeuristicFamily =
  <family_id,
   context,
   horizon,
   risk_class,
   claim_nodes,
   support_edges,
   attack_edges,
   assumption_nodes,
   evidence_refs,
   score_history,
   challenge_log,
   current_champion,
   family_status>
```

## 9.3 Graph model

Let:

- `V_c` be claim nodes,
- `V_a` be assumption nodes,
- `E_sup` be support edges,
- `E_att` be attack edges,
- `E_dep` be dependency edges from assumptions to claims,
- `E_meta` be meta-attack or credibility challenge edges.

This is a typed argumentation graph, not a flat list.

## 9.4 Preferred-set computation

Use Dung-style admissibility as the baseline semantics [R14].

Procedure:

1. Build the attack graph over active claim nodes.
2. Filter claims that violate hard admissibility constraints:
   - malformed provenance,
   - unavailable artifacts,
   - invalid signature lineage,
   - policy-incompatible context/horizon.
3. Compute admissible sets.
4. Compute maximal admissible sets = preferred sets.
5. Mark each claim:
   - `inadmissible`
   - `admissible`
   - `preferred-set member`

Preferred-set membership is necessary but not sufficient for operational reliance.

## 9.5 Graded ranking

Where preferred semantics leave multiple plausible candidates, HFAE applies graded ranking.

For each claim `c`, define:

```text
Base(c) =
  α1 * EvidenceQuality(c) +
  α2 * VerifierDiversity(c) +
  α3 * ProvenanceStrength(c) +
  α4 * ContextMatch(c) +
  α5 * HistoricalUsefulness(c)
```

And iteratively compute dialectical strength:

```text
Strength_{t+1}(c) =
  σ(
    Base(c)
    + β1 * Σ_{s in Supporters(c)} w_sup(s,c) * Strength_t(s)
    - β2 * Σ_{a in Attackers(c)} w_att(a,c) * Strength_t(a)
    - β3 * AssumptionFragility(c)
    - β4 * SentinelRisk(c)
  )
```

Where:

- `σ` is a bounded activation or normalization function,
- `AssumptionFragility(c)` measures exposure to unstable assumptions,
- `SentinelRisk(c)` measures anomaly or collusion suspicion,
- weights are policy-tuned and class-specific.

This ranking is not a replacement for admissibility. It is a refinement layer for selection and scheduling.

## 9.6 Challenge handling

A challenge is a first-class object:

```text
Challenge =
  <challenge_id,
   target_claim,
   challenger,
   challenge_type,
   evidence_refs,
   deadline_epoch,
   severity,
   status>
```

Challenge types include:

- factual contradiction,
- evidence invalidity,
- provenance break,
- calibration failure,
- context mismatch,
- policy incompatibility,
- hidden assumption exposure.

Challenge flow:

```text
raised -> admitted -> under_review -> sustained | dismissed | escalated
```

Sustained challenges MAY:
- remove preferred membership,
- trigger CRM downgrade,
- create a verifier escalation,
- invalidate dependent claims via assumption graph propagation.

## 9.7 Assumption graph integration

Many heuristic claims depend on assumptions that are not themselves claims of the same class. HFAE therefore tracks explicit assumption nodes.

If assumption `a` supports claims `{c1, c2, c3}`, then invalidating `a` must propagate through dependency edges.

Each claim SHOULD maintain:

- assumption closure,
- minimal assumption cut,
- dominant fragility contributors.

This allows the system to distinguish:
- strong claims built on fragile assumptions,
- moderate claims built on robust assumptions.

## 9.8 Champion selection

The current operational leader in a family is the **champion**.

Champion selection requires:

1. claim is a preferred-set member,
2. `Strength(c)` exceeds `strength_min`,
3. margin over next-best preferred candidate exceeds `margin_min`,
4. no unsatisfied high-severity challenge,
5. CRM policy permits the proposed reliance level.

Selection formula:

```text
ChampionScore(c) =
  λ1 * Strength(c)
  + λ2 * CalibrationTerm(c)
  + λ3 * ContextCoverage(c)
  - λ4 * Fragility(c)
  - λ5 * ChallengePressure(c)
```

The top candidate becomes `current_champion` if it also passes the policy gates above.

## 9.9 Sparse-ground-truth handling

When delayed truth does not exist or is too sparse:

- `CalibrationTerm` may be absent or heavily discounted,
- argumentation and assumption structure dominate,
- governance review thresholds become stricter,
- champion TTL should be shorter,
- reliance status should usually stop at `advisory` or tightly bounded `bounded_operational`.

## 9.10 Update policy

HFAE MUST support:

- incremental graph updates,
- re-ranking after new evidence,
- challenge-triggered fast recomputation,
- family compaction of retired nodes,
- supersession links to preserve auditability.

## 9.11 Output to CRM

HFAE outputs at least:

```text
FamilyAssessment =
  <family_id,
   preferred_members,
   strength_vector,
   champion_candidate,
   attack_pressure,
   assumption_fragility_map,
   recommended_reliance_ceiling,
   rationale_root>
```

CRM then decides whether and how that assessment becomes an actual reliance permit.

## 9.12 Acceptance criteria

HFAE is acceptable if it:

- preserves explicit contestation,
- distinguishes admissibility from usefulness,
- supports downgrade when assumptions break,
- does not force false uniqueness where several claims remain defensible.

---

## 10. Embedded directory spec: `Parcel_Controller_Simulator/`

# Parcel Controller Simulator

This section specifies the simulator that MUST exist before the parcel controller and CEP can be trusted.

## 10.1 Purpose

The simulator evaluates:

- parcel controller stability,
- partitioning quality,
- CEP frequency,
- verifier spillover,
- recovery cost,
- hotspot behavior,
- controller resistance to adversarial workloads.

## 10.2 Required directory layout

```text
Parcel_Controller_Simulator/
  README.md
  pyproject.toml
  configs/
    baseline.yaml
    hotspot_drift.yaml
    toggle_hotspot.yaml
    capsule_flood.yaml
    verifier_storm.yaml
    regional_partition.yaml
    anti_locality_attack.yaml
  traces/
    synthetic/
    replay/
  workloads/
    generators.py
    adversarial.py
  state/
    loci.py
    parcels.py
    cso.py
    capsules.py
    claims.py
  controller/
    fast_loop.py
    slow_loop.py
    candidate_gen.py
    hysteresis.py
    rollback.py
  network/
    topology.py
    delay.py
    partition.py
  metrics/
    collectors.py
    score.py
  experiments/
    run_matrix.py
    compare_baselines.py
  reports/
    plots/
    summaries/
```

## 10.3 Simulation inputs

The simulator MUST accept:

- locus definitions,
- initial parcelization,
- object popularity distribution,
- operation class mix,
- verifier demand model,
- artifact size / availability model,
- network topology and regional latency,
- failure schedule,
- adversarial policy selection.

## 10.4 Core event types

- M-class event
- B-class event
- X-class local event
- X-class capsule event
- V-class verification event
- artifact retrieval delay/failure event
- parcel split/merge event
- parcel migration event
- node/region failure event
- challenge escalation event

## 10.5 Trace replay

The simulator MUST support trace replay from real or recorded workloads.

Required replay features:

- preserve ordering timestamps or causal windows,
- preserve per-operation touched set,
- preserve operation class,
- preserve artifact references,
- preserve verification outcomes where known.

Trace replay is essential because synthetic workloads alone do not reveal controller pathologies.

## 10.6 Workload families

### Baseline stationary
Stable locality, moderate contention.

### Hotspot drift
Access concentration shifts gradually.

### Toggle hotspot
Two regions alternate rapidly.

### Adversarial churn
Access edges are manipulated to bait repartition.

### Partition loss
Regional failure removes replicas and increases network delay.

### Verifier backlog
Claims spike faster than Verichain committees can absorb them.

### Capsule frequency sweep
Increase X-class shared mutation rate to observe when CEP becomes too common.

### Artifact withholding
Artifact retrieval intermittently fails or is delayed.

## 10.7 Metrics

The simulator MUST collect at least:

- p50/p95/p99 latency by class,
- remote X-class fraction,
- CEP invocation rate,
- Cut Commit fallback rate,
- parcel churn rate,
- migration bytes,
- verifier spillover,
- artifact backpressure,
- recovery surface,
- rollback count,
- controller oscillation count,
- throughput under partition,
- failed admission count,
- challenge-induced downgrade count.

## 10.8 Acceptance thresholds

The simulator configuration SHOULD allow policy thresholds such as:

- `max_parcel_churn_per_epoch`
- `max_remote_x_fraction`
- `max_capsule_fraction`
- `max_cut_commit_fraction`
- `max_recovery_surface`
- `max_verifier_spillover`
- `rollback_budget`

A design that only works when these thresholds are violated is not acceptable.

## 10.9 Comparative baselines

The simulator MUST compare Locus Fabric against at least:

- static placement baseline,
- aggressive repartition baseline,
- Schism-style workload partitioning baseline,
- Clay-style online repartition baseline,
- no-capsule distributed X-class baseline.

## 10.10 Required experiment matrix

Minimum matrix:

1. low / medium / high locality
2. low / medium / high contention
3. low / medium / high verifier pressure
4. low / medium / high partition severity
5. low / medium / high adversarial churn
6. low / medium / high capsule-demand workload

## 10.11 Outputs

Each run MUST emit:

- summary JSON,
- time-series metrics,
- event logs,
- controller decisions,
- parcel plan diffs,
- capsule traces,
- recovery traces.

## 10.12 Decision use

The simulator is not optional. It is the decision engine for:

- parcel controller policy acceptance,
- CEP threshold tuning,
- split/merge hysteresis tuning,
- controller rollback tuning,
- identifying workloads that collapse the design back into distributed transaction overload.

---

## 11. Integrated implementation roadmap

### Phase A — Architecture lock

Produce reviewed schemas for:

- Locus,
- Parcel,
- LSO,
- CSO,
- Capsule,
- Bundle,
- Membrane Certificate,
- Reliance Permit,
- Witness Seal.

### Phase B — Proof-first high-risk subsystems

Start with the two highest-risk protocol components:

1. CEP
2. CRM / HFAE boundary rules

### Phase C — Simulation-first controller work

Build `Parcel_Controller_Simulator/` before shipping automatic parcel split/merge.

### Phase D — Minimal viable execution path

Support:
- M-class merge state,
- B-class CSO for one bounded resource type,
- X-class local execution,
- CEP for bounded touched sets,
- deterministic membrane lane,
- heuristic advisory lane.

### Phase E — Hardening

Add:
- Orthogonal Sortition,
- Sentinel graph integration,
- artifact withholding penalties,
- multi-region witness anchoring,
- broader claim-family policy coverage.

---

## 12. Open unresolved research questions

1. **Parcel controller stability**  
   The bi-timescale design is conceptually stronger, but policy quality still depends on simulation and trace realism.

2. **CSO proof obligations**  
   Each CSO-compatible resource type still needs a proof that local slice use preserves the declared invariant.

3. **CEP production proof burden**  
   The TLA+ seed is only the start. Code-level or refinement-level assurance is still required.

4. **Sparse-ground-truth reliance**  
   CRM solves the policy framing, not the underlying epistemic difficulty. High-risk sparse-truth domains may still require governance and human review.

5. **Cut Commit discipline**  
   The system still needs governance over its own escape hatch. Excess fallback usage should be treated as architecture failure.

6. **Verifier collusion under hidden common control**  
   Orthogonal sortition reduces obvious correlated-failure domains, but hidden economic control remains hard.

7. **Artifact-plane coupling**  
   Admission and recovery depend on artifact availability more than classical transaction systems do.

---

## 13. References and design antecedents

### Internal Atrahasis design context

- `collective_intelligence_master_blueprint.md`
- `AASL System.txt`
- `aichain_node_implementation_specification.md`
- `aichain_consensus_protocol.md`
- `atrahasis_master_handoff_complete.md`

### External references

**[R1]** Carlo Curino et al., *Schism: a Workload-Driven Approach to Database Replication and Partitioning*, VLDB 2010.  
<https://15799.courses.cs.cmu.edu/fall2013/static/papers/schism-vldb2010.pdf>

**[R2]** Marco Serafini et al., *Clay: Fine-Grained Adaptive Partitioning for General Database Schemas*, PVLDB 2016.  
<https://hstore.cs.brown.edu/papers/hstore-clay.pdf>

**[R3]** Aaron J. Elmore et al., *Squall: Fine-Grained Live Reconfiguration for Partitioned Main Memory Databases*, SIGMOD 2015.  
<https://db.cs.cmu.edu/papers/2015/p299-elmore.pdf>

**[R4]** Antonios Katsarakis et al., *Zeus: Locality-aware Distributed Transactions*, SIGMOD 2021 / arXiv.  
<https://www.microsoft.com/en-us/research/wp-content/uploads/2021/04/zeus-authors.pdf>

**[R5]** Patrick E. O’Neil, *The Escrow Transactional Method*, TODS 1986.  
<https://www.ics.uci.edu/~cs223/papers/p405-o_neil.pdf>

**[R6]** Vitor Balegas et al., *Extending Eventually Consistent Cloud Databases for Enforcing Numeric Invariants*, 2015.  
<https://www.dpss.inesc-id.pt/~rodrigo/srds15.pdf>

**[R7]** Peter Bailis et al., *Highly Available Transactions: Virtues and Limitations*, VLDB 2014.  
<https://www.vldb.org/pvldb/vol7/p181-bailis.pdf>

**[R8]** Martin Kleppmann and Heidi Howard, *Byzantine Eventual Consistency and the Fundamental Limits of Peer-to-Peer Databases*, 2020.  
<https://arxiv.org/pdf/2012.00472>

**[R9]** Mike Burrows, *The Chubby Lock Service for Loosely-Coupled Distributed Systems*, OSDI 2006.  
<https://research.google.com/archive/chubby-osdi06.pdf>

**[R10]** Iulian Moraru et al., *Paxos Quorum Leases: Fast Reads Without Sacrificing Writes*, SoCC 2014.  
<https://www.cs.cmu.edu/~dga/papers/leases-socc2014.pdf>

**[R11]** Chris Newcombe et al., *Use of Formal Methods at Amazon Web Services*, 2015.  
<https://lamport.azurewebsites.net/tla/formal-methods-amazon.pdf>

**[R12]** Chris Hawblitzel et al., *IronFleet: Proving Practical Distributed Systems Correct*, SOSP 2015.  
<https://www.andrew.cmu.edu/user/bparno/papers/ironfleet.pdf>

**[R13]** James R. Wilcox et al., *Verdi: A Framework for Implementing and Formally Verifying Distributed Systems*, PLDI 2015.  
<https://homes.cs.washington.edu/~ztatlock/pubs/verdi-wilcox-pldi15.pdf>

**[R14]** Phan Minh Dung, *On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games*, 1995.  
<https://www.sci.brooklyn.cuny.edu/~parsons/courses/716-spring-2010/papers/dung.pdf>

**[R15]** Matthias Thimm et al., *Probabilistic Graded Semantics*, 2018.  
<https://www.mthimm.de/pub/2018/Thimm_2018b.pdf>

**[R16]** Benjamin Irwin, Antonio Rago, and Francesca Toni, *Forecasting Argumentation Frameworks*, KR 2022.  
<https://proceedings.kr.org/2022/55/kr2022-0055-irwin-et-al.pdf>

**[R17]** Tilmann Gneiting and Adrian E. Raftery, *Strictly Proper Scoring Rules, Prediction, and Estimation*, JASA 2007.  
<https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf>

**[R18]** Yuqing Kong et al., *Calibration without Ground Truth*, 2026.  
<https://arxiv.org/pdf/2601.19862>

---

## Closing status

This master specification establishes the current best architecture baseline for Atrahasis AIChain redesign:

- **stable logical loci**
- **elastic parcels**
- **proof-carrying bounded resource objects**
- **capsule-based rare exclusive cross-parcel execution**
- **verification-gated memory admission**
- **contestable reliance rather than fake certainty**
- **simulation-first control for dynamic placement**

The next step is not another prose redesign.  
The next step is to instantiate the simulator, the TLA+ model, and the proof track.
