# C23 - Sovereign Cell Runtime (SCR)

## Master Technical Specification

**Document ID:** C23-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-12
**Invention ID:** C23
**System:** Atrahasis Agent System v2.4
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL - Atrahasis LLC
**Normative References:** C3 (Tidal Noosphere v2.0), C5 (PCVM v2.0), C7 (RIF v2.0), C8 (DSF v2.0), C22 (Implementation Planning), C31 (optional locality enrichment), C38 (FSPA), C39 (LCML), C40 (DAAF), C42 (LPEM), T-290 (AXIP-v1)
**Resolves:** T-061 Agent Execution Runtime

---

## Abstract

Atrahasis has no canonical runtime substrate between C7 Parcel Executors and actual agent work. C7 can decompose an intent and C3 can schedule an operation, but the stack never specifies what exists on the other side of that scheduling decision: how an assigned agent receives bounded rights, how model access is provisioned, how tool/network access is constrained, how execution is isolated, or how runtime activity becomes auditable evidence for C5 verification and C8 settlement.

This specification introduces the **Sovereign Cell Runtime (SCR)**. SCR separates persistent agent identity from transient execution. Each leaf intent runs inside a **Sovereign Cell** under an explicit **Execution Lease** that carries the runtime profile, allowed tools, inference rights, resource budget, evidence obligations, and required isolation class. SCR is subordinate to C3 and C7: it does not schedule parcels or decompose intents. It realizes already-assigned work inside parcel-local hosts, meters resource consumption, brokers model access, seals execution evidence, and reports outcomes upward.

The invention's central contribution is making a lease-bound sovereign cell the runtime's first-class object. That object binds together five concerns that existing systems usually scatter across separate tools: execution isolation, capability rights, model provisioning, evidence collection, and settlement metering.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Design Principles](#2-design-principles)
3. [Runtime Model](#3-runtime-model)
   - [3.1 Core Entities](#31-core-entities)
   - [3.2 Runtime Profiles](#32-runtime-profiles)
   - [3.3 Cell Profiles](#33-cell-profiles)
   - [3.4 Execution Lease](#34-execution-lease)
   - [3.5 Cell Lifecycle](#35-cell-lifecycle)
   - [3.6 State and Artifact Model](#36-state-and-artifact-model)
4. [Architecture](#4-architecture)
   - [4.1 Locus Runtime Controller](#41-locus-runtime-controller)
   - [4.2 Parcel Runtime Host](#42-parcel-runtime-host)
   - [4.3 Inference Lease Broker](#43-inference-lease-broker)
   - [4.4 Tool Capability Broker](#44-tool-capability-broker)
   - [4.5 Execution Evidence Bundle](#45-execution-evidence-bundle)
   - [4.6 End-to-End Flow](#46-end-to-end-flow)
5. [Integration Contracts](#5-integration-contracts)
6. [Parameters](#6-parameters)
7. [Formal Requirements](#7-formal-requirements)
8. [Patent-Style Claims](#8-patent-style-claims)
9. [Risk Analysis](#9-risk-analysis)
10. [Deployment and Implementation Path](#10-deployment-and-implementation-path)
11. [Appendix A: Pseudocode](#11-appendix-a-pseudocode)

---

## 1. Motivation

### 1.1 The Missing Runtime Layer

The current stack defines:

- **what** work exists (C7 intent algebra),
- **where** it should run (C3 parcel assignment),
- **how** output should be verified (C5),
- **how** it should be metered and paid (C8),
- **which** implementation technologies are planned (C22).

It does not define:

- the execution unit,
- the isolation boundary,
- the resource lease,
- model and tool rights,
- the evidence record produced by runtime execution.

This gap is not cosmetic. Without a runtime spec, C7's Parcel Executor pseudocode ends at `c3.schedule_operation(...)`, and C22's Wave 1 implementation plan assumes provider adapters and runtime components that have no normative contract.

### 1.2 Why Generic Runtime Patterns Are Not Enough

Generic container runtimes and workflow engines are insufficient because Atrahasis requires:

1. **Identity sovereignty.** Agent identity, governance standing, and credibility history cannot collapse into container lifetime.
2. **Operation-class-aware execution.** A governance action and a low-risk merge query cannot share the same runtime policy by default.
3. **Inference as a leased right.** Model access is part of execution policy, not ambient process state.
4. **Evidence-bearing runtime.** Runtime activity must produce auditable evidence for C5 and metering inputs for C8.

### 1.3 Scope

SCR adds the missing execution substrate. It does **not** replace:

- C7 decomposition or Parcel Executor authority,
- C3 parcel placement or epoch scheduling,
- C5 claim verification,
- C8 settlement policy,
- C22 implementation planning.

SCR defines how already-assigned work is admitted, realized, isolated, provisioned, observed, and sealed.

---

## 2. Design Principles

1. **Identity outside execution.** Agent identity persists independently of any particular runtime cell.
2. **Lease everything.** Tools, model access, budgets, and time windows are explicit lease fields, never ambient permissions.
3. **Stay below C7/C3.** SCR is an execution substrate, not a scheduler or planner.
4. **Evidence is mandatory.** Every completed lease emits an Execution Evidence Bundle (EEB).
5. **Provenance is not reproducibility.** Hosted and stochastic inference may be auditable without being replay-identical.
6. **Risk derives isolation.** Stronger trust and higher stakes require stronger cell profiles.
7. **One admission signal.** Upstream components see unified backpressure rather than hidden sub-queues.

---

## 3. Runtime Model

### 3.1 Core Entities

| Entity | Purpose |
|---|---|
| **Agent Identity** | Persistent Atrahasis subject with registry, credibility, and governance standing outside the runtime cell |
| **Runtime Profile** | Workload semantics for the agent's current execution mode |
| **Execution Lease** | Signed authorization to run one leaf intent under explicit rights and budgets |
| **Sovereign Cell** | The transient isolated execution environment created from an execution lease |
| **Inference Lease** | Sub-lease for model/provider access with token, latency, and provider policy bounds |
| **Tool Capability Token** | Scoped right to invoke a named tool, connector, or network egress class |
| **Execution Evidence Bundle (EEB)** | Sealed record of what the runtime did, what it consumed, and what artifacts it produced |

### 3.2 Runtime Profiles

Runtime profiles classify execution semantics. They are not constitutional AAS roles and do not override governance or authorship.

| Profile | Typical Work | Default Traits |
|---|---|---|
| `REASONER` | analysis, planning, decomposition support | high token budget, low external tool count |
| `TOOL_RUNNER` | bounded tool invocation, transformations, extraction | stricter tool token policy, moderate inference |
| `VERIFIER` | claim checking, replay, structural validation | stronger isolation, high evidence requirements |
| `SYNTHESIZER` | long-context integration and drafting | larger context lease, stronger artifact sealing |
| `SENTINEL` | monitoring and anomaly detection | low-latency repeated leases, narrow model/tool set |
| `GOVERNANCE` | constitutional actions, ratification support | strongest isolation, no discretionary network egress |

### 3.3 Cell Profiles

Every Sovereign Cell uses one derived cell profile:

| Cell Profile | Isolation Strength | Typical Use |
|---|---|---|
| `LIGHTWEIGHT` | process/user-namespace sandbox, no external network | low-risk M/B work, internal transforms |
| `SANDBOXED` | hardened container or equivalent sandbox, scoped filesystem and tool broker | X/V work, local tool invocation, file transforms |
| `ATTESTED` | microVM or equivalently strong attested sandbox | G-class work, verifier-critical work, external provider credentials, high-risk native machine actions |

**Derivation rules**

- `G` operation class -> `ATTESTED`
- `V` operation class -> at least `SANDBOXED`; `ATTESTED` if hosted provider or external connector is used
- `X` operation class -> at least `SANDBOXED`
- `B` and `M` operation classes -> `LIGHTWEIGHT` unless tool, filesystem, or network policy escalates
- any lease carrying external credentials -> `ATTESTED`

### 3.4 Execution Lease

The Execution Lease is the runtime's main object.

Required fields:

- `lease_id`
- `intent_id`
- `agent_id`
- `runtime_profile`
- `cell_profile`
- `operation_class`
- `deadline_epoch`
- `cpu_ms_budget`
- `memory_mib_budget`
- `scratch_mib_budget`
- `max_retries`
- `tool_tokens[]`
- `inference_policy`
- `evidence_level`
- `settlement_metering_class`

Semantics:

- one lease authorizes one active cell at a time,
- lease renewal requires an explicit controller action,
- lease expiry triggers quiesce and seal behavior,
- no lease means no execution.

### 3.5 Cell Lifecycle

```
PREPARED -> LEASED -> WARM -> ACTIVE -> QUIESCING -> SEALED -> DISSOLVED
```

| State | Meaning |
|---|---|
| `PREPARED` | image and inputs staged, not yet admitted |
| `LEASED` | lease accepted and rights materialized |
| `WARM` | reusable runtime shell ready but not yet executing user work |
| `ACTIVE` | leaf intent running |
| `QUIESCING` | deadline reached, cancellation received, or normal teardown starting |
| `SEALED` | evidence finalized, artifacts hashed, metering frozen |
| `DISSOLVED` | cell removed; only evidence and approved outputs remain |

The agent identity survives cell dissolution. The cell does not.

### 3.6 State and Artifact Model

SCR forbids hidden durable state inside the cell:

- inputs are mounted as immutable snapshots or declared handles,
- scratch space is bounded and destroyed on dissolution,
- durable outputs must be emitted as declared artifacts or claim parcels,
- long-term knowledge writes route through C6 contracts rather than private runtime storage.

This preserves auditability and keeps the runtime from becoming a shadow knowledge store.

---

## 4. Architecture

### 4.1 Locus Runtime Controller

Each locus hosts an **LRC** responsible for:

- validating lease requests from Parcel Executors,
- checking runtime-profile compatibility,
- issuing or rejecting execution leases,
- exporting one backpressure signal per parcel and per profile,
- managing warm-pool budgets.

The LRC does **not** choose parcel placement. It only decides whether the assigned parcel can realize the work under policy and capacity.

### 4.2 Parcel Runtime Host

Each parcel hosts one **PRH** that:

- materializes cells,
- binds tool and inference sub-leases,
- mounts inputs and scratch volumes,
- streams runtime telemetry,
- seals EEBs,
- returns completion/failure to the C7 Parcel Executor.

The PRH is the execution analog of a node-local runtime host, but it is parcel-scoped to preserve C3 locality semantics.

### 4.3 Inference Lease Broker

The **ILB** is the only legal path to model access.

Inputs:

- runtime profile,
- requested model class,
- latency target,
- secrecy requirements,
- token budget,
- provider allowlist / denylist.

Outputs:

- provider selection,
- endpoint handle,
- token ceiling,
- session TTL,
- replayability classification (`REPLAYABLE`, `PROVENANCE_ONLY`, `NON_REPLAYABLE`).

Provider classes:

- local in-locus serving,
- local cross-locus serving,
- hosted provider via approved adapter.

The ILB treats inference as scarce capacity. It can deny or defer a lease even when CPU is available.

### 4.4 Tool Capability Broker

All external rights other than model calls are issued through the **Tool Capability Broker (TCB)**.

Example capability classes:

- filesystem transform
- package execution
- HTTP egress to approved domain set
- database query
- governance-signing request
- artifact publishing

Tokens are:

- lease-bound,
- time-bounded,
- capability-specific,
- non-transferrable.

### 4.5 Execution Evidence Bundle

Every completed or failed lease emits an **EEB**.

Minimum fields:

- `lease_id`
- `intent_id`
- `agent_id`
- `runtime_profile`
- `cell_profile`
- `started_at`
- `ended_at`
- `resource_consumed`
- `inference_calls[]`
- `tool_invocations[]`
- `input_artifact_digests[]`
- `output_artifact_digests[]`
- `replayability_class`
- `error_summary`
- `controller_signature`

The EEB is not a claim verdict. It is runtime provenance. C5 may consume it to validate process conformance, tool disclosure, or replay support; C8 consumes it for settlement metering.

### 4.6 End-to-End Flow

1. C7 Parcel Executor submits a lease request for a leaf intent.
2. LRC validates capacity, profile compatibility, and policy.
3. PRH selects or prepares a compatible cell.
4. ILB and TCB issue sub-leases as needed.
5. Cell executes under budget and deadline.
6. PRH seals an EEB and emits declared outputs.
7. Parcel Executor receives the execution report.
8. C5 and C8 consume the EEB according to their own rules.

---

## 5. Integration Contracts

### 5.1 SCR <-> C7 RIF

What C7 provides:

- leaf intent,
- operation class,
- success criteria,
- assigned agent and parcel,
- deadline and priority.

What SCR returns:

- execution outcome,
- EEB reference,
- resource consumption,
- output artifact references,
- precise failure reason on denial, timeout, or policy breach.

### 5.2 SCR <-> C3 Tidal Noosphere

What C3 provides:

- parcel assignment,
- epoch boundaries,
- capacity snapshot inputs,
- schedule timing and local placement context.

What SCR returns:

- runtime backpressure metrics,
- warm-pool utilization,
- per-profile capacity claims,
- execution completion events aligned to epoch boundaries where required.

SCR must never rewrite parcel placement or the tidal scheduler.

### 5.3 SCR <-> C5 PCVM

SCR provides:

- EEBs,
- replayability classification,
- tool and model disclosure,
- artifact digests.

C5 uses this for:

- P-class process conformance,
- E/R/S claim support context,
- verifier audit replay planning.

### 5.4 SCR <-> C8 DSF

SCR provides:

- cpu/memory/time consumption,
- provider token spend,
- retry count,
- deadline compliance,
- completion class.

C8 uses this for settlement metering and runtime-cost accounting.

### 5.5 SCR <-> C22 Implementation Planning

SCR defines the missing normative contract beneath the provider adapters and runtime assumptions already referenced in C22. C22 remains the wave plan; SCR becomes the runtime subsystem that those waves implement.

### 5.6 Optional SCR <-> C31 CAT

If CAT is enabled, DAN locality may inform warm-pool reuse and artifact caching, but:

- DAN membership must not weaken isolation,
- DAN roles must not bypass leases,
- DAN data must not enter C5 verification decisions.

---

## 6. Parameters

| Parameter | Default | Meaning |
|---|---|---|
| `MAX_LEASE_EPOCHS` | 3 | maximum lease duration before explicit renewal |
| `LIGHTWEIGHT_MAX_SCRATCH_MIB` | 256 | scratch cap for lightweight cells |
| `SANDBOXED_MAX_SCRATCH_MIB` | 1024 | scratch cap for sandboxed cells |
| `ATTESTED_MAX_SCRATCH_MIB` | 2048 | scratch cap for attested cells |
| `PARCEL_WARM_POOL_TARGET` | 2 per profile | warm cell count target |
| `WARM_POOL_MAX_SHARE` | 0.20 | max parcel capacity reserved for warm cells |
| `INFERENCE_LEASE_TTL_MS` | 300000 | default inference session TTL |
| `MAX_TOOL_TOKENS_PER_LEASE` | 8 | upper bound on capability tokens |
| `EEB_REQUIRED` | true | require evidence bundle emission |
| `HOSTED_PROVIDER_ATTESTED_REQUIRED` | true | hosted-provider calls require attested profile |
| `LEASE_BACKPRESSURE_THRESHOLD` | 0.85 | deny or defer new leases above this utilization |
| `MAX_RETRIES_PER_LEAF` | 2 | runtime retry cap before escalation |
| `PROVENANCE_SAMPLE_PAYLOAD_BYTES` | 32768 | max raw payload retained in evidence |
| `NON_REPLAYABLE_DISCLOSURE_REQUIRED` | true | hosted/stochastic runs must say they are not replay-identical |

---

## 7. Formal Requirements

1. **SCR-01** Every active execution SHALL be bound to exactly one execution lease.
2. **SCR-02** No tool or network access SHALL exist outside lease-bound capability tokens.
3. **SCR-03** All model access SHALL flow through the Inference Lease Broker.
4. **SCR-04** The runtime SHALL preserve agent identity outside the cell lifecycle.
5. **SCR-05** SCR SHALL NOT change parcel placement or intent decomposition.
6. **SCR-06** Cell profile derivation SHALL be deterministic from operation class and lease policy.
7. **SCR-07** All G-class execution SHALL use the `ATTESTED` cell profile.
8. **SCR-08** Any hosted-provider inference using secrets or external credentials SHALL use the `ATTESTED` cell profile.
9. **SCR-09** Every completed or failed lease SHALL emit an EEB.
10. **SCR-10** The EEB SHALL distinguish replayability from provenance.
11. **SCR-11** Runtime scratch state SHALL be destroyed on dissolution unless explicitly emitted as a declared artifact.
12. **SCR-12** Warm-pool reservation SHALL remain below `WARM_POOL_MAX_SHARE`.
13. **SCR-13** The LRC SHALL export one admission/backpressure signal per parcel/profile combination.
14. **SCR-14** Runtime retries SHALL remain within `MAX_RETRIES_PER_LEAF` and SHALL be reported in the EEB.
15. **SCR-15** Settlement metering SHALL use lease and runtime telemetry rather than unbounded host-side estimates.
16. **SCR-16** A PRH SHALL reject any lease whose required rights exceed parcel policy or available capacity.
17. **SCR-17** Non-replayable executions SHALL carry explicit disclosure in both the EEB and the execution report.
18. **SCR-18** No cell may persist a hidden durable store outside declared artifact and knowledge-layer contracts.

---

## 8. Patent-Style Claims

1. A runtime system for multi-agent execution in which an assigned agent identity is decoupled from a transient execution cell, and wherein the execution cell is instantiated only under an explicit lease carrying resource limits, tool rights, model rights, and evidence obligations.
2. The runtime system of claim 1, wherein model access is granted only through an inference sub-lease broker that classifies each provider path by replayability and secrecy constraints.
3. The runtime system of claim 1, wherein each completed or failed execution emits a sealed execution evidence bundle containing runtime telemetry, tool invocations, inference disclosures, and artifact digests for downstream verification and settlement.
4. The runtime system of claim 1, wherein isolation strength is derived from operation class and trust boundary such that governance and high-trust executions are forced into an attested cell profile while lower-risk executions may use lighter-weight profiles.

---

## 9. Risk Analysis

### 9.1 Primary Risks

| Risk | Description | Mitigation |
|---|---|---|
| Evidence theater | provenance mistaken for reproducibility | explicit replayability classes |
| Warm-pool waste | too many pre-warmed cells or model sessions | bounded warm pools and controller feedback |
| Hidden bottlenecks | cell queue, tool queue, and model queue drift apart | single admission signal from the LRC |
| Permission creep | developers smuggle ambient rights into base images | no ambient rights, tokenized capabilities only |
| Runtime drift | SCR starts duplicating scheduler logic | explicit contract boundary with C3/C7 |

### 9.2 Residual Risk

Risk remains **HIGH** because the subsystem is foundational and touches isolation, provider integration, and settlement metering simultaneously. The risk is acceptable because the design is additive, bounded, and incrementally deployable.

---

## 10. Deployment and Implementation Path

### Phase 1 - Bootstrap

- implement LRC, PRH, and lightweight/sandboxed cells
- local provider adapters only
- EEB emission for all leases
- no hosted provider path for governance or verification work

### Phase 2 - Hardened Runtime

- attested cells
- hosted-provider inference leases
- richer capability tokens
- C5 and C8 integration hardening

### Phase 3 - Runtime Optimization

- warm-pool tuning
- parcel-local artifact caching
- optional C31 locality hints
- multi-locus inference routing with explicit policy

Kill criteria:

- runtime admission/backpressure is not observable upstream,
- EEB completeness cannot support basic C5 process-conformance checks,
- hosted-provider disclosure cannot honestly separate provenance from replayability.

---

## 11. Appendix A: Pseudocode

### A.1 Cell Profile Derivation

```text
function derive_cell_profile(op_class, requires_hosted_provider, has_external_connector):
    if op_class == "G":
        return "ATTESTED"
    if requires_hosted_provider or has_external_connector:
        return "ATTESTED"
    if op_class in {"V", "X"}:
        return "SANDBOXED"
    return "LIGHTWEIGHT"
```

### A.2 Lease Admission

```text
function admit_lease(request):
    profile = derive_cell_profile(
        request.operation_class,
        request.inference_policy.requires_hosted_provider,
        request.tool_policy.has_external_connector
    )

    if request.rights_exceed_policy:
        return REJECT("POLICY_DENIED")
    if parcel_utilization(request.parcel_id, profile) >= LEASE_BACKPRESSURE_THRESHOLD:
        return DEFER("BACKPRESSURE")

    return ISSUE_LEASE(profile)
```

### A.3 Execution Flow

```text
function execute_leaf(lease):
    cell = prh.materialize_cell(lease)
    tool_tokens = tcb.issue_tokens(lease)
    inference = ilb.issue_lease(lease)

    result = cell.run(
        inputs = lease.inputs,
        tool_tokens = tool_tokens,
        inference = inference,
        budgets = lease.budgets
    )

    eeb = seal_evidence(lease, result)
    report_to_parcel_executor(result, eeb)
```

---

## Conclusion

SCR supplies the missing runtime answer in the Atrahasis stack. It gives C7 and C3 a concrete execution substrate without turning the runtime into a rival scheduler. It gives C5 and C8 the evidence and metering contract they were missing. Most importantly, it defines how an Atrahasis agent actually runs: not as a generic process with ambient rights, but as a sovereign identity temporarily embodied in a lease-bound cell with explicit permissions, bounded resources, and mandatory evidence.
