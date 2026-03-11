# Atrahasis AASL Conversion Pipeline Specification

**Document ID:** ATR-AASL-CONVERT-001  
**Title:** Atrahasis AASL Conversion Pipeline Specification  
**Status:** Canonical Draft  
**Version:** 1.0.0  
**Authoring Context:** Atrahasis / AASL Core System  
**Last Updated:** 2026-03-08  
**Applies To:** Markdown-to-AASL, JSON-to-AASL, structured dataset-to-AASL, corpus ingestion, batch conversion, provenance capture, ambiguity management, reversible rendering, conversion profiles, and conversion-time admission controls.

---

## 1. Purpose

This document defines the canonical **conversion pipeline layer** for the Atrahasis Agentic Semantic Language (AASL). The conversion pipeline is the system that transforms external information sources into semantically valid AASL artifacts without collapsing provenance, structure, ambiguity, or operational auditability.

AASL cannot rely only on hand-authored `.aas` documents. A complete ecosystem requires the ability to ingest:

- human-authored Markdown documents,
- JSON objects and API payloads,
- tabular and record-oriented datasets,
- mixed corpora containing multiple source types,
- legacy semantic artifacts that predate AASL,
- machine-generated outputs that must be normalized into stable semantic form.

The purpose of this specification is to ensure that conversion into AASL is:

1. **Deterministic** under a declared conversion profile.
2. **Traceable** back to the source evidence that produced each semantic object.
3. **Loss-aware** when the source cannot be represented exactly.
4. **Composable** with the parser, validator, compiler, runtime, query engine, file infrastructure, and developer tooling.
5. **Scalable** from single files to large corpora.
6. **Reversible where feasible** so humans and systems can inspect or re-render transformed material.
7. **Safe for admission** into Atrahasis knowledge environments.

The conversion pipeline is not a convenience adapter. It is the formal bridge between external content and the internal semantic operating substrate of Atrahasis.

---

## 2. Scope

This specification covers:

- Canonical conversion architecture
- Source adapters and ingestion contracts
- Source classification and routing
- Intermediate representations used during conversion
- Markdown conversion
- JSON conversion
- Structured dataset conversion
- Multi-document and corpus conversion workflows
- Provenance capture and attribution rules
- Ambiguity management and human-review escalation
- Loss accounting and non-representable content policies
- Canonical output generation into `.aas`
- Optional generation of sidecar artifacts
- Batch processing and queue orchestration
- Conversion diagnostics and reporting
- Profile-driven conversion behavior
- Determinism, reproducibility, and security requirements
- Testing and conformance requirements

This specification does **not** redefine the AASL language grammar itself, the runtime object model, or the query algebra, except where those systems impose input or output contracts on conversion.

---

## 3. Design Principles

### 3.1 Semantics over syntax

The pipeline must convert source material into stable semantic structures, not merely wrap source text in AASL syntax.

### 3.2 Provenance is first-class

Every non-trivial semantic object produced by conversion must preserve enough provenance to explain where it came from and how it was derived.

### 3.3 Deterministic under profile

Given the same source material, profile, ontology version, and tool version, the conversion result must be reproducible.

### 3.4 Explicit ambiguity

When the source permits multiple reasonable interpretations, the pipeline must represent uncertainty explicitly rather than pretending certainty.

### 3.5 Loss must be visible

If some source information cannot be represented natively in AASL, the pipeline must report the loss and, where possible, preserve it in sidecar or attachment form.

### 3.6 Human override without silent drift

Humans may steer conversion, but every override must be declared, attributable, and reviewable.

### 3.7 Batch-safe by design

The same semantics must apply whether converting one file interactively or millions of records in a distributed corpus run.

### 3.8 Conversion is admission-critical

Converted artifacts must not bypass validator, policy, or closure requirements merely because they were machine-produced.

---

## 4. Conversion Layer Overview

The canonical conversion layer consists of cooperating stages.

| Stage | Primary Role | Key Outputs |
|---|---|---|
| Source Acquisition | obtain source bytes and metadata | source envelope |
| Source Classification | detect source type and profile | routing decision |
| Structural Parsing | extract source-native structure | source IR |
| Semantic Extraction | identify candidate entities, relations, assertions, events, constraints | semantic candidates |
| Ontology Mapping | align candidates to AASL types and modules | mapped semantic graph |
| Identity & Linking | assign IDs and resolve references | linked graph |
| Ambiguity Handling | preserve competing interpretations or request review | ambiguity set |
| Validation Preflight | check representability and profile compliance | preflight report |
| Canonical Emission | render `.aas` output and sidecars | AASL artifact set |
| Admission Handoff | pass outputs into validator/runtime/storage pipeline | conversion package |

The conversion pipeline is therefore neither a pure parser nor a pure compiler. It is a staged semantic transduction system.

---

## 5. Canonical Architecture

```text
External Source
   ↓
Source Envelope Builder
   ↓
Classifier / Router
   ├─ Markdown Adapter
   ├─ JSON Adapter
   ├─ Dataset Adapter
   ├─ Mixed Corpus Adapter
   └─ Future Custom Adapter
   ↓
Source IR
   ↓
Semantic Extraction Layer
   ↓
Mapping / Normalization Layer
   ↓
Identity / Linking Layer
   ↓
Ambiguity & Loss Manager
   ↓
Conversion Preflight Validator
   ↓
Canonical AASL Emitter
   ├─ .aas
   ├─ provenance sidecar
   ├─ conversion report
   ├─ diagnostics
   └─ patch / review queue payload
   ↓
Admission into Validator / Runtime / Storage
```

Each layer must operate on stable contracts. Direct source-to-text generation without intermediate contracts is non-canonical.

---

## 6. Core Concepts

### 6.1 Source envelope

A **source envelope** is the canonical metadata wrapper around source content. It must include at minimum:

- source identifier
- source URI or origin descriptor if available
- source type
- byte hash
- capture timestamp
- declared encoding if known
- media type
- profile selection
- trust tier
- source owner or authority metadata if available
- processing constraints

### 6.2 Source IR

A **source IR** is the normalized structural representation of a source before ontology mapping. It should preserve source-native hierarchy as much as possible.

Examples:

- Markdown IR preserving headings, paragraphs, lists, tables, links, code fences, callouts, quotations, and anchors.
- JSON IR preserving objects, arrays, scalar values, key paths, ordering semantics where required, and nullability.
- Dataset IR preserving rows, columns, schema hints, column statistics, inferred types, and source partitions.

### 6.3 Semantic candidate

A **semantic candidate** is a not-yet-final assertion, entity, relation, event, constraint, or policy element extracted from source material.

### 6.4 Mapping profile

A **mapping profile** declares how a class of sources should be transformed into AASL. It includes:

- source assumptions
- ontology/module preferences
- field-to-type mappings
- confidence thresholds
- naming policies
- ID assignment policy
- provenance granularity
- ambiguity escalation rules
- output segmentation rules

### 6.5 Conversion package

A **conversion package** is the full output of a conversion run, including the `.aas` artifact and all supporting sidecars, diagnostics, and review metadata.

---

## 7. Conversion Modes

The canonical pipeline shall support the following modes.

### 7.1 Interactive conversion

Used by developers, operators, or agents during active authoring. Must prioritize fast diagnostics, partial results, and explainability.

### 7.2 Batch conversion

Used for corpus-scale ingestion. Must prioritize throughput, resumability, deterministic sharding, and aggregated reporting.

### 7.3 Assisted conversion

Used when machine conversion may propose outputs but requires human review for low-confidence regions.

### 7.4 Strict conversion

Used for regulated or mission-critical content where ambiguity or non-representable data causes hard failure rather than best-effort emission.

### 7.5 Preservation-first conversion

Used when semantic extraction is intentionally conservative and source fidelity is prioritized over aggressive normalization.

---

## 8. Source Classification and Routing

Before semantic extraction begins, every source must be classified.

The classifier shall determine:

- whether the source is Markdown, JSON, dataset, mixed archive, or unsupported
- whether a declared profile already exists for the source class
- whether the source is complete, fragmented, or streaming
- whether source metadata implies a trust or compliance tier
- whether the source should be routed to single-document or corpus conversion

Routing may be based on:

- file extension
- media type
- content sniffing
- schema signature
- repository conventions
- profile binding rules
- explicit operator override

Classifier outcomes must be recorded in the conversion report.

---

## 9. Intermediate Representation Stack

To prevent semantic collapse, the pipeline must maintain layered representations.

| Layer | Role |
|---|---|
| Raw Source | original bytes or stream |
| Structural IR | source-native parse tree or table model |
| Extraction IR | candidate semantic units and evidence spans |
| Mapping IR | typed, ontology-aligned semantic units |
| Linked IR | identity-assigned graph with resolved references |
| Emission IR | render-ready canonical AASL object set |

No stage may discard information required by a later stage unless the loss is explicitly reported.

---

## 10. Markdown-to-AASL Conversion

### 10.1 Supported Markdown source classes

The canonical Markdown adapter must support at minimum:

- CommonMark-compatible prose
- heading hierarchies
- ordered and unordered lists
- tables
- links and references
- blockquotes
- fenced code blocks
- inline code
- admonition-like callouts if detectable
- front matter when present

### 10.2 Markdown structural extraction

The Markdown adapter shall produce a structural IR preserving:

- document title or inferred title
- heading tree
- section boundaries
- paragraph boundaries
- list nesting
- table coordinates
- quote nesting
- code block fences and declared languages
- inline anchors and links
- source span offsets

### 10.3 Markdown semantic extraction strategies

The adapter should identify candidate semantic structures such as:

- definitions
- requirements
- normative statements
- roles and actors
- process steps
- system components
- policies
- constraints
- failure modes
- timelines
- tables of mappings or enumerations

Markdown prose often contains latent semantics. The converter must transform these into explicit AASL objects where confidence is sufficient.

### 10.4 Heading semantics

Heading levels must influence semantic scoping but must not alone determine ontology type. A heading called `Security` does not automatically produce a `SecurityPolicy` object without supporting content.

### 10.5 Table handling

Markdown tables require special handling because they often encode enumerations, mappings, or operational matrices. The adapter shall:

- infer whether the table is relational, enumerative, or descriptive
- preserve headers and cell coordinates
- attach row/column provenance
- flag merged-meaning or malformed tables for review

### 10.6 Code fences in Markdown

Code fences are not automatically executable semantics. The adapter must preserve them as evidence blocks, examples, or attached artifacts unless a profile explicitly defines executable mapping behavior.

### 10.7 Markdown output segmentation

Large Markdown sources may be emitted as:

- one `.aas` document with nested modules,
- multiple `.aas` documents partitioned by section,
- a package containing a root document and imported fragments.

Segmentation policy must be profile-driven and deterministic.

---

## 11. JSON-to-AASL Conversion

### 11.1 Supported JSON source classes

The JSON adapter must support:

- canonical JSON documents
- API payloads
- configuration objects
- event streams batched as arrays
- schema-bound records
- nested object graphs
- nullable and optional field patterns

### 11.2 Structural extraction for JSON

The JSON adapter shall preserve:

- full key paths
- array indices
- scalar values and types
- nulls
- object boundaries
- schema hints if available
- field ordering when semantically meaningful under profile

### 11.3 Mapping strategies for JSON

JSON conversion may operate in one of three modes:

1. **Schema-bound mapping** where a known schema maps directly to AASL ontology types.
2. **Heuristic mapping** where field names, value patterns, and shape signatures infer candidate types.
3. **Wrapper mapping** where JSON is preserved mostly as structured evidence with minimal semantic lifting.

### 11.4 Identity from JSON

IDs may be derived from:

- declared primary keys,
- stable field combinations,
- canonical path plus source ID,
- profile-defined synthetic identity rules.

Identity derivation must be deterministic and collision-audited.

### 11.5 Arrays and collections

Arrays require explicit interpretation. The pipeline must distinguish between:

- lists of entities,
- ordered process steps,
- time series,
- key-value tuples,
- sparse collections,
- append-only event logs.

A JSON array is not semantically neutral and must not be mapped blindly.

### 11.6 Null and missing values

The converter must distinguish:

- field absent,
- field present but null,
- field unknown,
- field redacted,
- field not applicable.

Profiles may collapse some of these states only if explicitly configured.

---

## 12. Structured Dataset-to-AASL Conversion

### 12.1 Supported dataset classes

The dataset adapter shall support structured sources such as:

- CSV-like tabular files
- TSV-like files
- spreadsheet exports after normalization
- database extracts
- parquet-like logical tables after reader adaptation
- data warehouse query outputs

### 12.2 Dataset source IR

The dataset IR must preserve:

- dataset identity
- schema version if known
- columns and inferred types
- row count and partition metadata
- primary key candidates
- foreign key candidates
- null distributions
- unit hints
- source filters or query provenance

### 12.3 Dataset mapping modes

The pipeline shall support:

- row-as-entity conversion
- row-as-event conversion
- row-as-assertion conversion
- aggregate-to-summary conversion
- dimension/fact dual conversion for analytical models

### 12.4 Column interpretation

Columns may represent:

- scalar properties,
- enum categories,
- references to external objects,
- timestamps,
- measurements with units,
- state labels,
- confidence values,
- provenance fields.

Column interpretation must be profile-driven where possible and statistically assisted only where profiles are absent.

### 12.5 Relational linking

When multiple datasets are converted together, the pipeline should infer or apply:

- foreign key relationships,
- temporal joins,
- codebook resolution,
- dimension normalization,
- cross-file entity unification.

### 12.6 Scale considerations

Dataset conversion must support chunked execution, deterministic partitioning, and checkpoint resume. A corpus-scale data import cannot require full materialization in memory.

---

## 13. Mixed Corpus Conversion

A corpus may include Markdown specs, JSON APIs, datasets, logs, and manually curated AASL fragments. The mixed corpus adapter shall provide:

- per-source-type routing
- shared identity registry across the run
- cross-document linking
- duplicate detection
- conflict reporting
- package-level provenance rollup
- staged re-conversion when only subsets change

Corpus conversion is a first-class mode, not an afterthought.

---

## 14. Semantic Extraction Layer

The extraction layer identifies candidate semantic units from the source IR.

It shall be capable of extracting at minimum:

- entities
- types
- attributes
- references
- relationships
- events
- procedures
- obligations
- permissions
- prohibitions
- metrics
- thresholds
- assumptions
- invariants
- dependencies
- evidence blocks

Every extracted candidate must retain evidence references back to the source IR.

Extraction may be implemented using deterministic rules, schemas, controlled heuristics, or model-assisted methods, but the output contract must remain stable regardless of technique.

---

## 15. Ontology Mapping Layer

The ontology mapping layer aligns extracted candidates to AASL types, modules, predicates, and structural conventions.

### 15.1 Mapping responsibilities

The mapper shall:

- select target ontology modules
- assign candidate types
- normalize field names into canonical property names
- enforce unit normalization when configured
- determine relation directionality
- classify statements as facts, claims, requirements, hypotheses, or examples

### 15.2 Mapping confidence

Every non-trivial mapping should carry confidence metadata or an equivalent decision trace unless the mapping is profile-hardcoded.

### 15.3 Competing mappings

If two mappings are plausible, the pipeline shall:

- preserve both as alternatives,
- choose one and record the losing candidate,
- or escalate for human review,

according to profile policy.

### 15.4 Ontology version pinning

Mappings must record the ontology version and module signatures used during conversion so future re-conversion can explain drift.

---

## 16. Identity, Reference Resolution, and Linking

The linking layer creates a coherent graph.

### 16.1 ID assignment requirements

IDs must be:

- deterministic under profile,
- stable across reruns when source semantics do not materially change,
- collision-detectable,
- namespace-aware,
- reproducible across distributed batch workers.

### 16.2 Reference resolution

References may resolve against:

- local document scope,
- package scope,
- corpus registry,
- known ontology registries,
- external authority registries if allowed by policy.

### 16.3 Duplicate detection

The pipeline must detect likely duplicates and classify them as:

- exact duplicate,
- semantic duplicate,
- conflicting duplicate,
- unresolved near-match.

### 16.4 Link provenance

Every non-trivial link should record the basis of the link, such as schema constraint, key match, text normalization, or human override.

---

## 17. Ambiguity Management

Ambiguity is expected and must be handled as a formal subsystem.

### 17.1 Ambiguity classes

The pipeline shall classify ambiguity at minimum as:

- lexical ambiguity
- structural ambiguity
- referential ambiguity
- type ambiguity
- temporal ambiguity
- authority ambiguity
- unit ambiguity
- scope ambiguity
- contradiction ambiguity

### 17.2 Canonical handling options

A profile may specify one of the following actions for each ambiguity class:

- fail conversion
- emit alternatives
- choose highest-confidence interpretation
- mark unresolved and preserve evidence
- route to review queue

### 17.3 Review payloads

When escalation occurs, the pipeline must generate review payloads containing:

- source excerpt or coordinates
- competing interpretations
- confidence or rationale
- recommended decision
- downstream impact estimate

---

## 18. Loss Accounting and Non-Representable Content

Not all source material maps cleanly into AASL.

Examples include:

- complex visual layout with semantic significance
- images lacking machine-readable annotation
- malformed or contradictory tables
- intentionally ambiguous narrative prose
- executable code whose semantics are out of scope for the active ontology

The pipeline shall maintain a **loss ledger** describing:

- what information was not represented directly,
- why it was not represented,
- whether it was preserved as attachment or sidecar,
- whether human review is recommended.

No silent semantic discard is permitted in canonical mode.

---

## 19. Provenance Model

Provenance is mandatory.

### 19.1 Provenance granularity

The pipeline must support provenance at multiple levels:

- source-level provenance
- section-level provenance
- field-level provenance
- assertion-level provenance
- link-level provenance
- review-decision provenance

### 19.2 Required provenance elements

At minimum, provenance records should include:

- source ID
- source hash
- source coordinates or spans
- adapter version
- profile version
- ontology version
- conversion run ID
- worker or executor ID where relevant
- timestamps
- decision trace references

### 19.3 Derived assertions

Assertions inferred from multiple source elements must record all principal evidence inputs and the rule or model class that created the synthesis.

---

## 20. Conversion Preflight and Admission Controls

Before emitting final `.aas` artifacts, the pipeline must run a preflight phase.

Preflight shall check:

- representability under active ontology
- mandatory field completeness
- ID stability constraints
- reference integrity
- profile compliance
- policy restrictions
- prohibited source types or trust tiers
- closure requirements for partial graphs
- known validator blockers

Preflight is not the final validator, but it must catch predictable failures before emission.

---

## 21. Canonical Output Artifacts

A canonical conversion run may emit the following artifacts.

| Artifact | Required | Purpose |
|---|---|---|
| `.aas` document or package | Yes | canonical semantic output |
| provenance sidecar | Yes | fine-grained attribution |
| conversion report | Yes | summary of decisions, counts, outcomes |
| diagnostics file | Yes | warnings, errors, ambiguities, losses |
| review queue payload | Conditional | unresolved or low-confidence decisions |
| patch suggestions | Conditional | recommended human edits |
| re-render snapshot | Optional | human-readable transformed view |
| metrics manifest | Optional | operational telemetry summary |

### 21.1 Output determinism

Artifact ordering, serialization, ID emission order, and formatting must be deterministic.

### 21.2 Package emission

If conversion spans multiple logical documents, outputs should be emitted as an AASL package with an explicit root manifest.

---

## 22. Conversion Profiles

Profiles are the principal mechanism for domain-specific conversion control.

A conversion profile may specify:

- source classes covered
- adapter options
- ontology module bindings
- field mapping rules
- naming and ID policies
- confidence thresholds
- loss tolerance
- ambiguity routing rules
- output partitioning
- review requirements
- prohibited inferences
- normalization rules
- unit systems
- trust-tier behavior

Profiles must be versioned and treated as first-class configuration artifacts.

---

## 23. CLI and API Contracts

### 23.1 Canonical CLI commands

A canonical implementation should support commands similar to:

```text
aasl convert source.md --profile spec-doc
aasl convert payload.json --profile api-record
aasl convert data.csv --profile tabular-events
aasl convert-corpus ./repo --profile mixed-corpus
aasl convert --resume run_2026_03_08_001
```

### 23.2 Expected CLI output classes

The CLI must be able to produce:

- human-readable summaries
- machine-readable reports
- diagnostics in structured form
- emitted artifact paths
- review queue references
- stable exit codes

### 23.3 Programmatic API

A programmatic conversion API should expose:

- source submission
- profile selection
- dry run
- partial conversion
- structured diagnostics
- artifact retrieval
- resume tokens
- review resolution submission

---

## 24. Batch Orchestration and Distributed Execution

Corpus-scale conversion requires formal orchestration.

### 24.1 Batch run requirements

Batch conversion must support:

- deterministic sharding
- idempotent work units
- checkpointing
- resume after failure
- duplicate suppression
- worker-safe ID generation
- run-level metrics
- run-level provenance manifests

### 24.2 Queue model

A canonical queue-based implementation should distinguish:

- source intake queue
- parse/extract queue
- mapping/linking queue
- review escalation queue
- emission queue
- admission queue

### 24.3 Retry behavior

Retries must not create semantically divergent outputs. Retried work units must either reproduce the same artifacts or be flagged as non-deterministic failure.

---

## 25. Human-in-the-Loop Review

Some source classes require review.

### 25.1 Review triggers

Review may be triggered by:

- ambiguity above threshold
- ontology mismatch
- unresolved references
- collision risk
- prohibited inferred claims
- excessive information loss
- low trust source tier
- contradictions across sources

### 25.2 Review outcomes

Review may:

- approve proposed mapping
- choose among alternatives
- edit mappings or IDs
- mark content as unconvertible
- defer object creation
- request ontology extension

All review decisions must be persisted as provenance-bearing overrides.

---

## 26. Reversibility and Re-rendering

AASL conversion is not always perfectly reversible, but the system should preserve enough information to support useful re-rendering.

Re-rendering goals include:

- human inspection of converted Markdown meaning
- regeneration of structured JSON views where mappings are near-isomorphic
- evidence-centric audit displays
- diffing between source revisions and re-converted outputs

Profiles should declare whether reversibility is expected, approximate, or not guaranteed.

---

## 27. Diagnostics, Error Classes, and Exit Semantics

### 27.1 Diagnostic classes

The pipeline shall emit diagnostics classified at minimum as:

- fatal
- error
- warning
- advisory
- ambiguity
- loss
- policy violation
- review required

### 27.2 Canonical conversion error categories

Canonical error categories should include:

- unreadable source
- unsupported encoding
- malformed structure
- profile not found
- ontology mismatch
- identity collision
- unresolved reference
- ambiguous mapping
- prohibited inference
- emission failure
- non-determinism detected

### 27.3 Exit semantics

CLI and APIs must expose stable completion states such as:

- success
- success with warnings
- success requiring review
- partial success
- failed preflight
- failed conversion
- failed emission
- failed admission handoff

---

## 28. Security and Trust Boundaries

Conversion operates at a trust boundary because it transforms external material into internal semantic state.

### 28.1 Required security controls

The conversion subsystem must support:

- untrusted source isolation
- size and complexity limits
- parser abuse defenses
- malicious payload detection hooks
- path and URI sanitization
- content-type validation
- policy-based network isolation for remote sources
- redaction handling when sources contain sensitive data

### 28.2 Trust tiers

Profiles and admission policy may vary by trust tier, such as:

- trusted internal authoritative sources
- verified external authoritative sources
- unverified external sources
- model-generated sources
- anonymous or adversarial sources

Trust tier must influence allowable inferences and review requirements.

---

## 29. Performance and Scalability Requirements

A canonical implementation should aim for:

- incremental conversion for large text sources
- streaming row processing for datasets
- bounded memory growth per work unit
- deterministic parallelism
- cached ontology and profile resolution
- reusable source fingerprints for change detection

Performance optimizations must not weaken provenance fidelity or determinism.

---

## 30. Integration with Other AASL Subsystems

### 30.1 Parser integration

The emitter must produce `.aas` output that the canonical parser can re-parse without semantic drift.

### 30.2 Validator integration

All emitted artifacts must pass through validator policy before admission.

### 30.3 Runtime integration

Converted objects must be loadable into the runtime registry using the standard object lifecycle.

### 30.4 Query engine integration

Provenance, source coordinates, and conversion diagnostics should be queryable after admission.

### 30.5 File infrastructure integration

The conversion package must conform to canonical file layout and sidecar conventions.

### 30.6 Developer tooling integration

The CLI, language server, semantic explorer, and review tools must be able to inspect conversion traces and artifacts.

---

## 31. Testing and Conformance

A canonical implementation must include a conformance suite covering:

- Markdown heading and table conversion
- JSON nested object conversion
- dataset row/event conversion
- mixed corpus linking
- ambiguity emission
- loss reporting
- deterministic rerun equivalence
- ID stability under unchanged input
- controlled drift under changed ontology versions
- review override persistence
- malicious or malformed input handling

### 31.1 Goldens

The system should maintain golden test fixtures containing:

- source input
- profile
- expected `.aas` output
- expected provenance sidecar
- expected diagnostics
- expected loss ledger

### 31.2 Differential testing

Where model-assisted or heuristic components exist, differential testing must ensure the final structured contracts remain stable across versions.

---

## 32. Recommended Initial Deliverables

The first canonical implementation wave should produce at minimum:

1. Markdown adapter
2. JSON adapter
3. CSV/tabular dataset adapter
4. conversion profile schema
5. provenance sidecar schema
6. conversion report schema
7. review queue schema
8. deterministic ID policy library
9. mixed corpus batch runner
10. conformance test corpus

These deliverables establish the minimum viable full-spectrum conversion layer for AASL ingestion.

---

## 33. Non-Goals

The conversion pipeline is not intended to:

- replace the validator
- silently invent ontology extensions during routine conversion
- treat every source token as semantically meaningful
- guarantee perfect reversibility in all cases
- bypass trust, policy, or closure controls
- execute arbitrary source code during conversion

---

## 34. Acceptance Criteria

This specification is considered implemented only when all of the following are true:

1. Markdown, JSON, and tabular datasets can each be converted through a declared profile into deterministic `.aas` outputs.
2. Every emitted semantic object carries adequate provenance to trace back to its source basis.
3. Ambiguity and information loss are surfaced explicitly rather than silently hidden.
4. Corpus-scale conversion supports resumable, idempotent distributed execution.
5. Conversion outputs integrate cleanly with parser, validator, runtime, query, and file infrastructure contracts.
6. Human review can resolve low-confidence decisions without breaking determinism or auditability.
7. A conformance suite proves stability across representative source classes.

---

## 35. Closing Statement

AASL becomes truly operational only when external knowledge can be brought into the system without semantic corruption. The conversion pipeline is therefore a core language subsystem. It is the disciplined machinery that turns prose, payloads, datasets, and mixed corpora into traceable semantic state.

Without this layer, AASL remains hand-authored and narrow. With it, Atrahasis gains a principled ingestion path from the outside world into an auditable agentic semantic operating environment.
