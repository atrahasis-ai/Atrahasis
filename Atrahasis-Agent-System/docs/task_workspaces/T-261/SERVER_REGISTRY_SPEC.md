# T-261 Direct Specification Draft

## Title
AACP Server Registry Specification

## Task
Specify the canonical public registry for AACP servers.

This task defines:
- registry authority boundaries,
- manifest and tool indexing rules,
- trust-vector and ranking semantics,
- programmatic discovery surfaces,
- usage documentation format,
- lifecycle handling for native, probationary, quarantined, compatibility-only, and revoked subjects.

This task does not redefine:
- the endpoint-local manifest object model (`C41`),
- tool invocation or accountable result semantics (`C42`),
- transport bindings (`C38`),
- or full cross-layer consumption rules for the wider Atrahasis stack (`T-290`).

## Governing Context
- The Alternative B source packet requires a public registry analogous to the MCP registry, but grounded in AACP manifests, tool schemas, authentication disclosure, and trust scoring.
- `C39` already defines discovery-family message classes, including `agent_manifest_publish`, `agent_manifest_query`, and `agent_manifest_update`.
- `C40` already defines the public-key registry as the authoritative long-lived native trust source and requires registry-versus-manifest conflicts to fail closed.
- `C41` already defines the signed endpoint-scoped manifest and explicitly leaves registry source documents and searchable capability sections to `T-261`.
- `C42` already defines signed tool inventory snapshots and pinning rules for tool discovery.
- `C45` establishes the native server framework as the primary producer of registry-admissible native endpoints.
- `C47` introduces the Alternative C zero-bridge pivot; newly ingested external capability should arrive as native C45/C47 outputs rather than runtime bridge surfaces.

## 1. Registry Role

The AACP Server Registry is the canonical public discovery and lookup layer for server selection.

It exists to answer five questions:
1. Which native AACP subjects are available?
2. Which bindings, encodings, security profiles, and semantic surfaces do they expose?
3. Which tool schemas do they expose, and under what provenance and authority floors?
4. What trust and lifecycle posture does each subject currently hold?
5. Which subjects match a caller's capability, policy, and trust requirements?

The registry is not:
- a live-health dashboard,
- a runtime execution broker,
- a hidden bridge adapter,
- or a source of ambient authority.

## 2. Architectural Boundary

The registry is composed of four logical surfaces.

| Surface | Purpose | Authoritative input |
|---|---|---|
| `NativeTrustRegistry` | native root-key posture, revocation, lifecycle, and key-lineage truth | `C40`, `C32` |
| `ManifestRegistry` | immutable admitted `C41` manifest snapshots and supersession lineage | `C41`, `C40` |
| `CapabilityIndex` | searchable projection over bindings, message families, auth, semantics, and tags | `C41` |
| `ToolIndex` | searchable projection over `C42` signed tool inventory snapshots | `C42` |

The full "AACP Server Registry" is the composition of those four surfaces.

## 3. Core Objects

### 3.1 `RegistrySubjectRecord`

`RegistrySubjectRecord` is the top-level public entry for one discoverable subject.

```text
RegistrySubjectRecord := {
  subject_id,
  subject_kind,
  provider_id?,
  lifecycle_state,
  native_status,
  current_manifest_id,
  current_manifest_hash,
  current_tool_snapshot_ids[],
  usage_doc_ref?,
  trust_vector,
  discoverability_policy,
  created_at,
  updated_at
}
```

Semantics:
- `subject_kind` is derived from `C41 subject.subject_kind`.
- `native_status` is one of `native`, `probation`, `quarantined`, `compatibility_only`, or `revoked`.
- `discoverability_policy` controls whether the record is visible by default, native-only, or only through explicit compatibility queries.

### 3.2 `ManifestAdmissionRecord`

```text
ManifestAdmissionRecord := {
  manifest_id,
  subject_id,
  manifest_hash,
  admitted_at,
  issuer_chain[],
  endpoint_bindings[],
  profile_ids[],
  supported_types[],
  supersedes_manifest_id?,
  admission_verdict,
  staleness_deadline,
  rejection_reason?
}
```

This object preserves immutable manifest-admission truth. Superseded manifests remain queryable for provenance and audit.

### 3.3 `ToolSchemaProjection`

```text
ToolSchemaProjection := {
  subject_id,
  snapshot_id,
  inventory_hash,
  tool_id,
  tool_name,
  description?,
  input_schema_ref,
  output_schema_ref,
  permission_refs[],
  annotation_map?,
  provenance_floor?,
  verification_requirements?,
  searchable_tags[]
}
```

Semantics:
- Every tool projection is pinned to both `subject_id` and `snapshot_id`.
- The registry does not invent tool schemas. It indexes signed `C42` discovery state.

### 3.4 `RegistryTrustVector`

```text
RegistryTrustVector := {
  identity_assurance,
  manifest_assurance,
  conformance_assurance,
  verification_history_assurance,
  lifecycle_assurance,
  overall_rank_score?,
  score_explanation[]
}
```

`overall_rank_score` is optional and secondary. The factorized vector is the required surface.

### 3.5 `UsageDocumentationDescriptor`

```text
UsageDocumentationDescriptor := {
  usage_doc_id,
  subject_id,
  summary,
  auth_requirements,
  required_grants?,
  invocation_examples[],
  failure_modes[],
  provenance_notes?,
  verification_notes?,
  cost_notes?,
  support_ref?,
  version,
  updated_at
}
```

This is the canonical usage-documentation surface referenced by registry entries.

## 4. Admission Model

### 4.1 Admissible subject classes

The public registry may hold the following classes:
- `native`: an admitted native subject with valid trust and current manifest state
- `probation`: a C47-forged subject that has not yet cleared the quarantine/ascension path
- `quarantined`: a native-form subject held out of public production selection pending review
- `compatibility_only`: a non-native legacy record retained only for explicit compatibility visibility
- `revoked`: a previously admitted subject removed from discoverable trust

### 4.2 Admission pipeline

Subject admission follows this ordered pipeline:
1. Receive or fetch a `C41` manifest through `agent_manifest_publish`, `agent_manifest_update`, or controlled registry pull.
2. Validate signature chain, subject/endpoint binding, freshness, supersession, and registry agreement per `C40`.
3. Resolve native key posture in the `NativeTrustRegistry`.
4. Persist the manifest snapshot immutably in `ManifestRegistry`.
5. Build the capability projection from inline `C41` sections and bounded capability references.
6. If a tool catalog is referenced, obtain the signed `C42` tool discovery snapshot and build `ToolIndex` projections.
7. Bind or import the usage-documentation descriptor.
8. Publish or update the `RegistrySubjectRecord` only if all mandatory gates pass.

### 4.3 Alternative C admission overlay

Under the zero-bridge pivot:
- runtime bridge subjects are not first-class public registry results,
- C47-generated native outputs are first-class subjects but begin in `probation` or `quarantined`,
- compatibility-only records may exist for migration bookkeeping, but they are excluded from native-default search and cannot satisfy native-only policy.

## 5. Search Model

### 5.1 Searchable dimensions

The registry MUST support filtering across:
- `subject_id`
- `subject_kind`
- `provider_id`
- `binding_id`
- encoding
- `C40` security profile
- auth scheme
- supported message family or class
- supported `AASL` type
- ontology snapshot
- tool identity or tool name
- tool tags, permissions, or annotations
- lifecycle or native status
- minimum trust-vector thresholds
- explicit compatibility inclusion

### 5.2 Query semantics

Search results are projections from admitted artifacts, not free-form mutable listings.

Rules:
- hard trust failures exclude a result before ranking,
- revoked or stale records are excluded by default,
- compatibility-only records are excluded unless the caller opts into compatibility visibility,
- ranking happens only after hard policy filters are satisfied.

### 5.3 Result shape

A search result returns:
- `RegistrySubjectRecord` summary,
- manifest reference or inline manifest when within inline bounds,
- selected tool-match summaries,
- factorized trust vector,
- usage documentation reference or compact summary,
- pagination or snapshot token when the result set is large.

## 6. Programmatic Discovery Surfaces

### 6.1 Authoritative AACP-native interface

The authoritative interface is AACP-native and reuses `C39` discovery-family classes.

#### `agent_manifest_publish`
- Used by a subject or operator to publish a registry-admissible manifest.
- May also carry registry-visible usage-documentation reference material.

#### `agent_manifest_update`
- Used to supersede or amend the previously admitted manifest state.
- Must preserve visible supersession lineage.

#### `agent_manifest_query`
- Extended for `query_scope = global_registry`.
- Supports capability, tool, trust, lifecycle, and compatibility filters.
- Returns matched subject summaries plus manifest references or inline manifest bundles.

`T-261` does not mint a new discovery-family class. It extends registry-scoped use of the existing manifest-query surface.

### 6.2 Optional public mirror endpoints

Implementations MAY expose read-only HTTP mirrors for browsers, SDK convenience, or documentation tooling:
- `GET /registry/v1/subjects/{subject_id}`
- `GET /registry/v1/search`
- `GET /registry/v1/tools/{tool_id}`
- `GET /registry/v1/manifests/{manifest_id}`

If present, those mirrors are convenience surfaces only. The AACP-native registry state remains authoritative.

## 7. Trust Scoring

### 7.1 Factor model

The registry trust model is factorized into:
- `identity_assurance`: native-root validity, revocation, and lifecycle anchor quality
- `manifest_assurance`: signature, freshness, supersession, and endpoint binding correctness
- `conformance_assurance`: certification or conformance posture once `T-281` exists
- `verification_history_assurance`: summary of verified behavior and failure history from downstream verification consumers
- `lifecycle_assurance`: penalties or ceilings for `probation`, `quarantined`, `compatibility_only`, or `revoked`

### 7.2 Ranking rule

`overall_rank_score` MAY be computed for search ordering, but:
- it MUST be derived from the factor model,
- it MUST expose factor explanations,
- it MUST not hide a hard failure behind a high composite score,
- and it MUST not allow compatibility-only or revoked records to outrank valid native records in native-default search.

### 7.3 Verification-history source rule

Verification history is a downstream summary, not an ad hoc rating. It should be derived from bounded evidence such as:
- successful verification outcomes,
- failure frequency,
- severity-weighted incidents,
- quarantine or probation promotion/demotion events.

Absence of verification history lowers confidence but does not by itself imply malice.

## 8. Usage Documentation Format

Every public registry subject SHOULD expose usage documentation through `UsageDocumentationDescriptor`.

Minimum required fields:
- one-line purpose summary,
- authentication requirements,
- at least one invocation example,
- expected failure-mode summary,
- version and update time.

Optional fields:
- required grants,
- provenance or verification notes,
- rate/cost notes,
- support or escalation contact.

Usage documentation must remain subordinate to the admitted manifest and tool schemas. It explains use; it does not redefine authority or capability.

## 9. Lifecycle and State Transitions

### 9.1 Lifecycle states

The registry uses the following lifecycle states:
- `active`
- `probation`
- `quarantined`
- `compatibility_only`
- `revoked`
- `superseded`

### 9.2 Transition rules

- `probation -> active` requires the configured ascension checks to pass.
- `active -> quarantined` occurs when a serious trust, verification, or admission anomaly is detected.
- `active -> revoked` occurs when root trust, manifest posture, or policy legitimacy is withdrawn.
- `compatibility_only` cannot transition directly to `active`; a subject must become native by re-ingestion through the native production path.

## 10. Conformance Requirements

| ID | Requirement | Priority |
|---|---|---|
| REG-R01 | The registry MUST preserve immutable admitted manifest snapshots rather than mutating them in place | P0 |
| REG-R02 | Manifest admission MUST enforce all applicable `C40` anti-spoofing, freshness, supersession, and subject/endpoint binding checks before a subject becomes discoverable | P0 |
| REG-R03 | Registry-versus-manifest conflicts on native identity or trust posture MUST fail closed | P0 |
| REG-R04 | Public search MUST default to excluding revoked, stale, and compatibility-only records | P0 |
| REG-R05 | Any compatibility-only or bridge-derived record MUST remain explicitly non-native and MUST NOT satisfy native-only discovery filters | P0 |
| REG-R06 | Tool indexing MUST bind every projected tool record to a signed `C42` snapshot identity and inventory hash | P0 |
| REG-R07 | Searchable capability and tool tags MUST be projections from admitted artifacts rather than ungoverned mutable labels | P0 |
| REG-R08 | The authoritative programmatic discovery surface MUST reuse `agent_manifest_publish`, `agent_manifest_update`, and `agent_manifest_query` rather than minting a new discovery message family unnecessarily | P1 |
| REG-R09 | The registry MUST support filtering on bindings, encodings, security profiles, message-family capability, semantic types, tool metadata, and lifecycle state | P0 |
| REG-R10 | The registry MUST expose factorized trust vectors for search results; a composite rank score alone is insufficient | P0 |
| REG-R11 | Ranking MUST occur only after hard trust and policy filters are satisfied | P0 |
| REG-R12 | Usage documentation MUST be versioned and bound to the subject identity and current manifest lineage | P1 |
| REG-R13 | Optional HTTP mirror endpoints MUST reflect registry state without creating competing authority semantics | P1 |
| REG-R14 | Manifest supersession and subject revocation MUST become visible to search and detail consumers without silent disappearance of historical lineage | P0 |
| REG-R15 | Native probation and quarantine states MUST be explicit and machine-readable in discovery results | P0 |
| REG-R16 | Verification-history-derived trust inputs MUST be evidence-backed summaries rather than opaque social reputation numbers | P1 |
| REG-R17 | The registry MUST NOT make live telemetry, quota, or transient health a mandatory part of canonical discovery truth | P1 |
| REG-R18 | `T-262`, `T-280`, `T-281`, and `T-290` MUST be able to consume the registry without inventing new trust, query, or indexing primitives that contradict this task | P1 |

## 11. Parameters

| Parameter | Meaning | Initial guidance |
|---|---|---|
| `REGISTRY_PUBLIC_NATIVE_ONLY_DEFAULT` | whether default public search excludes non-native compatibility records | `true` |
| `REGISTRY_QUERY_PAGE_MAX` | maximum number of subjects returned per page | `100` |
| `REGISTRY_MAX_INLINE_MANIFESTS` | maximum number of full manifests inlined in one query result | `10` |
| `REGISTRY_MAX_INLINE_TOOL_MATCHES` | maximum number of tool summaries inlined per subject result | `25` |
| `REGISTRY_USAGE_DOC_INLINE_BYTES_MAX` | max inline usage-documentation payload size before reference-only mode is required | `16384` |
| `REGISTRY_TOOL_INDEX_REFRESH_TTL_MS` | max staleness window for cached tool projections before refresh is required | `300000` |
| `REGISTRY_VERIFICATION_HISTORY_WINDOW_DAYS` | lookback window for verification-derived trust summaries | `30` |
| `REGISTRY_DEFAULT_RANK_WEIGHTS` | default factor weights for optional rank score | `identity=.30, manifest=.20, conformance=.20, verification=.20, lifecycle=.10` |
| `REGISTRY_COMPATIBILITY_VISIBLE_BY_DEFAULT` | whether compatibility-only records appear in default public queries | `false` |
| `REGISTRY_PROBATION_VISIBLE_BY_DEFAULT` | whether probationary native records appear in default public queries | `true` |
| `REGISTRY_QUARANTINE_VISIBLE_BY_DEFAULT` | whether quarantined records appear in default public queries | `false` |
| `REGISTRY_HTTP_MIRROR_ALLOWED` | whether optional read-only HTTP mirrors are allowed | `true` |

## 12. Canonical Query Example

### 12.1 Global registry query

```json
{
  "query_scope": "global_registry",
  "filters": {
    "native_only": true,
    "binding_id": "AACP-HTTP",
    "profile_ids": ["SP-NATIVE-ATTESTED"],
    "supported_types": ["TL", "PRV"],
    "tool_tags": ["filesystem"],
    "minimum_trust": {
      "identity_assurance": 0.90,
      "manifest_assurance": 0.90
    }
  },
  "result_policy": {
    "inline_manifests": false,
    "inline_tool_matches": true
  }
}
```

### 12.2 Subject result sketch

```json
{
  "subject_id": "ag.fs.locus.01",
  "native_status": "active",
  "current_manifest_id": "amf.fs.003",
  "tool_matches": [
    {
      "tool_id": "tl.fs.read_file",
      "snapshot_id": "tis.fs.004",
      "input_schema_ref": "cst://fs.read.input",
      "output_schema_ref": "cst://fs.read.output"
    }
  ],
  "trust_vector": {
    "identity_assurance": 0.99,
    "manifest_assurance": 0.97,
    "conformance_assurance": 0.85,
    "verification_history_assurance": 0.93,
    "lifecycle_assurance": 1.00
  },
  "usage_doc_ref": "usage://ag.fs.locus.01/v3"
}
```

## 13. Downstream Contracts

| Task | `T-261` provides |
|---|---|
| `T-262` | registry client module, manifest-search API shape, trust-vector response structure |
| `T-280` | CLI and inspector discovery/search surfaces plus documentation retrieval shape |
| `T-281` | conformance targets for manifest admission, query semantics, trust-vector disclosure, and optional mirror behavior |
| `T-290` | stable discovery/trust contract for the wider Atrahasis stack |
| `T-305` | planning input for deployment, governance, and public-discovery rollout sequencing |

## 14. Conclusion

`T-261` defines the AACP Server Registry as a native-first discovery and trust-disclosure surface rather than a loose server list.

It preserves the Alternative B manifest and tool-discovery foundations while aligning them with the Alternative C zero-bridge pivot:
- native servers are first-class,
- C47-forged probationary and quarantined outputs remain visible but lifecycle-bounded,
- compatibility-only records never masquerade as native production results.
