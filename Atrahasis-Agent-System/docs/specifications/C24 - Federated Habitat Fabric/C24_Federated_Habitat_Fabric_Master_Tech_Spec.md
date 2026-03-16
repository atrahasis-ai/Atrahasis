# C24 - Federated Habitat Fabric (FHF)

## Master Technical Specification

**Document ID:** C24-MTS-v1.0
**Version:** 1.0.0
**Date:** 2026-03-12
**Invention ID:** C24
**System:** Atrahasis Agent System v2.4
**Status:** SPECIFICATION COMPLETE
**Classification:** CONFIDENTIAL - Atrahasis LLC
**Normative References:** C3 (Tidal Noosphere v2.0), C7 (RIF v2.0), C8 (DSF v2.0), C14 (AiBC v2.0), C22 (Implementation Planning), C23 (SCR v1.0)
**Resolves:** T-065 Infrastructure & Federation

---

## Abstract

Atrahasis defines logical coordination domains, runtime execution, governance, and settlement, but lacks the deployment primitive that maps those abstractions onto real infrastructure. This specification introduces the **Federated Habitat Fabric (FHF)**. FHF defines the **Habitat** as a region-scoped infrastructure domain that hosts loci, parcel runtime hosts, state services, governance relays, and explicit federation gateways.

Most operations remain habitat-local. Cross-region exchange is constrained to **Habitat Boundary Gateways (HBGs)** and typed **Habitat Boundary Capsules (HBCs)** that carry approved summaries, artifacts, governance payloads, and explicit cross-habitat coordination traffic. FHF does not replace C3's logical topology. It makes that topology deployable without collapsing into a flat global mesh or a generic “just run a cluster” answer.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Design Principles](#2-design-principles)
3. [Habitat Model](#3-habitat-model)
4. [Five-Plane Architecture](#4-five-plane-architecture)
5. [Federation Boundary Model](#5-federation-boundary-model)
6. [State Residency Model](#6-state-residency-model)
7. [Integration Contracts](#7-integration-contracts)
8. [Deployment Profiles](#8-deployment-profiles)
9. [Parameters](#9-parameters)
10. [Formal Requirements](#10-formal-requirements)
11. [Patent-Style Claims](#11-patent-style-claims)
12. [Risk Analysis](#12-risk-analysis)
13. [Appendix A: Pseudocode](#13-appendix-a-pseudocode)

---

## 1. Motivation

### 1.1 The Missing Deployment Primitive

C3 defines loci and parcels as logical execution structures. C23 defines how assigned work runs inside parcel-local runtime hosts. C22 defines technology choices and staffing. None of them define the region-scoped infrastructure domain that should host these components or the rules for moving information across regions.

Without such a primitive, implementation would drift into inconsistent assumptions about:

- region boundaries,
- failure domains,
- gateway policy,
- state placement,
- cross-region coordination.

### 1.2 Why Generic Cluster Topology Is Not Enough

Generic cluster architecture is insufficient because Atrahasis needs:

1. locality-first coordination,
2. explicit boundaries for exportable versus non-exportable state,
3. governance and runtime aligned to the same failure domains,
4. a clean migration path from single-region bootstrap to multi-region federation.

### 1.3 Scope

FHF defines the infrastructure boundary model below the logical stack and above substrate tooling. It does not redefine:

- C3 loci/parcels,
- C7 decomposition logic,
- C23 execution leases,
- C8 settlement semantics,
- C14 governance authority.

It defines where those systems live and how habitats federate.

---

## 2. Design Principles

1. **Local first.** Most traffic and state remain habitat-local.
2. **Boundaries are real.** Cross-habitat movement requires explicit gateway handling.
3. **One failure model per habitat.** Runtime, governance, and state align to the same regional boundary.
4. **Typed export only.** Exportable traffic crosses habitats as typed capsules, not ad hoc streams.
5. **Bootstrap small, scale cleanly.** A single-habitat deployment must preserve the same architecture rather than living on exceptions.

---

## 3. Habitat Model

### 3.1 Definition

A **Habitat** is the canonical region-scoped Atrahasis infrastructure domain.

Each habitat contains:

- one or more loci,
- parcel runtime hosts from C23,
- habitat-local message and control services,
- habitat-local state services,
- habitat governance relay,
- one or more habitat boundary gateways.

### 3.2 Hierarchy

```text
Region -> Habitat -> Locus Group -> Parcel Runtime Hosts -> Sovereign Cells
```

Rules:

- a parcel SHALL belong to exactly one habitat,
- a locus SHALL have a primary habitat,
- parcels SHALL NOT span habitats,
- sovereign cells run only on parcel runtime hosts inside the parcel's habitat.

### 3.3 Why Habitat Is Needed

The habitat is the missing deployment primitive between:

- logical topology (`locus`, `parcel`),
- physical/cloud substrates (clusters, hosts, storage, networks).

It makes locality and failure domains operational rather than merely conceptual.

---

## 4. Five-Plane Architecture

### 4.1 Habitat Control Plane

Responsibilities:

- habitat membership and placement policy,
- parcel-to-host assignment policy,
- capacity and warm-pool coordination,
- gateway and relay registration,
- habitat health summaries.

### 4.2 Habitat Data Plane

Carries:

- parcel-local task traffic,
- runtime execution traffic,
- habitat-local service communication,
- low-latency operational traffic that must stay within the habitat.

Default rule:

- data plane traffic does not cross habitat boundaries directly.

### 4.3 Habitat State Plane

Hosts:

- habitat-local ledgers and caches,
- runtime artifact stores,
- replicated summaries,
- state export queues.

The state plane enforces residency classes defined in Section 6.

### 4.4 Habitat Governance Plane

Carries:

- governance relay traffic,
- constitutional and operational voting transport,
- inter-habitat governance coordination payloads,
- audit-significant operational directives.

The governance plane is separate from the ordinary data plane because governance liveness must survive local workload churn.

### 4.5 Habitat Federation Plane

The federation plane is the only inter-habitat transport surface.

It is carried by **Habitat Boundary Gateways** and transmits **Habitat Boundary Capsules** only.

---

## 5. Federation Boundary Model

### 5.1 Habitat Boundary Gateway

An **HBG** is the only legal path for traffic crossing habitats.

Responsibilities:

- policy check on outgoing/imported capsules,
- traffic typing and prioritization,
- integrity and provenance checks,
- rate limiting and locality budget enforcement,
- export/import logging.

### 5.2 Habitat Boundary Capsule

An **HBC** is a typed, explicit inter-habitat exchange envelope.

Allowed capsule classes:

- `DISCOVERY_SUMMARY`
- `STATE_SUMMARY`
- `GOVERNANCE_RELAY`
- `APPROVED_ARTIFACT_EXPORT`
- `CROSS_HABITAT_OPERATION`
- `RECOVERY_SYNC_STUB`

Each HBC contains:

- capsule id,
- source habitat,
- destination habitat or federation group,
- capsule class,
- payload digest,
- payload location/reference,
- export policy tag,
- issuance epoch,
- expiry epoch,
- integrity signature.

### 5.3 Federation Windows

Cross-habitat exchange occurs during explicit **Federation Windows**:

- periodic windows every `FEDERATION_WINDOW_EPOCHS`,
- immediate windows for urgent governance or safety traffic,
- explicit X/G/V class workflows that require inter-habitat coordination.

This prevents background drift into a flat always-on WAN mesh.

### 5.4 Default-Deny Rule

No direct parcel-to-parcel or host-to-host inter-habitat traffic is allowed unless it is:

- encapsulated as an HBC,
- approved by HBG policy,
- attributable to an allowed capsule class.

---

## 6. State Residency Model

Every state class must declare a residency class:

| Residency Class | Meaning |
|---|---|
| `LOCAL_ONLY` | may not leave the habitat |
| `SUMMARY_EXPORTABLE` | local source of truth, only summary export permitted |
| `APPROVED_EXPORTABLE` | exportable with explicit gateway approval |
| `FEDERATED_DISCOVERABLE` | discoverable across habitats, but not necessarily fully replicated |

Examples:

- parcel runtime scratch state -> `LOCAL_ONLY`
- habitat capacity summaries -> `SUMMARY_EXPORTABLE`
- approved published artifacts -> `APPROVED_EXPORTABLE`
- habitat directory and routing metadata -> `FEDERATED_DISCOVERABLE`

This keeps consistency costs bounded and prevents accidental global replication of local state.

---

## 7. Integration Contracts

### 7.1 FHF <-> C3

FHF gives C3 a concrete hosting boundary:

- loci live within habitats,
- parcels are habitat-local,
- cross-habitat coordination must not masquerade as ordinary intra-locus traffic.

### 7.2 FHF <-> C23

Parcel Runtime Hosts are habitat-local resources. FHF determines:

- where they run,
- which state and buses they can reach,
- what failure domain they inherit,
- how their outputs may be exported.

### 7.3 FHF <-> C7

C7 retains logical orchestration authority. FHF provides:

- placement and reachability assumptions,
- habitat-local execution domains,
- the federation surface for explicit cross-habitat operations.

### 7.4 FHF <-> C8

Settlement remains logical and deterministic, but FHF determines where settlement-supporting state, export logs, and infrastructure metering live.

### 7.5 FHF <-> C14

Governance relays operate per habitat. Cross-habitat governance traffic must use the governance/federation planes rather than piggybacking on ordinary workload channels.

### 7.6 FHF <-> C22

FHF gives concrete shape to the implementation assumptions in C22:

- clusters,
- buses,
- storage tiers,
- multi-region rollout,
- phased deployment.

---

## 8. Deployment Profiles

### 8.1 Bootstrap Profile

One habitat in one region.

- single habitat control domain,
- no true federation,
- HBG still exists logically but loops back locally,
- suitable for Wave 1 and early Wave 2.

### 8.2 Regional Multi-Habitat Profile

Multiple habitats in one jurisdictional/latency zone.

- explicit inter-habitat traffic,
- habitat-local failure isolation,
- early gateway and residency enforcement.

### 8.3 Federated Multi-Region Profile

Multiple habitats across regions.

- HBGs required for all inter-habitat exchange,
- federation windows enforced,
- governance relay hardened,
- cross-region movement policy becomes fully active.

---

## 9. Parameters

| Parameter | Default | Meaning |
|---|---|---|
| `FEDERATION_WINDOW_EPOCHS` | 12 | periodic exchange window interval |
| `HABITAT_MAX_LOCI` | 64 | soft cap on loci per habitat |
| `HABITAT_MAX_PARCELS` | 4096 | soft cap on parcels per habitat |
| `HBG_MAX_OUTBOUND_CAPSULES_PER_WINDOW` | 10000 | outbound gateway budget |
| `DIRECT_INTER_HABITAT_TRAFFIC` | false | default-deny direct traffic |
| `STATE_SUMMARY_MAX_STALENESS_EPOCHS` | 2 | summary freshness bound |
| `LOCALITY_BUDGET_TARGET` | 0.90 | target fraction of traffic remaining habitat-local |
| `GOVERNANCE_RELAY_MIN_REDUNDANCY` | 3 | minimum relay replicas per habitat |
| `APPROVED_EXPORT_REQUIRES_SIGNATURE` | true | export approval signing requirement |
| `BOOTSTRAP_SINGLE_HABITAT_ALLOWED` | true | bootstrap profile flag |

---

## 10. Formal Requirements

1. **FHF-01** Every parcel SHALL belong to exactly one habitat.
2. **FHF-02** No sovereign cell SHALL execute outside the parcel's habitat.
3. **FHF-03** Direct inter-habitat data-plane traffic SHALL be disabled by default.
4. **FHF-04** All cross-habitat exchange SHALL use Habitat Boundary Capsules.
5. **FHF-05** Every HBC SHALL be typed, signed, and epoch-scoped.
6. **FHF-06** State managed by the habitat state plane SHALL declare a residency class.
7. **FHF-07** `LOCAL_ONLY` state SHALL never cross an HBG.
8. **FHF-08** Governance relay traffic SHALL use the governance or federation plane, not the ordinary data plane.
9. **FHF-09** A bootstrap deployment SHALL preserve the habitat abstraction even when only one habitat exists.
10. **FHF-10** The control, state, governance, and federation planes SHALL align to the same habitat boundary.
11. **FHF-11** Habitat reassignment of a locus SHALL occur only through an explicit migration procedure.
12. **FHF-12** HBGs SHALL enforce per-window outbound budgets.
13. **FHF-13** The system SHOULD sustain `LOCALITY_BUDGET_TARGET` habitat-local traffic under steady-state workload.
14. **FHF-14** Federated discoverability SHALL NOT imply full state replication.
15. **FHF-15** Recovery and monitoring subsystems SHALL inherit habitat boundaries rather than redefining new failure domains.

---

## 11. Patent-Style Claims

1. A distributed infrastructure architecture for a multi-agent system comprising region-scoped habitats, each habitat containing logical coordination domains, execution hosts, state services, governance relays, and boundary gateways, wherein most workload traffic remains habitat-local.
2. The architecture of claim 1, wherein all cross-habitat exchange is constrained to typed boundary capsules processed through dedicated habitat boundary gateways.
3. The architecture of claim 1, wherein system state is classified by residency classes controlling whether state is local-only, summary-exportable, approved-exportable, or federated-discoverable.
4. The architecture of claim 1, wherein a single-habitat bootstrap deployment preserves the same boundary model used by a later multi-region federated deployment.

---

## 12. Risk Analysis

### 12.1 Primary Risks

| Risk | Description | Mitigation |
|---|---|---|
| boundary erosion | direct cross-habitat shortcuts appear over time | default-deny gateway policy |
| rigid silos | habitats become hard to rebalance | explicit reassignment and migration paths |
| state confusion | teams export local state accidentally | residency classes required up front |
| plane divergence | runtime/governance/state adopt different boundaries | one habitat failure-domain model for all planes |

### 12.2 Residual Risk

Risk remains **HIGH** because infrastructure boundary mistakes become systemic quickly. The risk is acceptable because the design is explicit, incremental, and implementable with current infrastructure practice.

---

## 13. Appendix A: Pseudocode

### A.1 Export Check

```text
function may_export(state_obj, capsule_class):
    if state_obj.residency == LOCAL_ONLY:
        return false
    if capsule_class not in state_obj.allowed_capsule_classes:
        return false
    return true
```

### A.2 Cross-Habitat Send

```text
function send_cross_habitat(payload, src_habitat, dst_habitat, capsule_class):
    if DIRECT_INTER_HABITAT_TRAFFIC:
        error("unsupported policy")

    capsule = build_hbc(payload, src_habitat, dst_habitat, capsule_class)
    return src_habitat.hbg.export(capsule)
```

---

## Conclusion

FHF gives Atrahasis the deployment primitive it was missing. The Habitat makes locality, failure domains, and federation explicit. That lets the logical stack remain coherent as the system grows from a single deployment to a real multi-region infrastructure without dissolving into either generic cluster vagueness or an unbounded planetary mesh.
