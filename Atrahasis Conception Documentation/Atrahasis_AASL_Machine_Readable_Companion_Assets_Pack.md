# Atrahasis AASL Machine-Readable Companion Assets Pack

**Status:** Canonical Companion Asset Specification  
**Scope:** JSON/YAML schema packs, official sample `.aas` documents, official sample `.aasb` fixtures, machine-readable error catalog, machine-readable conformance manifests, and golden test corpora asset structure  
**Intended Audience:** Runtime implementers, compiler authors, validator maintainers, SDK teams, conformance labs, ontology stewards, CI/CD owners, and downstream integrators

---

## 1. Purpose

This document defines the machine-readable companion asset layer for the Atrahasis Agent Semantic Language (AASL). The canonical prose specification defines the language normatively for humans. This companion pack defines the normative machine-readable assets that allow implementations, validators, CI systems, editors, and certification pipelines to operate against a shared executable reference surface.

The goals of this companion asset pack are to:

1. Provide stable schema definitions for core AASL structures.
2. Provide official sample source documents in `.aas` form.
3. Provide official sample binary fixtures in `.aasb` form.
4. Publish a machine-readable error catalog used across parser, compiler, validator, runtime, and query layers.
5. Publish machine-readable conformance manifests that define test suite membership, expected outcomes, feature gates, and profile applicability.
6. Publish golden corpus packs as actual structured assets rather than prose-only examples.
7. Enable deterministic, repeatable interoperability across implementations.
8. Create a clean separation between human-readable standards and automation-ready artifacts.

This document is not a replacement for the prose AASL specification. It is the executable companion layer that operationalizes that specification.

---

## 2. Design Principles

The machine-readable asset ecosystem SHALL follow these principles:

### 2.1 Canonical determinism

Any canonical input paired with a declared profile and schema version SHALL produce deterministic validation and conformance outcomes.

### 2.2 Versioned evolution

All assets SHALL be versioned independently and collectively. Implementations SHALL declare which companion pack version they support.

### 2.3 Profile awareness

Assets SHALL support multiple runtime and implementation profiles without duplicating the entire corpus.

### 2.4 Tool neutrality

Assets SHALL be consumable by any language ecosystem and SHALL avoid unnecessary dependencies on platform-specific tooling.

### 2.5 Human inspectability

Where practical, machine-readable assets SHALL remain readable and reviewable by humans.

### 2.6 Binary transparency

Binary fixture packs SHALL always be accompanied by metadata, source mappings, and provenance information.

### 2.7 Explicit admissibility

Expected outcomes SHALL be expressed in machine-readable manifests rather than inferred implicitly from file location alone.

### 2.8 Layered extensibility

Core schemas SHALL be minimal and stable; optional modules, ontologies, and profiles SHALL extend them through controlled extension points.

---

## 3. Companion Pack Contents

The complete companion pack consists of the following top-level categories:

1. **Schema Packs**
   - JSON Schema set
   - YAML serialization conventions
   - schema meta-manifests
   - profile and feature declarations

2. **Official Sample `.aas` Documents**
   - minimal source examples
   - canonical examples
   - negative examples
   - edge-case examples
   - profile-specific examples

3. **Official Sample `.aasb` Fixtures**
   - encoded binary fixtures
   - decoded metadata sidecars
   - integrity manifests
   - cross-version fixtures

4. **Machine-Readable Error Catalog**
   - parser errors
   - compiler diagnostics
   - validator findings
   - runtime errors
   - query errors
   - federation and storage codes

5. **Machine-Readable Conformance Manifests**
   - suite manifests
   - test case metadata
   - expected outcomes
   - feature requirements
   - profile applicability
   - certification tier mappings

6. **Golden Test Corpora**
   - golden inputs
   - golden normalized outputs
   - golden AST/IR snapshots
   - golden validator outcomes
   - golden query result sets
   - golden federation and round-trip assets

---

## 4. Repository Layout Standard

A canonical companion asset repository SHALL use the following logical layout:

```text
/aasl-companion-pack/
  /schemas/
    manifest.json
    /json/
      aasl-document.schema.json
      aasl-entity.schema.json
      aasl-link.schema.json
      aasl-claim.schema.json
      aasl-query.schema.json
      aasl-error.schema.json
      aasl-conformance-manifest.schema.json
      aasl-testcase.schema.json
      aasl-profile.schema.json
      aasl-feature.schema.json
    /yaml/
      serialization-conventions.yaml
      examples/
  /samples/
    /aas/
      /minimal/
      /canonical/
      /negative/
      /edge/
      /profiles/
    /aasb/
      /fixtures/
      /metadata/
      /integrity/
  /errors/
    error-catalog.json
    error-catalog.yaml
  /conformance/
    suite-manifest.json
    suite-manifest.yaml
    /profiles/
    /tiers/
    /cases/
  /golden/
    /documents/
    /normalization/
    /ast/
    /ir/
    /validation/
    /query/
    /runtime/
    /interop/
    /fuzz-seeds/
  /profiles/
    core-runtime.json
    constrained-runtime.json
    distributed-runtime.json
    archival-runtime.json
  /provenance/
    release-manifest.json
    checksums.sha256
    signatures/
  /docs/
    asset-index.md
```

Alternative physical packaging is allowed, but the logical structure and asset semantics SHALL remain equivalent.

---

## 5. Versioning Model

Every machine-readable asset SHALL contain or inherit the following identifiers:

- `packVersion`
- `schemaVersion`
- `aaslVersion`
- `profileVersion` where applicable
- `assetKind`
- `assetId`
- `createdAt`
- `updatedAt`
- `provenance`

### 5.1 Pack version semantics

The companion pack SHALL use semantic versioning:

- **MAJOR**: breaking schema or expectation changes
- **MINOR**: additive fields, new cases, new profiles, new error codes, new samples
- **PATCH**: corrections, clarifications, metadata fixes, checksum refreshes without normative semantic change

### 5.2 Compatibility rule

An implementation declaring support for pack `X.Y` SHALL at minimum tolerate patch-level updates within the same minor line unless otherwise stated in profile rules.

---

## 6. JSON and YAML Serialization Policy

The companion assets SHALL support JSON as the normative machine-readable interchange form. YAML MAY be published as a convenience mirror where structural equivalence is exact.

### 6.1 Normative precedence

Where both JSON and YAML versions exist, the JSON artifact is normative unless explicitly marked otherwise.

### 6.2 YAML restrictions

YAML assets SHALL avoid advanced YAML features that reduce interoperability, including:

- anchors and aliases in normative artifacts
- custom tags
- merge keys for canonical documents
- implicit typing ambiguities

### 6.3 Encoding

All text assets SHALL be UTF-8 encoded without BOM.

### 6.4 Newlines

Canonical repository artifacts SHOULD use LF line endings.

---

## 7. Schema Packs

The schema pack provides the machine-validatable structural contracts for the companion asset ecosystem.

### 7.1 Schema categories

The core schema pack SHALL define schemas for:

1. document envelope
2. entity objects
3. relation/link objects
4. claim/assertion objects
5. annotations and provenance structures
6. query request and response objects
7. error diagnostics
8. conformance manifests
9. test case descriptors
10. profile descriptors
11. feature descriptors
12. binary fixture metadata

### 7.2 Schema packaging manifest

Each release SHALL include a schema manifest similar to the following:

```json
{
  "assetKind": "schema-pack-manifest",
  "assetId": "aasl.schema-pack.core",
  "packVersion": "1.0.0",
  "schemaVersion": "1.0.0",
  "aaslVersion": "1.0.0",
  "schemas": [
    {
      "name": "aasl-document",
      "path": "schemas/json/aasl-document.schema.json",
      "version": "1.0.0",
      "sha256": "<sha256>"
    },
    {
      "name": "aasl-error",
      "path": "schemas/json/aasl-error.schema.json",
      "version": "1.0.0",
      "sha256": "<sha256>"
    },
    {
      "name": "aasl-conformance-manifest",
      "path": "schemas/json/aasl-conformance-manifest.schema.json",
      "version": "1.0.0",
      "sha256": "<sha256>"
    }
  ]
}
```

### 7.3 Core document schema example

The companion pack SHALL provide a top-level document schema. An illustrative structure is shown below.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.dev/schemas/aasl-document.schema.json",
  "title": "AASL Document",
  "type": "object",
  "required": [
    "assetKind",
    "aaslVersion",
    "documentId",
    "kind",
    "body"
  ],
  "properties": {
    "assetKind": {
      "const": "aasl-document"
    },
    "aaslVersion": {
      "type": "string"
    },
    "documentId": {
      "type": "string",
      "minLength": 1
    },
    "kind": {
      "type": "string"
    },
    "profile": {
      "type": "string"
    },
    "imports": {
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true
    },
    "body": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/node"
      }
    }
  },
  "$defs": {
    "node": {
      "type": "object",
      "required": ["nodeType", "id"],
      "properties": {
        "nodeType": {
          "type": "string"
        },
        "id": {
          "type": "string"
        },
        "label": {
          "type": "string"
        },
        "properties": {
          "type": "object",
          "additionalProperties": true
        }
      },
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

### 7.4 Query schema example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.dev/schemas/aasl-query.schema.json",
  "title": "AASL Query Request",
  "type": "object",
  "required": ["assetKind", "queryId", "language", "statement"],
  "properties": {
    "assetKind": { "const": "aasl-query" },
    "queryId": { "type": "string" },
    "language": { "type": "string" },
    "statement": { "type": "string" },
    "parameters": {
      "type": "object",
      "additionalProperties": true
    },
    "options": {
      "type": "object",
      "additionalProperties": true
    }
  },
  "additionalProperties": false
}
```

### 7.5 Error schema example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.dev/schemas/aasl-error.schema.json",
  "title": "AASL Error",
  "type": "object",
  "required": [
    "assetKind",
    "code",
    "layer",
    "severity",
    "messageTemplate"
  ],
  "properties": {
    "assetKind": { "const": "aasl-error" },
    "code": { "type": "string" },
    "layer": { "type": "string" },
    "severity": { "type": "string" },
    "messageTemplate": { "type": "string" },
    "explanation": { "type": "string" },
    "suggestedActions": {
      "type": "array",
      "items": { "type": "string" }
    },
    "stable": { "type": "boolean" },
    "introducedIn": { "type": "string" },
    "deprecatedIn": { "type": ["string", "null"] }
  },
  "additionalProperties": false
}
```

### 7.6 Conformance manifest schema example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://atrahasis.dev/schemas/aasl-conformance-manifest.schema.json",
  "title": "AASL Conformance Manifest",
  "type": "object",
  "required": [
    "assetKind",
    "suiteId",
    "packVersion",
    "cases"
  ],
  "properties": {
    "assetKind": { "const": "aasl-conformance-manifest" },
    "suiteId": { "type": "string" },
    "packVersion": { "type": "string" },
    "certificationTier": { "type": "string" },
    "profiles": {
      "type": "array",
      "items": { "type": "string" }
    },
    "cases": {
      "type": "array",
      "items": { "$ref": "#/$defs/caseRef" }
    }
  },
  "$defs": {
    "caseRef": {
      "type": "object",
      "required": ["caseId", "path", "expectedOutcome"],
      "properties": {
        "caseId": { "type": "string" },
        "path": { "type": "string" },
        "expectedOutcome": { "type": "string" },
        "requiredFeatures": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

---

## 8. YAML Serialization Conventions

A YAML companion document SHALL map one-to-one with its JSON twin.

Example YAML representation:

```yaml
assetKind: aasl-conformance-manifest
suiteId: aasl.core.parser.tier1
packVersion: 1.0.0
certificationTier: tier1
profiles:
  - core-runtime
cases:
  - caseId: parser.minimal.accept.001
    path: conformance/cases/parser/minimal-accept-001.json
    expectedOutcome: pass
    requiredFeatures:
      - core.document
      - core.entity
```

YAML files SHALL be validated after canonical JSON conversion as part of release CI.

---

## 9. Official Sample `.aas` Documents

The companion pack SHALL ship official source examples that exercise the language as authored by humans.

### 9.1 Sample categories

The official sample set SHALL include:

- **minimal**: smallest admissible examples
- **canonical**: recommended idiomatic examples
- **negative**: intentionally invalid samples
- **edge**: boundaries, limits, and ambiguity stressors
- **profile-specific**: examples that only apply to specific runtime or feature profiles
- **migration**: version transition examples
- **round-trip**: examples used for parser-renderer stability

### 9.2 Naming convention

A sample naming convention SHOULD use:

```text
<category>.<domain>.<sequence>.aas
```

Examples:

- `minimal.entity.001.aas`
- `canonical.claims.004.aas`
- `negative.import-cycle.002.aas`
- `edge.deep-nesting.003.aas`

### 9.3 Sample metadata sidecar

Each official sample SHOULD have a sidecar metadata file:

```json
{
  "assetKind": "aasl-sample-metadata",
  "sampleId": "canonical.claims.004",
  "path": "samples/aas/canonical/canonical.claims.004.aas",
  "category": "canonical",
  "profiles": ["core-runtime"],
  "features": ["claims", "provenance", "links"],
  "expectedParse": "pass",
  "expectedValidate": "pass",
  "expectedCanonicalize": "pass",
  "notes": [
    "Exercises multi-claim entity with provenance blocks."
  ]
}
```

### 9.4 Minimal `.aas` source example

```aas
@document "minimal.entity.001"
@version "1.0.0"

entity person:joshua {
  label: "Joshua"
}
```

### 9.5 Canonical `.aas` source example

```aas
@document "canonical.claims.004"
@version "1.0.0"
@profile "core-runtime"

entity person:joshua {
  label: "Joshua"
  type: Person
}

entity org:atrahasis {
  label: "Atrahasis"
  type: Organization
}

claim employment:1 {
  subject: person:joshua
  predicate: employedBy
  object: org:atrahasis
  provenance {
    source: "internal-record"
    confidence: 0.98
  }
}
```

### 9.6 Negative sample example

```aas
@document "negative.duplicate-id.001"
@version "1.0.0"

entity person:joshua {
  label: "Joshua"
}

entity person:joshua {
  label: "Duplicate"
}
```

Expected outcome: parser pass, validator fail with duplicate identifier error.

### 9.7 Edge sample example

```aas
@document "edge.import-cycle.001"
@version "1.0.0"
@import "edge.import-cycle.002"
```

This sample is part of a pair that intentionally triggers import cycle detection.

---

## 10. Official Sample `.aasb` Fixtures

The binary fixture pack SHALL provide official encoded artifacts for runtime and tooling interoperability.

### 10.1 Fixture goals

`.aasb` fixtures exist to validate:

- encoding correctness
- decoding correctness
- checksum verification
- cross-language interoperability
- forward and backward compatibility policy
- binary framing stability
- compression behavior where applicable
- provenance and canonicalization linkage

### 10.2 Fixture categories

The `.aasb` fixture set SHALL include:

1. minimal fixtures
2. canonical fixtures
3. compatibility fixtures
4. corruption fixtures
5. boundary fixtures
6. streaming fixtures
7. partial decode fixtures
8. encrypted or signed fixture envelopes where profiles support them

### 10.3 Binary fixture metadata sidecar

Every `.aasb` fixture SHALL have a structured metadata sidecar.

Example:

```json
{
  "assetKind": "aasl-binary-fixture-metadata",
  "fixtureId": "aasb.canonical.claims.004",
  "path": "samples/aasb/fixtures/aasb.canonical.claims.004.aasb",
  "sourceDocument": "samples/aas/canonical/canonical.claims.004.aas",
  "encodingVersion": "1.0.0",
  "endianness": "little",
  "compression": "none",
  "framing": "standard",
  "sha256": "<sha256>",
  "payloadLength": 412,
  "expectedDecode": "pass",
  "expectedRoundTrip": "pass"
}
```

### 10.4 Fixture integrity manifest

```json
{
  "assetKind": "aasl-binary-integrity-manifest",
  "packVersion": "1.0.0",
  "fixtures": [
    {
      "fixtureId": "aasb.canonical.claims.004",
      "sha256": "<sha256>",
      "sizeBytes": 412
    },
    {
      "fixtureId": "aasb.corrupt.header.001",
      "sha256": "<sha256>",
      "sizeBytes": 33
    }
  ]
}
```

### 10.5 Example `.aasb` hex fixture descriptor

The binary payload itself is not represented here as normative prose, but a metadata descriptor MAY include a hex snapshot excerpt for debugging.

```json
{
  "fixtureId": "aasb.minimal.entity.001",
  "hexPreview": "41 41 53 42 01 00 10 00 7B 22 64 6F 63 75 6D 65"
}
```

### 10.6 Corruption fixture classes

The companion pack SHALL include negative binary fixtures for:

- invalid magic header
- unsupported encoding version
- truncated section
- invalid checksum
- invalid section length
- malformed string table
- unresolved symbol reference
- forbidden section ordering
- duplicate section IDs

---

## 11. Machine-Readable Error Catalog

The error catalog is the canonical registry of stable diagnostic codes across the AASL ecosystem.

### 11.1 Error catalog goals

The catalog SHALL:

- provide stable error codes
- categorize errors by architectural layer
- classify severity and admissibility impact
- standardize message templates
- provide remediation guidance
- support localization without changing semantic identity
- support tooling and certification expectations

### 11.2 Error code namespace format

A recommended format is:

```text
AASL-<LAYER>-<CLASS>-<NNNN>
```

Examples:

- `AASL-PARSE-SYNTAX-0001`
- `AASL-VALID-IDENTITY-0023`
- `AASL-COMP-ONTOLOGY-0104`
- `AASL-RUNTIME-TXN-0201`
- `AASL-QUERY-TYPE-0307`
- `AASL-FED-AUTH-0402`

### 11.3 Catalog structure

```json
{
  "assetKind": "aasl-error-catalog",
  "packVersion": "1.0.0",
  "entries": [
    {
      "code": "AASL-PARSE-SYNTAX-0001",
      "layer": "parser",
      "class": "syntax",
      "severity": "error",
      "admissibilityImpact": "reject",
      "messageTemplate": "Unexpected token '{token}' while parsing {context}.",
      "explanation": "The parser encountered a token sequence that does not match the grammar for the current construct.",
      "suggestedActions": [
        "Check delimiter balance.",
        "Verify the construct keyword and field separators.",
        "Review surrounding span information."
      ],
      "stable": true,
      "introducedIn": "1.0.0",
      "deprecatedIn": null,
      "tags": ["parser", "syntax", "core"]
    },
    {
      "code": "AASL-VALID-IDENTITY-0023",
      "layer": "validator",
      "class": "identity",
      "severity": "error",
      "admissibilityImpact": "reject",
      "messageTemplate": "Identifier '{id}' is duplicated within scope '{scope}'.",
      "explanation": "Identifiers must be unique within their declared visibility scope.",
      "suggestedActions": [
        "Rename one of the conflicting identifiers.",
        "Split the scope if separate identities were intended."
      ],
      "stable": true,
      "introducedIn": "1.0.0",
      "deprecatedIn": null,
      "tags": ["validator", "identity"]
    }
  ]
}
```

### 11.4 Severity taxonomy

Allowed severity values SHOULD include:

- `fatal`
- `error`
- `warning`
- `info`
- `hint`

### 11.5 Admissibility impact taxonomy

Allowed impact values SHOULD include:

- `reject`
- `quarantine`
- `allow-with-warning`
- `allow`
- `implementation-defined`

### 11.6 Localization policy

Localized rendering strings MAY be shipped separately, but the stable code and semantic definition SHALL remain language-independent.

---

## 12. Machine-Readable Conformance Manifests

Conformance manifests define the executable shape of the certification and compatibility suite.

### 12.1 Manifest responsibilities

A conformance manifest SHALL specify:

- suite identity
- suite version and pack version
- certification tier
- applicable profiles
- case membership
- required features
- expected outcomes
- waiver rules if any
- dependency relationships between cases
- implementation obligations

### 12.2 Top-level suite manifest example

```json
{
  "assetKind": "aasl-conformance-manifest",
  "suiteId": "aasl.core.tier1",
  "packVersion": "1.0.0",
  "certificationTier": "tier1",
  "profiles": ["core-runtime"],
  "cases": [
    {
      "caseId": "parser.minimal.accept.001",
      "path": "conformance/cases/parser.minimal.accept.001.json",
      "expectedOutcome": "pass",
      "requiredFeatures": ["core.document", "core.entity"]
    },
    {
      "caseId": "validator.duplicate-id.reject.001",
      "path": "conformance/cases/validator.duplicate-id.reject.001.json",
      "expectedOutcome": "fail",
      "requiredFeatures": ["core.identity"]
    }
  ]
}
```

### 12.3 Individual test case descriptor example

```json
{
  "assetKind": "aasl-testcase",
  "caseId": "validator.duplicate-id.reject.001",
  "title": "Duplicate identifier is rejected",
  "description": "Validation SHALL reject a document containing two entities with the same scoped identifier.",
  "profile": "core-runtime",
  "inputs": [
    {
      "kind": "aas-source",
      "path": "samples/aas/negative/negative.duplicate-id.001.aas"
    }
  ],
  "execution": {
    "parse": true,
    "canonicalize": false,
    "validate": true,
    "compile": false
  },
  "expected": {
    "status": "fail",
    "errors": ["AASL-VALID-IDENTITY-0023"]
  },
  "tags": ["validator", "identity", "negative"]
}
```

### 12.4 Feature flags and profiles

Conformance manifests SHALL explicitly state required features rather than relying only on informal grouping. This prevents hidden assumptions and allows partial implementations to declare precise compatibility.

---

## 13. Golden Test Corpora

Golden corpora are the authoritative test assets used to verify exact implementation behavior.

### 13.1 Purpose

Golden corpora SHALL provide:

- stable, reproducible inputs
- stable expected outputs
- cross-implementation comparability
- regression detection
- release gating data
- certification-grade evidence

### 13.2 Corpus categories

The official golden corpora SHALL include:

1. **source golden corpus**
2. **canonical normalization corpus**
3. **AST golden corpus**
4. **compiler IR golden corpus**
5. **validator findings corpus**
6. **query results corpus**
7. **runtime state transition corpus**
8. **binary round-trip corpus**
9. **interop corpus**
10. **fuzz seed corpus**

### 13.3 Golden document case example

```json
{
  "assetKind": "golden-case",
  "caseId": "golden.normalize.canonical.claims.004",
  "input": "samples/aas/canonical/canonical.claims.004.aas",
  "expectedCanonicalOutput": "golden/normalization/canonical.claims.004.normalized.aas",
  "expectedAst": "golden/ast/canonical.claims.004.ast.json",
  "expectedIr": "golden/ir/canonical.claims.004.ir.json",
  "expectedValidation": "golden/validation/canonical.claims.004.validation.json",
  "expectedBinary": "samples/aasb/fixtures/aasb.canonical.claims.004.aasb",
  "profiles": ["core-runtime"]
}
```

### 13.4 Golden validator output example

```json
{
  "assetKind": "aasl-validation-result",
  "documentId": "negative.duplicate-id.001",
  "status": "fail",
  "errors": [
    {
      "code": "AASL-VALID-IDENTITY-0023",
      "span": {
        "line": 7,
        "column": 8,
        "endLine": 7,
        "endColumn": 21
      }
    }
  ],
  "warnings": []
}
```

### 13.5 Golden AST example

```json
{
  "assetKind": "aasl-ast-snapshot",
  "documentId": "minimal.entity.001",
  "nodes": [
    {
      "nodeType": "Document",
      "id": "doc:minimal.entity.001",
      "children": ["entity:person:joshua"]
    },
    {
      "nodeType": "Entity",
      "id": "entity:person:joshua",
      "label": "Joshua"
    }
  ]
}
```

### 13.6 Golden query result example

```json
{
  "assetKind": "aasl-query-result",
  "queryId": "query.lookup.person.001",
  "status": "success",
  "rows": [
    {
      "entityId": "person:joshua",
      "label": "Joshua"
    }
  ],
  "rowCount": 1
}
```

---

## 14. Asset Provenance and Integrity

Every official machine-readable asset SHALL support provenance and integrity verification.

### 14.1 Provenance fields

Assets SHOULD carry:

- `generatedBy`
- `sourceInputs`
- `sourceSpecVersion`
- `generatorVersion`
- `generatedAt`
- `reviewedBy`
- `approvedAt`

### 14.2 Integrity release manifest example

```json
{
  "assetKind": "aasl-release-manifest",
  "packVersion": "1.0.0",
  "generatedAt": "2026-03-08T00:00:00Z",
  "artifacts": [
    {
      "path": "schemas/json/aasl-document.schema.json",
      "sha256": "<sha256>"
    },
    {
      "path": "errors/error-catalog.json",
      "sha256": "<sha256>"
    },
    {
      "path": "conformance/suite-manifest.json",
      "sha256": "<sha256>"
    }
  ]
}
```

### 14.3 Signing

Companion pack releases SHOULD support detached signatures. High-assurance certification releases SHOULD require signing.

---

## 15. Asset Lifecycle and Governance

### 15.1 Asset states

Machine-readable assets SHALL move through lifecycle states:

- draft
- review
- candidate
- canonical
- deprecated
- withdrawn

### 15.2 Change control

Normative changes to schemas, manifests, error codes, or golden expectations SHALL require the same governance rigor as prose specification changes.

### 15.3 Schema deprecation

Deprecated schemas SHALL remain available for a bounded support window, documented in release policy.

### 15.4 Golden corpus mutation policy

A golden corpus case SHALL NOT change silently. If expectations change normatively, the case SHALL either:

1. receive a new versioned case ID, or
2. record an explicit expected-output version bump in the manifest.

---

## 16. Certification and CI/CD Usage

The machine-readable pack is intended for direct integration into CI and certification pipelines.

### 16.1 CI use cases

CI systems SHOULD use the pack to:

- validate schemas
- run parser suites
- run validator suites
- verify error code stability
- verify round-trip behavior
- verify binary fixture handling
- compare golden outputs
- gate release certification claims

### 16.2 Certification evidence bundle

A certification run SHOULD emit an evidence bundle containing:

- implementation identity
- declared profiles and features
- pack version used
- manifest versions used
- pass/fail summary
- failed case details
- environment metadata
- artifact hashes

Example:

```json
{
  "assetKind": "aasl-certification-evidence",
  "implementationId": "org.example.aasl-rust",
  "implementationVersion": "2.4.1",
  "packVersion": "1.0.0",
  "profiles": ["core-runtime"],
  "summary": {
    "passed": 182,
    "failed": 0,
    "skipped": 4
  },
  "artifacts": [
    {
      "path": "results/parser-report.json",
      "sha256": "<sha256>"
    }
  ]
}
```

---

## 17. Interoperability Rules

Implementations claiming support for the companion pack SHALL observe the following:

1. They SHALL consume canonical JSON artifacts.
2. They SHALL preserve stable case IDs and error codes exactly.
3. They SHALL not reinterpret expected outcomes outside profile rules.
4. They SHALL honor declared schema and pack versions.
5. They SHALL emit machine-readable outputs in the defined result formats when participating in certification.
6. They SHALL not silently coerce invalid inputs into passing outcomes where golden or manifest expectations declare failure.

---

## 18. Reference Asset Families

The following asset families are RECOMMENDED for a first complete release:

### 18.1 Schema pack family

- `aasl-document.schema.json`
- `aasl-node.schema.json`
- `aasl-query.schema.json`
- `aasl-error.schema.json`
- `aasl-testcase.schema.json`
- `aasl-conformance-manifest.schema.json`
- `aasl-binary-fixture.schema.json`
- `aasl-release-manifest.schema.json`

### 18.2 Official sample `.aas` family

- `minimal.entity.001.aas`
- `minimal.link.001.aas`
- `canonical.claims.004.aas`
- `canonical.provenance.002.aas`
- `negative.duplicate-id.001.aas`
- `negative.import-cycle.001.aas`
- `edge.deep-nesting.003.aas`
- `profiles.distributed-runtime.002.aas`

### 18.3 Official sample `.aasb` family

- `aasb.minimal.entity.001.aasb`
- `aasb.canonical.claims.004.aasb`
- `aasb.compat.v1-to-v2.001.aasb`
- `aasb.corrupt.header.001.aasb`
- `aasb.truncated.section.002.aasb`

### 18.4 Machine-readable error family

- `error-catalog.json`
- `error-catalog.yaml`
- `error-index-by-layer.json`
- `error-index-by-stability.json`

### 18.5 Conformance manifest family

- `suite-manifest.json`
- `parser-tier1.json`
- `validator-tier1.json`
- `compiler-tier2.json`
- `query-tier2.json`
- `binary-tier2.json`
- `interop-tier3.json`

### 18.6 Golden corpus family

- normalization snapshots
- AST snapshots
- IR snapshots
- validation result snapshots
- binary round-trip outputs
- query answer sets
- fuzz seeds

---

## 19. Example End-to-End Case Bundle

A single complete conformance case bundle MAY look like the following:

```text
/cases/validator.duplicate-id.reject.001/
  testcase.json
  input.aas
  expected-validation.json
  expected-errors.json
  metadata.json
```

Illustrative `metadata.json`:

```json
{
  "assetKind": "aasl-case-metadata",
  "caseId": "validator.duplicate-id.reject.001",
  "title": "Duplicate scoped identifier rejection",
  "features": ["core.identity"],
  "profile": "core-runtime",
  "resultDeterminism": "strict",
  "maintainer": "Atrahasis Conformance Working Group"
}
```

---

## 20. Machine-Readable Asset Release Policy

A release of the companion asset pack SHALL include at minimum:

1. schema manifest
2. schema set
3. error catalog
4. conformance manifest set
5. official sample `.aas` set
6. official sample `.aasb` set
7. golden corpus set
8. release integrity manifest

A release SHOULD also include:

- changelog
- migration notes
- deprecated asset notices
- profile support matrix

---

## 21. Minimum Viable Companion Pack

For a minimum viable public release, the following assets are sufficient:

- one document schema
- one error schema
- one conformance manifest schema
- ten official `.aas` samples
- five official `.aasb` fixtures
- one initial error catalog with stable codes
- one tier-1 conformance manifest
- one golden normalization corpus
- one integrity manifest

This minimum release enables basic interoperability and implementation bootstrapping while preserving a clean path to broader certification.

---

## 22. Recommended Future Expansion

Future releases SHOULD add:

- localized diagnostic packs
- schema generation bindings for multiple languages
- richer ontology extension schemas
- signed release bundles
- large-scale archival corpora
- streaming query golden sets
- distributed federation replay fixtures
- red-team security fixture families
- performance benchmark corpora

---

## 23. Normative Implementation Summary

An implementation that supports the AASL machine-readable companion asset ecosystem SHALL:

1. parse and validate canonical JSON schema assets.
2. consume official sample `.aas` documents.
3. decode official `.aasb` fixtures where the claimed profile includes binary support.
4. recognize and preserve canonical error codes.
5. execute suites according to machine-readable conformance manifests.
6. compare outputs against golden corpora without hidden mutation.
7. declare the pack version, schema version, and supported profiles used during execution.

An implementation that fails any of the above SHALL NOT claim full companion-pack conformance for the relevant certification tier.

---

## 24. Canonical Output Naming Recommendation

The recommended filename for the full machine-readable asset specification is:

```text
Atrahasis_AASL_Machine_Readable_Companion_Assets_Pack.md
```

This document is the canonical human-readable specification for the machine-readable companion layer and is intended to sit alongside the broader AASL specification family.

---

## 25. Closing Statement

The AASL machine-readable companion asset layer converts the language from a prose-defined standard into an executable ecosystem. Without schemas, fixtures, error registries, conformance manifests, and golden corpora, interoperability claims remain soft and difficult to verify. With them, AASL becomes implementable, testable, certifiable, automatable, and governable across independent runtimes and toolchains.

The companion pack therefore serves as the bridge between specification intent and production-grade implementation reality.
