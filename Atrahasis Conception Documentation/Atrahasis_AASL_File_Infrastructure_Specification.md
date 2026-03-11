# Atrahasis AASL File Infrastructure Specification

**Document ID:** ATR-AASL-FILE-INFRA-001  
**Title:** Atrahasis AASL File Infrastructure Specification  
**Status:** Canonical Draft  
**Version:** 1.0.0  
**Authoring Context:** Atrahasis / AASL Core System  
**Last Updated:** 2026-03-08  
**Applies To:** `.aas`, `.aasp`, `.aaspkg`, `.aaslock`, `.aasidx`, future `.aasb`, file readers, file writers, packagers, loaders, repository tooling, canonicalization layer, integrity layer, signing layer, and document exchange workflows.

---

## 1. Purpose

This document defines the **canonical file infrastructure** for the Atrahasis Agentic Semantic Language (AASL). It specifies how AASL artifacts are represented on disk, exchanged between systems, validated at load time, canonicalized for deterministic behavior, packaged for transport, indexed for retrieval, and secured for trusted execution.

The purpose of the file infrastructure is not merely to store text. It exists to guarantee that AASL artifacts are:

1. **Portable** across environments and runtimes.
2. **Deterministic** when parsed, normalized, hashed, indexed, and executed.
3. **Composable** across repositories, packages, and semantic modules.
4. **Auditable** through traceable provenance and integrity metadata.
5. **Secure** under adversarial, corrupted, or partially trusted conditions.
6. **Efficient** for local development, distributed compilation, large corpus ingestion, and runtime loading.
7. **Future-compatible** with binary, compressed, and streaming representations.

This specification turns AASL from a language definition into a complete document ecosystem suitable for production use.

---

## 2. Scope

This specification covers:

- Canonical AASL text file format (`.aas`)
- Parsed artifact cache format (`.aasp`)
- Package/distribution format (`.aaspkg`)
- Lock and dependency pinning format (`.aaslock`)
- Semantic index format (`.aasidx`)
- Reserved future binary format (`.aasb`)
- Reader/writer behavior
- Load pipeline contracts
- Canonicalization and normalization rules
- On-disk integrity, signatures, and provenance
- Repository layout conventions
- Import resolution from local and remote sources
- Streaming and chunked loading
- Backup, snapshots, and archival expectations
- Failure handling and recovery requirements

This specification does **not** redefine the AASL language grammar itself, the validator pass model, or the compiler semantics, except where file representation affects those systems.

---

## 3. Design Principles

The AASL file infrastructure shall obey the following principles.

### 3.1 Text-first canonicality

The canonical human-authorable representation of AASL is a UTF-8 text file with extension `.aas`.

### 3.2 Parsed forms are derived, never primary

Any cached AST, semantic graph, index, or binary artifact is derived from canonical source and may be discarded and regenerated.

### 3.3 Reproducibility before convenience

Whitespace, ordering, hash calculation, package manifests, and metadata serialization must favor deterministic output over implementation-specific flexibility.

### 3.4 Separation of semantic content from transport concerns

The same AASL document should be representable as standalone text, package member, streamed payload, or binary frame without changing its semantic meaning.

### 3.5 Explicit provenance

Every nontrivial derived artifact should record where it came from, what version of tooling produced it, and what source hash it corresponds to.

### 3.6 Safe degradation

If advanced features like binary acceleration, signatures, or indexes are missing, the system must still be able to fall back to canonical `.aas` handling.

### 3.7 Zero hidden mutation

No reader, loader, formatter, or package manager may silently alter semantic content during routine open/load operations.

---

## 4. File Type Overview

The AASL ecosystem uses a family of related file types.

| Extension | Name | Role | Canonical Source of Truth | Required | Human Editable |
|---|---|---|---|---|---|
| `.aas` | AASL Source Document | Primary semantic text representation | Yes | Yes | Yes |
| `.aasp` | AASL Parsed Artifact | Cached parser/AST/IR output | No | Optional | No |
| `.aaspkg` | AASL Package Bundle | Distribution package for modules, corpora, schemas, assets | No | Optional | Indirectly |
| `.aaslock` | AASL Lockfile | Dependency and package resolution pin set | No | Optional but recommended | Yes |
| `.aasidx` | AASL Semantic Index | Retrieval and lookup acceleration | No | Optional | No |
| `.aasb` | AASL Binary Document | Reserved future binary canonical transport/compute form | Not yet | Reserved | No |
| `.sig` | Signature Sidecar | Detached signature for any artifact | No | Optional | No |
| `.prov.json` | Provenance Sidecar | Provenance metadata | No | Optional | Yes |

---

## 5. Canonical `.aas` Source Format

### 5.1 Encoding

A `.aas` file must be encoded as **UTF-8**.

Allowed:
- UTF-8 without BOM

Disallowed in canonical output:
- UTF-8 with BOM
- UTF-16
- UTF-32
- platform-local legacy encodings

Readers may detect and reject non-UTF-8 encodings, or optionally offer conversion in non-canonical recovery modes.

### 5.2 Newlines

Canonical newline is `LF` (`\n`).

Readers must accept:
- LF
- CRLF

Writers must emit:
- LF only

### 5.3 File extension

Canonical source files must use `.aas`.

Alternative temporary extensions may be used during editing, but tools must not treat them as canonical AASL source unless explicitly configured.

### 5.4 Text normalization

Before hashing or canonical serialization, the file content must be normalized according to the canonicalization rules in Section 11.

### 5.5 Header convention

A `.aas` document may begin with an optional structured header block containing identity and metadata fields such as:

- `document.id`
- `document.title`
- `document.version`
- `document.namespace`
- `document.authors`
- `document.created_at`
- `document.updated_at`
- `document.provenance`

The presence or absence of this header depends on the AASL language profile, but file infrastructure must preserve it exactly and expose it to the parser.

### 5.6 Single-document rule

A `.aas` file represents one primary AASL document unit. It may contain nested declarations, modules, objects, schemas, and imports, but it must resolve to one top-level document parse root.

---

## 6. `.aasp` Parsed Artifact Format

### 6.1 Purpose

`.aasp` is a cached parsed artifact used to accelerate repeated parsing, validation, semantic resolution, or editor tooling.

It is a **derived** artifact and must never be treated as the ultimate source of truth if the corresponding `.aas` file is available.

### 6.2 Use cases

- IDE/editor startup acceleration
- CI build caching
- parser regression baselines
- semantic diff acceleration
- runtime warm caches
- static analysis precomputation

### 6.3 Contents

A `.aasp` artifact should contain enough information to reconstruct or reuse parser-related outputs, such as:

- source file path or content address
- canonical source hash
- parser version
- grammar version
- token stream summary
- CST representation
- AST representation
- source span map
- diagnostics generated during parse
- optional symbol pre-index
- optional serialization checksum

### 6.4 Stability model

`.aasp` is **version-coupled** to:

- grammar version
- parser version
- serialization version
- canonicalization version

Any mismatch invalidates the cache unless the runtime explicitly supports compatible migration.

### 6.5 Trust model

`.aasp` must never be trusted blindly when:

- the source hash differs
- the parser version differs incompatibly
- the grammar profile differs
- the artifact signature fails
- the serialization checksum fails

### 6.6 Storage mode

A `.aasp` artifact may be stored as:

- JSON-based structured serialization
- compact binary blob
- memory-mappable internal format

The exact internal encoding is implementation-defined, but the artifact must declare a serialization format version.

---

## 7. `.aaspkg` Package Bundle Format

### 7.1 Purpose

`.aaspkg` is the canonical package bundle format for distributing AASL modules, schemas, corpora, ontology packs, policy bundles, and related assets.

### 7.2 Package contents

A package may include:

- one or more `.aas` source files
- package manifest
- dependency metadata
- module registry information
- semantic schemas
- policy files
- supporting assets
- prebuilt `.aasp` caches
- optional `.aasidx` indexes
- signatures and provenance sidecars

### 7.3 Manifest requirement

Every `.aaspkg` must include a manifest file named:

`aaspkg.json`

The manifest must minimally specify:

- package name
- package version
- package format version
- root module(s)
- package hash algorithm
- entrypoints
- dependency declarations
- compatibility constraints
- included file inventory

### 7.4 Archive container

At the transport level, `.aaspkg` may be implemented using a standard container such as ZIP or TAR, but the semantic format is defined by this specification, not by the archive technology.

Implementations must abstract away the transport container so package semantics remain stable.

### 7.5 Deterministic package build

Canonical package builds must produce deterministic artifacts when provided the same inputs, including:

- sorted manifest fields
- sorted file inventory
- normalized line endings where applicable
- fixed metadata emission rules
- stable hash algorithm
- stable compression policy if compression is used

### 7.6 Package modes

A package may be one of the following classes:

1. **Module package** – imports, schemas, reusable objects
2. **Ontology package** – vocabulary, semantic registry extensions
3. **Policy package** – governance, validation, compliance, safety policy
4. **Corpus package** – document sets for ingestion or retrieval
5. **Runtime package** – precompiled runtime assets and indices
6. **Bundle package** – composite distribution containing multiple package classes

### 7.7 Package trust states

Packages must be classified at load time into one of the following trust states:

- trusted and signed
- trusted but unsigned
- untrusted local
- untrusted remote
- revoked
- tampered
- unverifiable

Runtime policy determines which states are admissible.

---

## 8. `.aaslock` Lockfile Format

### 8.1 Purpose

`.aaslock` pins dependency resolution results so that AASL builds and runtime imports are reproducible.

### 8.2 Use cases

- deterministic CI/CD builds
- reproducible package restoration
- secure supply-chain resolution
- auditability of imported modules
- rollback after registry drift

### 8.3 Contents

A lockfile should include:

- resolver version
- lockfile format version
- registry source identifiers
- package names
- exact versions
- content hashes
- signature identities if available
- transitive dependency graph
- resolution timestamp
- compatibility policy snapshot

### 8.4 Mutation rules

A lockfile must not be mutated implicitly during ordinary reads.

It may only be rewritten by:

- explicit resolve/update command
- explicit package add/remove operation
- explicit migration command

### 8.5 Canonical project placement

Recommended location:

`./aas/aaslock`

or project root:

`./aaslock`

Implementations must support both, but repository policy should standardize one location.

---

## 9. `.aasidx` Semantic Index Format

### 9.1 Purpose

`.aasidx` provides retrieval and lookup acceleration for AASL repositories and packages.

It exists to support fast loading of:

- symbol references
- document identity maps
- ontology term lookup
- semantic object retrieval
- relation traversal seeds
- content-addressed source resolution
- query planner shortcuts

### 9.2 Derived status

`.aasidx` is derived from source and package state. It is always regenerable.

### 9.3 Index classes

Implementations may produce several logical index layers inside one `.aasidx` artifact:

- lexical index
- symbol index
- namespace index
- object ID index
- import/export graph index
- semantic relation index
- provenance index
- content hash index
- embedding or vector pointer map

### 9.4 Invalidations

An index must be invalidated when any of the following changes:

- source content hash
- package inventory
- ontology registry version
- resolver output
- query engine version requiring incompatible structures

### 9.5 Offline portability

An `.aasidx` file may be shipped with packages or repositories but must clearly indicate whether it is:

- local-only
- environment-specific
- platform-neutral
- partial
- complete

---

## 10. Reserved Future `.aasb` Binary Format

### 10.1 Status

`.aasb` is reserved for a future binary representation of AASL.

It is not the primary canonical authoring format in version 1.0 of the infrastructure.

### 10.2 Intended goals

The binary format is intended to support:

- compact transport
- zero-copy loading
- memory-mapped runtime access
- high-volume corpus deployment
- embedded runtime environments
- fast parser bypass for verified artifacts

### 10.3 Constraints

Any future `.aasb` format must preserve semantic equivalence with canonical `.aas` source and must define round-trip guarantees, canonical hashing behavior, and signature semantics.

### 10.4 Non-goal

`.aasb` must not become a vendor-proprietary opaque lock-in format. Its structure must be openly specified.

---

## 11. Canonicalization Rules

Canonicalization is the foundation of hashing, signatures, caching, packaging, diffing, and reproducible execution.

### 11.1 Canonicalization phases

Canonicalization of a `.aas` source document should occur in distinct phases:

1. Byte normalization
2. Encoding verification
3. Newline normalization
4. Unicode normalization policy
5. parser-aware structural normalization
6. deterministic serialization
7. canonical hash calculation

### 11.2 Byte normalization

Readers must decode source into a normalized in-memory string representation before semantic processing.

### 11.3 Newline normalization

All line endings are normalized to LF for canonical hashing and canonical writer output.

### 11.4 Trailing newline rule

Canonical writers should emit exactly one trailing newline at end of file.

### 11.5 Whitespace policy

Whitespace that is semantically insignificant may be normalized by canonical formatting tools, but simple readers must preserve original spans where needed for diagnostics.

### 11.6 Unicode policy

Implementations must choose and declare a Unicode normalization policy. The default recommended policy is:

- preserve source code points for author-facing editing
- normalize to NFC for canonical hashing unless the language profile marks string literal payloads or binary literal zones as exact-preserve regions

This rule prevents visually equivalent but byte-distinct source from causing silent divergence while preserving exact literal regions where required.

### 11.7 Deterministic ordering

When a serialization step emits maps, inventories, manifests, indexes, or metadata objects, field ordering must be deterministic.

Recommended default:
- lexicographic ascending key order

### 11.8 Canonical hash input

The canonical hash of a source artifact must be computed over canonicalized serialized content, not raw filesystem bytes, unless the hash is explicitly marked as a raw byte hash.

### 11.9 Hash declaration

Artifacts that store hashes must declare:

- algorithm name
- input basis (`raw_bytes`, `canonical_text`, `canonical_structure`, etc.)
- encoded digest format

---

## 12. Reader Architecture

### 12.1 Reader responsibilities

A compliant AASL reader must be able to:

- open source or packaged artifacts
- verify type and expected format
- decode content
- normalize content
- expose byte and span maps
- produce structured load diagnostics
- optionally invoke parser/validator hooks
- avoid unsafe implicit mutation

### 12.2 Reader modes

Readers should support these modes:

1. **Strict mode** – reject any non-canonical or invalid construct
2. **Compatibility mode** – accept certain legacy variants and emit diagnostics
3. **Recovery mode** – attempt best-effort loading for damaged artifacts
4. **Streaming mode** – incremental decoding and parse handoff
5. **Secure mode** – enforce signatures, trust policy, and origin constraints

### 12.3 Reader outputs

A reader should expose a structured result object containing:

- artifact type
- path or source URI
- decoded content or stream handle
- canonicalization result
- content hash(es)
- detected metadata
- trust state
- diagnostics
- optional provenance

### 12.4 Reader failure classes

Reader failures must be classed distinctly:

- not found
- unreadable
- unsupported encoding
- malformed package
- corrupted archive
- signature failure
- canonicalization failure
- invalid type
- policy-blocked source

These classes should be surfaced consistently to downstream systems.

---

## 13. Writer Architecture

### 13.1 Writer responsibilities

A compliant writer must be able to:

- serialize canonical `.aas` text
- emit package manifests and inventories deterministically
- preserve semantic integrity
- optionally preserve stylistic layout under non-canonical edit modes
- attach provenance and hash metadata
- produce atomic writes where possible

### 13.2 Writer modes

Writers should support:

1. **Canonical write** – deterministic output for source control and hashing
2. **Preserving write** – minimal-diff updates when safe
3. **Repair write** – fix known non-canonical formatting problems
4. **Bundle write** – build `.aaspkg` with manifest and optional indexes
5. **Snapshot write** – create immutable point-in-time artifact copies

### 13.3 Atomicity

Where supported by the host environment, writers must perform atomic replacement using temp file + fsync + rename semantics to avoid partial corruption.

### 13.4 Backup behavior

Writers may optionally produce timestamped backups or journaled recovery entries, especially when modifying package manifests or lockfiles.

---

## 14. Repository Layout Convention

A standard AASL project should use a consistent repository layout.

### 14.1 Recommended structure

```text
project-root/
  aas/
    src/
      core/
      modules/
      policies/
      ontologies/
    packages/
    cache/
    index/
    snapshots/
    imports/
    temp/
    aaspkg.json
    aaslock
  docs/
  tests/
  tools/
```

### 14.2 Directory semantics

- `src/` – canonical editable `.aas` sources
- `packages/` – restored or built `.aaspkg` artifacts
- `cache/` – `.aasp` parser/runtime caches
- `index/` – `.aasidx` indexes
- `snapshots/` – immutable archival copies
- `imports/` – vendored imported sources or mirrors
- `temp/` – transient build products only

### 14.3 Source control recommendations

Generally include in source control:

- `.aas`
- package manifests
- `.aaslock`
- selected policy/provenance files if part of governance record

Usually exclude from source control:

- local caches (`.aasp`)
- transient indexes (`.aasidx`) unless intentionally versioned
- temp artifacts
- machine-specific package expansions

---

## 15. Import and Path Resolution

### 15.1 Resolution domains

AASL file resolution may occur across:

- relative local paths
- project-root anchored paths
- package entrypoints
- registry identifiers
- content-addressed references
- remote signed artifact URIs

### 15.2 Resolution precedence

Unless overridden by project policy, the recommended precedence is:

1. explicit in-memory override
2. explicitly provided local path
3. project-local source path
4. vendored/import mirror
5. lockfile-pinned package resolution
6. registry resolution
7. remote fallback resolution

### 15.3 Resolution constraints

Resolvers must prevent:

- path traversal outside allowed roots
- unauthorized network fetch in offline mode
- registry drift when lockfile pinning is required
- ambiguous import shadowing without explicit policy

### 15.4 Content-addressed imports

AASL should support content-addressed imports for high-trust reproducibility. Such imports resolve artifacts by hash rather than mutable name/version alone.

---

## 16. Integrity and Hashing

### 16.1 Required hash support

Implementations must support at least one cryptographically strong hash algorithm. Recommended default:

- SHA-256

Optional stronger or alternate algorithms may be supported, but interoperability profiles should standardize one baseline algorithm.

### 16.2 Hash classes

Artifacts may declare multiple hashes, including:

- raw byte hash
- canonical text hash
- canonical structural hash
- package inventory hash
- semantic graph hash

### 16.3 Use of hashes

Hashes are used for:

- cache invalidation
- lockfile pinning
- package verification
- provenance linking
- semantic deduplication
- content-addressed import
- signature payload framing

### 16.4 Mismatch handling

Hash mismatch must be treated as a first-class diagnostic event. Policy determines whether it is warning, error, or security incident.

---

## 17. Signatures and Trust

### 17.1 Signature model

AASL artifacts may be signed using either:

- detached sidecar signatures (`.sig`)
- embedded manifest signature sections
- package-level signature blocks

### 17.2 What may be signed

- single `.aas` document
- `.aaspkg` bundle
- `.aaslock` lockfile
- `.aasidx` index
- snapshot bundle
- provenance record

### 17.3 Signature input basis

Every signature must specify whether it signs:

- raw archive bytes
- canonical package manifest + file hash inventory
- canonical text content
- canonical structural serialization

### 17.4 Trust policy integration

Readers and loaders should evaluate signatures against environment trust policy, including:

- accepted issuers
- revoked issuers
- required signing levels
- allowed unsigned local development exceptions
- offline verification capabilities

### 17.5 Revocation and expiration

If a signing policy is used, the infrastructure must support revocation awareness and expiration semantics for production environments.

---

## 18. Provenance Metadata

### 18.1 Purpose

Provenance metadata records where an artifact came from and how it was produced.

### 18.2 Recommended provenance fields

- source path or URI
- source hash
- parent artifact hash
- build tool name/version
- parser/compiler/validator version
- packaging timestamp
- author identity if available
- signature identity if available
- environment or pipeline ID
- generation mode (manual, compiled, restored, mirrored, exported)

### 18.3 Provenance storage

Provenance may be stored:

- inline in manifest
- inline in document header metadata
- as sidecar `.prov.json`
- in repository audit logs

### 18.4 Integrity relationship

If provenance influences trust decisions, it should itself be signed or included in signed payloads.

---

## 19. Load Pipeline

### 19.1 Standard load pipeline

The canonical load pipeline is:

1. Locate artifact
2. Detect artifact type
3. Open container or source stream
4. Decode bytes
5. Verify encoding and structure
6. Normalize content
7. Compute or verify content hashes
8. Verify signatures if policy requires
9. Emit reader diagnostics
10. Parse or hydrate derived artifact
11. Optionally validate
12. Register in runtime/document store

### 19.2 Loader contracts

The loader must expose enough structured state to downstream components so parser, validator, compiler, and runtime can distinguish file-level failures from language-level failures.

### 19.3 Partial-load support

Large packages and corpora should support partial load where only requested inventory members, indexes, or entry modules are hydrated.

### 19.4 Lazy materialization

A package loader may defer extracting or decoding embedded members until they are requested, provided integrity metadata is still available.

---

## 20. Streaming and Chunked Handling

### 20.1 Motivation

AASL must support large corpora, distributed transport, and editor usage over partial content.

### 20.2 Streaming requirements

Readers should support streaming modes for:

- large package download
- incremental document parsing
- remote registry transport
- corpus ingestion pipelines
- memory-limited environments

### 20.3 Chunk integrity

If chunked transfer is used, the system should support per-chunk checksums plus whole-artifact verification.

### 20.4 Semantic caution

Chunking must never produce silent semantic truncation. Partial documents must be explicitly marked incomplete.

---

## 21. Snapshots, Journals, and Recovery

### 21.1 Snapshot role

Snapshots provide point-in-time immutable copies of AASL states for rollback, audit, reproducibility, and forensic analysis.

### 21.2 Journal role

For mutable workflows, a write journal may record staged changes before final commit to protect against interruption and corruption.

### 21.3 Recovery expectations

A compliant infrastructure should support recovery from:

- interrupted writes
- corrupt package extraction
- stale cache mismatches
- lockfile/package divergence
- signature verification failures after restoration

### 21.4 Recovery priority order

Recommended recovery order:

1. restore from canonical `.aas` source
2. restore from signed package inventory
3. rebuild indexes and parsed caches
4. consult journal/backups
5. fall back to snapshot or remote mirror

---

## 22. Compatibility and Versioning

### 22.1 Version axes

File infrastructure compatibility depends on several version axes:

- file format version
- parser version
- grammar version
- canonicalization version
- package manifest version
- resolver version
- signature/profile version

### 22.2 Forward compatibility

Readers should ignore unknown manifest fields when policy allows, provided required fields remain valid.

### 22.3 Backward compatibility

Compatibility shims may be supported, but canonical writers must always target the current stable format unless explicitly instructed otherwise.

### 22.4 Migration tools

The ecosystem should provide migration tooling for:

- legacy manifest version upgrades
- lockfile schema migrations
- cache invalidation and rebuild
- package normalization rebuilds

---

## 23. Security Requirements

### 23.1 Threat model

File infrastructure must assume the possibility of:

- malicious documents
- poisoned packages
- malformed archives
- path traversal attempts
- decompression bombs
- signature stripping
- tampered lockfiles
- conflicting shadow imports
- stale or forged caches

### 23.2 Minimum protections

Implementations must protect against:

- arbitrary path escape during archive extraction
- uncontrolled resource exhaustion from crafted inputs
- unsigned artifact substitution when signatures are required
- cache poisoning through mismatched source hashes
- execution of packaged code or hooks during passive read operations

### 23.3 Safe extraction

Package extraction must sanitize paths and reject unsafe entries such as:

- absolute paths
- `..` traversal entries
- device paths
- duplicate conflicting entries under case-insensitive collisions

### 23.4 Resource limits

Readers should expose configurable limits for:

- maximum file size
- maximum archive expansion ratio
- maximum number of package members
- maximum nesting depth
- maximum manifest size
- maximum streaming chunk size

### 23.5 Secure defaults

Remote artifact loading should default to least privilege:

- no execution
- no implicit trust
- no silent install
- no mutation of lockfile
- no registry fallback when policy forbids drift

---

## 24. Performance Requirements

### 24.1 Performance goals

The infrastructure should enable:

- fast cold open of small source docs
- low-latency warm open using `.aasp`
- scalable package restoration
- fast symbol lookup via `.aasidx`
- partial loading of large corpora
- efficient CI rebuilds through content hashing

### 24.2 Optimization hierarchy

Optimization must preserve correctness. The hierarchy is:

1. correctness
2. determinism
3. trust/integrity
4. debuggability
5. performance

### 24.3 Acceptable accelerators

Accelerators may include:

- memory mapping
- incremental hashing
- package member index tables
- lazy decoding
- AST cache reuse
- index prefetch
- parallel integrity verification

Provided they do not change semantic results.

---

## 25. CLI and Tooling Contracts

### 25.1 Expected file infrastructure commands

A standard AASL CLI should eventually expose commands such as:

- `aas open`
- `aas format`
- `aas canonicalize`
- `aas hash`
- `aas sign`
- `aas verify`
- `aas pack`
- `aas unpack`
- `aas restore`
- `aas lock`
- `aas index`
- `aas snapshot`
- `aas recover`

### 25.2 Tooling interoperability

All tools that read or write AASL artifacts must rely on the same canonical file infrastructure library or equivalent normative behavior.

### 25.3 Editor integration

Editors should use `.aasp` and `.aasidx` opportunistically but always remain anchored to `.aas` source as the editable truth.

---

## 26. Normative Validation Rules for File Infrastructure

The following file infrastructure rules are normative.

### 26.1 Source rules

- A canonical source document must be UTF-8 without BOM.
- Canonical writer output must use LF newlines.
- Canonical source extension must be `.aas`.
- Source hashing must declare its canonicalization basis.

### 26.2 Cache rules

- `.aasp` artifacts must declare parser and grammar compatibility metadata.
- Cache reuse is invalid if source hash mismatches.

### 26.3 Package rules

- `.aaspkg` must contain `aaspkg.json`.
- Package manifest must declare inventory and version.
- Package extraction must reject unsafe paths.

### 26.4 Lockfile rules

- `.aaslock` must pin exact resolved artifact identities.
- Lockfiles must not mutate implicitly during read or import.

### 26.5 Index rules

- `.aasidx` must declare the source/package state it corresponds to.
- Indexes are invalid on source drift.

### 26.6 Security rules

- Signature failure must be surfaced explicitly.
- Path traversal during extraction must be rejected.
- Hash mismatches must not be silently ignored.

---

## 27. Conformance Levels

### 27.1 Minimal conformance

A minimal implementation supports:

- `.aas` read/write
- canonical newline normalization
- UTF-8 enforcement
- canonical hashing
- basic diagnostics

### 27.2 Standard conformance

A standard implementation supports:

- `.aas`
- `.aasp`
- `.aaspkg`
- `.aaslock`
- `.aasidx`
- deterministic packaging
- trust states
- provenance metadata
- safe extraction rules

### 27.3 Full conformance

A full implementation supports:

- all standard capabilities
- signatures and verification
- content-addressed resolution
- snapshots/journals/recovery
- streaming and lazy materialization
- migration tooling
- advanced policy-controlled trust enforcement

---

## 28. Reference Serialization Profiles

To maximize interoperability, the ecosystem should standardize a small number of named serialization profiles.

### 28.1 `canonical-text-v1`

For `.aas` canonical text emission.

### 28.2 `parsed-cache-v1`

For `.aasp` serialization.

### 28.3 `package-manifest-v1`

For `.aaspkg` manifest schema.

### 28.4 `lockfile-v1`

For `.aaslock` resolution pinning schema.

### 28.5 `semantic-index-v1`

For `.aasidx` metadata framing.

These profiles should be versioned explicitly and referenced by tooling.

---

## 29. Example Artifact Lifecycle

A typical lifecycle for an AASL source module is:

1. Author creates `module.aas`
2. Writer saves canonical UTF-8 LF output
3. Hash is computed over canonical text
4. Parser produces `.aasp`
5. Indexer generates `.aasidx`
6. Resolver updates `.aaslock`
7. Packager emits `module.aaspkg`
8. Signer attaches signature/provenance
9. Runtime loader verifies and imports package
10. Snapshot subsystem archives immutable copy

This lifecycle shows how every file type participates while preserving `.aas` as the human-editable source of truth.

---

## 30. Implementation Guidance

### 30.1 Recommended build order

Implement the file infrastructure in this order:

1. canonical `.aas` reader/writer
2. canonicalization + hashing library
3. atomic write and diagnostics layer
4. `.aasp` cache serializer
5. `.aaspkg` manifest + bundler
6. `.aaslock` resolver support
7. `.aasidx` index layer
8. signature/provenance support
9. snapshot/recovery subsystem
10. future `.aasb` exploration

### 30.2 Avoid early overcomplexity

The system should not wait for `.aasb` or advanced package registries before reaching production viability. Text-first correctness is the foundation.

### 30.3 Shared library requirement

All AASL ecosystem tools should use a shared infrastructure library to avoid divergent hashing, packaging, or canonicalization behavior.

---

## 31. Open Reserved Fields

The following areas are intentionally reserved for future expansion:

- binary frame encoding for `.aasb`
- vector index embeddings in `.aasidx`
- encrypted package members
- selective disclosure signatures
- trust delegation chains
- distributed registry proofs
- content-defined chunking for large corpora

Future additions must remain backward-aware and clearly versioned.

---

## 32. Final Normative Statement

AASL file infrastructure exists to make AASL **real, portable, reproducible, and trustworthy** outside the abstract language definition.

The canonical source artifact is the `.aas` UTF-8 text document. All other file forms are derivatives, transport frames, reproducibility anchors, or acceleration layers around that truth. A compliant AASL ecosystem must therefore treat file infrastructure as a first-class systems problem encompassing canonicalization, packaging, hashing, trust, resolution, and recovery.

Any implementation that stores AASL content without deterministic canonicalization, explicit provenance, safe load behavior, and reproducible artifact identity is incomplete.

---

## 33. Next Recommended Document

**Next document to generate:** `Atrahasis_AASL_Developer_Tooling_Specification.md`

This should define the CLI, editor integration, formatter, language server, semantic explorer, graph viewer, test harness tooling, and developer workflow contracts required to make the file infrastructure usable in practice.

