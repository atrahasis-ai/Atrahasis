# C41 Feasibility Report: Layered Semantic Capability Manifest (LSCM)

**Invention:** C41 - Layered Semantic Capability Manifest (LSCM)
**Stage:** FEASIBILITY
**Date:** 2026-03-12
**Status:** COMPLETE
**Input Documents:** `docs/task_workspaces/T-214/IDEATION_COUNCIL_OUTPUT.yaml`, `docs/task_workspaces/T-214/PRIOR_ART_REPORT.md`, `docs/task_workspaces/T-214/LANDSCAPE_REPORT.md`, `docs/task_workspaces/T-214/SCIENCE_ASSESSMENT.md`

---

## 1. Refined concept

LSCM refines `T-214` into five bounded manifest components:

1. **Subject and trust posture**
   - manifest subject identity,
   - native / federated / bridge posture,
   - issuer chain and signature roots tied to `C40`.

2. **Endpoint and binding matrix**
   - canonical manifest URL,
   - endpoint URLs by binding,
   - supported encodings and discovery channels.

3. **Security and compatibility disclosure**
   - supported `C40` security profiles,
   - supported auth schemes,
   - endpoint-scoped operational keys and signing posture,
   - ontology snapshot and compatibility declarations.

4. **Message and semantic capability disclosure**
   - supported `C39` discovery / tool / resource / prompt / stream / sampling families,
   - supported `AASL` types and verification methods,
   - bounded references to `TL`, `PMT`, `DS`, and `SES` surfaces.

5. **Supersession and update lineage**
   - publish / query / update flows anchored to `C39`,
   - visible supersession chain,
   - fail-closed registry / manifest conflict rule inherited from `C40`.

## 2. Why this is feasible

### 2.1 The upstream contracts already exist
- `C38` defines the discovery boundary and canonical manifest URL posture.
- `C39` defines manifest publish, query, and update message classes.
- `C40` defines trust-chain, auth-scheme, and conflict-failure rules.
- `T-212` defines `TL`, `PMT`, and `SES` object surfaces.

### 2.2 The invention uses known primitives
- signed manifests,
- well-known discovery URLs,
- key-chain and issuer validation,
- capability and schema advertisement,
- version and supersession metadata.

### 2.3 The task can stay bounded
LSCM does not need to specify:
- tool invocation semantics,
- registry ranking algorithms,
- bridge translation details,
- live health or telemetry surfaces,
- transport-local carrier rules beyond what the manifest must advertise.

### 2.4 The resulting design directly unblocks the backlog
- `T-251` gains a concrete A2A Agent Card replacement target.
- `T-261` gains registry input shape and searchable capability metadata.
- `T-262` gains manifest-fetch and capability-negotiation module shape.
- `T-281` gains a manifest conformance target.
- `T-290` gains a stable external capability contract for stack integration.

## 3. Adversarial analysis summary

### Attack A - The manifest becomes a shallow marketing card
- Risk: too little structure forces later tasks to invent incompatible capability
  surfaces.
- Resolution: require bounded machine-readable sections for trust, transport,
  message families, semantic support, and capability references.

### Attack B - The manifest turns into live telemetry
- Risk: health, quotas, and dynamic status make the manifest unstable and hard to
  sign or cache.
- Resolution: keep runtime state out of the manifest and treat updates as
  supersession of durable capability truth only.

### Attack C - Registry and endpoint truth diverge
- Risk: clients see conflicting trust posture or key state.
- Resolution: inherit `C40` fail-closed behavior for registry / manifest
  conflicts and keep supersession lineage explicit.

### Attack D - Inline capability disclosure explodes document size
- Risk: tool, prompt, resource, and session detail make manifests unreadable and
  brittle.
- Resolution: define inline-versus-reference rules so the manifest advertises
  bounded capability truth and points to deeper surfaces when needed.

## 4. Assessment council

### Advocate
Alternative B needs more than a signed card. LSCM gives the ecosystem one
bounded document that tells peers what an endpoint is, how it should be trusted,
and what semantic protocol surface it truly supports.

### Skeptic
The invention fails if it either:
- becomes an oversized omnibus ledger, or
- stays so shallow that downstream tasks must recreate its missing structure.

### Arbiter verdict

**Decision: ADVANCE**

| Dimension | Score | Notes |
|---|---|---|
| Novelty | 4.0 / 5 | Strong in the combined signed trust and semantic-capability disclosure surface |
| Feasibility | 4.0 / 5 | Built from established primitives with bounded scope |
| Impact | 4.5 / 5 | Foundational for discovery, registry, bridge, SDK, and conformance tasks |
| Risk | 5 / 10 | MEDIUM |

### Required actions for SPECIFICATION

1. Define the manifest object model and required sections explicitly.
2. Define inline-versus-reference rules for downstream capability surfaces.
3. Define trust-chain, native-versus-bridge posture, and conflict handling.
4. Define publish / query / update and supersession behavior.
5. State non-goals clearly so runtime state and registry behavior stay out of scope.

---

**Stage Verdict:** ADVANCE to DESIGN
