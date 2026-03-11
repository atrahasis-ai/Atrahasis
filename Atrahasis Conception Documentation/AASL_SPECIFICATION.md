# AASL Specification
## Atrahasis Agent Specification Language

**Document Status:** Canonical Bootstrap Specification  
**Version:** 1.0.0  
**Applies To:** Atrahasis AASL authoring, parsing, validation, compilation, storage, query, federation, and runtime interoperability  
**Normative Language:** The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are to be interpreted as normative requirement levels.

---

## 1. Purpose

AASL is the canonical declarative language used by Atrahasis to represent agents, tasks, tools, memory resources, workflows, policies, messages, events, execution contexts, and semantic relationships in a form that is simultaneously:

1. human-readable,
2. machine-parseable,
3. semantically constrained,
4. compilable into normalized graph structures,
5. safe for multi-agent exchange,
6. durable for storage and retrieval,
7. governable over time through explicit ontology evolution.

AASL exists to solve a recurring failure mode in agentic systems: agents can generate plans, messages, and structured outputs, but those outputs are often not stable enough to serve as long-lived system objects. AASL defines the object language that closes that gap.

---

## 2. Design Goals

A conforming AASL ecosystem MUST satisfy the following design goals:

### 2.1 Human Legibility
AASL documents MUST remain readable to humans without requiring binary tooling or hidden execution semantics.

### 2.2 Semantic Determinism
The same valid AASL document MUST compile to the same canonical semantic representation under the same ontology version.

### 2.3 Layer Separation
Syntax, validation, semantics, execution, storage, and governance MUST remain separable layers.

### 2.4 Safe Extensibility
The language MUST support namespace-based extension without collapsing interoperability.

### 2.5 Canonical Identity
Every durable object represented in AASL MUST admit stable identity rules.

### 2.6 Partial Operability
Implementations SHOULD be able to parse, validate, and compile documents even when some optional runtime services are unavailable.

### 2.7 Auditability
All admitted AASL artifacts SHOULD support provenance, version traceability, validation traceability, and semantic diffability.

---

## 3. Scope

This specification defines the minimum interoperable standard for:

- AASL document model
- lexical and structural rules
- object identity rules
- module and namespace model
- schema and typing model
- relation model
- validation classes
- compilation targets
- canonicalization requirements
- storage expectations
- query expectations
- federation expectations
- security and policy attachment points
- compatibility and evolution model

This specification does **not** define:

- a single parser implementation,
- a single storage backend,
- a single runtime engine,
- a single editor or CLI,
- proprietary model weights or execution logic.

---

## 4. Conceptual Model

AASL treats the world as a typed semantic graph expressed through declarative source documents.

An AASL document contains declarations. Declarations define objects. Objects have properties, relations, constraints, provenance, and lifecycle metadata. Objects may reference one another by stable identifiers. Documents compile into canonical semantic graphs. Runtimes consume those graphs to drive execution, orchestration, analysis, and governance.

At minimum, the model includes the following conceptual layers:

1. **Source Layer**: `.aas` author text
2. **Syntax Layer**: tokens, blocks, declarations, references, literals
3. **Structural Layer**: CST/AST forms
4. **Semantic Layer**: typed objects and relations
5. **Canonical Layer**: normalized semantic graph
6. **Operational Layer**: runtime-resolved objects and executable bindings
7. **Governance Layer**: ontology versioning, compatibility, policy, admission

---

## 5. Core Entity Classes

A conforming implementation MUST support the ability to represent at least the following conceptual classes, whether as built-in types or standardized ontology modules:

- Agent
- Role
- Capability
- Tool
- Task
- Workflow
- Plan
- Message
- Event
- State
- Resource
- MemoryNode
- MemoryStore
- Policy
- Constraint
- Contract
- Dataset
- Evaluation
- Runtime
- Queue
- Scheduler
- Trigger
- Identity
- CredentialReference
- Namespace
- Module
- Ontology
- ProvenanceRecord
- AuditRecord

Implementations MAY provide additional classes through extension namespaces.

---

## 6. Document Model

### 6.1 Document Units
An AASL source document is a UTF-8 text artifact that SHALL normally use the `.aas` extension.

### 6.2 Logical Sections
An AASL document SHOULD contain, where applicable:

- document metadata
- imports
- namespace declarations
- type declarations
- object declarations
- relation declarations
- policy declarations
- validation hints
- export or publication directives

### 6.3 Multi-Document Systems
AASL systems MAY be composed of multiple documents. Cross-document references MUST be resolvable through import, namespace, registry, or explicit resolver policy.

### 6.4 Document Identity
A document MAY define an explicit document identifier. If omitted, the system MAY derive a content-addressable or repository-qualified identifier.

### 6.5 Comments
Comments MAY exist and MUST NOT affect compiled semantics.

---

## 7. Namespaces and Modules

### 7.1 Namespace Requirement
Every non-trivial AASL deployment MUST support namespaces.

### 7.2 Purpose
Namespaces prevent type collision, support ontology evolution, and enable extension without semantic ambiguity.

### 7.3 Module Structure
A module is a coherent set of declarations that may export:

- types,
- relations,
- constraints,
- aliases,
- macros if supported by the implementation,
- version metadata,
- deprecation metadata.

### 7.4 Import Semantics
Imports MUST be explicit or canonically inferable. Hidden ambient imports SHOULD be avoided in production systems.

### 7.5 Reserved Namespaces
Implementations SHOULD reserve a system namespace for Atrahasis core semantics, and MAY reserve implementation namespaces for parser/runtime internals.

---

## 8. Syntax Principles

This bootstrap specification is syntax-principled rather than grammar-exhaustive. Full grammar is defined by the parser architecture document and reference grammar.

A conforming syntax layer MUST support the following abstract constructs:

### 8.1 Declaration
A declaration introduces a named or anonymous semantic object.

### 8.2 Assignment
A property or field may be assigned a literal, reference, collection, block, or expression form supported by the ontology.

### 8.3 Reference
A reference points to another object by stable identifier, local symbol, qualified path, or resolver form.

### 8.4 Block Structure
Nested blocks MUST be representable in a deterministic way.

### 8.5 Collections
Lists, sets, or maps MAY be supported, but their canonicalization rules MUST be explicit.

### 8.6 Literals
Implementations MUST support at least:

- string literals
- numeric literals
- boolean literals
- null-like absence form or omitted-field semantics
- identifiers
- references

### 8.7 Source Spans
Parser-capable implementations SHOULD preserve source span information for diagnostics and tooling.

---

## 9. Type System

### 9.1 Typed Objects
AASL is a typed specification language. Objects MUST have either:

- an explicit declared type, or
- a type inferable from a governing declaration context.

### 9.2 Type Kinds
Implementations SHOULD support:

- primitive types,
- structured record types,
- enumerations,
- relation types,
- union-like admissibility forms,
- constrained scalar forms,
- collection types,
- reference types.

### 9.3 Required vs Optional Fields
The ontology layer MUST define which fields are required, optional, repeated, derived, or prohibited.

### 9.4 Type Refinement
Extensions MAY refine base types so long as compatibility contracts are respected.

### 9.5 Validation and Types
Syntactic validity does not imply semantic type validity. Type validation MUST occur as a distinct pass or clearly defined integrated pass.

---

## 10. Identity Model

### 10.1 Stable Identity
Durable objects SHOULD have stable identifiers.

### 10.2 Identifier Sources
Identifiers MAY be:

- author-assigned,
- system-assigned,
- content-derived,
- namespace-qualified,
- registry-issued.

### 10.3 Local Symbols
Local symbols MAY be used during authoring but SHOULD resolve to stable canonical identifiers by compile time or admission time.

### 10.4 Identity Immutability
Once admitted into a durable registry, an object's canonical identifier MUST NOT change unless explicitly superseded through versioning policy.

### 10.5 Aliases
Aliases MAY exist, but one canonical identity MUST be designated.

---

## 11. Relation Model

AASL is not purely record-oriented; it is graph-oriented.

### 11.1 First-Class Relations
Relations SHOULD be representable as first-class semantic structures when provenance, constraints, or edge properties matter.

### 11.2 Edge Semantics
A relation MAY include:

- source object
- target object
- relation type
- role labels
- directionality
- cardinality semantics
- temporal validity
- confidence or provenance
- policy overlays

### 11.3 Referential Integrity
A conforming validator SHOULD verify relation endpoint admissibility.

---

## 12. Constraints and Policy Attachments

### 12.1 Constraint Semantics
AASL MUST permit the declaration of semantic constraints over objects, fields, or relations.

### 12.2 Policy Semantics
AASL SHOULD permit policy attachments that influence:

- admission,
- visibility,
- execution permission,
- mutation permission,
- retention,
- federation export,
- confidentiality,
- redaction,
- escalation behavior.

### 12.3 Separation of Fact and Policy
Core object semantics SHOULD remain separable from policy overlays where possible.

---

## 13. Provenance

### 13.1 Provenance Support
AASL systems SHOULD preserve provenance for authored and compiled objects.

### 13.2 Provenance Dimensions
Provenance MAY include:

- author
- originating agent
- source document
- import chain
- generation toolchain
- compile version
- ontology version
- admission timestamp
- review status
- evidence links

### 13.3 Provenance Non-Interference
Changing provenance metadata alone SHOULD NOT alter semantic identity unless the ontology explicitly defines it as identity-bearing.

---

## 14. Validation Model

A conforming AASL stack MUST support validation as a first-class lifecycle stage.

### 14.1 Validation Layers
Validation SHOULD distinguish among:

1. lexical validity
2. syntactic validity
3. structural validity
4. reference validity
5. type validity
6. ontology validity
7. policy validity
8. admission validity
9. compatibility validity

### 14.2 Diagnostic Severity
Diagnostics SHOULD support at least:

- fatal
- error
- warning
- advisory

### 14.3 Repair
Implementations MAY provide repair suggestions, but MUST NOT silently mutate meaning-critical semantics without explicit policy.

---

## 15. Canonicalization

### 15.1 Purpose
Canonicalization ensures deterministic semantic representation independent of benign authoring variance.

### 15.2 Canonicalization Responsibilities
Canonicalization SHOULD define rules for:

- normalized identifiers
- field ordering where relevant
- collection normalization
- whitespace-insensitive structure
- import expansion behavior
- default-value materialization policy
- alias resolution
- reference normalization
- ontology version pinning

### 15.3 Output
Canonicalization MUST produce a stable internal representation suitable for semantic comparison, hashing, compilation traceability, or storage.

---

## 16. Compilation

### 16.1 Compilation Role
Compilation transforms AASL source into normalized semantic structures consumable by runtimes, graph stores, query engines, and governance layers.

### 16.2 Compiler Expectations
A conforming compiler SHOULD support:

- source parsing
- symbol resolution
- type resolution
- ontology binding
- identity assignment or normalization
- constraint lowering
- relation expansion
- provenance capture
- semantic graph emission
- diagnostics emission

### 16.3 Partial Compilation
Compilation MAY proceed in partial mode for authoring environments, but production admission SHOULD require policy-defined completeness.

---

## 17. Runtime Interoperability

### 17.1 Runtime Independence
AASL is not itself an execution engine. It is the declarative substrate from which runtime engines operate.

### 17.2 Runtime Binding
Runtime systems MAY bind AASL objects to:

- live agents,
- queues,
- schedulers,
- memory stores,
- external tools,
- policy guards,
- orchestration channels.

### 17.3 Runtime Fidelity
A runtime MUST NOT reinterpret core semantic content in ways that violate admitted ontology meaning.

### 17.4 Runtime State
Ephemeral runtime state MAY be represented in AASL-derived forms, but systems SHOULD distinguish durable declarative truth from transient operational state.

---

## 18. Storage Expectations

AASL does not require a specific storage engine, but admitted objects SHOULD be storable in a manner that preserves:

- canonical identity
- type information
- relation information
- provenance
- version history
- validation state
- policy state

Common storage targets MAY include:

- graph stores,
- relational projections,
- document stores,
- event logs,
- content-addressed artifacts,
- registry indexes.

---

## 19. Query Expectations

### 19.1 Queryability
Compiled AASL semantic graphs SHOULD be queryable through a deterministic query layer.

### 19.2 Query Domains
The query system SHOULD support queries over:

- object identity
- type
- field values
- relations
- provenance
- policy visibility
- graph reachability
- temporal/version dimensions

### 19.3 Query Safety
Queries MUST respect policy and visibility constraints where applicable.

---

## 20. Federation

### 20.1 Federated Exchange
AASL SHOULD support object exchange across registries, runtimes, organizations, or agent collectives.

### 20.2 Federated Requirements
Federated use SHOULD define explicit handling for:

- namespace collision
- trust boundaries
- signature or attestation
- import provenance
- policy translation
- redaction
- partial trust
- compatibility gates

### 20.3 Non-Equivalence Risk
Two federated systems using the same syntax are not automatically semantically equivalent unless ontology and policy assumptions are also aligned.

---

## 21. Security Considerations

### 21.1 Declarative Surface
AASL source MUST be treated as data first, not executable code by default.

### 21.2 Dangerous Attachments
Embedded executable directives, tool bindings, or code payload references MUST be policy-gated.

### 21.3 Resolver Safety
Import and reference resolution MUST defend against:

- spoofed namespaces
- malicious shadowing
- unauthorized external dereference
- policy bypass through aliasing

### 21.4 Provenance Trust
Systems SHOULD distinguish asserted provenance from verified provenance.

### 21.5 Admission Controls
Production registries SHOULD gate admission on validation, signature policy, or trusted pipeline rules.

---

## 22. Versioning and Compatibility

### 22.1 Versioned Evolution
AASL documents, ontologies, modules, and compiled artifacts SHOULD carry explicit version metadata.

### 22.2 Compatibility Classes
Implementations SHOULD distinguish:

- backward compatible changes
- forward compatible tolerances
- breaking semantic changes
- deprecated but admissible forms
- experimental forms

### 22.3 Deprecation
Deprecated types or fields SHOULD remain machine-discernible and migration guidance SHOULD be available.

### 22.4 Migration
Migration tools MAY translate legacy AASL into newer admissible forms, but semantic preservation rules MUST be explicit.

---

## 23. Conformance

An implementation may claim one or more conformance profiles.

### 23.1 Authoring Profile
Supports creation, parsing, diagnostics, and formatting.

### 23.2 Validation Profile
Supports multi-layer validation against a declared ontology set.

### 23.3 Compilation Profile
Supports canonical semantic graph emission.

### 23.4 Registry Profile
Supports admission, identity, provenance, versioning, and retrieval.

### 23.5 Runtime Profile
Supports execution bindings to live agent systems.

### 23.6 Federation Profile
Supports signed or policy-governed inter-system exchange.

A full-stack AASL implementation SHOULD clearly declare which profiles it supports.

---

## 24. Minimal Example Shape

The following is illustrative, not grammar-authoritative:

```aasl
namespace atr.core@1
import atr.agents@1
import atr.tasks@1

agent Agent:planner.alpha {
  display_name: "Planner Alpha"
  role: atr.agents/Planner
  capabilities: [atr.agents/plan, atr.agents/reason, atr.agents/delegate]
}

task Task:market.scan {
  title: "Scan market opportunities"
  owner: Agent:planner.alpha
  priority: 7
}

relation assigned_to {
  from: Task:market.scan
  to: Agent:planner.alpha
  type: atr.core/assigned_to
}
```

This example demonstrates that AASL is declaration-centric, typed, reference-aware, and relation-capable.

---

## 25. Implementation Guidance

Implementers SHOULD follow this lifecycle:

1. read source,
2. tokenize,
3. parse,
4. build structural representation,
5. resolve imports and namespaces,
6. resolve symbols and references,
7. validate types and constraints,
8. canonicalize,
9. compile to semantic graph,
10. enforce admission policy,
11. persist and expose via query/runtime layers.

---

## 26. Non-Goals

AASL is not intended to be:

- a general-purpose programming language,
- an opaque binary interchange format,
- a substitute for model weights,
- a hidden prompt transport layer without governance,
- an excuse to blur policy with object truth,
- an execution substrate that bypasses validation.

---

## 27. Reference Companion Documents

This bootstrap specification is complemented by more detailed subsystem documents, including:

- Parser Architecture
- Runtime Model
- Compiler Architecture
- Validator Architecture
- Query Engine Specification
- File Infrastructure Specification
- Developer Tooling Specification
- Conversion Pipeline Specification
- Ontology Registry and Governance Operations
- Primer and Test Set documents

Where companion documents provide a deeper operational rule set, they SHOULD refine this specification rather than contradict it.

---

## 28. Acceptance Criteria for an AASL Ecosystem

An AASL ecosystem can be considered minimally complete when it can:

- author valid `.aas` documents,
- parse them deterministically,
- validate them against declared ontologies,
- compile them into canonical graph objects,
- preserve identity and provenance,
- query stored semantics,
- bind admitted objects to runtime systems,
- govern versioning and federation safely.

---

## 29. Final Principle

AASL is the semantic contract surface for Atrahasis.

It exists so that agents, humans, and systems can all refer to the same durable objects with the same meaning under the same rules. Any implementation choice that weakens determinism, identity, auditability, or ontology-governed meaning is contrary to the purpose of AASL.

