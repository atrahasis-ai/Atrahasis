# Atrahasis AASL Implementation-Ready Engineering Packs

**Document ID:** AASL-ENG-PACK-001  
**Status:** Canonical Design / Engineering Reference  
**Scope:** API Surface Contracts, Protobuf/IDL/Event Contracts, Database Schema Reference Pack, Repository Layout Standard, CI/CD Pipeline Reference, Release Engineering Handbook  
**Applies To:** AASL toolchains, runtimes, compilers, validators, query engines, storage services, SDKs, ecosystem integrations, certification infrastructure  

---

## 1. Purpose

This document defines the implementation-ready engineering pack for the Atrahasis Agentic Semantic Language (AASL) ecosystem. It converts the broader AASL architectural and operational design into a concrete engineering baseline that can be handed directly to platform engineers, runtime teams, SDK authors, DevOps operators, and release managers.

This pack has six objectives:

1. Define the canonical API surface contracts for all major AASL services.
2. Define transport-level contracts for protobuf, IDL, and event envelopes.
3. Define the reference database schema model across metadata, content, indexes, registries, governance, and certification.
4. Define the standard repository layout for mono-repo or multi-repo implementations.
5. Define the CI/CD pipeline model for deterministic, secure, auditable builds and releases.
6. Define the release engineering lifecycle from development through certification and long-term support.

This document is intentionally implementation-oriented. It should be read as a bridge between architecture and execution.

---

## 2. Design Principles

All engineering packs in the AASL ecosystem shall follow these principles.

### 2.1 Contract-first engineering

Every external or internal service boundary must be represented as a formal contract before feature implementation begins. Code generation, tests, mocks, docs, and certification vectors should derive from the contract whenever practical.

### 2.2 Deterministic semantics

Systems that parse, compile, validate, canonicalize, encode, store, query, or federate AASL content must produce reproducible outputs for the same input under the same profile.

### 2.3 Observable behavior

Every critical path must expose metrics, logs, traces, and state transition records sufficient for debugging, SLO management, certification review, and post-incident analysis.

### 2.4 Profile-aware compatibility

All interfaces and schemas must support feature negotiation, versioning, profile declarations, and compatibility signaling.

### 2.5 Security by default

Interfaces must assume hostile input, partial trust boundaries, replay attempts, invalid identities, malformed encodings, downgrade attempts, and unauthorized access.

### 2.6 Progressive extensibility

The engineering surface must allow experimental modules, optional features, storage backends, transport adapters, and platform runtimes without destabilizing the canonical core.

---

## 3. Engineering Pack Structure

This document is organized into the following sections:

1. API Surface Contracts
2. Protobuf / IDL / Event Contract Pack
3. Database Schema Reference Pack
4. Repository Layout Standard
5. CI/CD Pipeline Reference
6. Release Engineering Handbook
7. Appendices and sample skeletons

---

# PART I — API SURFACE CONTRACTS

## 4. API Surface Philosophy

The AASL platform should expose a layered API surface rather than a single monolithic endpoint family.

The recommended layers are:

1. **Core language services**: parse, validate, canonicalize, compile, format, query.
2. **Runtime services**: load documents, materialize graphs, resolve identities, transactions, namespace operations.
3. **Storage services**: ingest, persist, retrieve, snapshot, replicate, garbage collect.
4. **Governance services**: ontology registration, RFC lifecycle, namespace claims, deprecation notices.
5. **Certification services**: profile testing, evidence upload, conformance evaluation, result publication.
6. **Developer tooling services**: lint, format, explain, diagnostics, migration assist, code actions.
7. **Federation services**: capability discovery, artifact exchange, remote query delegation, trust material exchange.

These services may be implemented as:

- a single process with local module boundaries,
- a modular monolith with internal service contracts,
- a microservice deployment,
- an edge/client hybrid architecture,
- or a certified offline toolchain with no network dependencies.

The contract definitions in this section are logical contracts. Transport-specific mappings follow later.

---

## 5. Service Catalog

### 5.1 Parser Service

**Purpose:** Convert `.aas`, source fragments, and tool-authored buffers into token streams, parse trees, ASTs, and syntax diagnostics.

**Primary operations:**
- parseDocument
- parseFragment
- tokenize
- recoverParse
- syntaxExplain
- listGrammarProfile

**Key responsibilities:**
- lexical analysis
- grammar selection
- source span preservation
- recovery-mode parsing
- syntax error reporting
- CST/AST emission

### 5.2 Validator Service

**Purpose:** Evaluate syntactic, structural, semantic, referential, profile, governance, and policy constraints.

**Primary operations:**
- validateDocument
- validateBundle
- validateAgainstProfile
- validateNamespaceClaims
- validatePolicyPack
- explainDiagnostic

### 5.3 Canonicalizer / Formatter Service

**Purpose:** Transform valid or recoverable AASL content into canonical or selected style-preserving representations.

**Primary operations:**
- canonicalizeDocument
- formatDocument
- computeCanonicalHash
- rewriteImports
- normalizeOrdering

### 5.4 Compiler Service

**Purpose:** Compile natural language, structured data, or foreign input sources into AASL documents or bundles.

**Primary operations:**
- compileInput
- compileBatch
- mapOntology
- synthesizeIds
- emitTrace
- reverseRender

### 5.5 Runtime Service

**Purpose:** Materialize AASL objects, documents, graphs, module registries, namespace bindings, and transaction state.

**Primary operations:**
- loadDocument
- loadBundle
- resolveObject
- resolveReference
- transact
- snapshotRuntime
- inspectGraph

### 5.6 Query Service

**Purpose:** Execute AASL query language requests over documents, graphs, indexes, and federated endpoints.

**Primary operations:**
- query
- explainQuery
- planQuery
- subscribeQuery
- exportResult

### 5.7 Storage Service

**Purpose:** Persist source, canonical outputs, binary encodings, indexes, derived artifacts, snapshots, manifests, and audit records.

**Primary operations:**
- putArtifact
- getArtifact
- listArtifacts
- createSnapshot
- restoreSnapshot
- compactStore
- publishManifest

### 5.8 Governance Service

**Purpose:** Manage ontologies, RFCs, namespace registration, compatibility metadata, deprecation events, and review workflows.

**Primary operations:**
- submitProposal
- reviewProposal
- registerNamespace
- publishDecision
- listCompatibilityNotices
- resolveAuthority

### 5.9 Certification Service

**Purpose:** Execute conformance suites, ingest implementation evidence, compare outputs to golden vectors, and publish certification results.

**Primary operations:**
- submitImplementation
- runSuite
- uploadEvidence
- getFindings
- publishCertificate
- revokeCertificate

### 5.10 Federation Service

**Purpose:** Discover capabilities, exchange trust materials, negotiate profiles, synchronize manifests, and delegate queries.

**Primary operations:**
- discoverCapabilities
- exchangeManifest
- exchangeTrustBundle
- delegateQuery
- fetchRemoteArtifact
- validatePeer

---

## 6. API Style Baseline

AASL implementations may expose REST, gRPC, local IPC, or embedded library APIs. The canonical logical contract should remain stable across transports.

Recommended conventions:

- Noun-oriented resources for persistent entities.
- Verb-oriented actions for analysis, compilation, transformation, and execution.
- Deterministic request and response schemas.
- Explicit request identifiers.
- Explicit profile/version fields.
- Explicit diagnostic sections.
- Pagination, streaming, and snapshot semantics defined per operation.
- Stable machine-readable error bodies.

Every request should include, where applicable:

- `request_id`
- `api_version`
- `profile`
- `client_capabilities`
- `trace_context`
- `auth_context` or equivalent transport metadata

Every response should include, where applicable:

- `request_id`
- `status`
- `diagnostics`
- `warnings`
- `compatibility_notes`
- `artifact_hashes`
- `timing`
- `trace_context`

---

## 7. Canonical Logical API Schemas

### 7.1 Common envelope

```yaml
RequestEnvelope:
  request_id: string
  api_version: string
  profile: string
  caller:
    type: string
    id: string
  capabilities: [string]
  trace:
    trace_id: string
    span_id: string
  payload: object

ResponseEnvelope:
  request_id: string
  status: string
  profile_applied: string
  diagnostics: [Diagnostic]
  warnings: [Diagnostic]
  compatibility_notes: [string]
  timing:
    started_at: string
    completed_at: string
    duration_ms: integer
  payload: object
```

### 7.2 Diagnostic model

```yaml
Diagnostic:
  code: string
  severity: string
  phase: string
  message: string
  source:
    uri: string
    start_line: integer
    start_col: integer
    end_line: integer
    end_col: integer
  related_objects: [string]
  suggested_fixes: [string]
  docs_ref: string
```

### 7.3 Artifact reference model

```yaml
ArtifactRef:
  artifact_id: string
  kind: string
  media_type: string
  profile: string
  version: string
  hash:
    algorithm: string
    value: string
  size_bytes: integer
  storage_locator: string
```

---

## 8. Endpoint Families (Reference REST Mapping)

### 8.1 Parser endpoints

- `POST /v1/parser/tokenize`
- `POST /v1/parser/parse`
- `POST /v1/parser/parse-fragment`
- `POST /v1/parser/recover`
- `POST /v1/parser/explain`
- `GET /v1/parser/profiles`

Example request:

```json
{
  "request_id": "req-123",
  "api_version": "1.0",
  "profile": "aasl-core-1",
  "payload": {
    "source_text": "entity Person { name: \"Ada\" }",
    "source_uri": "memory://example.aas",
    "emit": ["tokens", "cst", "ast", "diagnostics"]
  }
}
```

### 8.2 Validator endpoints

- `POST /v1/validator/document`
- `POST /v1/validator/bundle`
- `POST /v1/validator/profile`
- `POST /v1/validator/policy`
- `GET /v1/validator/codes/{code}`

### 8.3 Compiler endpoints

- `POST /v1/compiler/compile`
- `POST /v1/compiler/compile-batch`
- `POST /v1/compiler/map-ontology`
- `POST /v1/compiler/reverse-render`
- `GET /v1/compiler/traces/{trace_id}`

### 8.4 Runtime endpoints

- `POST /v1/runtime/load`
- `POST /v1/runtime/load-bundle`
- `POST /v1/runtime/resolve`
- `POST /v1/runtime/transact`
- `GET /v1/runtime/snapshots/{snapshot_id}`
- `GET /v1/runtime/graph/{graph_id}`

### 8.5 Query endpoints

- `POST /v1/query/execute`
- `POST /v1/query/plan`
- `POST /v1/query/explain`
- `POST /v1/query/subscribe`
- `POST /v1/query/export`

### 8.6 Storage endpoints

- `PUT /v1/storage/artifacts/{artifact_id}`
- `GET /v1/storage/artifacts/{artifact_id}`
- `POST /v1/storage/search`
- `POST /v1/storage/snapshots`
- `POST /v1/storage/restore`
- `POST /v1/storage/compact`

### 8.7 Governance endpoints

- `POST /v1/governance/proposals`
- `POST /v1/governance/proposals/{proposal_id}/review`
- `POST /v1/governance/namespaces/register`
- `GET /v1/governance/notices`
- `GET /v1/governance/authorities/{authority_id}`

### 8.8 Certification endpoints

- `POST /v1/certification/implementations`
- `POST /v1/certification/suites/run`
- `POST /v1/certification/evidence`
- `GET /v1/certification/findings/{run_id}`
- `POST /v1/certification/certificates/publish`
- `POST /v1/certification/certificates/revoke`

### 8.9 Federation endpoints

- `GET /v1/federation/capabilities`
- `POST /v1/federation/manifests/exchange`
- `POST /v1/federation/trust/exchange`
- `POST /v1/federation/query/delegate`
- `GET /v1/federation/artifacts/{artifact_id}`

---

## 9. Non-HTTP Interface Expectations

### 9.1 Embedded library interfaces

All major SDKs should expose strongly typed functions equivalent to the logical API contracts. The same diagnostics, envelopes, and result models should be reused.

### 9.2 gRPC mapping

All request/response envelopes should have protobuf definitions. Streaming operations should use bidirectional or server-side streaming where useful for:

- query subscriptions,
- parse token emission,
- long-running batch compilation,
- certification result streaming,
- federated synchronization.

### 9.3 CLI mapping

Every major API operation should have a CLI equivalent where feasible. The CLI should be a thin orchestration and UX layer over the same core contracts.

---

## 10. Compatibility and Versioning Rules

### 10.1 Version dimensions

The engineering surface has at least five version dimensions:

1. language version
2. profile version
3. API version
4. storage schema version
5. transport contract version

These must be tracked independently but related through compatibility matrices.

### 10.2 Backward compatibility

Minor version changes may add fields, capabilities, warnings, or optional behaviors, but may not silently change canonical meaning.

### 10.3 Breaking changes

Breaking changes require:

- RFC approval,
- transition documentation,
- migration strategy,
- updated test vectors,
- dual-support period where practical,
- explicit deprecation notices.

---

# PART II — PROTOBUF / IDL / EVENT CONTRACT PACK

## 11. Purpose

This section defines the reference transport and message contract layer for distributed AASL systems. It is the baseline for inter-service communication, SDK generation, event streaming, audit pipelines, and federation.

---

## 12. Contracting Strategy

Three complementary forms of contracts are recommended:

1. **API IDL contracts** for request/response services.
2. **Event contracts** for asynchronous state transitions and notifications.
3. **Data contracts** for persisted manifests, registries, diagnostics, snapshots, and certification results.

Recommended formats:

- Protobuf for network and service interfaces.
- JSON Schema / YAML Schema for human-readable validation and configuration.
- Avro or Protobuf for event bus transport where needed.
- OpenAPI as a documentation and tooling artifact layered on top of logical APIs.

---

## 13. Reference Protobuf Package Layout

```text
proto/
  aasl/
    common/v1/common.proto
    diagnostics/v1/diagnostics.proto
    parser/v1/parser.proto
    validator/v1/validator.proto
    compiler/v1/compiler.proto
    runtime/v1/runtime.proto
    query/v1/query.proto
    storage/v1/storage.proto
    governance/v1/governance.proto
    certification/v1/certification.proto
    federation/v1/federation.proto
    events/v1/events.proto
```

Namespace convention:

- package names use domain + version
- message names use PascalCase
- field names use snake_case
- enum values are prefixed by enum name where necessary

---

## 14. Common protobuf definitions (illustrative)

```proto
syntax = "proto3";

package aasl.common.v1;

message HashRef {
  string algorithm = 1;
  string value = 2;
}

message SourceSpan {
  string uri = 1;
  uint32 start_line = 2;
  uint32 start_col = 3;
  uint32 end_line = 4;
  uint32 end_col = 5;
}

message TraceContext {
  string trace_id = 1;
  string span_id = 2;
  string parent_span_id = 3;
}

message RequestMeta {
  string request_id = 1;
  string api_version = 2;
  string profile = 3;
  TraceContext trace = 4;
  repeated string capabilities = 5;
}
```

---

## 15. Parser service IDL example

```proto
syntax = "proto3";

package aasl.parser.v1;

import "aasl/common/v1/common.proto";
import "aasl/diagnostics/v1/diagnostics.proto";

message ParseRequest {
  aasl.common.v1.RequestMeta meta = 1;
  string source_text = 2;
  string source_uri = 3;
  repeated string emit = 4;
}

message ParseResponse {
  aasl.common.v1.RequestMeta meta = 1;
  string ast_json = 2;
  string cst_json = 3;
  repeated aasl.diagnostics.v1.Diagnostic diagnostics = 4;
}

service ParserService {
  rpc ParseDocument(ParseRequest) returns (ParseResponse);
}
```

---

## 16. Event contract taxonomy

AASL event streams should be broken into domains.

### 16.1 Build and analysis events

- `parser.document_parsed`
- `parser.syntax_error_detected`
- `validator.document_validated`
- `compiler.compilation_completed`
- `canonicalizer.hash_computed`

### 16.2 Runtime events

- `runtime.document_loaded`
- `runtime.object_resolved`
- `runtime.transaction_committed`
- `runtime.snapshot_created`
- `runtime.reference_unresolved`

### 16.3 Storage events

- `storage.artifact_written`
- `storage.snapshot_restored`
- `storage.compaction_completed`
- `storage.manifest_published`

### 16.4 Governance events

- `governance.proposal_submitted`
- `governance.review_completed`
- `governance.namespace_registered`
- `governance.deprecation_notice_published`

### 16.5 Certification events

- `certification.run_started`
- `certification.vector_failed`
- `certification.suite_completed`
- `certification.certificate_published`
- `certification.certificate_revoked`

### 16.6 Federation events

- `federation.peer_discovered`
- `federation.capabilities_exchanged`
- `federation.query_delegated`
- `federation.manifest_synchronized`
- `federation.trust_bundle_updated`

---

## 17. Standard event envelope

```yaml
EventEnvelope:
  event_id: string
  event_type: string
  event_version: string
  occurred_at: string
  producer:
    system: string
    instance: string
  subject:
    kind: string
    id: string
  correlation:
    request_id: string
    trace_id: string
    causation_id: string
  profile: string
  payload: object
  signatures:
    - algorithm: string
      key_id: string
      value: string
```

Requirements:

- all events are immutable,
- event ordering guarantees must be documented per topic,
- exactly-once delivery is not assumed,
- idempotency keys are required for mutating consumers,
- schema registry compatibility mode must be defined.

---

## 18. Schema evolution rules

### 18.1 Protobuf evolution

Allowed:
- adding new optional fields,
- reserving removed field numbers,
- adding new enum values with careful downgrade behavior,
- introducing new services or methods.

Disallowed without major contract version:
- reusing field numbers,
- changing semantic meaning of existing fields,
- changing message meaning while preserving names,
- redefining canonical hash inputs without explicit versioning.

### 18.2 Event evolution

Each event type must define compatibility class:

- additive-compatible,
- consumer-warning,
- breaking-major,
- deprecated-emitted,
- retired.

---

## 19. Event bus reference guidance

Recommended stream partitioning keys:

- artifact id
n- namespace id
- document id
- certification run id
- governance proposal id
- tenant id

Recommended topics:

- `aasl.analysis`
- `aasl.runtime`
- `aasl.storage`
- `aasl.governance`
- `aasl.certification`
- `aasl.federation`
- `aasl.audit`

Recommended metadata headers:

- `event_type`
- `profile`
- `schema_ref`
- `tenant_id`
- `trace_id`
- `auth_subject`

---

# PART III — DATABASE SCHEMA REFERENCE PACK

## 20. Purpose

This section defines the conceptual and reference physical data model for AASL implementations. It is not a mandate for a single database engine; it is a normalized reference pack intended to support portability, auditing, federation, and certification.

---

## 21. Persistence domains

A complete AASL implementation commonly persists the following domains:

1. source artifacts
2. canonical artifacts
3. binary artifacts (`.aasb`)
4. document metadata
5. object registry
6. reference graph
7. namespace registry
8. ontology registry
9. query indexes
10. snapshots and manifests
11. diagnostics and audit logs
12. certification assets
13. governance workflows
14. security and trust metadata
15. tenancy and billing metadata where applicable

---

## 22. Storage engine roles

A full implementation may use multiple storage engines:

- relational store for transactional metadata and governance state,
- object store for large artifacts and fixture packs,
- document store for flexible intermediate structures,
- graph store for reference traversal and semantic relationships,
- search index for diagnostics, code search, and query optimization,
- time-series store for observability and performance data,
- key-value cache for runtime acceleration.

The canonical schema pack is relational-first and graph-aware.

---

## 23. Core relational tables

### 23.1 `artifacts`

Stores immutable artifact records.

Columns:
- `artifact_id` PK
- `artifact_kind`
- `media_type`
- `profile`
- `language_version`
- `storage_uri`
- `hash_algorithm`
- `hash_value`
- `size_bytes`
- `created_at`
- `created_by`
- `tenant_id` nullable
- `status`

Indexes:
- unique `(hash_algorithm, hash_value)`
- `(artifact_kind, created_at)`
- `(tenant_id, created_at)`

### 23.2 `documents`

Represents logical document identity across artifact versions.

Columns:
- `document_id` PK
- `current_artifact_id`
- `document_kind`
- `namespace_id`
- `title`
- `lifecycle_state`
- `created_at`
- `updated_at`
- `supersedes_document_id` nullable

### 23.3 `document_versions`

Tracks version lineage.

Columns:
- `document_version_id` PK
- `document_id` FK
- `artifact_id` FK
- `version_label`
- `canonical_hash`
- `is_current`
- `created_at`
- `created_by`
- `change_summary`

### 23.4 `objects`

Stores canonical object registry entries.

Columns:
- `object_id` PK
- `document_id` FK
- `object_type`
- `object_name`
- `stable_identity_hash`
- `source_span_ref`
- `state_blob_ref`
- `created_at`
- `updated_at`

Indexes:
- unique `(stable_identity_hash)`
- `(document_id, object_type)`
- `(object_name)`

### 23.5 `references`

Stores edges between objects or documents.

Columns:
- `reference_id` PK
- `source_object_id` FK
- `target_object_id` nullable FK
- `target_external_ref` nullable
- `reference_kind`
- `resolution_status`
- `source_span_ref`
- `created_at`

Indexes:
- `(source_object_id)`
- `(target_object_id)`
- `(reference_kind, resolution_status)`

### 23.6 `namespaces`

Columns:
- `namespace_id` PK
- `namespace_uri`
- `authority_id`
- `status`
- `profile_scope`
- `registered_at`
- `deprecated_at` nullable

### 23.7 `ontologies`

Columns:
- `ontology_id` PK
- `namespace_id` FK
- `name`
- `version`
- `status`
- `artifact_id`
- `compatibility_class`
- `published_at`

### 23.8 `diagnostics`

Columns:
- `diagnostic_id` PK
- `request_id`
- `code`
- `severity`
- `phase`
- `artifact_id` nullable
- `document_id` nullable
- `object_id` nullable
- `message`
- `details_json`
- `created_at`

### 23.9 `snapshots`

Columns:
- `snapshot_id` PK
- `snapshot_kind`
- `manifest_id`
- `storage_uri`
- `created_at`
- `created_by`
- `restore_tested_at` nullable

### 23.10 `manifests`

Columns:
- `manifest_id` PK
- `manifest_kind`
- `artifact_id`
- `hash_value`
- `published_at`
- `published_by`

### 23.11 `governance_proposals`

Columns:
- `proposal_id` PK
- `proposal_type`
- `title`
- `status`
- `submitted_by`
- `submitted_at`
- `decision_at` nullable
- `decision_summary` nullable

### 23.12 `certification_runs`

Columns:
- `run_id` PK
- `implementation_id`
- `suite_id`
- `profile`
- `status`
- `started_at`
- `completed_at` nullable
- `result_summary_json`

### 23.13 `certification_findings`

Columns:
- `finding_id` PK
- `run_id` FK
- `vector_id`
- `severity`
- `status`
- `expected_ref`
- `actual_ref`
- `notes`

### 23.14 `tenants`

Columns:
- `tenant_id` PK
- `name`
- `status`
- `profile_limits_json`
- `created_at`

### 23.15 `auth_principals`

Columns:
- `principal_id` PK
- `principal_type`
- `display_name`
- `status`
- `created_at`

---

## 24. Graph model reference

For graph-oriented backends, the minimum node and edge categories should be:

Nodes:
- Document
- Object
- Namespace
- Ontology
- Proposal
- Certificate
- Manifest
- Tenant

Edges:
- CONTAINS
- REFERENCES
- IMPORTS
- EXTENDS
- SUPERSEDES
- GOVERNS
- CERTIFIES
- BELONGS_TO
- EMITS
- DEPENDS_ON

Graph traversals should support:

- inbound and outbound reference resolution,
- namespace impact analysis,
- deprecation blast radius,
- certification dependency lineage,
- federated artifact provenance.

---

## 25. Query indexing model

Recommended derived indexes:

- full-text index over source and diagnostics,
- canonical object identity index,
- namespace membership index,
- unresolved reference index,
- profile compatibility index,
- certification failure code index,
- observability incident correlation index.

---

## 26. Data retention and lifecycle

Artifacts are immutable. Metadata may evolve only through append-only lineage or explicit controlled mutation.

Retention classes:

1. permanent canonical artifacts,
2. long-retention audit artifacts,
3. medium-retention CI artifacts,
4. short-retention caches and ephemeral execution state.

Deletion should prefer tombstoning and manifest invalidation over physical erasure unless legal requirements demand hard deletion.

---

# PART IV — REPOSITORY LAYOUT STANDARD

## 27. Purpose

This section defines the canonical repository organization for AASL implementations. It supports discoverability, multi-language SDK generation, certification reproducibility, onboarding, and automation.

---

## 28. Repository topology options

Supported strategies:

1. **Monorepo standard** for the core platform and reference tooling.
2. **Federated multi-repo** with a central contract repository.
3. **Hybrid** where canonical contracts and golden assets live centrally, while runtime implementations live separately.

Recommended default for Atrahasis core: monorepo with strict module boundaries.

---

## 29. Canonical monorepo layout

```text
/aasl
  /docs
    /spec
    /architecture
    /operations
    /governance
    /certification
  /schemas
    /json
    /yaml
    /openapi
  /proto
  /idl
  /fixtures
    /aas
    /aasb
    /golden
    /fuzz
    /interop
  /packages
    /parser-core
    /validator-core
    /compiler-core
    /runtime-core
    /query-core
    /storage-core
    /formatter-core
    /diagnostics-core
  /services
    /parser-service
    /validator-service
    /compiler-service
    /runtime-service
    /query-service
    /storage-service
    /governance-service
    /certification-service
    /federation-service
  /sdks
    /typescript
    /python
    /go
    /rust
    /java
  /tools
    /cli
    /lsp
    /formatter
    /migration-assistant
    /schema-generator
  /infra
    /docker
    /k8s
    /terraform
    /helm
    /observability
  /scripts
  /test
    /unit
    /integration
    /e2e
    /conformance
    /performance
    /security
  /ci
  /release
  /examples
  /rfcs
  /governance
  /third_party
```

---

## 30. Layout rules

### 30.1 Separation of concerns

Core deterministic libraries belong in `/packages`. Networked or deployable wrappers belong in `/services`. Tooling UX layers belong in `/tools`.

### 30.2 Contract centralization

All protobuf, JSON Schema, YAML schema, OpenAPI, and event contracts must originate in `/proto`, `/idl`, or `/schemas` and be versioned with explicit ownership.

### 30.3 Fixture discipline

Golden vectors, `.aas`, `.aasb`, fuzz corpora, and interop packs must live in `/fixtures` with machine-readable metadata and manifest hashes.

### 30.4 Release compartmentalization

Release manifests, changelogs, SBOMs, signatures, and certification evidence must be produced into `/release` or its generated outputs.

### 30.5 RFC governance locality

Normative process artifacts belong in `/rfcs` and `/governance` and should be directly linked to code and schema changes.

---

## 31. Branching model reference

Recommended baseline:

- `main`: always releasable or near-releasable.
- `develop` optional for large teams.
- `release/*`: stabilization branches.
- `hotfix/*`: urgent production fixes.
- `feature/*`: scoped branches tied to issue or RFC IDs.
- `rfc/*`: proposal work where contracts and docs are primary artifacts.

Every merge into a protected branch must satisfy:

- passing tests,
- required review count,
- contract diff review,
- security checks,
- changelog impact classification,
- migration note requirement where applicable.

---

# PART V — CI/CD PIPELINE REFERENCE

## 32. Purpose

This section defines the reference CI/CD lifecycle for building, validating, packaging, testing, certifying, and releasing AASL implementations.

---

## 33. Pipeline goals

A compliant pipeline should guarantee:

- deterministic builds,
- reproducible test runs,
- verified schema integrity,
- controlled artifact publication,
- signed releases,
- security and supply-chain enforcement,
- certification evidence generation,
- rollback-ready deployment manifests.

---

## 34. Canonical pipeline stages

### Stage 1 — Pre-merge static checks

Tasks:
- lint source and contracts,
- schema validation,
- protobuf breaking-change detection,
- dependency policy checks,
- secret scanning,
- license compliance checks,
- commit message and PR template validation.

### Stage 2 — Build and generation

Tasks:
- compile libraries and services,
- generate SDK bindings from contracts,
- generate OpenAPI docs,
- generate schema bundles,
- build CLI binaries,
- produce immutable build metadata.

### Stage 3 — Deterministic analysis tests

Tasks:
- parser golden tests,
- validator rule tests,
- compiler trace tests,
- canonicalization determinism tests,
- error code catalog consistency checks.

### Stage 4 — Integration and conformance tests

Tasks:
- API integration tests,
- storage backend profile tests,
- query engine integration tests,
- federation protocol tests,
- multi-tenant boundary tests,
- certification vector dry runs.

### Stage 5 — Security and resilience tests

Tasks:
- dependency vulnerability scanning,
- image scanning,
- fuzz tests,
- malformed artifact tests,
- authz regression tests,
- replay and downgrade scenario tests.

### Stage 6 — Performance validation

Tasks:
- parser throughput benchmark,
- query latency benchmark,
- storage compaction benchmark,
- runtime snapshot restore benchmark,
- memory regression checks.

### Stage 7 — Packaging

Tasks:
- package containers,
- build installer bundles,
- publish schemas,
- publish SDKs,
- assemble release manifests,
- generate SBOMs,
- sign artifacts.

### Stage 8 — Staging deployment and verification

Tasks:
- deploy to ephemeral or staging environment,
- run smoke suite,
- run migration rehearsal,
- verify observability hooks,
- verify federation capability advertisement,
- verify rollback package presence.

### Stage 9 — Release approval gate

Tasks:
- changelog sign-off,
- release notes approval,
- security sign-off,
- governance sign-off for normative changes,
- certification evidence attachment,
- promotion approval.

### Stage 10 — Production promotion

Tasks:
- canary or blue/green deployment,
- progressive rollout,
- SLO watch period,
- artifact publication,
- certification state update,
- post-release verification report.

---

## 35. Pipeline orchestration model

Reference trigger model:

- push to feature branch → lightweight checks,
- pull request → full pre-merge suite,
- merge to main → build + integration + packaging,
- release tag → full certification + signed publication,
- nightly → extended fuzzing, long performance runs, drift checks,
- weekly → backup restore drills, dependency refresh analysis, federation interoperability rehearsals.

---

## 36. Required pipeline artifacts

Each pipeline should emit machine-readable artifacts such as:

- build manifest,
- dependency lock snapshot,
- contract diff report,
- test summary report,
- conformance result bundle,
- performance benchmark report,
- SBOM,
- signature bundle,
- container digest map,
- deployment manifest set,
- rollback manifest set.

---

## 37. Supply-chain integrity controls

Minimum expectations:

- hermetic or controlled builds where practical,
- pinned dependencies,
- checksum verification,
- signed source tags,
- signed build provenance,
- SBOM generation,
- artifact signing,
- release attestations,
- policy enforcement for untrusted transitive dependencies.

Recommended standards to align with:

- SLSA-style provenance levels,
- in-toto attestations,
- Sigstore/Cosign-style signing,
- SPDX or CycloneDX SBOMs.

---

## 38. Deployment patterns

### 38.1 Local developer deployment

- single-node runtime,
- embedded stores,
- mock federation peer,
- reduced auth complexity,
- fast fixture loading.

### 38.2 Staging deployment

- production-like contracts,
- representative datasets,
- observability enabled,
- migration rehearsal required,
- test federation peers,
- certificate test endpoints.

### 38.3 Production deployment

- HA services,
- isolated tenants,
- rolling or blue/green deployment,
- audited secret handling,
- mandatory rollback path,
- incident hooks and runbooks.

---

# PART VI — RELEASE ENGINEERING HANDBOOK

## 39. Purpose

This section defines the end-to-end release engineering model for AASL components, services, SDKs, schemas, fixtures, and documentation.

---

## 40. Release object types

AASL release engineering must support multiple release object types:

1. language/spec releases,
2. contract releases,
3. library releases,
4. service releases,
5. SDK releases,
6. fixture pack releases,
7. certification suite releases,
8. documentation releases,
9. profile releases,
10. governance decision bundle releases.

These object types may move on different cadences but must be linked by a common release manifest.

---

## 41. Semantic versioning policy

Recommended policy:

- **MAJOR**: incompatible contract or semantic change.
- **MINOR**: backward-compatible feature additions.
- **PATCH**: bug fixes, clarifications, non-semantic improvements.

For normative language changes, semver is necessary but not sufficient. Every normative change must also declare:

- compatibility impact,
- migration requirements,
- canonicalization impact,
- certification suite delta,
- profile scope.

---

## 42. Release trains

Reference release trains:

- **nightly**: internal validation only,
- **alpha**: unstable experimentation,
- **beta**: external preview,
- **release candidate**: stabilization and certification,
- **general availability**: certified public release,
- **LTS**: long-term support stream,
- **hotfix**: urgent corrective release.

---

## 43. Release checklist

Every releasable component should pass this checklist.

### 43.1 Readiness

- issues triaged,
- blockers resolved or accepted,
- RFC-linked changes completed,
- docs updated,
- migrations authored,
- deprecation notices drafted where needed.

### 43.2 Validation

- full test suite passed,
- golden vectors passed,
- certification deltas reviewed,
- fuzz suite status acceptable,
- performance regressions reviewed,
- compatibility report approved.

### 43.3 Packaging

- artifacts built reproducibly,
- manifests complete,
- hashes generated,
- SBOM attached,
- signatures attached,
- release notes drafted.

### 43.4 Approval

- engineering approval,
- security approval,
- governance approval for normative changes,
- release manager sign-off,
- incident rollback readiness confirmed.

### 43.5 Publication

- git tag or source release published,
- package registries updated,
- containers published,
- schema registries updated,
- docs site updated,
- certification records updated.

---

## 44. Release manifests

Every release should produce a signed manifest like the following:

```yaml
release_id: aasl-runtime-1.4.0
release_type: service
version: 1.4.0
source_tag: refs/tags/runtime-v1.4.0
build_provenance_ref: provenance://build/12345
artifacts:
  - artifact_id: runtime-linux-amd64
    hash: sha256:...
  - artifact_id: runtime-container
    digest: sha256:...
contracts:
  - parser-api-v1.2
  - runtime-api-v1.1
schemas:
  - query-grammar-v1.0
fixtures:
  - golden-pack-2026.03
certification:
  suite: core-profile-1
  result: pass
approvals:
  engineering: approved
  security: approved
  governance: n/a
published_at: 2026-03-08T00:00:00Z
```

---

## 45. Migration and upgrade discipline

Any release affecting storage, contracts, profiles, or canonical behavior must include:

- migration plan,
- downgrade/rollback assessment,
- dual-read/dual-write strategy where applicable,
- data backfill plan,
- contract negotiation behavior,
- runbook for staged rollout.

---

## 46. Rollback strategy

Release engineering must never depend on “just redeploy the previous version” as the only rollback approach.

Rollback planning must consider:

- binary rollback,
- schema rollback or forward-fix,
- contract compatibility downgrades,
- queue/event replay handling,
- partial artifact invalidation,
- stale cache invalidation,
- federation peer compatibility preservation,
- tenant-specific mitigation.

Recommended rollback package contents:

- prior deploy manifests,
- previous signed artifacts,
- known-good config set,
- DB restore or migration reversal instructions,
- queue offset handling notes,
- incident owner and approval chain.

---

## 47. Long-term support policy

LTS streams should define:

- supported duration,
- backport eligibility rules,
- security patch SLA,
- certification renewal schedule,
- end-of-support notice timelines,
- compatibility promises.

Recommended baseline:

- two active supported minor trains,
- one designated LTS line,
- emergency security backports for critical issues,
- fixed retirement windows with published calendar.

---

## 48. Release roles and responsibilities

### 48.1 Release manager

Owns release coordination, gates, checklists, approval collection, publication timing, rollback readiness, and communication.

### 48.2 Domain owner

Owns the correctness of subsystem changes for parser, validator, compiler, runtime, query, storage, governance, or certification.

### 48.3 Security reviewer

Owns security sign-off, risk acceptance, vulnerability exceptions, key management compliance, and supply-chain integrity review.

### 48.4 Governance authority

Owns approval for normative language, profile, ontology, namespace, or compatibility changes.

### 48.5 SRE / platform owner

Owns production rollout, observability readiness, canary evaluation, rollback execution, and post-release health verification.

---

## 49. Release communications

Every significant release should publish:

- executive summary,
- technical summary,
- breaking changes section,
- migration notes,
- security notes,
- certification status,
- known issues,
- rollout schedule,
- rollback conditions.

---

# PART VII — IMPLEMENTATION GUIDANCE APPENDICES

## 50. Sample API contract inventory

A minimal implementation should at least ship contracts for:

- parser parse/tokenize/explain,
- validator validate/explain,
- formatter format/canonicalize,
- query execute/explain,
- storage artifact get/put,
- runtime load/resolve,
- certification run/findings,
- governance namespace register/proposal submit.

An enterprise or federated implementation should additionally ship:

- delegate query,
- trust exchange,
- manifest sync,
- tenant administration,
- audit export,
- long-running workflow orchestration contracts.

---

## 51. Sample database migration policy

Migration rules:

1. all schema migrations are versioned and reviewed,
2. destructive migrations require explicit release classification,
3. backfills must be idempotent,
4. rollback notes are mandatory,
5. schema drift detection must run in CI,
6. migrations affecting canonical outputs require certification reruns.

---

## 52. Sample repository code ownership model

Suggested ownership map:

- `/proto`, `/schemas`, `/idl` → architecture + platform contracts team
- `/packages/parser-core` → parser domain team
- `/packages/compiler-core` → compiler domain team
- `/packages/runtime-core` → runtime domain team
- `/services/*` → service owners + platform team
- `/fixtures/golden` → certification authority + domain owners
- `/rfcs`, `/governance` → standards/governance board
- `/infra` → platform engineering / SRE
- `/release` → release engineering

---

## 53. Sample CI gate policy matrix

| Change Type | Required Gates |
|---|---|
| Parser grammar change | syntax tests, golden corpus, perf smoke, contract review |
| Validator rule change | rule tests, diagnostics diff, conformance rerun |
| Query planner change | planner tests, integration tests, performance regression |
| Storage schema change | migration rehearsal, backup restore drill, rollback review |
| Federation protocol change | interop suite, peer compatibility tests, security review |
| Governance rule change | RFC approval, docs sync, certification impact review |

---

## 54. Sample release artifact set

A robust release should publish:

- source archive,
- compiled binaries,
- container images,
- schema bundle,
- protobuf descriptor set,
- OpenAPI bundle,
- fixture manifest,
- SBOM,
- provenance attestation,
- checksums,
- signatures,
- changelog,
- migration guide,
- certification result bundle.

---

## 55. Recommended implementation sequence

For a new engineering team building the implementation pack in order:

1. establish repository layout,
2. define common schemas and diagnostics,
3. publish API and protobuf contracts,
4. implement parser and validator reference services,
5. stand up storage metadata schema,
6. implement runtime and query contracts,
7. wire CI generation and test gates,
8. add release engineering manifests and signing,
9. add governance and certification automation,
10. harden production deployment and rollback workflows.

---

## 56. Final normative guidance

An AASL implementation should not be considered engineering-complete merely because the parser works or the runtime compiles documents. It becomes implementation-ready only when all of the following are true:

- service boundaries are formalized,
- data contracts are versioned,
- persistence is modeled and migratable,
- repository structure supports scale,
- CI/CD enforces determinism and trust,
- release engineering is reproducible and auditable,
- rollback and upgrade behavior are explicit,
- governance and certification are wired into the build lifecycle.

This engineering pack is therefore a foundational operationalization document. It is meant to be used directly by implementation teams building the real AASL platform, not merely as a conceptual appendix.

---

## 57. Suggested companion artifacts to derive from this document

The following implementation artifacts should be generated next from this pack:

1. OpenAPI bundle for all service endpoints
2. Protobuf descriptor set and generated SDK stubs
3. SQL DDL starter pack for the relational schema
4. Graph schema starter pack
5. Repository scaffold template
6. CI pipeline templates for GitHub Actions / GitLab / Buildkite
7. Release manifest schema and signer utility
8. Rollback runbook template
9. Migration checklist template
10. Ownership and code review policy pack

---

**End of Document**
