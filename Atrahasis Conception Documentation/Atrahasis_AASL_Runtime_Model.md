# Atrahasis AASL Runtime Model

Version: 1.0.0  
Status: Canonical Subsystem Specification  
Date: 2026-03-08

---

# 1. Purpose

This document defines the canonical architecture for the **AASL Runtime Model**, the subsystem that converts parsed AASL into active, addressable, stateful semantic objects inside the Atrahasis system.

If the parser turns AASL source text into structured syntax, the runtime turns that structure into **live semantic state** that agents, validators, canonicalizers, storage engines, query systems, and developer tools can operate against.

This document exists to fully specify:

- runtime role and system position
- runtime design principles
- object model and in-memory representation
- loading and hydration pipeline
- registries and indexes
- reference resolution model
- document and workspace handling
- lifecycle and state management
- mutation and transaction rules
- query-facing contracts
- provenance and verification attachment model
- conflict handling
- extensibility boundaries
- performance expectations
- package boundaries
- testing strategy
- implementation sequencing

The runtime does **not** define the language grammar, the validator’s admissibility logic, the canonicalizer’s normalization rules, or the query engine’s full declarative language. It provides the operational substrate on which those systems depend.

---

# 2. System Role

The AASL Runtime Model is the semantic execution substrate of the AASL ecosystem.

It sits between parsed structure and every subsystem that needs to work with semantic objects as more than raw text.

High-level position in Atrahasis:

External Source or `.aas` Document  
→ File Reader / Source Intake  
→ AASL Parser  
→ Validator / Canonicalizer  
→ **AASL Runtime Model**  
→ Query Engine / Agents / Memory / Storage / Visualization / Tooling

The runtime may also host non-final objects during authoring and compilation workflows:

English / Markdown / JSON / Dataset  
→ AASC Compiler  
→ Draft AASL  
→ Parser  
→ **Runtime Draft Workspace**  
→ Validation / Canonicalization / Verification  
→ Canonical Runtime / Storage / Federation

Because of this role, the runtime must support both:

- strict canonical production pipelines
- tolerant authoring and editor workflows
- batch compiler ingestion workflows
- multi-document semantic workspaces
- agent-driven mutation and verification workflows

---

# 3. Architectural Objectives

The runtime must satisfy the following system objectives.

## 3.1 Semantic Operability

Parsed objects must become operational semantic entities that can be looked up, traversed, inspected, validated, canonicalized, mutated under control, and exported.

## 3.2 Deterministic Identity

Object identity must remain stable across load, validation, canonicalization, and export, unless versioning or supersession explicitly creates a new identity.

## 3.3 State Visibility

Every meaningful semantic state transition must be explicit and inspectable. The runtime must never hide whether an object is unresolved, invalid, unverified, dirty, disputed, or immutable.

## 3.4 Multi-Document Coherence

The runtime must treat a collection of AASL artifacts as a semantic workspace rather than a sequence of isolated files.

## 3.5 Controlled Mutability

Draft knowledge must be editable. Stable knowledge must be protected. The runtime must distinguish mutable working state from immutable trusted state.

## 3.6 Loss Awareness

The runtime must preserve enough source and semantic context for diagnostics, reverse rendering, provenance tracing, conflict analysis, and canonical re-emission.

## 3.7 Extensibility

The core runtime must support future ontology modules, new object families, future storage backends, and policy overlays without redesigning the entire object system.

## 3.8 Query Readiness

The runtime must expose a stable substrate for exact lookup, traversal, filtering, relationship analysis, provenance inspection, and higher-level semantic retrieval.

---

# 4. Scope of Responsibility

The runtime is responsible for:

- instantiating typed runtime objects from AST nodes
- preserving object identity and source metadata
- maintaining object and document registries
- resolving references and tracking unresolved links
- tracking lifecycle, mutability, and trust state
- supporting controlled mutation and transactional updates
- exposing runtime APIs for other subsystems
- supporting semantic traversal and query prerequisites
- supporting canonical and non-canonical co-existence
- preserving provenance and verification attachments
- tracking document membership and cross-document relationships
- surfacing conflicts, duplicates, disputes, and supersession
- supporting export-ready object representation

The runtime is **not** responsible for:

- parsing raw AASL text
- deciding ontology legality by itself
- proving canonical ordering rules
- determining claim truth
- executing distributed federation protocols by itself
- enforcing final governance decisions
- replacing the query engine with ad hoc search logic

---

# 5. Runtime Position in the AASL Stack

The runtime is the first subsystem where AASL becomes a living semantic graph instead of a structured textual artifact.

Its main dependency and consumer relationships are:

## 5.1 Depends On

- file intake and source envelopes
- parser CST/AST output
- symbol and reference tables from parse stage
- ontology definitions and object templates
- validation and canonicalization services

## 5.2 Feeds

- validator re-check and selective validation workflows
- canonicalizer and hash generation workflows
- query engine
- semantic memory and storage engine
- agent orchestration and task systems
- visualization and inspection tooling
- CLI, editor, and repository tooling
- export and reverse-render pipelines

## 5.3 Interacts Bidirectionally With

- mutation manager
- verification manager
- provenance systems
- document manager
- storage admission layer
- versioning and supersession layer

---

# 6. Core Runtime Concepts

The runtime is built around six core concepts.

## 6.1 Runtime Object

A live semantic object representing one parsed AASL entity in machine-operable form.

## 6.2 Runtime Graph

The full network of runtime objects and their typed references, attachments, and state relations.

## 6.3 Runtime Workspace

A loaded environment containing one or more documents, indexes, caches, policies, and mutation context.

## 6.4 Runtime State

The explicit lifecycle and quality state associated with each object and document.

## 6.5 Runtime Transaction

A staged unit of change that can be validated, committed atomically, or rolled back.

## 6.6 Runtime View

A scoped representation over the graph for query, tooling, document inspection, conflict analysis, or agent interaction.

---

# 7. Runtime Layers

The runtime must be internally layered so it does not collapse into a single undifferentiated memory store.

## 7.1 Object Layer

Holds typed semantic objects and their field values.

## 7.2 Reference Layer

Maintains typed links, attachment edges, reverse edges, and unresolved references.

## 7.3 State Layer

Tracks lifecycle, validation, canonicalization, verification, mutability, and dirty state.

## 7.4 Document Layer

Tracks source documents, section membership, namespaces, and multi-document workspace state.

## 7.5 Mutation Layer

Handles creation, update, deletion, supersession, merge, and transaction control.

## 7.6 Query Substrate Layer

Provides the lookup, traversal, filtering, and indexing primitives on which the query engine is built.

## 7.7 Emission Layer

Supports export back into canonical `.aas`, AASL-JSON, future AASL-Binary, and inspection-oriented render forms.

---

# 8. Runtime Inputs and Handoff Contracts

The runtime receives structured artifacts from earlier subsystems.

## 8.1 Required Inputs

At minimum, the runtime loader must be able to receive:

- AST nodes or equivalent semantic parse output
- source document identity
- parser diagnostics
- symbol table
- outbound reference table
- parse spans and offsets
- section membership metadata
- parse mode metadata

## 8.2 Optional Inputs

When available, the runtime may also receive:

- precomputed canonical forms
- validation results
- source hashes
- source revision identifiers
- compiler-origin metadata
- authoring environment context
- ontology module activation context

## 8.3 Handoff Guarantees

The parser-to-runtime handoff must guarantee:

- deterministic object enumeration order
- stable object source spans
- declared object type availability
- explicit reference token visibility
- explicit diagnostic visibility
- no hidden parser-only semantics

---

# 9. Runtime Object Model

The runtime must not operate on raw parser nodes indefinitely. It needs a stable in-memory semantic object model.

Every runtime object must preserve its declared AASL object type and must expose a consistent structural shape regardless of storage backend or execution environment.

Each runtime object should include:

- object type
- object ID
- field map
- typed reference map
- attachment map
- source document identity
- source section identity
- source parse span
- source parser diagnostics summary
- validation state
- canonical state
- verification state
- mutability state
- dirty state
- conflict state
- version lineage metadata
- runtime-local metadata

A runtime object is therefore not just “parsed data.” It is an operational unit of semantic knowledge.

---

# 10. Canonical Runtime Object Fields

Every runtime object must expose a canonical minimum field model.

## 10.1 Identity Fields

- `object_id`
- `object_type`
- `document_id`
- `workspace_id`
- `version_id` if versioned

## 10.2 Source Fields

- `source_section`
- `source_span_start`
- `source_span_end`
- `source_revision`
- `source_hash` if known

## 10.3 Semantic Fields

- `declared_fields`
- `normalized_fields` when canonicalized
- `typed_references`
- `attached_objects`

## 10.4 State Fields

- `load_state`
- `resolution_state`
- `validation_state`
- `canonical_state`
- `verification_state`
- `mutability_state`
- `dirty_state`
- `conflict_state`

## 10.5 Runtime Metadata Fields

- `created_at_runtime`
- `updated_at_runtime`
- `last_validated_at`
- `last_canonicalized_at`
- `last_verified_at`
- `extension_slots`

---

# 11. Object Typing Model

The runtime must preserve AASL’s object typing exactly.

Core object families include, at minimum:

- `AGT` agent identity
- `MOD` model definition
- `DS` dataset
- `TSK` task
- `ACT` action
- `CLM` claim
- `EVD` evidence
- `CNF` confidence
- `PRV` provenance
- `VRF` verification
- `CST` constraint
- `TIM` timestamp

The runtime must not erase type boundaries by collapsing everything into generic JSON-like maps. Generic storage may exist internally, but the public runtime contract must preserve typed semantics.

---

# 12. Runtime Loading Process

The process of entering the runtime must be explicit and reproducible.

## 12.1 Step 1: Receive Parse Result

The parser outputs AST nodes, diagnostics, symbol tables, and reference tables.

## 12.2 Step 2: Instantiate Runtime Objects

Each AST node becomes a runtime object of the correct type.

## 12.3 Step 3: Register Objects

Objects are placed in runtime registries indexed by identity, type, section, and document.

## 12.4 Step 4: Resolve References

Fields such as `actor`, `target`, `subject`, and `object` are linked to referenced runtime objects when resolvable.

## 12.5 Step 5: Assign Initial Runtime State

Each object is marked with explicit state such as:

- loaded
- unresolved or resolved
- validation pending
- canonical or non-canonical
- verified, pending, rejected, or disputed where applicable

## 12.6 Step 6: Attach Source Metadata

The runtime preserves source document identity, source section, parse span, and diagnostics.

## 12.7 Step 7: Publish Workspace View

The loaded semantic graph becomes available to validators, canonicalizers, agents, tooling, and query subsystems according to policy.

---

# 13. Runtime Registries

To support efficient lookup and traversal, the runtime must maintain internal registries.

## 13.1 Object Registry

Maps object ID to runtime object.

Examples:

- `ag.research.01` → Agent object
- `ds.climate.44` → Dataset object
- `c.correlation.001` → Claim object

## 13.2 Type Registry

Groups objects by type.

Examples:

- all `AGT` objects
- all `CLM` objects
- all `VRF` objects

## 13.3 Section Registry

Tracks which objects originated from which document section.

## 13.4 Document Registry

Tracks loaded documents, document versions, namespaces, and document membership.

## 13.5 Reference Registry

Tracks inbound and outbound references.

Examples:

- what objects reference `c.correlation.001`
- what objects are referenced by `a.analyze.201`

## 13.6 State Registry

Indexes objects by lifecycle and quality state.

Examples:

- all unresolved objects
- all invalid objects
- all verified immutable objects
- all disputed claims

## 13.7 Conflict Registry

Tracks duplicates, shadows, supersessions, disputes, and unresolved identity collisions.

These registries are foundational to every runtime API.

---

# 14. Reference Resolution Model

Because AASL is reference-based, reference handling is central.

The runtime must distinguish between the following categories.

## 14.1 Direct Scalar Values

Examples:

- `role:research`
- `status:verified`
- `val:0.92`

## 14.2 Identifier References

Examples:

- `actor:ag.research.01`
- `target:c.correlation.001`
- `dataset:ds.climate.44`

## 14.3 Deferred References

References that could not be resolved at load time.

## 14.4 External References

References pointing to known but not locally loaded objects, remote namespaces, or future federated resources.

The runtime must maintain unresolved and external references as first-class state rather than silently discarding them.

This matters because:

- tolerant and editor modes may load incomplete documents
- distributed documents may reference knowledge not yet loaded
- later hydration may resolve missing objects
- batch loading may resolve references only after all documents are present

---

# 15. Reference Edge Model

Reference resolution must produce a typed edge system rather than generic untyped pointers.

Each reference edge should preserve:

- source object ID
- target object ID if resolved
- source field name
- edge semantic type
- resolution status
- source span of the reference token
- whether the edge is primary, secondary, or attachment-like
- whether the target is local, external, deferred, or invalid

This enables traversal, provenance tracing, conflict analysis, and precise diagnostics.

---

# 16. Unresolved Reference Handling

The runtime must make unresolved references visible, queryable, and recoverable.

Each unresolved reference record should include:

- referencing object ID
- referencing field
- unresolved target token
- reason for unresolved state
- first observed timestamp
- most recent resolution attempt timestamp
- workspace and document scope
- suggested remediation if available

Common unresolved causes include:

- missing object in current workspace
- duplicate ambiguous target
- invalid target type
- malformed identifier
- remote-only target not hydrated
- load order incomplete

Unresolved references must never be silently converted into null semantics.

---

# 17. Runtime State Model

Every runtime object must have explicit lifecycle state.

At minimum, state should include:

- parsed
- loaded
- resolved or unresolved
- validated or invalid
- canonical or non-canonical
- verified, pending, rejected, or disputed where applicable
- mutable or immutable
- dirty or clean
- active, shadowed, superseded, or deleted-in-workspace where applicable

These are not mere implementation details. They are part of how AASL becomes safe and useful.

A verified claim should often be treated differently from an unverified draft claim, even when both share similar structural fields.

---

# 18. Object Lifecycle

Objects in the runtime must move through a clear lifecycle.

## 18.1 Draft

Object has entered runtime but has not yet passed validation and canonicalization.

## 18.2 Structured

Object is syntactically parsed, instantiated, and loaded.

## 18.3 Validated

Object has passed structural, schema, and ontology validation.

## 18.4 Canonical

Object has been normalized into canonical structure suitable for stable hashing and deterministic export.

## 18.5 Verified

Object has attached verification state sufficient for the active trust policy.

## 18.6 Immutable

Object is frozen for stable knowledge use, publication, and repeatable hashing.

This lifecycle matters because Atrahasis is not just storing text. It is managing knowledge quality and semantic maturity.

---

# 19. Document State Model

The runtime must also track state at the document level.

Each document should expose:

- load state
- validation state
- canonicalization state
- document hash state
- mutation state
- conflict state
- trust tier
- workspace visibility
- export eligibility

A document may contain a mixture of object-level states, but the runtime still needs document-level summary state for tooling, storage, and publication workflows.

---

# 20. Mutability Model

Not every object should be arbitrarily editable.

The runtime must distinguish between:

## 20.1 Mutable Working Objects

Draft and active workspace objects that may be edited, revalidated, re-canonicalized, or deleted under policy.

## 20.2 Protected Objects

Objects that may be readable and traversable but only updatable by privileged mutation flows.

## 20.3 Immutable Canonical Objects

Verified stable knowledge objects that must not be edited in place.

When immutable objects must change, the runtime must support:

- new version creation
- supersession records
- replacement records
- lineage tracking
- deprecation or retirement state

This preserves traceability and long-term correctness.

---

# 21. Dirty State and Derived State

The runtime must distinguish between canonical truth, mutable draft state, and derived state.

## 21.1 Dirty State

An object becomes dirty when a mutation changes any field, attachment, or reference state such that previous validation or canonicalization status may no longer be trusted.

## 21.2 Derived State

Certain values may be derived from existing semantic structures, such as:

- effective verification summary
- conflict summary
- transitive provenance summary
- trust tier summary
- document-level object counts

Derived state must never overwrite raw source semantics. It must remain separable and recomputable.

---

# 22. Transactions and Update Safety

Because AASL is intended for distributed and agentic systems, updates must not be sloppy.

The runtime must support transactional update semantics.

This means:

- changes may be staged
- changes may be validated before commit
- related changes may be committed atomically
- failed updates may be rolled back
- emitted events must correspond to committed state only

Examples:

- adding a claim and its confidence together
- updating verification state only if the target exists
- canonicalizing multiple objects as one unit
- superseding an immutable object with a new version atomically

---

# 23. Mutation Operations

The runtime must support controlled updates.

Mutation types include:

- adding objects
- editing fields
- resolving references
- attaching confidence, provenance, or verification objects
- re-canonicalizing changed objects
- deleting draft objects where allowed
- merging workspace branches
- superseding immutable objects through versioned replacement

Every mutation operation must declare:

- target scope
- actor or system identity
- mutation intent
- expected preconditions
- validation requirements
- commit strategy
- rollback behavior

---

# 24. Runtime Query Substrate

The runtime must provide semantic access, not just dictionary lookup.

Agents and tools should be able to ask questions like:

- get object by ID
- get all claims
- get all claims targeting a given subject
- get all actions performed by an agent
- get confidence for a claim
- get verification state for a claim
- get provenance trail for an object
- get all unresolved references
- get all immutable verified objects in a document

This means the runtime needs both direct lookup APIs and graph traversal primitives.

The dedicated query engine later expands this into a full retrieval layer, but the runtime must provide the substrate.

---

# 25. Lookup APIs

At minimum, the runtime API should support:

- `get_by_id(id)`
- `get_many_by_ids(ids)`
- `get_by_type(type)`
- `get_by_document(document_id)`
- `get_by_section(section_name)`
- `get_by_state(state_filter)`
- `exists(id)`

These APIs must return deterministic results, explicit error states, and policy-compliant visibility.

---

# 26. Relationship APIs

The runtime must expose stable relationship access.

At minimum:

- `get_references_from(id)`
- `get_references_to(id)`
- `get_attachments(id)`
- `get_confidence_for_claim(id)`
- `get_verification_for_object(id)`
- `get_provenance_for_object(id)`
- `get_supersession_chain(id)`
- `get_conflicts_for_object(id)`

These are core semantic APIs, not convenience wrappers.

---

# 27. Filter and Traversal APIs

The runtime must support graph-aware traversal and filtering.

Examples include:

- filter all `CLM` objects with `verification_state = pending`
- traverse all evidence supporting a claim
- traverse from an action to produced claims
- collect all objects in a provenance chain
- list all unresolved references within a document
- list all objects shadowed by a later version

Traversal must respect scope, policy, and cycle handling rules.

---

# 28. Runtime and Validation

The validator is a separate subsystem, but the runtime must integrate with it tightly.

The runtime should support:

- validation on load
- validation on mutation
- selective validation of changed objects
- validation state caching
- invalidation of validation state after relevant mutation

The runtime must never assume every loaded object is valid unless validation has actually run.

Each object should therefore track:

- validation pending
- validation passed
- validation failed
- validation warnings present

---

# 29. Runtime and Canonicalization

Canonicalization is not only a one-time preprocessing artifact.

The runtime must be able to work with both draft and canonical objects.

It must support:

- draft load
- canonicalization request
- canonical state update or replacement
- dirty state tracking after mutation
- re-hashing readiness after canonical change

A common flow is:

- parser loads draft AASL
- runtime stores draft objects
- canonicalizer transforms them
- runtime updates canonical forms
- hash generator operates on canonical state

So the runtime must support both pre- and post-canonical states without ambiguity.

---

# 30. Runtime and Verification State

Verification is a native part of AASL, so the runtime must model it directly.

A claim should not merely exist as a `CLM` object. The runtime must also understand its associated:

- confidence
- provenance
- verification status
- verification method
- verification hash
- verification lineage when updated over time

The runtime should therefore support semantically meaningful attachment patterns such as:

- claim → confidence
- claim → provenance entries
- claim → verification record

These are not arbitrary links and should be accessible through dedicated APIs.

---

# 31. Runtime and Provenance

Provenance is equally important.

The runtime must allow systems to ask:

- where did this claim come from
- what source document contributed to this object
- what action generated this result
- what parse span originated this node
- what transformed this object into canonical form
- what agent or subsystem mutated it

Provenance must exist at two levels.

## 31.1 Source Provenance

Document origin, parse span, section identity, source revision, and compiler or authoring origin.

## 31.2 Semantic Provenance

Referenced `PRV` objects and semantic lineage carried inside AASL itself.

The runtime must preserve both.

---

# 32. Runtime and Documents

The runtime must not only manage individual objects. It must also manage document membership.

It must know:

- which objects belong to which loaded document
- what document versions are loaded
- what section each object came from
- whether multiple documents define overlapping objects
- whether two documents conflict or complement one another
- whether one document supersedes another

The runtime must support both:

- object-centric view
- document-centric view

---

# 33. Multi-Document Workspace Model

A real AASL system will load more than one document.

The runtime must support a multi-document environment where:

- multiple `.aas` files are loaded simultaneously
- objects can reference objects defined in other documents
- shared memory can merge many semantic sources
- document-level namespaces can be tracked
- conflicts can be detected and surfaced
- local draft workspaces can coexist with canonical baselines

This turns the runtime from a file interpreter into a semantic workspace.

---

# 34. Namespaces and Scope

The runtime must support scope without undermining object identity.

Relevant scope dimensions include:

- workspace scope
- document scope
- section scope
- namespace scope
- trust tier scope
- visibility scope
- agent authorization scope

Objects may be globally unique, document-local, or workspace-staged depending on policy and lifecycle.

Namespace handling must remain explicit so that cross-document loading does not create silent semantic ambiguity.

---

# 35. Conflict Handling

Once multiple documents and updates are possible, the runtime must handle conflicts explicitly.

Common conflict cases include:

- duplicate IDs from two documents
- conflicting claim definitions
- multiple verification records with incompatible statuses
- type mismatch under same identity
- document-local draft object colliding with canonical object
- two versions of the same object both marked active

The runtime must support conflict states such as:

- duplicate
- shadowed
- superseded
- disputed
- ambiguous target
- invalid merge candidate

The runtime must not guess silently.

---

# 36. Supersession and Version Lineage

Stable knowledge must evolve without destroying history.

The runtime must support:

- object version creation
- supersession chains
- replacement relationships
- retirement or deprecation state
- lineage traversal
- current-effective-object resolution

This allows canonical immutable objects to remain historically stable while newer knowledge becomes operationally current.

---

# 37. Deletion Model

Deletion in AASL runtime must be conservative.

## 37.1 Draft Deletion

Draft objects may be deleted in workspace contexts when policy allows.

## 37.2 Canonical Deletion

Canonical immutable objects should generally not be physically deleted from trusted knowledge stores. They should instead become superseded, deprecated, retired, hidden by policy, or marked invalid.

## 37.3 Reference-Safe Deletion

Deletion workflows must detect inbound dependencies and either block deletion, stage related updates, or produce an explicit orphaned-reference state.

---

# 38. Caching Strategy

Because the runtime will be heavily accessed, it should support caching.

Relevant cache layers include:

- parsed document cache
- instantiated object cache
- resolved reference cache
- canonical object cache
- verification lookup cache
- query substrate cache
- document summary cache

Cache must never obscure source truth. It must preserve consistency with:

- runtime mutation state
- document version state
- validation invalidation rules
- authorization and visibility policy

---

# 39. Serialization and Emission

The runtime must support turning live semantic objects back into serialized forms.

That includes:

- canonical `.aas`
- AASL-JSON
- future AASL-Binary
- human-readable summaries via reverse rendering

The runtime must preserve sufficient structure and metadata for loss-aware export.

It must distinguish between:

- original parse order
- canonical export order
- inspection order used by tools

The file writer later uses this, but the runtime must maintain the underlying structured state.

---

# 40. Runtime Security and Isolation

Because AASL may become part of distributed agent infrastructure, the runtime must support isolation and safety.

This includes:

- controlled mutation permissions
- document sandboxing where required
- protection against malformed object injection
- size and complexity limits
- reference explosion protection
- restricted APIs for untrusted contexts
- state transition guards
- audit logging for sensitive mutations

Not every agent should have permission to mutate every object or observe every workspace.

---

# 41. Policy Integration

The runtime must be policy-aware without becoming policy-defined.

The runtime core should expose hooks for:

- authorization checks
- state transition guards
- publication gating
- trust tier gating
- mutation privilege checks
- workspace visibility checks

Policy logic may live elsewhere, but the runtime must provide the enforcement points.

---

# 42. Performance Expectations

The runtime must be designed for predictable performance.

At minimum, the architecture should target:

- constant-time exact lookup by object ID under normal registry conditions
- efficient grouped access by type, document, section, and state
- amortized efficient reference traversal through indexed edges
- selective revalidation and selective re-canonicalization after mutation
- partial reload and incremental workspace updates

Performance must not come at the cost of semantic correctness, state visibility, or provenance integrity.

---

# 43. Failure Modes

The runtime must fail visibly and safely.

Common failure categories include:

- unresolved reference storms
- duplicate identity collisions
- invalid state transitions
- partial transaction failure
- document load inconsistency
- mutation against immutable objects
- stale cache exposure
- authorization mismatch
- export of non-admissible artifacts as canonical

Failure handling principles:

- fail explicitly
- preserve diagnostics
- preserve recoverable state when possible
- never silently coerce semantic ambiguity into false certainty

---

# 44. Internal Runtime Architecture

Internally, the runtime should be divided into major subcomponents.

## 44.1 Runtime Loader

Receives AST and instantiates runtime objects.

## 44.2 Object Store

Holds runtime objects and primary identity indexes.

## 44.3 Reference Resolver

Maintains local, external, deferred, and reverse links.

## 44.4 State Manager

Tracks validation, canonicalization, verification, mutability, dirty state, and lifecycle transitions.

## 44.5 Document Manager

Tracks loaded documents, membership, sections, versions, and workspace scope.

## 44.6 Mutation Manager

Handles safe updates, transactional staging, rollback, and supersession flows.

## 44.7 Query Core

Provides lookup, filtering, and traversal primitives.

## 44.8 Export Manager

Supports serialization back to `.aas`, JSON, and future binary forms.

## 44.9 Runtime API Layer

Exposes interfaces to agents, tools, canonicalizers, validators, and storage systems.

This modular structure keeps the runtime maintainable and testable.

---

# 45. Package Boundaries

A production implementation should keep runtime modules separated.

Suggested package boundaries:

- `runtime.loader`
- `runtime.objects`
- `runtime.registry`
- `runtime.references`
- `runtime.state`
- `runtime.documents`
- `runtime.mutation`
- `runtime.transactions`
- `runtime.querycore`
- `runtime.export`
- `runtime.policy`
- `runtime.events`
- `runtime.testing`

No single package should own parser logic, canonicalization logic, validator logic, and runtime mutation logic all at once.

---

# 46. Event Model

The runtime should emit explicit internal events for important state changes.

Examples:

- object loaded
- reference resolved
- reference unresolved
- validation state changed
- canonical state changed
- verification attached
- mutation committed
- transaction rolled back
- conflict detected
- supersession recorded
- document reloaded

These events are useful for tooling, observability, indexing, and future distributed synchronization.

---

# 47. Agent Interface Model

Agents should not manipulate raw AASL text directly once runtime APIs exist.

They should work through runtime contracts.

Agents should be able to:

- request semantic objects
- retrieve claims and supporting evidence
- inspect verification state
- submit new draft objects
- request canonicalization
- attach provenance or verification data
- stage transactional updates
- inspect unresolved dependencies

This makes the runtime the semantic interface layer for agent operations.

---

# 48. Tooling Interface Model

Developer tools will depend heavily on the runtime.

Tooling-facing capabilities include:

- object inspection
- document exploration
- unresolved reference review
- conflict inspection
- state transition tracing
- supersession chain visualization
- canonical vs draft comparison
- export preview

Tooling must rely on runtime contracts rather than private memory internals.

---

# 49. Storage Interface Model

The storage layer and runtime must be tightly integrated but separable.

The runtime must expose enough information for storage systems to:

- persist objects and documents
- preserve lifecycle state
- preserve provenance and verification attachments
- persist conflict and supersession records
- snapshot workspaces
- restore prior runtime state
- materialize indexes for efficient retrieval

The runtime is the live substrate. Storage is the persistence substrate. The boundary must remain clean.

---

# 50. Testing Strategy

The runtime must have a comprehensive conformance and regression test strategy.

## 50.1 Object Instantiation Tests

Verify that AST nodes produce the correct runtime object type and field model.

## 50.2 Registry Tests

Verify identity, type, document, section, state, and conflict indexes.

## 50.3 Reference Resolution Tests

Verify resolved, unresolved, ambiguous, and external reference handling.

## 50.4 Lifecycle Tests

Verify legal and illegal state transitions.

## 50.5 Mutation and Transaction Tests

Verify staging, commit, rollback, revalidation, and dirty-state propagation.

## 50.6 Multi-Document Tests

Verify cross-document references, collisions, shadowing, and workspace membership.

## 50.7 Provenance and Verification Tests

Verify semantic attachment integrity and retrieval behavior.

## 50.8 Export Tests

Verify loss-aware serialization and canonical re-emission readiness.

## 50.9 Policy and Security Tests

Verify mutation permissions, visibility controls, and safety limits.

---

# 51. Implementation Sequence

Recommended implementation order:

## 51.1 Phase 1: Core Object Instantiation

Implement runtime object classes, object registry, and document loader.

## 51.2 Phase 2: Reference Resolution

Implement typed references, reverse edges, and unresolved reference tracking.

## 51.3 Phase 3: State Management

Implement lifecycle, mutability, dirty-state, validation-state, and canonical-state tracking.

## 51.4 Phase 4: Mutation and Transactions

Implement safe update APIs, staged commits, and rollback behavior.

## 51.5 Phase 5: Query Substrate

Implement lookup, filtering, traversal, and relationship primitives.

## 51.6 Phase 6: Multi-Document Workspace

Implement namespace handling, conflict registry, and workspace-wide views.

## 51.7 Phase 7: Export and Tooling Hooks

Implement serialization support, inspection hooks, and event emission.

---

# 52. Relationship to Other AASL Components

The runtime fits into the broader AASL ecosystem like this.

Depends on:

- parser
- file reader
- source envelopes
- object type and ontology definitions

Feeds:

- validator
- canonicalizer
- query engine
- storage engine
- visualization system
- CLI and IDE tooling
- agent interfaces

Interacts bidirectionally with:

- mutation/update systems
- export/writer systems
- verification metadata systems
- governance and policy layers

The runtime is therefore the central operating substrate for all live AASL semantics.

---

# 53. What the Runtime Changes About AASL

Before the runtime exists, AASL is:

- a specification
- a parser target
- a structured text format
- a canonicalizable artifact

After the runtime exists, AASL becomes:

- an in-memory semantic graph
- an operational machine language
- a queryable knowledge substrate
- an active interface for agents and tools
- a controlled environment for semantic updates and verification

This is the point where AASL stops feeling like a markup format and starts behaving like a semantic operating language.

---

# 54. Final Summary

The **AASL Runtime Model** is the layer that turns parsed AASL into active machine knowledge. It loads typed semantic objects into memory, resolves references, organizes them into registries and document scopes, tracks validation, canonicalization, verification, mutability, and conflict state, exposes lookup and mutation APIs, and supports export back into canonical forms.

It is the bridge between:

- parsed semantic structure
- live semantic operation

Without it, AASL can be read.  
With it, AASL can be used.

---

# 55. Next Canonical Document

The next document to generate should be:

**Atrahasis_AASC_Compiler_Architecture.md**

That is the correct next step because, once the parser and runtime are fully specified, the compiler becomes the subsystem that explains how English, Markdown, JSON, datasets, and mixed external inputs are transformed into canonical AASL for production use.
