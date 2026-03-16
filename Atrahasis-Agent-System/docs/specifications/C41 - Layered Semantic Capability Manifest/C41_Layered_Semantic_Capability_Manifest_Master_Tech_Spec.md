# C41 Master Tech Spec
## Layered Semantic Capability Manifest (LSCM)

**Invention ID:** C41  
**Task:** T-214  
**Version:** 1.0.0  
**Status:** COMPLETE  
**Agent:** Inanna (Codex)

---

## 1. Purpose

Alternative B needs a canonical discovery document richer than an A2A Agent Card
and more trustworthy than an unsigned service listing. The Atrahasis Agent
Manifest must let a client or registry answer six questions before deeper
interaction:

1. What endpoint or agent am I looking at?
2. What trust posture does it claim?
3. How should that trust be validated?
4. Which AACP bindings, encodings, and message families does it support?
5. Which semantic capability surfaces does it support?
6. How do I know whether this manifest supersedes an earlier one?

LSCM answers those questions through one signed, endpoint-scoped manifest
published at `/.well-known/atrahasis.json`.

---

## 2. Scope and non-goals

### 2.1 In scope
- manifest object model,
- required and optional manifest sections,
- trust posture and signing rules,
- capability disclosure rules,
- native-versus-bridge disclosure,
- publish / query / update / supersession behavior,
- conformance requirements.

### 2.2 Out of scope
- live health or telemetry,
- registry ranking and search algorithms,
- tool invocation semantics,
- prompt, resource, or streaming business logic,
- transport-local carrier behavior,
- bridge translation mechanics.

---

## 3. Governing inputs

LSCM is downstream of:
- `C38` FSPA for overall layer boundaries and canonical manifest URL posture,
- `C39` LCML for discovery-family message classes,
- `C40` DAAF for trust profiles, manifest trust distribution, and fail-closed
  registry / manifest conflict handling,
- `T-212` for `TL`, `PMT`, and `SES` object surfaces,
- `C36` EMA-I as the canonical external interaction membrane.

LSCM must not contradict any of those sources.

---

## 4. Core innovation

The invention is not merely "an agent manifest exists." The invention is a
bounded manifest that unifies four surfaces usually split or blurred across
multiple documents:

1. signed trust posture,
2. transport and message capability,
3. semantic capability disclosure,
4. explicit supersession lineage.

It does this without collapsing dynamic runtime state into discovery truth.

---

## 5. Design principles

1. **Durable truth only**  
   The manifest describes stable capability and trust truth, not transient
   health, quota, or telemetry state.

2. **Trust is explicit**  
   Native, federated, and bridged postures must be machine-readable.

3. **Bounded disclosure**  
   The manifest must advertise enough capability to guide discovery without
   inlining every downstream schema or operational detail.

4. **Reference over duplication when depth is high**  
   Deep tool, prompt, resource, and session detail may be referenced rather than
   fully inlined.

5. **Supersession is visible**  
   A newer manifest never silently erases the lineage of the older one.

---

## 6. Manifest object model

### 6.1 Top-level object

The canonical manifest object is `AgentManifest`.

```text
AgentManifest := {
  manifest_id,
  version,
  subject,
  trust_posture,
  discovery,
  endpoints,
  security,
  messaging,
  semantics,
  capability_refs?,
  constraints?,
  supersession,
  signatures
}
```

### 6.2 Required sections

| Section | Purpose |
|---|---|
| `subject` | identify the endpoint-scoped subject and its declared posture |
| `trust_posture` | declare native / federated / bridge status and issuer chain |
| `discovery` | declare canonical retrieval URL and discovery metadata |
| `endpoints` | list supported bindings, URLs, and encodings |
| `security` | advertise `C40` profiles, auth schemes, and endpoint-scoped keys |
| `messaging` | advertise supported `C39` message families or classes |
| `semantics` | advertise supported `AASL` types, ontology snapshots, and verification methods |
| `supersession` | declare lifecycle and replacement lineage |
| `signatures` | bind the manifest to accepted issuer trust |

### 6.3 Optional sections

| Section | Purpose |
|---|---|
| `capability_refs` | references to deeper `TL`, `PMT`, `DS`, or `SES` surfaces |
| `constraints` | bounded non-operational limits such as unsupported classes or profile restrictions |

---

## 7. Section semantics

### 7.1 `subject`

The `subject` section declares:
- `subject_id`,
- `subject_kind`,
- `display_name`,
- `operator_ref` or `owner_ref` when available,
- `bridge_origin` when the subject is bridged rather than native.

`subject_kind` must distinguish at least:
- `native_agent`,
- `federated_service`,
- `local_tool_host`,
- `bridge_endpoint`.

### 7.2 `trust_posture`

The `trust_posture` section declares:
- posture class,
- root issuer or native trust anchor,
- manifest issuer,
- native-versus-bridge statement,
- whether the manifest is authoritative for endpoint-scoped keys only or also
  asserts native identity facts.

Rules:
- native identity facts must not override registry truth,
- bridge posture must remain visible,
- posture conflicts with registry truth must fail closed per `C40`.

### 7.3 `discovery`

The `discovery` section declares:
- canonical manifest URL,
- publication channels,
- supported discovery message classes,
- optional discoverability tags.

The canonical retrieval path is `/.well-known/atrahasis.json` unless a later
governance decision explicitly changes it.

### 7.4 `endpoints`

Each endpoint entry declares:
- `binding_id`,
- `endpoint_url`,
- supported encodings,
- whether handshake is required,
- transport-specific notes allowed by profile.

The manifest may advertise multiple bindings, for example:
- `AACP-HTTP`,
- `AACP-gRPC`,
- `AACP-WS`,
- `AACP-Stdio` when locally meaningful.

### 7.5 `security`

The `security` section declares:
- supported `C40` security profiles,
- supported auth schemes,
- endpoint-scoped key references,
- signature verification expectations,
- any bounded capability-grant prerequisites for sensitive flows.

This section may advertise:
- `SP-NATIVE-ATTESTED`,
- `SP-FEDERATED-SESSION`,
- `SP-WORKLOAD-MTLS`,
- `SP-BRIDGE-LIMITED`,
or later admitted extensions.

### 7.6 `messaging`

The `messaging` section declares:
- supported message families,
- optional supported class list,
- supported interaction modes,
- whether publish, query, and update are supported for manifest flows.

At minimum, LSCM requires explicit disclosure for the discovery-family classes:
- `agent_manifest_publish`,
- `agent_manifest_query`,
- `agent_manifest_update`.

### 7.7 `semantics`

The `semantics` section declares:
- supported `AASL` object types,
- pinned ontology snapshot identifiers,
- supported verification method families,
- any explicit semantic exclusions.

This is where an endpoint may say it supports, for example:
- `CLM`, `CNF`, `EVD`, `PRV`, `VRF`,
- `TL`, `PMT`, `SES`,
- `DS`,
- and other admitted types.

### 7.8 `capability_refs`

The manifest may reference deeper capability surfaces rather than inline them.
Examples:
- a tool catalog reference,
- a prompt-template set reference,
- a resource collection reference,
- a supported session-mode reference.

Rule:
- deep capability objects should be referenced when inline detail would create
  unstable or oversized manifests.

### 7.9 `constraints`

This optional section declares bounded caveats such as:
- unsupported message families,
- unsupported profiles,
- bridge-limited operations,
- required capability-grant preconditions for specific surfaces.

### 7.10 `supersession`

The supersession section declares:
- `lifecycle_state`,
- `published_at`,
- `supersedes_manifest_id?`,
- `replacement_manifest_id?`,
- `supersession_reason?`.

This section is the durable manifest lifecycle surface. It is not a place for
runtime health.

### 7.11 `signatures`

The manifest must carry signatures or references sufficient to validate:
- issuer identity,
- manifest integrity,
- and trust-chain admission.

LSCM requires signatures to bind to the canonical manifest projection, not a
transport-local byte stream.

---

## 8. Inline-versus-reference rule

LSCM uses one rule to prevent manifest bloat:

**Inline when the information is required for pre-interaction trust and
capability selection. Reference when the information is only needed after deeper
interaction begins.**

### 8.1 Inline examples
- trust posture,
- auth schemes,
- supported bindings and encodings,
- supported message families,
- supported type families,
- ontology snapshot identifiers.

### 8.2 Reference examples
- large tool inventories,
- full prompt-template bodies,
- complex resource schemas,
- detailed session-policy internals,
- operational dashboards or health feeds.

---

## 9. Native-versus-bridge posture

LSCM makes bridge posture first-class.

### 9.1 Native manifest

A native manifest:
- roots identity in accepted native trust,
- may advertise endpoint-scoped keys,
- may declare native-only capability surfaces,
- must not be represented as bridge-limited.

### 9.2 Bridged manifest

A bridged manifest:
- must disclose bridge origin,
- must disclose translated or degraded trust posture,
- must not silently advertise native-only trust or capability,
- must carry a provenance floor sufficient for clients to distinguish bridge
  output from native output.

### 9.3 Federated or workload manifest

Federated and workload manifests may be non-native without being bridges, but
they still must disclose which `C40` profile governs their trust posture.

---

## 10. Discovery behavior

### 10.1 Retrieval

The simplest retrieval path is:
- HTTP `GET` against `/.well-known/atrahasis.json`.

### 10.2 Message-based publication and query

The manifest also participates in `C39` discovery-family flows:
- `agent_manifest_publish`,
- `agent_manifest_query`,
- `agent_manifest_update`.

### 10.3 Update rule

An update must either:
- supersede the previous manifest,
- or explicitly declare itself as an amendment within the visible lineage chain.

Silent replacement is forbidden.

---

## 11. Trust and conflict rules

### 11.1 Registry and manifest agreement

If registry truth and manifest truth agree, the manifest is a valid endpoint-
scoped disclosure surface.

### 11.2 Conflict rule

If registry truth and manifest truth disagree on native key or trust posture:
- the receiver must fail closed,
- the manifest must not silently override registry truth,
- the conflict must remain visible to policy and provenance consumers.

### 11.3 Key disclosure

Endpoint-scoped operational keys may be advertised in the manifest when allowed
by policy, but they do not replace long-lived native trust anchors.

---

## 12. Compatibility rules

### 12.1 Versioning

LSCM versioning applies at three levels:
- manifest schema version,
- ontology snapshot version,
- endpoint-supported binding/profile compatibility.

### 12.2 Backward-compatible growth

Additive optional sections and additive fields are allowed when:
- older consumers can safely ignore them,
- and their absence does not alter the meaning of required fields.

### 12.3 Incompatible changes

Changes to:
- required field meaning,
- trust posture semantics,
- supersession semantics,
- or native-versus-bridge interpretation
require explicit version advancement and migration guidance.

---

## 13. Conformance requirements

| ID | Requirement | Priority |
|---|---|---|
| LSCM-R1 | Every Alternative B endpoint MUST publish exactly one canonical manifest retrieval surface at `/.well-known/atrahasis.json` or an explicitly governed successor path | P0 |
| LSCM-R2 | Every manifest MUST declare subject identity and subject kind explicitly | P0 |
| LSCM-R3 | Every manifest MUST declare native-versus-bridge posture explicitly | P0 |
| LSCM-R4 | Every manifest MUST declare at least one supported binding and one supported encoding | P0 |
| LSCM-R5 | Every manifest MUST declare supported `C40` security profiles and auth schemes | P0 |
| LSCM-R6 | Every manifest MUST declare support for discovery-family manifest flows or explicitly declare them unsupported | P1 |
| LSCM-R7 | Every manifest MUST declare supported `AASL` type families and ontology snapshot identifiers | P0 |
| LSCM-R8 | Manifest signatures MUST bind to canonical manifest identity rather than transport-local bytes alone | P0 |
| LSCM-R9 | Registry and manifest conflicts on native trust posture MUST fail closed | P0 |
| LSCM-R10 | A bridged manifest MUST disclose bridge origin and must not silently advertise native-only trust posture | P0 |
| LSCM-R11 | Runtime telemetry and live health MUST NOT be mandatory fields in the manifest | P1 |
| LSCM-R12 | Deep capability detail MAY be referenced, but required trust and capability selection facts MUST remain inline | P1 |
| LSCM-R13 | Manifest updates MUST preserve visible supersession lineage | P0 |
| LSCM-R14 | Additive optional fields MUST NOT reinterpret required field meaning | P1 |
| LSCM-R15 | Endpoint-scoped operational keys MAY be advertised only under allowed trust posture and must not replace native trust anchors | P1 |
| LSCM-R16 | Consumers MUST be able to determine whether an endpoint is native, federated/workload, or bridge-limited from the manifest alone | P0 |
| LSCM-R17 | Manifest content MUST remain stable enough for cache and conformance use; ephemeral operational metrics are prohibited from the canonical surface | P1 |
| LSCM-R18 | Manifest builders and validators MUST apply explicit inline-versus-reference rules for `TL`, `PMT`, `DS`, and `SES` capability disclosure | P1 |

---

## 14. Parameters

| Parameter | Meaning |
|---|---|
| `MANIFEST_PATH` | canonical retrieval path |
| `MANIFEST_SCHEMA_VERSION` | LSCM schema version |
| `MAX_INLINE_CAPABILITY_SET` | maximum inline capability disclosure footprint before references are required |
| `REQUIRED_DISCOVERY_CLASSES` | required discovery-family classes |
| `REQUIRED_TRUST_FIELDS` | minimum trust-posture field set |
| `REQUIRED_SEMANTIC_FIELDS` | minimum semantic support field set |
| `SUPERSESSION_TTL_POLICY` | policy for manifest retirement and replacement visibility |
| `BRIDGE_POSTURE_LABEL_SET` | allowed bridge/native posture labels |
| `ONTOLOGY_SNAPSHOT_REF_FORMAT` | canonical snapshot reference format |
| `MANIFEST_SIGNATURE_PROFILE` | allowed signature / issuer validation profile set |

---

## 15. Example manifest skeleton

```json
{
  "manifest_id": "amf.example.001",
  "version": "1.0.0",
  "subject": {
    "subject_id": "ag.example.01",
    "subject_kind": "native_agent",
    "display_name": "Example Analyst Agent"
  },
  "trust_posture": {
    "posture": "native",
    "profile_ids": ["SP-NATIVE-ATTESTED"],
    "issuer_chain": ["mia-root", "endpoint-issuer"]
  },
  "discovery": {
    "canonical_url": "https://example.ai/.well-known/atrahasis.json",
    "classes": ["agent_manifest_publish", "agent_manifest_query", "agent_manifest_update"]
  },
  "endpoints": [
    {
      "binding_id": "AACP-HTTP",
      "endpoint_url": "https://example.ai/aacp/message",
      "supported_encodings": ["AASL-J", "AASL-B"]
    }
  ],
  "security": {
    "auth_schemes": ["oauth2.1", "ed25519"],
    "profile_ids": ["SP-NATIVE-ATTESTED"]
  },
  "messaging": {
    "families": ["DISCOVERY", "TOOL", "RESOURCE"]
  },
  "semantics": {
    "supported_types": ["CLM", "CNF", "EVD", "PRV", "VRF", "TL", "PMT", "SES"],
    "ontology_snapshots": ["atr.protocol@1"]
  },
  "capability_refs": {
    "tool_catalog": "ref://tools/default"
  },
  "supersession": {
    "lifecycle_state": "active",
    "published_at": "2026-03-12T00:00:00Z"
  },
  "signatures": {
    "profile": "MANIFEST_SIGNATURE_PROFILE",
    "signature_ref": "sig://manifest/1"
  }
}
```

---

## 16. Patent-style claims

1. A signed endpoint-scoped manifest method that simultaneously discloses trust
   posture, protocol message capability, semantic capability support, and
   manifest supersession lineage while excluding live operational state from the
   canonical discovery surface.

2. The method of claim 1, wherein native-versus-bridge posture is a first-class
   machine-readable field that constrains downstream trust interpretation.

3. The method of claim 1, wherein deep capability surfaces are governed by an
   inline-versus-reference rule that preserves discovery usefulness without
   forcing full downstream schema inlining.

4. The method of claim 1, wherein registry and manifest conflicts on native
   trust posture fail closed rather than being heuristically reconciled.

---

## 17. Downstream contracts

| Task | LSCM provides |
|---|---|
| `T-251` | canonical replacement target for A2A Agent Cards |
| `T-261` | registry source document and searchable capability sections |
| `T-262` | manifest fetch, parse, and negotiation module surface |
| `T-281` | manifest conformance target |
| `T-290` | stable external capability contract for the wider Atrahasis stack |

---

## 18. Conclusion

LSCM gives Alternative B a canonical discovery contract.

It is richer than an agent card, stricter than a service listing, and more
bounded than an operational ledger. That is the right architectural posture for
the next phase of the Alternative B backlog.
