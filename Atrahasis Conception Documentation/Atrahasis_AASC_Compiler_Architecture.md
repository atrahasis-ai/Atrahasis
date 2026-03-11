# Atrahasis AASC Compiler Architecture

Version: 1.0.0  
Status: Canonical Subsystem Specification  
Date: 2026-03-08

---

# 1. Purpose

This document defines the canonical architecture for the **AASC Compiler** (**Atrahasis Semantic Compiler**), the subsystem that converts external information into valid, structured, machine-operable **AASL** artifacts.

If the parser turns AASL text into structure, the AASC compiler turns non-AASL inputs into **draft or canonical AASL** suitable for parser ingestion, validation, canonicalization, runtime loading, storage, and federation.

This document exists to fully specify:

- compiler role and system position
- compiler design principles
- input and output contracts
- source adapter architecture
- semantic extraction pipeline
- ontology mapping model
- identity and reference assignment
- ambiguity handling and uncertainty representation
- draft generation and emission model
- validation and canonicalization handoff
- provenance capture requirements
- compile trace and explainability model
- batch and streaming compilation modes
- failure and quarantine behavior
- extensibility boundaries
- performance expectations
- package boundaries
- testing strategy
- implementation sequencing

The compiler does **not** replace human judgment, truth verification, or runtime governance. Its role is to transform external information into **structured semantic candidates** with explicit provenance and bounded interpretation.

---

# 2. System Role

The AASC Compiler is the semantic ingress transformer of the Atrahasis system.

It sits between external information sources and the formal AASL language layer.

High-level position in Atrahasis:

External Source  
→ **AASC Compiler**  
→ Draft AASL  
→ AASL Parser  
→ Validator  
→ Canonicalizer  
→ Runtime Loader  
→ Query / Memory / Agents / Federation

The compiler is the bridge that allows Atrahasis to ingest information that was **not originally authored in AASL**.

Without the compiler, Atrahasis would only be able to operate on manually written AASL. With the compiler, external documents, payloads, datasets, and natural-language artifacts can be transformed into semantically structured internal knowledge.

---

# 3. Architectural Objectives

The compiler must satisfy the following system objectives.

## 3.1 Semantic Fidelity

The compiler must preserve source meaning as faithfully as possible while avoiding hidden inference inflation.

## 3.2 Explicitness Over Guessing

Any semantic interpretation that is uncertain, ambiguous, partial, or inferred must be represented explicitly rather than silently assumed.

## 3.3 Deterministic Structural Output

For a given compiler configuration, source artifact, ontology snapshot, and normalization policy, the compiler must produce deterministic draft output and deterministic compile traces.

## 3.4 Separation of Concerns

The compiler extracts and structures meaning. The parser proves syntax. The validator proves admissibility. The canonicalizer proves deterministic representation. The verifier evaluates trust and truth.

## 3.5 Provenance Preservation

Every emitted semantic object must remain traceable to the source material, extraction path, compiler version, and transformation decisions that produced it.

## 3.6 Bounded Interpretation

The compiler may transform, normalize, and structure information, but it must not silently invent unsupported claims, identities, relationships, or verification states.

## 3.7 Extensibility

The compiler must support new source types, ontology families, extractor modules, and output policies without redesigning the compiler core.

## 3.8 Explainability

A human operator, downstream validator, or auditing agent must be able to reconstruct why the compiler emitted a given AASL artifact.

## 3.9 Batch Operability

The compiler must scale from single-document interactive use to large corpus ingestion and scheduled recurring data conversion.

---

# 4. Scope of Responsibility

The compiler is responsible for:

- accepting external source material
- normalizing source envelopes
- selecting a source adapter
- extracting candidate semantic units
- mapping extracted semantics into AASL ontology structures
- assigning or proposing identifiers
- attaching provenance and extraction confidence
- generating draft AASL artifacts
- routing output to parser, validator, and canonicalizer
- emitting compile traces and diagnostics
- quarantining inadmissible or unresolved outputs when necessary

The compiler is **not** responsible for:

- acting as the final source of truth
- adjudicating factual correctness
- granting verification status beyond compile-local markers
- storing knowledge as canonical memory by itself
- overriding validator failures
- silently repairing ontology violations without traceability
- policy approval for federation publication

---

# 5. Supported Input Classes

The compiler must support multiple source families.

## 5.1 Natural Language Text

Examples:

- analyst notes
- freeform research summaries
- problem statements
- chat transcripts
- operator instructions
- generated summaries

## 5.2 Markdown and Rich Text Documents

Examples:

- technical documentation
- project specifications
- reports
- design notes
- README files
- policy manuals

## 5.3 Structured Data

Examples:

- JSON
- YAML
- CSV
- TSV
- relational exports
- event logs
- spreadsheet-derived tabular data

## 5.4 Existing Draft AASL

Examples:

- partially valid AASL
- auto-generated AASL requiring normalization
- migrated legacy AASL fragments

## 5.5 Dataset and Knowledge Corpus Inputs

Examples:

- benchmark collections
- claim/evidence corpora
- research archives
- machine-generated annotation sets

## 5.6 API and Transport Payloads

Examples:

- webhook payloads
- REST responses
- connector outputs
- ETL stream records

---

# 6. Compiler Output Classes

The compiler must emit one or more of the following output classes.

## 6.1 Draft AASL Text

Human-readable or machine-generated AASL intended for parser ingestion.

## 6.2 Draft Semantic Bundle

A structured output package containing:

- generated AASL text
- compile metadata
- source envelope metadata
- compile diagnostics
- extraction trace
- unresolved ambiguity records

## 6.3 Structured Intermediate Representation

An internal compiler IR that exists before final AASL emission. This IR is not the canonical storage language, but it is necessary for stable compilation stages.

## 6.4 Compile Diagnostics Stream

Structured information about:

- unsupported source forms
- extraction failures
- ontology mismatches
- unresolved references
- ambiguous mappings
- output emission failures

## 6.5 Quarantine Package

When compilation cannot safely produce admissible AASL, the compiler must emit a quarantine package containing the failed source, partial IR if allowed, and machine-readable reasons for non-admission.

---

# 7. Position Relative to Other Subsystems

The compiler has strict upstream and downstream relationships.

Upstream:

- file readers
- transport connectors
- corpus importers
- APIs
- user-authored external text

Downstream:

- AASL parser
- validator
- canonicalizer
- runtime loader
- audit and diagnostics tooling
- batch ingestion orchestrators

The compiler must never bypass the parser or validator when generating normal AASL output.

Even compiler-produced AASL must still be treated as authored source and passed through the formal AASL pipeline.

---

# 8. Compiler Design Principles

## 8.1 Compiler Output Must Be Auditable

Every emitted object must be explainable through a compile trace.

## 8.2 No Hidden Semantic Jumps

The compiler must not leap from vague source text to strong ontology commitments without recording the transformation rationale.

## 8.3 Representation of Uncertainty Is Mandatory

If the compiler is unsure whether something is a claim, evidence artifact, agent, task, relationship, or temporal anchor, that uncertainty must be represented explicitly.

## 8.4 Preserve Raw Source Anchors

Source spans, row identifiers, record ids, section paths, and source hashes must remain attached throughout the pipeline.

## 8.5 Strong Template Discipline

Compiler output should target known AASL object templates whenever available.

## 8.6 Modular Adapters

Source-specific logic must live in adapters rather than contaminating the compiler core.

## 8.7 Deterministic Emission Order

Within a given compile job and configuration, output ordering must be deterministic.

---

# 9. Compiler Package Boundaries

The compiler subsystem should be implemented as a dedicated package:

`aasc-compiler`

Recommended internal modules:

- `api/` — public compiler entrypoints and request contracts
- `source/` — source envelopes and normalization
- `adapters/` — source-family adapters
- `segmenters/` — document chunking and record segmentation
- `extractors/` — semantic extraction passes
- `ir/` — intermediate representation types
- `mapping/` — ontology and template mapping
- `identity/` — ID and reference assignment
- `emission/` — AASL rendering and bundle emission
- `provenance/` — provenance attachment logic
- `diagnostics/` — compile diagnostics and codes
- `trace/` — compile trace and explainability records
- `quarantine/` — failure packaging and review queues
- `batch/` — corpus and job execution orchestration
- `config/` — compile profiles and policy overlays

The compiler package must not depend on runtime mutation services, memory admission logic, or federation publication side effects.

---

# 10. Compiler Pipeline Overview

The compiler should operate as a staged pipeline.

Source Intake  
→ Source Adapter Selection  
→ Segmentation  
→ Semantic Extraction  
→ Intermediate Representation Assembly  
→ Ontology Mapping  
→ Identity and Reference Assignment  
→ Provenance Attachment  
→ Draft AASL Emission  
→ Parser Pass  
→ Validator Pass  
→ Canonicalization Pass  
→ Admission / Quarantine Routing

Each stage must have explicit inputs, outputs, diagnostics, and trace records.

---

# 11. Source Envelope Model

Before active compilation begins, all incoming material must be wrapped in a normalized source envelope.

## 11.1 Source Envelope Responsibilities

The source envelope provides a stable container for source metadata and content.

It must capture:

- source id
- source kind
- source media type
- origin system or connector
- path, URI, or record locator if available
- acquisition timestamp
- original content hash if available
- normalization hash if applicable
- source language if known
- record boundaries if structured
- ownership / access tags if required

## 11.2 Source Envelope Invariants

The source envelope is immutable for the lifetime of the compile job.

Downstream stages may annotate it through linked trace records, but they must not mutate the source contents or identifying metadata.

---

# 12. Source Adapter Architecture

Adapters convert source-specific material into a normalized compiler-facing form.

## 12.1 Adapter Responsibilities

Adapters are responsible for:

- validating source compatibility
- decoding transport or file structure
- extracting primary textual or structural content
- exposing source segments
- surfacing source-local metadata
- preserving source anchors for provenance

## 12.2 Adapter Types

The first canonical adapter families should include:

- `NaturalLanguageAdapter`
- `MarkdownAdapter`
- `JsonAdapter`
- `TabularAdapter`
- `DraftAaslAdapter`
- `ApiPayloadAdapter`
- `CorpusRecordAdapter`

## 12.3 Adapter Output Contract

Each adapter must produce a normalized adapter output containing:

- source envelope reference
- segment list
- segment hierarchy if applicable
- extracted source-local metadata
- raw content handles or normalized content strings
- adapter diagnostics

## 12.4 Adapter Constraints

Adapters must not directly emit canonical AASL.

Their role is normalization and segmentation, not final semantic emission.

---

# 13. Segmentation Model

Many sources cannot be compiled as a single monolithic block. The compiler therefore requires a segmentation layer.

## 13.1 Segment Types

Examples of segment granularity:

- paragraph
- heading section
- list item
- table row
- JSON object
- event record
- transcript utterance
- document block

## 13.2 Segmentation Objectives

Segmentation should:

- preserve semantic locality
- improve provenance precision
- reduce ambiguity during extraction
- enable incremental recompile
- support partial quarantine instead of whole-document rejection

## 13.3 Segment Identity

Each segment must receive a stable segment id scoped to the source envelope.

Segments should also preserve parent-child relationships where relevant.

---

# 14. Semantic Extraction Layer

The semantic extraction layer transforms normalized source segments into candidate semantic units.

## 14.1 Extraction Responsibilities

The extraction layer is responsible for identifying candidate instances of:

- entities
- tasks
- actions
- claims
- evidence references
- constraints
- timestamps
- provenance anchors
- model or agent identities
- relationships

## 14.2 Extraction Output

Extraction must emit a structured candidate set rather than raw prose assumptions.

Each candidate should include:

- candidate id
- candidate type hypothesis
- source segment reference
- extracted fields
- extraction confidence or bounded certainty marker
- extraction rationale summary
- unresolved ambiguity flags

## 14.3 Extraction Modes

The compiler should support at least three extraction modes.

### Strict mode

Low-risk extraction with conservative emission thresholds.

### Balanced mode

Normal production mode with explicit uncertainty recording.

### Exploratory mode

Broader candidate capture for research, ingestion exploration, or human review.

## 14.4 Extraction Boundary

The extraction layer may identify semantic candidates, but it must not unilaterally claim that a candidate is admissible AASL without passing downstream mapping and validation.

---

# 15. Compiler Intermediate Representation (CIR)

The compiler requires a stable internal representation between extraction and final AASL emission.

This document refers to that representation as the **Compiler Intermediate Representation** or **CIR**.

## 15.1 Why CIR Exists

CIR isolates extraction logic from AASL emission logic.

It allows the compiler to:

- accumulate candidates across segments
- merge related evidence
- attach provenance before emission
- resolve conflicts and ambiguities
- support multiple source adapters through one common structure
- generate compile traces consistently

## 15.2 CIR Node Families

The first CIR should support at minimum:

- `EntityCandidate`
- `ClaimCandidate`
- `EvidenceCandidate`
- `TaskCandidate`
- `ActionCandidate`
- `ConstraintCandidate`
- `TimeCandidate`
- `ReferenceCandidate`
- `RelationshipCandidate`
- `DocumentCandidate`

## 15.3 CIR Invariants

The CIR must be:

- typed
- inspectable
- traceable to source spans or records
- serializable for debugging if needed
- independent of final AASL text formatting

---

# 16. Ontology Mapping Layer

The ontology mapping layer transforms CIR nodes into AASL object families and field templates.

## 16.1 Mapping Responsibilities

The mapping layer is responsible for:

- selecting the appropriate AASL object family
- selecting the correct field template
- mapping source-specific labels into ontology-approved terms
- normalizing enumerations where allowed
- detecting unsupported semantic categories
- routing unresolved concepts to extension or quarantine paths

## 16.2 First-Pass Object Family Mapping

Typical mappings include:

- agent-like entities → `AGT`
- model definitions → `MOD`
- datasets or corpora → `DS`
- tasks → `TSK`
- actions → `ACT`
- claims → `CLM`
- evidence artifacts → `EVD`
- confidence records → `CNF`
- provenance records → `PRV`
- verification records → `VRF`
- constraints → `CST`
- timestamps / time anchors → `TIM`

## 16.3 Template Mapping

Object-family selection alone is insufficient. The compiler must also map candidates into field templates.

Examples:

- a claim template for causal claims
- a claim template for descriptive statements
- an evidence template for citation-backed evidence
- a task template for workflow tasks
- a constraint template for policy constraints

## 16.4 Mapping Failure Classes

The mapping layer must emit explicit failures for:

- no suitable object family
- no suitable template
- required field missing
- conflicting ontology assignments
- prohibited field population
- unresolved enumerations

---

# 17. Identity Assignment Model

The compiler must assign or propose stable identities for emitted objects.

## 17.1 Identity Responsibilities

The identity layer is responsible for:

- assigning draft object ids when none exist
- reusing stable external ids when policy allows
- avoiding collisions inside the compile workspace
- linking repeated source mentions to candidate shared identities when justified
- recording identity provenance and confidence

## 17.2 Identity Classes

The compiler should distinguish:

- source-native identifiers
- compiler-assigned draft identifiers
- canonical identifiers after downstream validation/canonicalization
- temporary session-only identifiers for exploratory workflows

## 17.3 Identity Stability Rules

Identity assignment must be deterministic within a given compile job and configuration.

Where persistent recompile stability is required, identity generation should incorporate stable source anchors and object-class rules rather than arbitrary run order.

## 17.4 Identity Collisions

If two candidates plausibly refer to the same semantic object but the compiler cannot safely merge them, it must not silently collapse them.

Instead it should:

- emit separate draft identities
- create a relationship or equivalence candidate if allowed
- flag the ambiguity for review or downstream reconciliation

---

# 18. Reference Assignment and Linking

AASL objects rarely exist in isolation. The compiler must therefore assign references as well as identities.

## 18.1 Reference Responsibilities

The reference layer is responsible for:

- connecting claims to evidence
- connecting tasks to agents
- connecting actions to targets
- connecting constraints to governed objects
- connecting timestamps to events or claims
- connecting provenance to every emitted object or bundle

## 18.2 Reference States

Each reference should be marked as one of:

- resolved
- unresolved
- provisional
- external
- ambiguous
- invalid

## 18.3 Cross-Segment Linking

The compiler must support reference creation across segments and across records inside a single compile job.

## 18.4 Cross-Document Linking

Where the compiler has access to a known workspace or memory context, it may propose references to existing semantic objects, but such links must remain explicitly marked until validated.

---

# 19. Ambiguity and Uncertainty Model

Ambiguity is a first-class compiler concern, not an edge case.

## 19.1 Sources of Ambiguity

Examples include:

- unclear entity boundaries
- pronoun or alias uncertainty
- multiple possible ontology classes
- partial timestamps
- implied rather than explicit relationships
- missing identifiers
- contradictory source statements
- uncertain evidence support

## 19.2 Mandatory Handling Rule

When ambiguity cannot be safely resolved, the compiler must represent it explicitly rather than guess.

## 19.3 Explicit Ambiguity Records

The compiler should emit machine-readable ambiguity records containing:

- ambiguity id
- affected candidates or fields
- alternative interpretations
- reason for ambiguity
- resolution status
- review recommendation if applicable

## 19.4 Uncertainty Representation in AASL

Where the language permits, uncertainty should be represented through dedicated confidence, provenance, or provisional status fields rather than by omitting the issue.

---

# 20. Provenance Attachment Model

Every compiler-emitted object must retain explicit provenance.

## 20.1 Provenance Minimum Requirements

The compiler must be able to answer:

- what source produced this object
- what segment or record produced it
- what compiler version generated it
- what adapter and extractor path was used
- what transformations occurred before emission
- whether any ambiguity or normalization was applied

## 20.2 Provenance Attachment Scope

Provenance must attach to:

- each emitted object
- each major relationship
- the compile job as a whole
- any quarantine package

## 20.3 Provenance Structure

The compiler should create or populate `PRV` objects or equivalent provenance sections that include:

- source id
- source hash
- segment ids
- extraction stage identifiers
- compiler configuration id
- compile timestamp
- compile trace id

---

# 21. Draft AASL Emission

After mapping and identity assignment, the compiler must render draft AASL.

## 21.1 Emission Responsibilities

The emission layer is responsible for:

- selecting section placement
- ordering emitted objects deterministically
- rendering valid draft syntax
- preserving field-level meaning from CIR nodes
- attaching provenance and confidence records
- generating supporting metadata where required

## 21.2 Emission Output Forms

The compiler should support:

- single-document draft AASL output
- multi-document bundle output
- object-fragment output for embedded workflows
- human-readable annotated draft mode for debugging

## 21.3 Emission Constraints

The compiler must not emit syntactically invalid AASL as normal success output.

If the compiler cannot emit valid AASL text, it must fail the job or route to quarantine.

## 21.4 Emission Ordering

At minimum, output ordering must be deterministic by:

- section
- object family
- stable object id or stable generation key
- field order according to template or draft policy

---

# 22. Parser, Validator, and Canonicalizer Handoff

The compiler is not complete when it has emitted text. It is complete only when downstream formal subsystems have accepted or rejected the emission.

## 22.1 Mandatory Handoff Sequence

Normal handoff sequence:

Draft AASL Emission  
→ Parser  
→ Validator  
→ Canonicalizer  
→ Runtime / Storage / Quarantine

## 22.2 Compiler Obligations During Handoff

The compiler must preserve the relationship between:

- compile diagnostics
- parse diagnostics
- validation diagnostics
- canonicalization diagnostics

This allows a single ingestion job to produce a unified audit trail.

## 22.3 Compiler Success Conditions

Compiler success should be classified at multiple levels.

### Emission success

Draft AASL was rendered.

### Parse success

Rendered AASL parsed successfully.

### Validation success

Output satisfied language and template rules.

### Canonical success

Output canonicalized successfully.

### Admission success

Output became eligible for runtime loading or storage according to higher-level policy.

---

# 23. Compile Trace Model

The compile trace is the primary explainability artifact for the compiler.

## 23.1 Purpose of Compile Trace

The compile trace must let a human or agent answer:

- why an object exists
- which source segment caused its emission
- what interpretation path was taken
- which alternatives were rejected
- where ambiguity remained
- which downstream stage failed if the job did not complete

## 23.2 Compile Trace Events

The trace should record events such as:

- source accepted
- adapter selected
- segment created
- candidate extracted
- candidate merged
- ontology mapped
- id assigned
- reference linked
- ambiguity recorded
- AASL emitted
- parser success/failure
- validator success/failure
- canonicalizer success/failure
- quarantine routed

## 23.3 Trace Identity

Each compile job must receive a stable compile trace id.

Sub-events should have stable event ids and parent-child relationships.

---

# 24. Diagnostics Model

The compiler must produce structured diagnostics rather than only human-readable errors.

## 24.1 Diagnostic Categories

Required categories include:

- source intake diagnostics
- adapter diagnostics
- segmentation diagnostics
- extraction diagnostics
- ontology mapping diagnostics
- identity diagnostics
- reference diagnostics
- emission diagnostics
- handoff diagnostics
- quarantine diagnostics

## 24.2 Diagnostic Payload

Each diagnostic record should include:

- diagnostic code
- severity
- message
- stage
- source reference
- segment reference if applicable
- candidate or object reference if applicable
- recovery or review suggestion where possible

## 24.3 Severity Classes

Recommended severities:

- info
- warning
- error
- fatal
- quarantine-required

---

# 25. Failure Handling and Quarantine

Not all source material can be safely compiled into admissible AASL.

## 25.1 Quarantine Triggers

Quarantine should occur when:

- the source is malformed beyond safe normalization
- extraction cannot produce minimally coherent candidates
- ontology mapping is fundamentally unresolved
- identity or reference ambiguity is unsafe to auto-resolve
- emitted draft cannot parse
- emitted output systematically fails validation
- prohibited source policies block normal conversion

## 25.2 Quarantine Package Contents

A quarantine package should include:

- source envelope reference
- source snapshot or secure handle
- partial CIR if allowed
- diagnostics list
- compile trace id
- stage of failure
- review recommendation

## 25.3 Partial Success Handling

For multi-segment or multi-record jobs, the compiler should prefer partial success over all-or-nothing failure when policy permits.

That means unaffected segments can proceed while failing segments are quarantined independently.

---

# 26. Batch Compilation Architecture

AASL must support large-scale corpus ingestion, not only one-off conversions.

## 26.1 Batch Responsibilities

Batch compilation must support:

- job queues
- resumable compile tasks
- source partitioning
- parallel segment processing where safe
- partial failure tolerance
- deterministic result collation
- audit-friendly job reporting

## 26.2 Batch Job Identity

Each batch job must have:

- batch job id
- source set id or corpus id
- compiler profile id
- start and end timestamps
- success and quarantine counts
- output bundle references

## 26.3 Deterministic Collation

Parallelism must not make final output nondeterministic.

Batch collation must preserve deterministic ordering rules.

---

# 27. Streaming and Incremental Compilation

Some Atrahasis ingestion workflows will be continuous rather than batch-oriented.

## 27.1 Streaming Use Cases

Examples:

- event stream ingestion
- webhook pipelines
- recurring document updates
- chat transcript growth
- append-only research logs

## 27.2 Streaming Requirements

The compiler should support:

- incremental source envelopes
- record-by-record compilation
- replay-safe trace generation
- deduplication hooks
- stable identity continuity where possible

## 27.3 Incremental Recompile

When a source changes, the compiler should recompile the smallest safe unit rather than reprocessing the entire corpus whenever feasible.

---

# 28. Reverse Rendering and Round-Trip Expectations

The compiler is primarily an ingress system, but it must still respect round-trip realities.

## 28.1 Round-Trip Goal

A source converted to AASL and later inspected should still allow an operator to understand the origin and rationale of emitted semantics.

## 28.2 Reverse Rendering Support

The compiler should therefore preserve enough metadata to support:

- source-to-AASL explanation views
- AASL-to-source anchor navigation
- human review interfaces
- diff views across recompiles

---

# 29. Security and Trust Boundaries

The compiler processes untrusted external content and therefore sits on a critical trust boundary.

## 29.1 Security Requirements

The compiler must:

- treat all inbound content as untrusted
- isolate adapter decoding from runtime mutation services
- prevent executable payload interpretation in non-executable sources
- preserve source hashes for tamper awareness
- log compile decisions for auditability

## 29.2 Trust Boundary Rule

Compiler output is not trusted merely because it is structurally valid.

Trust, verification, and admission remain downstream responsibilities.

---

# 30. Performance Expectations

The first canonical compiler does not need premature optimization, but it must be designed for practical production behavior.

## 30.1 Performance Objectives

The compiler should aim for:

- predictable latency for small interactive documents
- scalable throughput for corpus ingestion
- bounded memory usage during large jobs
- deterministic output even under concurrency

## 30.2 Performance Strategy

Recommended strategies include:

- adapter-specific streaming reads where possible
- segment-level processing
- structured IR reuse
- batched identity lookup
- deterministic job collation

---

# 31. Public API Surface

The compiler should expose a narrow and explicit public API.

## 31.1 Core Entry Points

Recommended entry points:

- `compileSource()`
- `compileBatch()`
- `recompileSegment()`
- `emitDraftAasl()`
- `explainCompileTrace()`
- `quarantinePackage()`

## 31.2 Compile Request Contract

A compile request should include:

- source input or source envelope
- source kind
- compiler profile
- extraction mode
- ontology snapshot or registry reference
- identity policy
- output mode
- quarantine policy

## 31.3 Compile Response Contract

A compile response should include:

- compile job id
- compile trace id
- status summary
- draft AASL output or output bundle references
- diagnostics
- quarantine references if any
- downstream parser/validator/canonicalizer results

---

# 32. Configuration Profiles

Different workflows require different compiler behavior. The compiler therefore needs profile-driven configuration.

## 32.1 Example Profiles

- conservative production compile
- research ingestion compile
- exploratory ontology discovery compile
- bulk migration compile
- editor-assisted draft compile

## 32.2 Profile Controls

Profiles may influence:

- extraction thresholds
- ambiguity tolerance
- identity reuse policy
- allowed draft fields
- quarantine strictness
- output annotation verbosity

Profile behavior must be explicit, versioned, and recorded in provenance.

---

# 33. Testing Strategy

The compiler must be tested as a staged semantic system rather than only as a text transformer.

## 33.1 Unit Testing

Test individually:

- source normalization
- adapters
- segmenters
- extractors
- ontology mapping rules
- identity assignment
- reference linking
- emission logic
- diagnostics generation

## 33.2 Golden Tests

Golden tests should assert:

- stable draft AASL output
- stable compile traces
- stable diagnostics ordering
- stable quarantine decisions

## 33.3 Corpus Regression Tests

Maintain a curated corpus of:

- valid conversions
- ambiguous conversions
- known-failure sources
- partial-acceptance jobs
- ontology drift cases

## 33.4 Adversarial Tests

Test for:

- malformed markdown
- inconsistent JSON
- alias collisions
- unsupported object categories
- contradictory source statements
- malicious payloads disguised as documents

---

# 34. Implementation Sequencing

A safe build order for the AASC compiler is as follows.

## Phase 1 — Core skeleton

- source envelopes
- compiler API shell
- compile job identity
- diagnostics framework
- trace framework

## Phase 2 — Adapters and segmentation

- natural language adapter
- markdown adapter
- JSON adapter
- basic tabular adapter
- segmentation layer

## Phase 3 — CIR and extraction

- candidate node types
- extraction passes
- ambiguity records
- provenance anchors

## Phase 4 — Ontology mapping and identity

- object family mapping
- template mapping
- ID assignment
- reference linking

## Phase 5 — Emission and handoff

- draft AASL emitter
- parser handoff
- validator handoff
- canonicalizer handoff
- quarantine packaging

## Phase 6 — Batch and incremental features

- batch jobs
- partial recompile
- streaming support
- deterministic collation

## Phase 7 — Tooling and explainability

- compile trace viewers
- source-to-AASL inspection tools
- review queues
- annotated emission mode

---

# 35. Canonical Non-Negotiables

The following rules are mandatory for any compliant AASC implementation.

1. The compiler must not silently invent unsupported semantic facts.  
2. The compiler must preserve explicit provenance for emitted objects.  
3. The compiler must represent ambiguity explicitly rather than bury it.  
4. The compiler must pass normal output through the parser and validator.  
5. The compiler must maintain deterministic output for fixed inputs and configuration.  
6. The compiler must keep adapter logic modular and source-specific.  
7. The compiler must expose compile traces and structured diagnostics.  
8. The compiler must quarantine unsafe or inadmissible outputs rather than force admission.  
9. The compiler must preserve the boundary between structuring information and verifying truth.  
10. The compiler must remain ontology-aware but not ontology-hardcoded in ways that block extension.

---

# 36. Closing Statement

The AASC Compiler is the mechanism that allows Atrahasis to convert the outside world into formal semantic language.

It is therefore one of the most important trust-boundary subsystems in the entire architecture.

If it is under-specified, Atrahasis will ingest noise, drift, and silent semantic corruption. If it is designed correctly, it becomes the disciplined transformation layer that allows external documents, datasets, payloads, and human-authored text to become reliable AASL-native knowledge artifacts.

The compiler must therefore be treated not as a convenience parser, but as a **semantic conversion engine with strict provenance, deterministic structure, explicit ambiguity handling, and auditable output generation**.
