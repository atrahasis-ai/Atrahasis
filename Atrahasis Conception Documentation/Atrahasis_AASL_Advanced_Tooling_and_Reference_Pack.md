# Atrahasis AASL Advanced Tooling and Reference Pack
## Canonical Extended Documentation Set for the Agentic Application Specification Language (AASL)

**Document ID:** ATRAHASIS-AASL-EXT-001  
**Status:** Canonical Extended Specification  
**Version:** 1.0.0  
**Scope:** Extended operational, tooling, encoding, grammar, error, conformance, proposal, and runtime reference documentation for AASL  
**Parent Documents:**
- `Atrahasis_AASL_Parser_Architecture.md`
- `Atrahasis_AASL_Runtime_Model.md`
- `Atrahasis_AASC_Compiler_Architecture.md`
- `Atrahasis_AASL_Validator_Architecture.md`
- `Atrahasis_AASL_Query_Engine_Specification.md`
- `Atrahasis_AASL_File_Infrastructure_Specification.md`
- `Atrahasis_AASL_Developer_Tooling_Specification.md`
- `Atrahasis_AASL_Conversion_Pipeline_Specification.md`
- `Atrahasis_AASL_Ontology_Registry_and_Governance_Operations.md`
- `Atrahasis_AASL_Conformance_and_Certification_Framework.md`

---

# Table of Contents

1. Purpose and Positioning  
2. AASL CLI Command Reference  
3. AASL Formatter Specification  
4. VS Code Extension Design  
5. `.aasb` Binary Encoding Specification  
6. Query Language Grammar Appendix  
7. Official Error Code Catalog  
8. Certification Test Catalog and Test Vectors Pack  
9. Ontology Proposal Template Pack  
10. Implementation Reference Profiles for Different Runtimes  
11. Cross-Subsystem Compatibility Rules  
12. Security, Trust, and Supply Chain Controls  
13. Release and Versioning Policy for Extended Tooling  
14. Acceptance Criteria  
15. Appendices  

---

# 1. Purpose and Positioning

This document consolidates the principal second-order documentation required to operationalize AASL as a mature language ecosystem rather than only a core specification. The base AASL documents define the language, parser, validator, compiler, file infrastructure, runtime model, governance, and conformance architecture. This extended pack defines the major operational artifacts needed by implementers, tool builders, certifiers, runtime maintainers, ontology stewards, extension authors, IDE integrators, and downstream product teams.

This document is intentionally comprehensive. It merges nine advanced subdomains that would otherwise exist as separate deep-reference documents. It is designed for use as:

- a canonical engineering reference for implementation teams,
- a direct prompt/context document for code-generation agents,
- a policy reference for ecosystem maintainers,
- a practical field guide for runtime integrators,
- and a stable operational contract for compatibility across tools.

## 1.1 Included Subdomains

This document includes the following domains in a single canonical artifact:

- AASL CLI command reference
- AASL formatter specification
- VS Code extension design
- `.aasb` binary encoding specification
- query language grammar appendix
- official error code catalog
- certification test catalog and test vectors pack
- ontology proposal template pack
- implementation reference profiles for different runtimes

## 1.2 Non-Goals

This document does not replace the base language specification, parser architecture, runtime model, or validator architecture. Instead, it extends them and binds them into operational form.

## 1.3 Normative Language

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL are to be interpreted as normative requirement levels.

---

# 2. AASL CLI Command Reference

## 2.1 Overview

The AASL CLI is the canonical command-line interface for authoring, validating, formatting, querying, compiling, packaging, certifying, diffing, migrating, and inspecting AASL artifacts. The CLI MUST be usable by:

- human developers,
- CI/CD systems,
- offline validators,
- code generation agents,
- batch conversion pipelines,
- IDE integrations,
- and certification runners.

The CLI MUST support deterministic output, machine-readable error emission, strict exit codes, structured logs, and profile-based execution.

## 2.2 CLI Design Principles

The CLI SHALL be:

- deterministic for identical inputs and flags,
- scriptable without interactive requirements,
- safe for CI automation,
- explicit in destructive operations,
- profile-aware,
- version-reporting,
- forward-compatible through capability negotiation,
- and composable in pipelines.

## 2.3 Executable Names

Accepted canonical executable names:

- `aasl`
- `aasl-cli`

Preferred canonical executable name:

- `aasl`

## 2.4 Global Syntax

```text
Command:
  aasl <command> [subcommand] [arguments] [flags]

Global form:
  aasl [--version] [--help] [--profile <name>] [--format <json|yaml|text>] [--quiet] [--verbose] [--color <auto|always|never>]
```

## 2.5 Global Flags

| Flag | Meaning | Required Behavior |
|---|---|---|
| `--help` | Show help | MUST print scoped help and exit 0 |
| `--version` | Show version | MUST print CLI version, spec compatibility, formatter version, profile support |
| `--profile <name>` | Runtime/validation profile | MUST constrain behavior to selected reference profile |
| `--format <json|yaml|text>` | Output encoding | MUST affect non-file command output only |
| `--quiet` | Suppress non-essential output | MUST still emit errors |
| `--verbose` | Expand output | SHOULD include phase timing and diagnostics |
| `--color <auto|always|never>` | Terminal color handling | MUST NOT affect semantic output |
| `--cwd <path>` | Override working directory | MUST apply to relative path resolution |
| `--config <path>` | Explicit config file | MUST override default discovery |
| `--no-config` | Ignore discovered config | MUST disable implicit config loading |
| `--trace` | Emit trace identifiers | SHOULD be machine-parseable |
| `--timing` | Emit phase timing | SHOULD show per-stage durations |
| `--fail-fast` | Stop on first hard error | MUST exit immediately on first fatal condition |
| `--strict` | Enable strict mode | MUST elevate warnings according to active profile |
|

## 2.6 Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Generic failure |
| 2 | CLI usage error |
| 3 | Input file not found or unreadable |
| 4 | Parse failure |
| 5 | Validation failure |
| 6 | Compile failure |
| 7 | Query failure |
| 8 | Formatting changed file with `--check` |
| 9 | Serialization or encoding failure |
| 10 | Profile incompatibility |
| 11 | Certification failure |
| 12 | Governance or ontology resolution failure |
| 13 | Security policy violation |
| 14 | Internal implementation error |
| 15 | Unsupported feature or capability mismatch |
|

## 2.7 Command Families

### 2.7.1 `init`
Create new AASL workspaces, packages, modules, example docs, and starter configs.

```text
aasl init workspace <path>
aasl init module <path>
aasl init document <path>
aasl init ontology <path>
aasl init profile <path>
```

Required behavior:

- MUST generate deterministic starter artifacts.
- MUST support `--template <name>`.
- MUST support `--force` for overwrites.
- SHOULD generate comments and examples when requested.
- MUST record schema/version headers where required.

Common flags:

- `--template <minimal|standard|federated|governed|runtime-pack>`
- `--name <name>`
- `--namespace <namespace>`
- `--force`
- `--with-examples`

### 2.7.2 `validate`
Validate one or more `.aas` or `.aasb` artifacts.

```text
aasl validate <path...>
aasl validate <path> --recursive
aasl validate <path> --profile edge-lite
aasl validate <path> --report report.json
```

Required behavior:

- MUST perform parse + semantic validation unless `--syntax-only` is set.
- MUST support validation against specific profile versions.
- MUST emit structured diagnostics.
- MUST support batch mode.
- MUST support deterministic report emission.

Flags:

- `--syntax-only`
- `--semantic-only`
- `--recursive`
- `--report <path>`
- `--max-errors <n>`
- `--warnings-as-errors`
- `--explain <code>`
- `--fix` for safe machine-applicable repairs only

### 2.7.3 `format`
Format `.aas` documents and optionally check style compliance.

```text
aasl format <path...>
aasl format <path> --check
aasl format <path> --write
aasl format <path> --diff
```

Required behavior:

- MUST use the canonical formatter rules in Section 3.
- MUST support read-only check mode.
- MUST preserve semantics exactly.
- MUST preserve trivia only where defined by formatter contracts.

Flags:

- `--check`
- `--write`
- `--stdin`
- `--stdout`
- `--diff`
- `--line-width <n>`
- `--normalize-eol <lf|crlf|preserve>`
- `--idempotence-check`

### 2.7.4 `compile`
Compile external source material into AASL or transform across internal targets.

```text
aasl compile markdown input.md -o output.aas
aasl compile json input.json -o output.aas
aasl compile dataset manifest.yaml -o corpus/
aasl compile reverse input.aas -o output.md
```

Required behavior:

- MUST invoke AASC-compatible compile pipelines.
- MUST produce provenance traces.
- MUST support ambiguity reports.
- SHOULD support batch compilation.

### 2.7.5 `query`
Execute AASL query language statements.

```text
aasl query -f graph.aas 'select agent where role = "planner"'
aasl query -f corpus/ --script find_agents.aq
aasl query shell -f workspace/
```

Required behavior:

- MUST support single query mode and script mode.
- MUST support REPL/shell mode.
- MUST support profile-aware query capability negotiation.
- MUST support structured result serialization.

Flags:

- `-f, --from <path>`
- `--script <path>`
- `--params <json>`
- `--limit <n>`
- `--timeout-ms <n>`
- `--explain-plan`
- `--analyze`
- `--output <path>`

### 2.7.6 `inspect`
Inspect parser trees, runtime graphs, ontology bindings, and metadata.

```text
aasl inspect ast file.aas
aasl inspect cst file.aas
aasl inspect graph file.aas
aasl inspect symbols file.aas
aasl inspect imports file.aas
aasl inspect ids file.aas
```

Required behavior:

- MUST support JSON export for all inspection forms.
- SHOULD support line/span location output.
- SHOULD support filtering by node type or object id.

### 2.7.7 `pack`
Package collections of documents, ontologies, assets, and manifests.

```text
aasl pack create workspace/ -o bundle.aaspkg
aasl pack verify bundle.aaspkg
aasl pack extract bundle.aaspkg -o out/
```

Package support requirements:

- MUST support signed package manifests.
- MUST support deterministic packaging order.
- MUST support manifest hashing.
- SHOULD support embedded `.aasb` payloads.

### 2.7.8 `diff`
Compute semantic or textual differences.

```text
aasl diff old.aas new.aas
aasl diff old.aas new.aas --semantic
aasl diff old.aas new.aas --ids-only
```

Required behavior:

- MUST support textual diff.
- MUST support semantic diff.
- MUST distinguish reformat-only changes from semantic changes.
- SHOULD produce patch-classification summaries.

### 2.7.9 `migrate`
Upgrade documents to newer schema/profile versions.

```text
aasl migrate input.aas --to 1.2.0 -o output.aas
aasl migrate workspace/ --profile server-strict-v2
```

Required behavior:

- MUST preserve semantics where migration rules define safe upgrade.
- MUST emit transformation logs.
- MUST refuse unsafe destructive migrations without `--allow-breaking`.

### 2.7.10 `certify`
Run conformance and certification suites.

```text
aasl certify validate-impl ./impl-config.yaml
aasl certify run-suite core-parser
aasl certify run-suite profile-edge-lite
```

Required behavior:

- MUST execute official certification catalogs.
- MUST generate signed reports when configured.
- MUST capture runtime profile, version, host metadata, and capability matrix.

### 2.7.11 `ontology`
Manage ontology proposals, registries, namespaces, and compatibility checks.

```text
aasl ontology validate-proposal proposal.yaml
aasl ontology render-template --type class
aasl ontology diff old.yaml new.yaml
aasl ontology check-compat ontology.yaml
```

### 2.7.12 `errors`
Lookup official errors and remediation guidance.

```text
aasl errors explain AASL-VAL-0031
aasl errors search import cycle
aasl errors emit-catalog --format json
```

### 2.7.13 `capabilities`
Inspect tool and runtime capabilities.

```text
aasl capabilities local
aasl capabilities runtime http://runtime:8080
aasl capabilities formatter
aasl capabilities profile server-strict-v2
```

### 2.7.14 `doctor`
Health-check a workspace.

```text
aasl doctor
aasl doctor workspace/
aasl doctor --fix-safe
```

The doctor command SHOULD verify:

- installed toolchain consistency,
- formatter version mismatch,
- spec/profile mismatch,
- missing ontology references,
- stale cache state,
- inconsistent line endings,
- broken imports,
- certification state,
- and known runtime incompatibilities.

## 2.8 Config File Conventions

Canonical config files MAY be discovered in this order:

- `aasl.toml`
- `aasl.yaml`
- `aasl.json`
- workspace `.aasl/config.toml`

Config domains MAY include:

- formatter settings,
- validation profile,
- ontology registry source,
- query defaults,
- certification suites,
- binary encoding settings,
- editor integration hints,
- package signing settings.

## 2.9 Machine Output Contract

All machine outputs MUST include:

- `tool`
- `version`
- `spec_version`
- `profile`
- `command`
- `status`
- `timestamp`
- `results`
- `diagnostics`
- `trace_id` when tracing is enabled

---

# 3. AASL Formatter Specification

## 3.1 Overview

The AASL formatter is the canonical normalization engine for `.aas` textual documents. Its purpose is to ensure that semantically equivalent documents converge to a standard layout, minimizing diff noise and authoring inconsistency.

The formatter MUST be:

- semantics-preserving,
- idempotent,
- deterministic,
- stable across platforms,
- Unicode-safe in parsing but ASCII-conscious in canonical emission where required by profile,
- and tightly aligned with parser span semantics.

## 3.2 Primary Goals

The formatter SHALL:

- normalize whitespace,
- normalize indentation,
- normalize line wrapping,
- normalize block ordering where explicitly permitted,
- preserve comments according to attachment rules,
- preserve exact tokens where values are semantically token-sensitive,
- and emit stable output across versions unless a major formatter revision changes canonical style.

## 3.3 Non-Goals

The formatter SHALL NOT:

- repair semantic errors not marked safe-fixable,
- rewrite ontology meaning,
- rename identifiers unless a dedicated migration mode is enabled,
- or reorder content whose order is semantically meaningful.

## 3.4 Formatting Pipeline

Canonical formatter pipeline:

1. Parse input into CST.
2. Attach comments and trivia to stable anchors.
3. Convert CST to formatting IR.
4. Apply canonical layout rules.
5. Emit text document.
6. Re-parse emitted document.
7. Verify semantic equivalence.
8. Optionally verify byte-stable idempotence on second pass.

If semantic equivalence fails, the formatter MUST abort and emit a fatal internal formatter error.

## 3.5 Formatting Domains

### 3.5.1 Whitespace

- Tabs MUST NOT be used for indentation in canonical output.
- Indentation width MUST default to 2 spaces unless profile overrides to 4.
- Trailing whitespace MUST be removed.
- Multiple blank lines MUST be collapsed according to block rules.
- Final newline MUST be present.

### 3.5.2 Line Endings

Canonical emission SHOULD default to LF.

Modes:

- `lf`
- `crlf`
- `preserve`

### 3.5.3 Comments

Comment classes:

- line comments
- block comments
- doc comments
- detached header comments

Attachment rules:

- Leading comments attach to nearest following syntactic anchor unless separated by two or more blank lines.
- Trailing comments attach to prior same-line construct.
- Detached comments MUST remain detached if they describe file-level intent.

### 3.5.4 Key-Value Alignment

The formatter MUST NOT align values into visual columns unless the canonical style for a construct explicitly permits that. Visual alignment tends to create unstable diffs.

### 3.5.5 Collections

Lists MAY be emitted inline if:

- item count is small,
- combined width fits within line limit,
- and no item contains multiline content.

Otherwise, lists MUST be multiline with one item per line.

### 3.5.6 Block Ordering

The formatter MAY reorder constructs only if the relevant AASL construct explicitly declares order-insensitive semantics and canonical ordering rules exist.

Permitted canonical ordering domains MAY include:

- import blocks,
- annotation maps,
- attribute maps,
- capability lists,
- metadata headers,
- test vector maps.

Order MUST remain unchanged for:

- imperative action sequences,
- dependency resolution sequences if order-significant,
- authored examples,
- any explicitly ordered graph fragments.

## 3.6 Canonical Layout Rules

### 3.6.1 Header Layout

Canonical file header order SHOULD be:

1. version/header directive
2. module/package declaration
3. imports
4. ontology bindings
5. top-level declarations
6. tests/examples if embedded

### 3.6.2 Imports

Imports MUST be grouped by class and sorted lexicographically within group.

Suggested groups:

- core/system imports
- ontology imports
- local module imports
- external package imports

A blank line SHOULD separate groups.

### 3.6.3 Maps and Objects

Maps SHOULD be multiline if they exceed line width or contain nested structures.

Example canonical style:

```text
agent Planner {
  role: "planner"
  capabilities: ["decompose", "schedule", "route"]
  constraints: {
    maxRetries: 3
    timeoutMs: 1500
  }
}
```

### 3.6.4 String Handling

- Prefer double quotes for standard strings.
- Preserve block string form when multiline semantics matter.
- Escape sequences MUST be normalized.
- Equivalent Unicode escapes SHOULD be normalized to canonical representation per profile.

### 3.6.5 Numeric Handling

The formatter MUST preserve numeric value semantics exactly.

Rules:

- Remove redundant leading zeros unless value class requires them.
- Normalize exponent case if allowed.
- Preserve fixed precision only if precision is semantically meaningful.
- Hex/binary forms MAY be normalized only if semantics permit.

## 3.7 Formatter Safety Guarantees

The formatter MUST guarantee:

- parse-after-format success,
- semantic equivalence,
- reference stability,
- comment preservation according to attachment rules,
- no hidden state dependency,
- deterministic output under same formatter version/profile.

## 3.8 Formatter Modes

Supported modes SHOULD include:

- canonical write mode
- check mode
- diff mode
- minimal-change mode
- import-sort-only mode
- comment-normalize mode
- migration-aware formatting mode

## 3.9 Formatter Versioning

Formatter versions MUST be separately versioned from CLI versions. A formatter major version bump indicates potential canonical layout changes that may alter textual output while preserving semantics.

## 3.10 Formatter Acceptance Tests

The formatter MUST pass:

- idempotence suite,
- comment stability suite,
- semantic preservation suite,
- mixed line ending suite,
- wide Unicode text suite,
- malformed input refusal suite,
- profile-specific style suite.

---

# 4. VS Code Extension Design

## 4.1 Purpose

The VS Code extension is the reference IDE integration for AASL authoring. It MUST provide first-class authoring support for `.aas`, `.aasb` manifests, query scripts, ontology proposals, and certification packs.

## 4.2 Functional Goals

The extension SHOULD support:

- syntax highlighting,
- semantic tokenization,
- parser-aware diagnostics,
- formatter integration,
- hover documentation,
- go-to-definition,
- find references,
- document symbols,
- workspace symbol search,
- query execution,
- graph/object explorer integration,
- ontology proposal authoring tools,
- certification test runner hooks,
- profile-aware warnings,
- and live conformance overlays.

## 4.3 Architecture Overview

The extension SHOULD be split into the following components:

1. Language client
2. Language server protocol (LSP) server
3. CLI bridge
4. Query runner integration
5. Graph/object explorer webviews
6. Certification/test explorer integration
7. Ontology template wizard
8. Binary inspector helpers for `.aasb`

## 4.4 Language Server Responsibilities

The LSP server MUST provide:

- parse diagnostics,
- semantic validation diagnostics,
- code actions,
- completion,
- hover,
- definitions,
- references,
- document formatting,
- range formatting where supported,
- rename provider for safe identifiers,
- document links,
- document symbols,
- semantic tokens,
- workspace indexing,
- inlay hints,
- folding ranges,
- and custom AASL capability negotiation.

## 4.5 Extension Features

### 4.5.1 Syntax Highlighting

The extension MUST distinguish:

- keywords,
- type names,
- ontology symbols,
- identifiers,
- strings,
- numbers,
- comments,
- annotations,
- import declarations,
- query keywords,
- diagnostics overlays.

### 4.5.2 Semantic Validation

The extension SHOULD support live validation modes:

- on type,
- on save,
- manual only,
- profile-specific background validation.

### 4.5.3 Hover Cards

Hover cards SHOULD display:

- declaration summary,
- resolved ontology meaning,
- profile constraints,
- documentation snippet,
- source module,
- compatibility notes,
- deprecation state,
- related certification expectations.

### 4.5.4 IntelliSense and Completion

Completion SHOULD support:

- language keywords,
- available construct templates,
- ontology classes/properties,
- imported module symbols,
- query functions,
- error code identifiers,
- profile names,
- certification suite names.

### 4.5.5 Code Actions

Code actions MAY include:

- safe autofix for formatter issues,
- add missing imports,
- expand shorthand forms,
- convert inline structure to block form,
- rename deprecated ontology symbol,
- generate proposal template,
- create missing test skeleton,
- insert profile header,
- resolve safe validation repair.

### 4.5.6 Explorer Views

Custom side panel views SHOULD include:

- AASL Symbols
- Runtime Graph
- Ontology Registry Browser
- Diagnostics by Severity
- Certification Tests
- Query History
- Binary Package Inspector

### 4.5.7 Query Integration

The extension SHOULD include:

- query editor mode,
- execute selected query,
- result preview table/tree,
- execution plan display,
- parameterized query forms,
- profile-aware query linting.

### 4.5.8 `.aasb` Support

The extension SHOULD support:

- binary metadata inspection,
- package tree visualization,
- decode-to-text preview,
- hash/signature verification status,
- payload manifest browsing.

## 4.6 Configuration Settings

Illustrative settings:

```json
{
  "aasl.validation.mode": "onSave",
  "aasl.profile": "server-strict-v2",
  "aasl.formatter.lineWidth": 100,
  "aasl.query.timeoutMs": 5000,
  "aasl.binary.preview.enabled": true,
  "aasl.certification.autoDiscover": true,
  "aasl.ontology.registrySource": "workspace"
}
```

## 4.7 Performance Constraints

The extension SHOULD remain responsive for:

- files under 5 MB with near-real-time diagnostics,
- workspaces with 10k+ AASL symbols,
- large ontology registries with indexed lookup,
- background validation with cancellation support.

## 4.8 Security Requirements

The extension MUST:

- avoid arbitrary code execution in workspaces,
- validate external tool invocation paths,
- sandbox preview renderers where possible,
- clearly separate trusted and untrusted workspace modes,
- and require explicit enablement for network-backed registry fetches.

## 4.9 Extension Packaging

The extension SHOULD ship as:

- stable channel,
- insiders channel,
- offline-compatible enterprise build,
- reproducible package build with signed release artifacts.

---

# 5. `.aasb` Binary Encoding Specification

## 5.1 Purpose

`.aasb` is the canonical binary representation for AASL documents, bundles, and pre-indexed runtime packages where textual `.aas` is insufficient for distribution efficiency, runtime startup speed, integrity verification, or transport constraints.

## 5.2 Goals

The `.aasb` format SHALL support:

- compact storage,
- fast decoding,
- deterministic serialization,
- streaming decode where feasible,
- strong integrity verification,
- optional signatures,
- embedded indexes,
- capability/profile metadata,
- efficient random access to sections,
- and compatibility with signed packages.

## 5.3 Non-Goals

`.aasb` SHALL NOT be designed as a general arbitrary-object binary container. It exists specifically to encode AASL structures, indexes, manifests, and related artifacts under AASL rules.

## 5.4 File Signature

Each `.aasb` file MUST begin with a magic header and version declaration.

Illustrative layout:

```text
Bytes 0-3   Magic: AASB
Bytes 4-5   Major version
Bytes 6-7   Minor version
Bytes 8-15  Flags and reserved fields
```

## 5.5 Endianness

Canonical binary encoding MUST use little-endian integer encoding unless a future major version specifies otherwise.

## 5.6 High-Level Container Layout

Illustrative section order:

1. Header
2. Capability/profile block
3. Section directory
4. String table
5. Symbol table
6. Ontology table
7. Object graph section
8. Query index section
9. Source map section
10. Integrity section
11. Signature section
12. Optional extension sections

## 5.7 Section Directory

The section directory MUST include for each section:

- section id
- byte offset
- byte length
- compression type
- checksum/hash
- flags
- dependency info where relevant

## 5.8 Core Data Sections

### 5.8.1 String Table

The string table SHOULD deduplicate repeated strings. It MUST provide indexed access for:

- identifiers,
- ontology IRIs,
- symbol names,
- property keys,
- string literals where deduplication is appropriate.

### 5.8.2 Symbol Table

The symbol table MUST map symbol IDs to declaration metadata.

Minimum fields:

- symbol id
- kind
- name string index
- namespace index
- defining section reference
- span/source reference if present
- flags (exported, deprecated, internal, experimental)

### 5.8.3 Ontology Table

The ontology table MUST encode imported ontology references and local bindings.

### 5.8.4 Object Graph Section

The object graph section MUST encode runtime-semantic objects, not merely parse trees. The encoding SHOULD be structured to minimize decode overhead for common runtime queries.

### 5.8.5 Query Index Section

This section MAY precompute indexes used by query engines, including:

- type/class postings,
- attribute key maps,
- id maps,
- relation adjacency lists,
- path lookups,
- and optional text search side indexes.

### 5.8.6 Source Map Section

If present, this section maps binary structures back to textual spans, line numbers, and source files.

### 5.8.7 Integrity Section

The integrity section MUST include hash trees or equivalent digest structures sufficient to verify file integrity and, optionally, section-level tampering.

## 5.9 Encoding Rules

### 5.9.1 Canonical Serialization

Equivalent semantic content MUST serialize identically under the same `.aasb` version, profile, and serialization mode.

### 5.9.2 Numeric Encoding

- fixed-width ints for schema-critical fields,
- varints MAY be used for repeated compact indexes,
- floating-point values MUST define exact allowed encoding classes,
- NaN canonicalization MUST be specified if floats are permitted.

### 5.9.3 Nullability and Optional Fields

Optional fields MUST use explicit presence markers or tagged field encoding.

### 5.9.4 Tagged Schema Evolution

The binary format SHOULD support forward-compatible tagged sections/fields so readers can safely skip unknown optional sections.

## 5.10 Compression

Compression MAY be applied per section.

Supported modes SHOULD include:

- none
- zstd
- lz4

Readers MUST reject unsupported required compression methods.

## 5.11 Integrity and Signature Model

Integrity layers:

1. section checksum
2. file digest
3. optional manifest digest
4. optional detached or embedded signature

Signature metadata SHOULD include:

- signing algorithm
- signer id
- signature scope
- signing timestamp
- certificate chain or key reference

## 5.12 Streaming and Partial Read

Readers SHOULD support partial reads for:

- header only,
- section directory only,
- graph-only loads,
- query-index-only loads,
- manifest verification without full decode.

## 5.13 Text/Binary Equivalence Contract

Where `.aas` and `.aasb` represent the same artifact:

- semantic equivalence MUST hold,
- object identity mapping MUST hold,
- profile compatibility MUST hold,
- source map SHOULD be preserved where round-trip traceability is required.

## 5.14 `.aasb` Modes

Recommended modes:

- `doc` single document binary
- `bundle` multi-document package
- `runtime` pre-indexed runtime package
- `cert` certification pack
- `ontology` ontology distribution package

## 5.15 Reader Requirements

A compliant reader MUST:

- verify magic/version,
- verify required sections,
- reject malformed section references,
- validate integrity data when required,
- expose capability/profile metadata,
- and fail safely on unsupported critical extensions.

## 5.16 Writer Requirements

A compliant writer MUST:

- emit canonical section ordering,
- canonicalize serialization,
- write correct offsets and lengths,
- generate integrity metadata,
- optionally emit source maps,
- and declare profile constraints.

## 5.17 Binary Conformance Tests

`.aasb` conformance MUST include:

- round-trip equivalence tests,
- malformed header tests,
- section overlap tests,
- unsupported compression tests,
- hash mismatch tests,
- partial read tests,
- extension skipping tests,
- random mutation rejection tests.

---

# 6. Query Language Grammar Appendix

## 6.1 Purpose

This appendix provides a deeper quasi-formal grammar reference for the AASL query language. It supplements the main query engine specification by providing grammar-oriented implementation guidance.

## 6.2 Design Goals

The query language SHALL be:

- readable by humans,
- easy for agents to generate,
- deterministic to parse,
- composable,
- expressive enough for graph and object traversal,
- profile-constrainable,
- and statically lintable.

## 6.3 Query Model

Primary query families:

- selection queries
- projection queries
- path traversal queries
- pattern match queries
- aggregation queries
- mutation queries if enabled by runtime profile
- explain-plan queries
- schema/metadata inspection queries

## 6.4 Lexical Elements

Tokens SHOULD include:

- identifiers
- qualified names
- string literals
- numeric literals
- booleans
- null
- keywords
- punctuation
- comparison operators
- logical operators
- path operators
- wildcard operators
- parameter markers

## 6.5 Illustrative EBNF

The following grammar is illustrative and intended as an implementation appendix, not the sole normative semantic source.

```ebnf
query            = statement , { ";" , statement } ;

statement        = selectStmt
                 | inspectStmt
                 | explainStmt
                 | aggregateStmt
                 | letStmt ;

selectStmt       = "select" , selectTarget , fromClause? , whereClause? , orderClause? , limitClause? ;
selectTarget     = "*" | projectionList | typeSelector ;
projectionList   = projectionItem , { "," , projectionItem } ;
projectionItem   = identifier | pathExpr | functionCall | aliasExpr ;
aliasExpr        = ( identifier | pathExpr | functionCall ) , "as" , identifier ;

typeSelector     = identifier | qualifiedName ;
fromClause       = "from" , sourceExpr ;
sourceExpr       = identifier | stringLiteral | pathExpr | functionCall ;
whereClause      = "where" , expr ;
orderClause      = "order" , "by" , orderItem , { "," , orderItem } ;
orderItem        = pathExpr , ( "asc" | "desc" )? ;
limitClause      = "limit" , integerLiteral ;

inspectStmt      = "inspect" , inspectTarget , fromClause? , whereClause? ;
inspectTarget    = "schema" | "symbols" | "imports" | "ids" | "types" | "plan" ;

explainStmt      = "explain" , statement ;

aggregateStmt    = "aggregate" , aggregationList , fromClause? , whereClause? , groupClause? ;
aggregationList  = aggregationItem , { "," , aggregationItem } ;
aggregationItem  = functionCall , ( "as" , identifier )? ;
groupClause      = "group" , "by" , pathExpr , { "," , pathExpr } ;

letStmt          = "let" , identifier , "=" , expr ;

expr             = orExpr ;
orExpr           = andExpr , { "or" , andExpr } ;
andExpr          = unaryExpr , { "and" , unaryExpr } ;
unaryExpr        = [ "not" ] , comparisonExpr ;
comparisonExpr   = additiveExpr , [ compOp , additiveExpr ] ;
compOp           = "=" | "!=" | ">" | ">=" | "<" | "<=" | "in" | "matches" | "contains" ;

additiveExpr     = multiplicativeExpr , { ( "+" | "-" ) , multiplicativeExpr } ;
multiplicativeExpr = pathPrimary , { ( "*" | "/" | "%" ) , pathPrimary } ;

pathPrimary      = atom , { pathSuffix } ;
pathSuffix       = "." , identifier
                 | "[" , expr , "]"
                 | "->" , identifier
                 | "?" ;

atom             = identifier
                 | qualifiedName
                 | literal
                 | functionCall
                 | parameterRef
                 | "(" , expr , ")" ;

functionCall     = identifier , "(" , [ argumentList ] , ")" ;
argumentList     = expr , { "," , expr } ;
parameterRef     = "$" , identifier ;
qualifiedName    = identifier , { "::" , identifier } ;
literal          = stringLiteral | integerLiteral | floatLiteral | booleanLiteral | "null" ;
```

## 6.6 Semantic Constraints

In addition to grammar validity, compliant query implementations MUST enforce semantic constraints such as:

- referenced symbols must resolve,
- functions must exist in active profile,
- mutation forms must be disabled unless runtime profile permits,
- aggregations must operate on valid value domains,
- path traversal must respect type/object model semantics,
- ambiguity must be surfaced clearly where name resolution is non-unique.

## 6.7 Standard Functions

Illustrative standard function families:

- `count()`
- `sum()`
- `avg()`
- `min()`
- `max()`
- `exists()`
- `typeOf()`
- `idOf()`
- `resolve()`
- `path()`
- `depth()`
- `neighbors()`
- `hasCapability()`
- `matchesProfile()`

## 6.8 Explain Plan Grammar

The query engine SHOULD support:

```text
explain select agent from workspace where capability contains "route"
```

`explain` output SHOULD include:

- parsed AST
- normalized query
- resolution steps
- index usage
- plan nodes
- estimated cardinality
- cost notes
- warnings

## 6.9 Query Profiles

Profiles MAY limit:

- supported functions,
- maximum traversal depth,
- recursion support,
- regex support,
- mutation support,
- user-defined functions,
- text-search support,
- timeout ranges.

## 6.10 Query Lint Rules

Query lint rules SHOULD detect:

- unused `let` bindings,
- always-true predicates,
- impossible predicates,
- unindexed expensive scans,
- deprecated functions,
- unbounded traversal in strict profiles,
- ambiguity in dotted paths.

---

# 7. Official Error Code Catalog

## 7.1 Purpose

This section defines the official AASL ecosystem error taxonomy. Every compliant parser, validator, formatter, CLI, query engine, binary reader/writer, and certification runner SHOULD map internal failures into these stable codes where applicable.

## 7.2 Error Code Structure

Canonical format:

```text
AASL-<DOMAIN>-<NNNN>
```

Where domain is one of:

- `LEX` lexical/parsing-front-end token issues
- `PAR` parse grammar issues
- `VAL` semantic validation issues
- `FMT` formatter issues
- `CMP` compiler issues
- `QRY` query issues
- `BIN` binary encoding issues
- `ONT` ontology/governance issues
- `CFG` configuration issues
- `CER` certification issues
- `SEC` security issues
- `RT` runtime issues
- `CLI` CLI usage/system issues
- `INT` internal implementation errors

## 7.3 Error Record Shape

Each emitted error SHOULD include:

- code
- title
- severity
- domain
- summary
- explanation
- likely causes
- safe remediation guidance
- source span if applicable
- profile context if applicable
- trace id if enabled

## 7.4 Severity Classes

- `fatal`
- `error`
- `warning`
- `info`
- `hint`

## 7.5 Catalog

### 7.5.1 Lexical Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-LEX-0001 | Invalid Character | error | Input contains a character disallowed by active lexical mode |
| AASL-LEX-0002 | Unterminated String | error | String literal not closed |
| AASL-LEX-0003 | Invalid Escape Sequence | error | Unsupported or malformed escape |
| AASL-LEX-0004 | Invalid Numeric Literal | error | Numeric token malformed |
| AASL-LEX-0005 | Invalid Unicode Escape | error | Unicode escape malformed or incomplete |
| AASL-LEX-0006 | Illegal Control Character | error | Forbidden raw control character encountered |
| AASL-LEX-0007 | Unexpected Byte Order Mark | warning | BOM present where profile discourages it |
| AASL-LEX-0008 | Comment Not Closed | error | Block comment unterminated |

### 7.5.2 Parse Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-PAR-0001 | Unexpected Token | error | Parser encountered an unexpected token |
| AASL-PAR-0002 | Missing Required Token | error | Required syntactic element missing |
| AASL-PAR-0003 | Invalid Declaration Form | error | Declaration shape invalid |
| AASL-PAR-0004 | Unbalanced Delimiter | error | Braces/brackets/parentheses mismatched |
| AASL-PAR-0005 | Duplicate Header Directive | error | Header directive repeated illegally |
| AASL-PAR-0006 | Invalid Import Syntax | error | Import clause malformed |
| AASL-PAR-0007 | Ambiguous Parse Form | error | Construct cannot be parsed unambiguously under grammar |
| AASL-PAR-0008 | Recovery Inserted Token | warning | Parser recovered by implicit insertion |
| AASL-PAR-0009 | Recovery Dropped Token | warning | Parser recovered by dropping token |

### 7.5.3 Validation Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-VAL-0001 | Unknown Symbol | error | Referenced symbol does not resolve |
| AASL-VAL-0002 | Duplicate Identifier | error | Identifier duplicated in forbidden scope |
| AASL-VAL-0003 | Type Mismatch | error | Value violates declared or inferred type |
| AASL-VAL-0004 | Missing Required Field | error | Required semantic field absent |
| AASL-VAL-0005 | Invalid Enum Value | error | Value outside permitted enumeration |
| AASL-VAL-0006 | Import Cycle | error | Import graph contains forbidden cycle |
| AASL-VAL-0007 | Incompatible Profile Feature | error | Construct unsupported by active profile |
| AASL-VAL-0008 | Deprecated Construct Used | warning | Deprecated feature referenced |
| AASL-VAL-0009 | Invalid Reference Target | error | Reference points to invalid target kind |
| AASL-VAL-0010 | Ontology Symbol Not Found | error | Ontology binding unresolved |
| AASL-VAL-0011 | Namespace Collision | error | Namespace mapping collides |
| AASL-VAL-0012 | Integrity Constraint Violation | error | Constraint rule violated |
| AASL-VAL-0013 | Conflicting Attribute Values | error | Mutually inconsistent values present |
| AASL-VAL-0014 | Unsupported Experimental Feature | error | Experimental construct disabled |
| AASL-VAL-0015 | Unsafe Migration Artifact | warning | Upgraded document contains unresolved migration marker |
| AASL-VAL-0016 | Invalid Capability Declaration | error | Capability declaration inconsistent or malformed |
| AASL-VAL-0017 | Unreachable Declaration | warning | Declaration cannot be reached/resolved |
| AASL-VAL-0018 | Non-Canonical Ordering | warning | Order violates canonical conventions |
| AASL-VAL-0019 | Duplicate Semantic Meaning | warning | Different declarations collapse to same semantic identity |
| AASL-VAL-0020 | Invalid Constraint Expression | error | Constraint expression cannot be evaluated |
| AASL-VAL-0021 | Unsafe Default Value | warning | Default value violates policy or profile guidance |
| AASL-VAL-0022 | Profile Header Missing | error | Profile-required header absent |
| AASL-VAL-0023 | Reserved Namespace Misuse | error | Reserved namespace used illegally |
| AASL-VAL-0024 | Version Compatibility Failure | error | Artifact incompatible with requested version target |
| AASL-VAL-0025 | Invalid Object Identity | error | Object identity malformed or unstable |
| AASL-VAL-0026 | Forbidden Side Effect Declaration | error | Side-effectful declaration prohibited in this profile |
| AASL-VAL-0027 | Query Capability Missing | error | Required query capability not supported |
| AASL-VAL-0028 | Binary/Text Equivalence Failure | error | `.aas` and `.aasb` representations diverge semantically |
| AASL-VAL-0029 | Source Map Inconsistency | warning | Source map entries inconsistent |
| AASL-VAL-0030 | Certification Metadata Missing | error | Required certification metadata absent |
| AASL-VAL-0031 | Unbound Proposal Placeholder | error | Template placeholder not resolved |
| AASL-VAL-0032 | Illegal Runtime Mutation | error | Mutation rule violated |
| AASL-VAL-0033 | Governance Policy Denial | error | Artifact rejected by governance policy |
| AASL-VAL-0034 | Invalid Signature Metadata | error | Signature metadata malformed or incomplete |
| AASL-VAL-0035 | Extension Capability Conflict | error | Extension requires conflicting capabilities |

### 7.5.4 Formatter Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-FMT-0001 | Non-Idempotent Format Result | fatal | Formatter output changes on second pass |
| AASL-FMT-0002 | Comment Attachment Failure | error | Formatter could not preserve comment anchors safely |
| AASL-FMT-0003 | Semantic Drift Detected | fatal | Reparse after format changed semantics |
| AASL-FMT-0004 | Unsupported Trivia Shape | warning | Trivia preserved imperfectly due to unsupported shape |
| AASL-FMT-0005 | Check Mode Would Rewrite | info | File differs from canonical formatting |

### 7.5.5 Compiler Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-CMP-0001 | Source Parse Failure | error | Source format could not be parsed |
| AASL-CMP-0002 | Ambiguous Source Mapping | warning | Multiple plausible semantic mappings |
| AASL-CMP-0003 | Unsupported Source Construct | error | Source construct cannot be represented |
| AASL-CMP-0004 | Provenance Trace Missing | warning | Compile path missing provenance detail |
| AASL-CMP-0005 | Reverse Rendering Loss | warning | Reverse transform loses representational detail |

### 7.5.6 Query Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-QRY-0001 | Query Parse Failure | error | Query text invalid |
| AASL-QRY-0002 | Unknown Function | error | Function unresolved |
| AASL-QRY-0003 | Invalid Path Traversal | error | Path traversal not valid for type |
| AASL-QRY-0004 | Timeout Exceeded | error | Query timed out |
| AASL-QRY-0005 | Resource Limit Exceeded | error | Query exceeded memory or traversal limits |
| AASL-QRY-0006 | Mutation Disabled | error | Query attempted mutation in read-only context |
| AASL-QRY-0007 | Parameter Missing | error | Required parameter not supplied |
| AASL-QRY-0008 | Plan Generation Failure | error | Engine failed to build execution plan |
| AASL-QRY-0009 | Unindexed Expensive Scan | warning | Query forces full scan |
| AASL-QRY-0010 | Result Serialization Failure | error | Query result could not be serialized |

### 7.5.7 Binary Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-BIN-0001 | Invalid Magic Header | error | `.aasb` magic bytes invalid |
| AASL-BIN-0002 | Unsupported Binary Version | error | Reader cannot parse version |
| AASL-BIN-0003 | Section Directory Corrupt | error | Directory invalid or inconsistent |
| AASL-BIN-0004 | Section Overlap Detected | error | Sections overlap illegally |
| AASL-BIN-0005 | Missing Required Section | error | Mandatory section absent |
| AASL-BIN-0006 | Integrity Hash Mismatch | error | Integrity check failed |
| AASL-BIN-0007 | Unsupported Compression | error | Required compression method unsupported |
| AASL-BIN-0008 | String Table Corrupt | error | String table malformed |
| AASL-BIN-0009 | Object Graph Decode Failure | error | Graph section invalid |
| AASL-BIN-0010 | Signature Verification Failure | error | Signature invalid or unverifiable |

### 7.5.8 Ontology Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-ONT-0001 | Proposal Schema Invalid | error | Proposal document malformed |
| AASL-ONT-0002 | Breaking Ontology Change | error | Proposal introduces incompatible change |
| AASL-ONT-0003 | Namespace Ownership Conflict | error | Proposal targets owned namespace illegally |
| AASL-ONT-0004 | Missing Compatibility Analysis | error | Required analysis not supplied |
| AASL-ONT-0005 | Missing Steward Approval | error | Required approver missing |
| AASL-ONT-0006 | Deprecation Window Violated | error | Removal before policy window end |
| AASL-ONT-0007 | Insufficient Example Coverage | warning | Proposal lacks usage examples |
| AASL-ONT-0008 | Undefined Semantics | error | Proposed term semantics incomplete |

### 7.5.9 Certification Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-CER-0001 | Suite Not Found | error | Requested certification suite unknown |
| AASL-CER-0002 | Test Vector Missing | error | Required vector not present |
| AASL-CER-0003 | Report Signature Invalid | error | Certification report signature invalid |
| AASL-CER-0004 | Coverage Threshold Not Met | error | Required coverage level not reached |
| AASL-CER-0005 | Determinism Failure | error | Repeated run produced different canonical results |
| AASL-CER-0006 | Baseline Mismatch | error | Runtime behavior differs from baseline expectation |

### 7.5.10 Security Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-SEC-0001 | Untrusted Registry Source | error | Registry source not trusted |
| AASL-SEC-0002 | Signature Required But Missing | error | Required signature absent |
| AASL-SEC-0003 | Dangerous Extension Blocked | error | Extension denied by security policy |
| AASL-SEC-0004 | Path Traversal Attempt | error | File system escape detected |
| AASL-SEC-0005 | Unsafe Workspace Trust State | warning | Workspace not trusted for requested action |

### 7.5.11 Runtime Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-RT-0001 | Runtime Initialization Failure | error | Runtime failed to initialize graph or state |
| AASL-RT-0002 | Object Resolution Failure | error | Runtime object cannot be resolved |
| AASL-RT-0003 | Transaction Conflict | error | Runtime mutation conflict |
| AASL-RT-0004 | Persistence Failure | error | Runtime could not persist state |
| AASL-RT-0005 | Profile Policy Denial | error | Runtime denied operation due to profile |

### 7.5.12 CLI/Internal Errors

| Code | Title | Severity | Meaning |
|---|---|---|---|
| AASL-CLI-0001 | Invalid Flag Combination | error | Flags incompatible |
| AASL-CLI-0002 | Command Requires Path | error | Required path missing |
| AASL-CLI-0003 | Config Load Failure | error | Config unreadable or invalid |
| AASL-INT-0001 | Unreachable Internal State | fatal | Internal invariant violated |
| AASL-INT-0002 | Panic Recovered | fatal | Tool recovered from panic but cannot continue safely |
| AASL-INT-0003 | Unexpected Null Internal Value | fatal | Required internal structure missing |

## 7.6 Remediation Standard

Every documented error SHOULD have a remediation block structured as:

- What happened
- Why it likely happened
- How to confirm
- Safe repair steps
- When auto-fix is appropriate
- Whether certification is affected

---

# 8. Certification Test Catalog and Test Vectors Pack

## 8.1 Purpose

This section defines the structure of the official certification test catalog and reusable test vector pack for AASL implementations.

## 8.2 Goals

The certification test catalog SHALL verify:

- syntactic correctness,
- semantic validation behavior,
- formatter determinism,
- binary/text equivalence,
- query behavior,
- ontology governance compliance,
- profile compliance,
- runtime determinism where required,
- and security rejection behavior.

## 8.3 Test Artifact Types

Test artifact classes:

- positive syntax vectors
- negative syntax vectors
- positive semantic vectors
- negative semantic vectors
- formatter golden files
- query input/expected output packs
- `.aasb` encode/decode vectors
- ontology proposal validation vectors
- CLI exit-code vectors
- certification report integrity vectors
- profile capability vectors
- fuzz regression packs

## 8.4 Test Catalog Structure

Illustrative structure:

```text
cert/
  catalog.yaml
  parser/
  validator/
  formatter/
  query/
  binary/
  ontology/
  cli/
  runtime/
  profiles/
  security/
```

## 8.5 Catalog Entry Schema

Each test entry SHOULD define:

- `id`
- `name`
- `domain`
- `profile`
- `purpose`
- `inputs`
- `expected_result`
- `expected_errors`
- `required_capabilities`
- `deterministic`
- `tags`
- `references`

Example:

```yaml
id: VAL-CORE-0012
name: Reject duplicate identifiers in local scope
domain: validator
profile: core
purpose: Verify duplicate identifier detection
inputs:
  - file: inputs/duplicate_ids.aas
expected_result: fail
expected_errors:
  - AASL-VAL-0002
deterministic: true
tags: [scope, identifiers, semantic]
```

## 8.6 Test Vector Requirements

Every official vector SHOULD include:

- stable identifier,
- reproducible input payload,
- expected output or diagnostic set,
- profile target,
- minimum tool version,
- notes on allowed variations,
- and a golden hash where appropriate.

## 8.7 Core Test Suites

### 8.7.1 Parser Core

Must include:

- valid minimal docs
- nested structures
- import syntax variants
- comment and trivia stress cases
- malformed delimiters
- malformed literals
- recovery diagnostics
- Unicode edge cases

### 8.7.2 Validator Core

Must include:

- symbol resolution
- type mismatches
- missing fields
- duplicate IDs
- import cycles
- namespace collisions
- profile rejection
- ontology resolution errors

### 8.7.3 Formatter Core

Must include:

- simple canonicalization
- comment stability
- multiline wrapping
- import sorting
- idempotence
- line ending normalization
- no-semantic-drift verification

### 8.7.4 Query Core

Must include:

- simple selects
- path traversals
- filters
- aggregations
- explain plan
- missing parameter errors
- timeout simulation
- profile-disabled feature rejection

### 8.7.5 Binary Core

Must include:

- text->binary->text equivalence
- malformed section directory
- hash mismatch
- unsupported compression
- partial reads
- signature failure

### 8.7.6 Ontology Governance Core

Must include:

- valid class proposal
- breaking change rejection
- namespace ownership conflicts
- missing examples
- missing compatibility analysis
- deprecation window enforcement

### 8.7.7 Security Core

Must include:

- unsafe extension rejection
- path traversal rejection
- unsigned package rejection when required
- untrusted registry warning/error modes

## 8.8 Golden Files

Golden files MUST be versioned and immutable within a certification release line. If behavior changes legitimately, the release MUST rev the suite version.

## 8.9 Determinism Rules

Tests marked deterministic MUST produce byte-identical outputs across repeated runs under same implementation version, configuration, and platform-allowed normalization rules.

## 8.10 Fuzz and Mutation Testing

The official pack SHOULD include fuzz seeds and mutation cases for:

- parser crash safety,
- binary decode hardening,
- formatter stability,
- query planner robustness.

## 8.11 Report Format

Certification reports SHOULD include:

- implementation id
- tool version(s)
- profile matrix
- suite version
- pass/fail summary
- per-test results
- flaky/waived test list if any
- signatures and timestamps

## 8.12 Example Test Vectors

### 8.12.1 Positive Syntax Vector

```text
id: PAR-POS-0001
input:
  agent Planner {
    role: "planner"
  }
expected:
  parse_success: true
```

### 8.12.2 Negative Syntax Vector

```text
id: PAR-NEG-0002
input:
  agent Planner {
    role: "planner"
expected:
  parse_success: false
  errors:
    - AASL-PAR-0004
```

### 8.12.3 Formatter Vector

```text
id: FMT-CORE-0003
input: "agent  Planner{role:\"planner\"}"
expected_output: |
  agent Planner {
    role: "planner"
  }
expected_idempotent: true
```

### 8.12.4 Binary Vector

```text
id: BIN-CORE-0004
input_file: graph.aas
action: encode_decode
expected_semantic_hash: 4c0d...e1
expected_errors: []
```

---

# 9. Ontology Proposal Template Pack

## 9.1 Purpose

This section defines the canonical templates used to propose ontology changes in the AASL ecosystem.

## 9.2 Proposal Classes

Supported proposal classes SHOULD include:

- new class/type
- new property/field
- controlled vocabulary addition
- alias or synonym addition
- deprecation request
- breaking change request
- namespace transfer
- profile-specific ontology extension
- semantic clarification only

## 9.3 General Proposal Schema

Each proposal SHOULD include:

- proposal id
- title
- author(s)
- date
- status
- target namespace
- proposal class
- summary
- motivation
- detailed semantics
- compatibility analysis
- migration path
- examples
- validation implications
- query implications
- formatter implications if any
- security considerations
- stewardship approvals

## 9.4 Canonical Template: New Class

```yaml
proposal_id: ONT-NEWCLASS-XXXX
title: Add TaskOrchestrator class to core.agent namespace
authors:
  - name: Example Author
status: draft
target_namespace: core.agent
proposal_class: new_class
summary: Introduces a class for orchestration agents responsible for task routing.
motivation: |
  Existing planner and executor classes do not explicitly model orchestration semantics.
semantics:
  name: TaskOrchestrator
  parent: core.agent.Agent
  required_properties:
    - routingPolicy
    - handoffMode
  optional_properties:
    - escalationPolicy
    - failureBudget
compatibility_analysis:
  breaking: false
  impact: additive
migration_path: Not required for existing documents.
examples:
  - |
    agent Orchestrator {
      isa: core.agent.TaskOrchestrator
      routingPolicy: "priority_weighted"
      handoffMode: "tracked"
    }
validation_implications:
  - Add required property checks for routingPolicy and handoffMode
query_implications:
  - New class should be discoverable through isa traversal
security_considerations:
  - None beyond existing agent capability policy
approvals:
  required:
    - namespace_steward
    - governance_board
```

## 9.5 Canonical Template: New Property

```yaml
proposal_id: ONT-NEWPROP-XXXX
proposal_class: new_property
target_namespace: core.agent
property:
  name: failureBudget
  domain: core.agent.TaskOrchestrator
  range: integer
  required: false
  default: null
  semantics: Maximum recoverable failures before escalation
compatibility_analysis:
  breaking: false
```

## 9.6 Canonical Template: Deprecation

```yaml
proposal_id: ONT-DEPRECATE-XXXX
proposal_class: deprecation_request
target_symbol: core.agent.LegacyCoordinator
reason: Superseded by TaskOrchestrator with clearer semantics
deprecation_window:
  start: 2026-01-01
  end: 2027-01-01
replacement:
  symbol: core.agent.TaskOrchestrator
migration_notes: |
  Rename class and map legacy routingMode to routingPolicy.
compatibility_analysis:
  breaking: false
```

## 9.7 Canonical Template: Breaking Change

Breaking changes MUST include:

- explicit break type,
- impact matrix,
- migration automation possibilities,
- minimum deprecation window,
- justification for why additive path is insufficient,
- and approval requirements beyond standard additive proposals.

## 9.8 Required Analyses

Every proposal SHOULD include:

- semantic clarity analysis,
- collision analysis,
- compatibility analysis,
- implementation burden analysis,
- test impact analysis,
- documentation impact analysis.

## 9.9 Example Checklist

Proposal reviewers SHOULD ask:

- Is the semantic distinction real and stable?
- Could this be represented as an annotation instead?
- Does it overlap existing ontology terms?
- Is migration practical?
- Are examples sufficient?
- Are validation and query effects specified?
- Does this create profile fragmentation?

---

# 10. Implementation Reference Profiles for Different Runtimes

## 10.1 Purpose

AASL must function across different runtime environments with different constraints. This section defines implementation reference profiles that standardize capability expectations, constraints, and behavioral deltas.

## 10.2 Profile Philosophy

Profiles exist to prevent accidental incompatibility while still allowing constrained environments. A profile specifies what a compliant implementation supports, forbids, optimizes, or relaxes.

## 10.3 Profile Dimensions

Profiles MAY vary across:

- maximum file/document size,
- query capabilities,
- mutation support,
- binary support,
- formatter strictness,
- registry access model,
- cryptographic verification requirements,
- extension support,
- memory ceilings,
- concurrency assumptions,
- source map availability.

## 10.4 Canonical Reference Profiles

### 10.4.1 `core-portable`

Purpose:

- baseline interoperable implementation for broad tooling support.

Requirements:

- full `.aas` parsing
- semantic validation core
- canonical formatting
- basic query support
- no required network access
- optional `.aasb` read support
- no mutation support required

Use cases:

- CLI tools
- offline validators
- documentation processors
- teaching/reference environments

### 10.4.2 `server-strict`

Purpose:

- authoritative server-side enforcement profile.

Requirements:

- full parse/validate/format/query stack
- `.aasb` read/write support
- signature verification support
- governance policy enforcement
- certification hooks
- deterministic batch operation
- strict warning policy
- profile header required

Use cases:

- central registries
- enterprise enforcement services
- canonical CI/CD validators
- package publication pipelines

### 10.4.3 `edge-lite`

Purpose:

- low-resource runtime profile.

Requirements:

- lightweight parsing
- reduced query feature set
- optional semantic validation subsets
- `.aasb` preferred for load speed
- no heavy planner/explain support required
- limited memory footprint

Use cases:

- mobile runtimes
- local embedded assistants
- thin edge agents

### 10.4.4 `browser-safe`

Purpose:

- secure browser/webview execution profile.

Requirements:

- no arbitrary file system access
- no unsafe extension loading
- sandbox-safe query runtime
- text parse/format support
- optional `.aasb` read through safe adapters
- deterministic client-side linting

Use cases:

- in-browser editors
- documentation portals
- web IDEs

### 10.4.5 `runtime-mutable`

Purpose:

- live stateful runtimes that allow controlled mutations.

Requirements:

- object identity stability
- transaction model
- mutation validation rules
- conflict detection
- persistence support
- audit trail support

Use cases:

- orchestrators
- live agent graphs
- stateful simulation systems

### 10.4.6 `cert-authority`

Purpose:

- certification execution and signing environment.

Requirements:

- all conformance suites
- secure report signing
- strict determinism auditing
- version pinning
- offline reproducibility mode

Use cases:

- certification bodies
- trusted release pipelines

## 10.5 Profile Matrix

| Capability | core-portable | server-strict | edge-lite | browser-safe | runtime-mutable | cert-authority |
|---|---:|---:|---:|---:|---:|---:|
| `.aas` parse | Yes | Yes | Yes | Yes | Yes | Yes |
| semantic validation | Yes | Yes | Partial | Yes | Yes | Yes |
| formatter | Yes | Yes | Optional | Yes | Yes | Yes |
| `.aasb` read | Optional | Yes | Yes | Optional | Yes | Yes |
| `.aasb` write | Optional | Yes | Optional | No | Yes | Yes |
| query basic | Yes | Yes | Partial | Yes | Yes | Yes |
| query explain | Optional | Yes | No | Optional | Yes | Yes |
| mutation support | No | Optional | No | No | Yes | No |
| signatures verify | Optional | Yes | Optional | Optional | Optional | Yes |
| governance enforcement | Optional | Yes | No | Optional | Optional | Yes |
| certification runner | No | Optional | No | No | Optional | Yes |

## 10.6 Profile Declaration

Artifacts SHOULD declare their intended profile compatibility in metadata. Tools MUST be able to reject incompatible artifacts or downgrade behavior safely.

## 10.7 Profile Negotiation

When a tool or runtime loads an artifact, it SHOULD compare:

- artifact required profile
- implementation supported profile
- extension requirements
- query capability requirements
- binary section requirements

If incompatible, the tool MUST fail clearly and emit the appropriate profile incompatibility error.

## 10.8 Reference Runtime Guidance

### 10.8.1 Rust Runtime Reference

Recommended for:

- parser,
- validator,
- formatter,
- `.aasb` reader/writer,
- certification tooling,
- server-grade deterministic services.

Strengths:

- memory safety,
- strong binary handling,
- deterministic performance,
- CLI ecosystem fit.

### 10.8.2 TypeScript/Node Runtime Reference

Recommended for:

- editor tooling,
- web IDE integrations,
- LSP servers,
- interactive query tools,
- developer UX surfaces.

Strengths:

- VS Code ecosystem alignment,
- easy IDE integration,
- broad accessibility.

### 10.8.3 Go Runtime Reference

Recommended for:

- operational services,
- registries,
- package servers,
- distributed validators,
- CI agents.

Strengths:

- deployability,
- concurrency ergonomics,
- operational simplicity.

### 10.8.4 Python Runtime Reference

Recommended for:

- conversion pipelines,
- experimentation,
- analysis scripts,
- ontology maintenance utilities,
- test vector generation.

Strengths:

- high iteration speed,
- broad data tooling,
- friendly for scripting and research.

### 10.8.5 WASM Runtime Reference

Recommended for:

- browser-safe linting,
- portable validation kernels,
- embedded doc viewers,
- secure preview tooling.

Strengths:

- sandboxing,
- portability,
- browser compatibility.

## 10.9 Runtime Reference Expectations

Each reference runtime SHOULD publish:

- supported profile matrix,
- unsupported features,
- performance characteristics,
- known deviations,
- certification status,
- and release alignment with spec versions.

---

# 11. Cross-Subsystem Compatibility Rules

## 11.1 Purpose

This section defines compatibility obligations across the nine domains consolidated in this document.

## 11.2 Required Cross-Consistency

The following MUST remain aligned:

- CLI commands and error codes
- formatter and parser grammar
- VS Code extension and CLI formatter version
- `.aasb` reader/writer and validation rules
- query grammar appendix and query engine implementation
- ontology template pack and governance validator
- certification catalog and official error semantics
- runtime profiles and profile validation logic

## 11.3 Compatibility Examples

- If a new error code is introduced, CLI, IDE, certification reports, and documentation search tooling SHOULD all surface it consistently.
- If `.aasb` adds a new critical section type, profile declarations and capability negotiation MUST be updated.
- If query grammar changes, IDE highlighting, linting, parser, and certification vectors MUST all be revised in lockstep.

---

# 12. Security, Trust, and Supply Chain Controls

## 12.1 Toolchain Integrity

Official tooling SHOULD be reproducibly built and signed.

## 12.2 Registry Trust

Ontology registry sources SHOULD be trust-scoped. Enterprise deployments MAY whitelist approved registries only.

## 12.3 Workspace Trust

Editor integrations MUST distinguish trusted and untrusted workspaces before enabling:

- network fetches,
- unsafe extensions,
- local CLI execution,
- binary preview decoding from unknown sources,
- mutation-capable query execution.

## 12.4 Package and Binary Trust

`.aasb` and package artifacts SHOULD support signature verification in strict profiles.

## 12.5 Safe Failure

On integrity or signature uncertainty, tools MUST fail safely or downgrade to a clearly marked untrusted mode.

---

# 13. Release and Versioning Policy for Extended Tooling

## 13.1 Version Tracks

Each subsystem MAY have its own version track, but the extended documentation pack MUST publish compatibility mappings.

Versioned tracks include:

- CLI version
- formatter version
- VS Code extension version
- `.aasb` format version
- query grammar version
- error catalog revision
- certification suite version
- ontology template pack version
- profile catalog version

## 13.2 Compatibility Table Requirement

Every official release SHOULD include a matrix such as:

| Component | Version | Compatible Spec Versions |
|---|---|---|
| CLI | 1.4.0 | 1.0.x - 1.2.x |
| Formatter | 2.0.0 | 1.2.x |
| `.aasb` | 1.1 | 1.1.x - 1.2.x |
| Query Grammar | 1.3 | 1.2.x |
|

## 13.3 Breaking Change Discipline

Breaking changes to any canonicalized external interface SHOULD require:

- explicit migration notes,
- test vector updates,
- compatibility statement,
- and release note classification.

---

# 14. Acceptance Criteria

This document is considered satisfied as a canonical extended specification when:

1. The CLI command families are sufficient to cover the operational lifecycle of AASL artifacts.
2. The formatter rules are deterministic, semantics-preserving, and testable.
3. The VS Code extension design is specific enough for direct implementation.
4. The `.aasb` binary encoding is defined strongly enough to build compliant readers and writers.
5. The query grammar appendix is strong enough to guide parser implementation.
6. The error catalog is stable and structured enough for ecosystem-wide adoption.
7. The certification catalog structure is sufficient for conformance automation.
8. The ontology proposal templates are usable as direct governance artifacts.
9. The runtime reference profiles clearly constrain compatibility expectations.
10. Cross-subsystem compatibility obligations are explicit.

---

# 15. Appendices

## Appendix A: Recommended File Names for Future Split-Outs

If this singular document is later separated into independent canonical files, recommended names are:

- `Atrahasis_AASL_CLI_Command_Reference.md`
- `Atrahasis_AASL_Formatter_Specification.md`
- `Atrahasis_AASL_VSCode_Extension_Design.md`
- `Atrahasis_AASB_Binary_Encoding_Specification.md`
- `Atrahasis_AASL_Query_Language_Grammar_Appendix.md`
- `Atrahasis_AASL_Official_Error_Code_Catalog.md`
- `Atrahasis_AASL_Certification_Test_Catalog_and_Vectors.md`
- `Atrahasis_AASL_Ontology_Proposal_Template_Pack.md`
- `Atrahasis_AASL_Implementation_Reference_Profiles.md`

## Appendix B: Recommended Build Order

Recommended implementation order:

1. Error catalog
2. CLI shell and machine output contract
3. Formatter engine
4. Query grammar parser
5. VS Code extension core with LSP
6. `.aasb` read support
7. certification vector harness
8. ontology proposal validator
9. runtime profile enforcement matrix
10. `.aasb` writer and signing support

## Appendix C: Minimal Delivery Milestone Pack

A minimum credible release of this extended pack SHOULD include:

- stable CLI validate/format/query commands
- formatter idempotence suite
- VS Code syntax + diagnostics + formatting
- `.aasb` reader
- error catalog search command
- core certification vectors
- proposal templates
- at least two published runtime profiles

---

**End of Document**
