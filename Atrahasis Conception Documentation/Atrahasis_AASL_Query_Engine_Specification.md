# Atrahasis AASL Query Engine Specification

Version: 1.0.0  
Status: Canonical Subsystem Specification  
Date: 2026-03-08

---

# 1. Purpose

This document defines the canonical architecture for the **AASL Query Engine**, the subsystem that retrieves, traverses, filters, ranks, inspects, and packages semantic knowledge from the AASL runtime.

If the parser turns source into structure, the validator decides admissibility, the canonicalizer normalizes form, and the runtime hosts live semantic objects, then the query engine is the layer that allows agents, tools, memory systems, workflows, and operators to *ask meaningful questions of that semantic state*.

This document exists to fully specify:

- the role of the query engine in the AASL stack
- the supported query classes and retrieval model
- the internal execution pipeline
- the canonical query language surface
- exact lookup and structured filtering behavior
- graph traversal and path semantics
- provenance and verification inspection behavior
- workspace and scope handling
- trust-aware and policy-aware retrieval
- ranking, packaging, and response shaping
- indexes and performance model
- mutation and consistency interaction rules
- APIs, package boundaries, and subsystem contracts
- testing, certification, and implementation sequencing

This document does **not** redefine the parser, validator, runtime object model, canonicalization rules, or distributed federation protocol. It depends on them and exposes a stable retrieval interface over their outputs.

---

# 2. System Role

The AASL Query Engine is the semantic retrieval subsystem of Atrahasis.

Its job is not to search text blindly. Its job is to interrogate a structured semantic graph made of typed objects, fields, relationships, provenance attachments, verification records, document membership, and lifecycle state.

High-level system position:

External Source or `.aas` Document  
→ File Intake / Compiler / Parser  
→ Validator / Canonicalizer  
→ Runtime Workspace  
→ **AASL Query Engine**  
→ Agents / Memory / APIs / CLI / Visualization / Federation / Tooling

The query engine must support both of the following realities:

- precise deterministic retrieval over canonical semantic state
- practical retrieval workflows over mixed, draft, unresolved, disputed, or partial workspaces

Because of this, the engine must not behave like either a simple key-value lookup layer or a purely probabilistic search engine. It is a **semantic retrieval system with explicit trust, state, and scope awareness**.

---

# 3. Architectural Objectives

The query engine must satisfy the following system objectives.

## 3.1 Semantic Precision

Queries must operate on typed semantic objects and typed relations, not merely string matching.

## 3.2 Deterministic Core Behavior

Given the same workspace, query, policy profile, and engine version, deterministic query modes must return the same result set and ordering.

## 3.3 Graph-Native Retrieval

The engine must treat the runtime as a traversable semantic graph and support path-aware exploration.

## 3.4 Trust-Aware Retrieval

The engine must be able to constrain results by provenance quality, verification state, canonical status, dispute state, and policy admissibility.

## 3.5 Scope Awareness

Queries must operate against explicit workspace boundaries, document scopes, namespaces, modules, snapshots, and federation scopes.

## 3.6 Authoring Tolerance

The engine must support draft workspaces where unresolved references, partial validation, and non-final objects may still exist.

## 3.7 Packaging Readiness

The engine must return not only raw objects, but also useful structured packages for agents, tools, APIs, and human operators.

## 3.8 Explainability

The engine must surface how a result was obtained, which filters applied, what traversal steps were taken, and why certain candidates were excluded.

## 3.9 Extensibility

The engine must support future ontology modules, future query operators, future ranking policies, and future storage backends without redesigning its core execution model.

## 3.10 Performance Discipline

Common retrieval workflows must be index-backed and predictable enough for production use, while heavier graph exploration workflows may be staged, streamed, or bounded.

---

# 4. Scope of Responsibility

The query engine is responsible for:

- object identity lookup
- type-based retrieval
- field and attribute filtering
- path and relationship traversal
- provenance and verification inspection retrieval
- document, namespace, module, and workspace scoping
- trust-aware filtering
- result ranking where ranking is permitted
- response packaging and projection
- query planning and execution
- index selection and execution strategies
- pagination, limits, streaming, and continuation cursors
- execution diagnostics and explain output
- stable APIs for agents, tools, and services

The query engine is **not** responsible for:

- parsing raw `.aas` text
- inventing semantic structure that the runtime does not expose
- deciding whether an invalid object becomes valid
- canonicalizing source on its own
- proving truth of claims
- replacing the full verification layer
- bypassing policy restrictions enforced by higher layers
- serving as an uncontrolled natural-language search interface without compiler mediation

---

# 5. Core Query Principle

The core principle of the AASL Query Engine is:

**query over semantics first, evidence and trust second, text only when explicitly requested or compiler-mediated.**

This means:

- exact semantic retrieval is primary
- text-like search is optional and secondary
- ambiguous user intent should be compiled into structured retrieval plans through AASC or another compiler layer
- retrieval results must preserve the distinction between canonical knowledge, draft knowledge, disputed knowledge, and unsupported candidates

---

# 6. Query Engine Position in the AASL Stack

## 6.1 Depends On

The query engine depends on:

- runtime workspace APIs
- runtime object registries and indexes
- reference resolution tables
- validation state and admissibility markers
- canonicalization state and hashes
- provenance attachments
- verification records
- policy overlays
- document and namespace metadata

## 6.2 Feeds

The query engine feeds:

- agent reasoning workflows
- memory retrieval and bundle reuse
- API responses
- CLI inspection tools
- visual graph explorers
- operator debugging tools
- federation selection logic
- export and reporting workflows

## 6.3 Interacts Bidirectionally With

The query engine interacts bidirectionally with:

- mutation workflows for snapshot-safe querying
- cache and index managers
- access-control and policy enforcement layers
- compiler systems that turn natural language into query plans
- storage backends that materialize or hydrate result subsets

---

# 7. Primary Query Classes

The engine must support the following primary query classes.

## 7.1 Identity Lookup

Retrieve an object by stable identifier, alias, canonical hash, external reference, or other identity-bearing key.

Examples:

- get object `clm.market.2026.14`
- get artifact by canonical semantic hash
- resolve alias to canonical object

## 7.2 Type Retrieval

Retrieve all objects of one or more semantic types, optionally within a scope.

Examples:

- all `claim` objects in workspace
- all `dataset` objects in namespace `finance`
- all `evidence` objects attached to one document

## 7.3 Field Filtering

Retrieve objects whose fields satisfy predicates.

Examples:

- all claims with confidence greater than `0.85`
- all observations with `subject = company.x`
- all records created after a given timestamp

## 7.4 Relationship Traversal

Traverse typed links through the runtime graph.

Examples:

- evidence supporting a claim
- claims derived from a dataset
- policies governing a module
- transitive supersession chain of an artifact

## 7.5 Provenance Retrieval

Retrieve provenance envelopes, source records, derivation history, and lineage paths.

Examples:

- show source chain for this claim
- find all claims originating from source `src.alpha`
- trace derivation path from dataset to published report

## 7.6 Verification Retrieval

Retrieve verification state, verification records, disputes, corroboration state, or unresolved review status.

Examples:

- all verified claims for dataset `ds.climate.44`
- show disputed objects in current workspace
- return pending verification records assigned to module `health`

## 7.7 Document and Workspace Retrieval

Retrieve objects by document, package, workspace, or snapshot membership.

Examples:

- all objects in document `casebook-17.aas`
- all canonical objects in workspace snapshot `r42`

## 7.8 Structural Inspection Queries

Retrieve schema-relevant structure for tooling and debugging.

Examples:

- all unresolved references
- all duplicate identifiers
- all objects missing required provenance field

## 7.9 Composite Semantic Queries

Combine lookup, filters, graph steps, provenance constraints, and trust policies in a single retrieval plan.

Examples:

- all verified causal claims in module `economics` supported by at least two evidence objects from independent sources
- all disputed entities affected by policy `gov.v2` and superseded after `2026-01-01`

## 7.10 Analytical Retrieval Queries

Produce aggregate or grouped outputs over semantic objects.

Examples:

- count claims by verification state
- group evidence by source family
- return top namespaces by unresolved reference count

Analytical retrieval is permitted only where semantics remain explicit and explainable.

---

# 8. Query Modes

The engine must expose explicit modes because not all retrieval behaviors are appropriate in every context.

## 8.1 Strict Deterministic Mode

Used for APIs, canonical workflows, certification tests, and reproducible evaluation.

Properties:

- no heuristic ranking unless explicitly requested
- exact semantics only
- no fuzzy fallback
- stable ordering rules
- strict policy enforcement

## 8.2 Authoring Mode

Used in editors, workspaces, and draft pipelines.

Properties:

- may include draft and unresolved objects
- can return warnings with results
- may include partial matches under declared tolerance rules
- prioritizes usability while preserving semantic state visibility

## 8.3 Inspection Mode

Used for debugging, auditing, and operational introspection.

Properties:

- exposes hidden state markers
- includes execution trace and exclusion reasons
- surfaces unresolved edges and inconsistent state

## 8.4 Agent Retrieval Mode

Used by Atrahasis agents.

Properties:

- can return enriched packages rather than raw records only
- may include trust summaries and relevance ordering
- must remain policy constrained
- must surface confidence and result provenance explicitly

## 8.5 Federated Mode

Used when querying across multiple nodes or imported remote snapshots.

Properties:

- tracks origin node and trust domain
- distinguishes local from remote truth states
- requires explicit equivalence and conflict handling rules

---

# 9. Query Surface Model

The query engine must expose a layered query surface rather than a single interface.

## 9.1 Canonical Structured Query API

A machine-stable structured query representation for services, agents, tools, and test suites.

## 9.2 Human-Oriented DSL

A readable textual query language for CLI, developer tooling, documentation, and debugging.

## 9.3 Compiler-Mediated Natural Language Entry

Natural language must not hit the runtime directly. It must first be compiled into structured query plans by AASC or an equivalent query compiler.

## 9.4 Programmatic SDK APIs

Language bindings for TypeScript, Python, Rust, and future supported runtimes must compile down to the canonical structured query representation.

---

# 10. Canonical Query Representation

The canonical representation for a query must be a structured query object, referred to here as a **Query Plan Envelope** or **QPE**.

A QPE must include:

- query identifier
- engine version
- query mode
- workspace scope
- root selectors
- predicates
- traversal steps
- trust constraints
- projection rules
- ordering rules
- pagination or streaming rules
- timeout and cost limits
- explain flags
- policy context

Illustrative conceptual shape:

```text
QPE
  id
  mode
  scope
  root
  filters[]
  traversals[]
  trust_constraints[]
  projection
  order
  limit
  cursor
  explain
  policy_profile
```

This document intentionally defines the semantics of this envelope, not a final JSON syntax.

---

# 11. Human-Oriented DSL

The human-oriented query DSL should be expressive but disciplined.

Illustrative examples:

```text
FIND claim WHERE confidence >= 0.85
FIND claim IN module economics WHERE verification.state = verified
TRAVERSE FROM claim:clm.market.14 VIA supported_by TO evidence
FIND evidence WHERE source.family = "peer_review" ORDER BY created_at DESC LIMIT 20
TRACE PROVENANCE OF claim:clm.energy.2
COUNT claim GROUP BY verification.state
```

The DSL must compile into the same canonical query representation as SDK and service callers.

---

# 12. Root Selection Model

Every query begins from a root selection, even if the user does not write one explicitly.

Supported root kinds include:

- explicit object identity
- object type family
- document membership
- namespace or module
- canonical hash
- verification record family
- provenance record family
- saved result set or prior cursor
- federated source domain

Root selection must always resolve into a bounded candidate set before later execution stages.

---

# 13. Predicate Model

The engine must support typed predicates over semantic fields and metadata.

## 13.1 Predicate Families

The engine must support at minimum:

- equality and inequality
- numeric comparison
- set membership
- null or existence checks
- string exact matching
- temporal comparison
- status comparison
- canonical hash comparison
- policy tag matching
- namespace and module matching

## 13.2 Type-Aware Semantics

Predicates must be evaluated according to field type, not only serialized representation.

Examples:

- timestamps compare as timestamps
- confidence compares as bounded numeric type
- identifiers compare in normalized identifier form
- enums compare against canonical enum domains

## 13.3 Multi-Valued Field Semantics

For multi-valued fields, the engine must make explicit whether a predicate means:

- any member matches
- all members match
- cardinality threshold matches

The default behavior must be explicit in the language and stable across implementations.

---

# 14. Graph Traversal Model

Graph traversal is a first-class function of the query engine.

## 14.1 Traversal Step

Each traversal step must define:

- source set
- edge type or edge family
- direction
- hop constraints
- optional edge predicates
- optional target predicates
- deduplication behavior

## 14.2 Directions

Traversals must support:

- outbound
- inbound
- bidirectional where permitted

## 14.3 Hop Semantics

The engine must support:

- one-hop traversal
- bounded multi-hop traversal
- transitive closure under explicit limits
- path existence queries
- shortest-path style structural retrieval where defined

## 14.4 Path Materialization

Where requested, results must include the traversed path, not just the terminal node.

## 14.5 Cycle Handling

The engine must explicitly handle cycles through:

- visited-set tracking
- cycle-safe path limits
- configurable deduplication
- explain markers when results were cycle-pruned

---

# 15. Provenance and Verification Retrieval Semantics

The query engine must support these as first-class dimensions, not afterthought metadata filters.

## 15.1 Provenance Retrieval

The engine must be able to retrieve:

- direct source attachments
- derivation chains
- transformation lineage
- compiler-origin traces
- document-of-origin information
- source timestamps and acquisition metadata

## 15.2 Verification Retrieval

The engine must be able to retrieve and filter on:

- verification state
- verification record identity
- verifier domain
- corroboration count
- dispute markers
- rejection reason families
- pending review status

## 15.3 Trust Constraints

Trust constraints must be composable, such as:

- only verified
- exclude disputed
- minimum corroboration count of 2
- provenance source family must be independent
- only canonical and signed artifacts

---

# 16. Workspace, Snapshot, and Scope Model

The same object identifier may appear in different semantic contexts. The query engine must therefore operate with explicit scope.

## 16.1 Scope Dimensions

Scope may include:

- workspace identifier
- snapshot identifier
- document subset
- module subset
- namespace subset
- environment profile
- local vs federated domain
- draft vs canonical inclusion flags

## 16.2 Snapshot Safety

A query must execute against a consistent runtime snapshot. It must not observe half-committed mutation state.

## 16.3 Cross-Workspace Behavior

Cross-workspace querying is allowed only through explicit multi-scope plans. Implicit bleeding between workspaces is forbidden.

---

# 17. Projection Model

Not every consumer needs the full semantic object.

The engine must support projections including:

- full object materialization
- selected field projection
- identity-only projection
- edge-only projection
- path projection
- compact summary projection
- trust summary projection
- provenance bundle projection
- aggregate output projection

Projection rules must not alter the underlying result semantics. They only change representation.

---

# 18. Ordering, Ranking, and Relevance

## 18.1 Stable Ordering

In deterministic modes, ordering must be explicit and reproducible.

Supported ordering dimensions include:

- identifier
- created timestamp
- updated timestamp
- confidence
- verification rank
- provenance recency
- graph distance
- canonical priority

## 18.2 Ranking

Ranking is permitted only when explicitly invoked or when the mode allows it.

Permitted ranking signals may include:

- exactness of predicate satisfaction
- trust quality
- canonical preference
- verification strength
- graph proximity
- recency
- source independence count

## 18.3 Explainable Ranking

Any non-trivial ranking must be explainable. The engine must be able to return a ranking breakdown when requested.

---

# 19. Query Execution Pipeline

The query execution pipeline must be internally staged.

## 19.1 Stage 1: Parse or Decode Query

The engine decodes the DSL, SDK call, or service payload into a canonical query representation.

## 19.2 Stage 2: Validate Query

The engine validates structural correctness, operator legality, type compatibility, policy restrictions, and cost bounds.

## 19.3 Stage 3: Bind Scope

The engine resolves workspace, snapshot, document subset, and policy profile.

## 19.4 Stage 4: Plan Query

The planner selects indexes, candidate roots, traversal strategies, join order, and execution operators.

## 19.5 Stage 5: Execute Root Retrieval

The engine resolves the root candidate set.

## 19.6 Stage 6: Apply Predicates and Traversals

The engine filters, expands, joins, traverses, and prunes candidates according to the plan.

## 19.7 Stage 7: Apply Trust and Policy Constraints

The engine enforces verification, provenance, policy, visibility, and admissibility filters.

## 19.8 Stage 8: Order, Rank, and Project

The engine finalizes ordering, ranking, projection, packaging, and pagination.

## 19.9 Stage 9: Emit Response and Diagnostics

The engine returns results, execution metadata, cursor state, warnings, and optional explain output.

---

# 20. Query Planner Architecture

The planner converts valid query envelopes into executable retrieval plans.

## 20.1 Planner Responsibilities

The planner must:

- choose execution operators
- choose indexes where possible
- minimize broad graph scans
- enforce traversal bounds
- respect policy and cost limits
- produce explainable plans

## 20.2 Cost Model

The planner must maintain a cost model including:

- estimated candidate set size
- index selectivity
- traversal fanout estimates
- projection cost
- expected materialization cost
- expected remote or federated fetch cost

## 20.3 Plan Stability

Deterministic mode should prefer stable plans when materially equivalent options exist, to support reproducibility.

---

# 21. Execution Operators

The engine should expose an internal operator model.

Representative operators include:

- identity lookup operator
- type scan operator
- index seek operator
- field filter operator
- edge expand operator
- path materialization operator
- group operator
- aggregate operator
- dedup operator
- sort operator
- projection operator
- pagination operator
- trust filter operator
- policy filter operator

Operators may be chained into executable plans.

---

# 22. Index Architecture

Indexes are required for production-grade retrieval.

## 22.1 Required Index Families

The engine must support at minimum:

- object id index
- canonical hash index
- type index
- namespace and module index
- document membership index
- field value index for filterable fields
- edge adjacency index
- reverse edge index
- verification state index
- provenance source index
- lifecycle state index

## 22.2 Optional and Advanced Indexes

Future implementations may add:

- compound indexes
- temporal indexes
- path summary indexes
- aggregation helper indexes
- federated result caches
- materialized trust views

## 22.3 Index Freshness

Indexes must remain synchronized with committed runtime state. Querying against stale indexes without explicit declaration is forbidden.

---

# 23. Result Envelope

Every query must return a **Result Envelope** with both data and execution context.

A result envelope should include:

- query id
- engine version
- workspace and snapshot bound
- result items
- total count when available
- continuation cursor when applicable
- warnings
- trust summary
- timing summary
- execution mode
- partial result marker if relevant
- explain payload when requested

Illustrative conceptual shape:

```text
RESULT
  query_id
  mode
  scope
  items[]
  count
  cursor
  warnings[]
  trust_summary
  timing
  explain
```

---

# 24. Streaming and Pagination

The query engine must support both bounded and streaming retrieval.

## 24.1 Pagination

Pagination must use stable continuation cursors, not offset-only semantics, for large semantic result sets.

## 24.2 Streaming

Streaming is appropriate for:

- large graph traversals
- large export workflows
- inspection queries over operational state
- federated retrieval where remote latency varies

## 24.3 Partial Results

If partial results are returned due to timeout, cost cap, or remote incompleteness, the result envelope must explicitly state this.

---

# 25. Policy and Access Enforcement

The query engine must never bypass policy.

## 25.1 Policy Dimensions

Policy may constrain:

- visible namespaces
- visible object types
- draft object access
- disputed object visibility
- verification record visibility
- source metadata exposure
- remote node exposure
- sensitive field projection

## 25.2 Enforcement Phase

Policy must be applied both:

- during planning where it affects legal execution
- during result shaping where it affects returned fields or records

## 25.3 Redaction

When policy permits access to an object but not all of its fields, the engine must support field-level redaction with explicit markers.

---

# 26. Error Model

The query engine must return structured errors.

Representative error families include:

- malformed query
- unsupported operator
- illegal traversal
- type mismatch
- unknown scope
- policy denial
- cost limit exceeded
- timeout
- inconsistent snapshot
- unresolved index state
- federated source unavailable

Errors must be machine-readable and include actionable diagnostics where possible.

---

# 27. Explainability Model

Explainability is mandatory for a semantic retrieval system.

## 27.1 Explain Payload

When enabled, explain output should include:

- normalized query plan
- bound scope
- selected indexes
- operator sequence
- pruning decisions
- policy applications
- ranking signals
- exclusion reasons
- timing per stage

## 27.2 User-Facing Explain Variants

The engine should support:

- compact explain for CLI and APIs
- verbose explain for debugging
- audit explain for governance or certification workflows

---

# 28. Caching Strategy

Caching may improve performance but must not compromise semantic correctness.

## 28.1 Cacheable Artifacts

The engine may cache:

- normalized query plans
- index metadata
- result pages for immutable snapshots
- common projections
- federated remote responses with freshness bounds

## 28.2 Cache Safety

Caches must be scoped by:

- engine version
- workspace snapshot
- policy profile
- query mode
- projection shape

---

# 29. Interaction with Mutation and Runtime State

The query engine must coexist safely with mutable draft workspaces and commit workflows.

## 29.1 Snapshot Isolation

Queries execute against committed or explicitly staged snapshots.

## 29.2 Draft Visibility

Draft objects may be queryable in authoring mode, but their draft state must remain visible.

## 29.3 Consistency Rules

The engine must never mix objects from incompatible snapshots in one deterministic result set unless the query explicitly requests cross-snapshot analysis.

---

# 30. Interaction with Memory Systems

The query engine is the retrieval substrate for Atrahasis memory.

Memory-oriented retrieval must support:

- canonical hash lookup
- reusable bundle retrieval
- prior task result retrieval
- semantic neighborhood expansion
- verification-aware recall
- trust-preserving package assembly

The memory system may build higher-order behaviors on top of the query engine, but must not bypass its semantics.

---

# 31. Interaction with AASC and Natural Language Interfaces

Natural language requests must flow through compiler mediation.

Illustrative path:

user asks question  
→ AASC query compiler interprets intent  
→ emits QPE  
→ query engine executes  
→ result envelope returned  
→ agent or UI renders answer

This preserves explicit semantics and prevents uncontrolled lexical guessing at the retrieval layer.

---

# 32. Interaction with Federation

Federated query is a later-stage capability, but the query engine must be designed for it.

## 32.1 Federated Retrieval Requirements

Federated retrieval must support:

- querying remote canonical snapshots
- origin labeling
- trust domain separation
- conflict and equivalence markers
- remote timeout and partial-result handling

## 32.2 Local-First Principle

Where possible, local canonical state should be evaluated first, with remote augmentation occurring under explicit federated plans.

---

# 33. APIs and Package Boundaries

The query engine should be implemented as a dedicated subsystem with clear package boundaries.

Suggested package layout:

```text
/aasl/query/
  query_types/
  parser/
  planner/
  operators/
  execution/
  indexes/
  projection/
  ranking/
  explain/
  policy/
  api/
  sdk/
  tests/
```

Representative APIs:

- `executeQuery(qpe, scope, options)`
- `explainQuery(qpe, scope, options)`
- `streamQuery(qpe, scope, options)`
- `prepareCursor(resultEnvelope)`
- `compileDslToQuery(dsl)`

Exact method names may vary by language, but subsystem boundaries should remain stable.

---

# 34. Canonical Minimum Viable Capability

The first production-meaningful version of the query engine must support:

- object lookup
- type lookup
- field filtering
- one-hop graph traversal
- provenance retrieval
- verification inspection
- stable scoping
- deterministic pagination
- structured result envelopes
- basic explain output

This aligns with the implementation board requirement that semantic queries must succeed.

---

# 35. Extended Capability Targets

After the minimum viable capability, the engine should expand toward:

- bounded multi-hop traversal
- aggregate queries
- path materialization
- ranking policies
- saved queries and reusable plans
- federated retrieval
- trust-aware package assembly
- graph analytics helpers
- compiler-optimized natural language query plans

---

# 36. Testing Strategy

The query engine must have a dedicated certification-grade test suite.

## 36.1 Test Families

Required test families include:

- identity lookup tests
- type retrieval tests
- field predicate tests
- traversal tests
- provenance retrieval tests
- verification retrieval tests
- scope isolation tests
- projection tests
- ordering tests
- pagination tests
- explain output tests
- policy enforcement tests
- cache safety tests
- snapshot consistency tests
- federated partial-result tests

## 36.2 Golden Query Suites

The engine should ship with a canonical golden query suite containing:

- known workspaces
- known query plans
- expected result envelopes
- expected explain summaries

This is critical for multi-language and multi-node compatibility.

## 36.3 Property Testing

Property-based tests should be used for:

- traversal determinism under graph permutations
- cursor stability
- projection consistency
- dedup correctness
- cycle handling

---

# 37. Certification Criteria

A query engine implementation is compliant only if it demonstrates:

- correct semantic retrieval over canonical workspaces
- stable scope isolation
- correct trust-aware filtering
- deterministic behavior in strict mode
- explainable plan generation
- safe coexistence with runtime mutation and snapshots
- policy-constrained result shaping

---

# 38. Operational Metrics

The engine should expose operational metrics such as:

- query count by mode
- latency by query family
- index hit ratios
- planner fallback frequency
- traversal fanout statistics
- partial-result frequency
- policy-denied query count
- cache hit ratio
- federated timeout rate

Metrics must never replace semantic correctness, but they are essential for operating the engine safely at scale.

---

# 39. Failure Modes and Protections

Representative failure modes include:

- accidental graph explosion from unbounded traversal
- stale index reads after mutation
- hidden scope leakage across workspaces
- ranking that obscures deterministic truth ordering
- query plans that silently downgrade to scans
- draft results mistaken for canonical truth
- federated results mistaken for local verified knowledge

Required protections include:

- mandatory traversal bounds
- snapshot binding
- explicit draft and dispute markers
- explain output
- policy enforcement at plan and result stages
- deterministic-mode safeguards
- cost caps and timeout controls

---

# 40. End-to-End Example Workflows

## 40.1 Exact Claim Retrieval

Request:

```text
FIND claim WHERE id = "clm.market.2026.14"
```

Execution:

- bind workspace snapshot
- perform id index lookup
- materialize claim object
- project full object and trust summary
- return result envelope

## 40.2 Verified Evidence for a Claim

Request:

```text
TRAVERSE FROM claim:clm.market.2026.14 VIA supported_by TO evidence
WHERE verification.state = verified
```

Execution:

- resolve claim root
- expand `supported_by` adjacency list
- filter evidence by verification state
- sort by provenance recency if requested
- return evidence objects with path materialization

## 40.3 Workspace Inspection

Request:

```text
FIND object WHERE lifecycle.state = unresolved_reference
```

Execution:

- scan lifecycle state index
- bind authoring workspace scope
- return unresolved objects with source spans and explain output

---

# 41. Implementation Sequence

Recommended implementation order:

1. query type definitions and result envelopes  
2. scope binding and snapshot-safe execution  
3. id and type indexes  
4. field predicate execution  
5. one-hop traversal operators  
6. provenance and verification filtering  
7. projection, ordering, and pagination  
8. explain output  
9. aggregate operators  
10. multi-hop traversal with bounds  
11. policy-redacted projections  
12. federated query extension

The first architecturally credible implementation appears once one-hop traversal, provenance-aware filtering, deterministic pagination, and explain output are all functional.

---

# 42. Non-Negotiable Rules

The AASL Query Engine must never:

- collapse semantic retrieval into raw text search by default
- hide whether returned objects are draft, disputed, unresolved, or unverified
- cross workspace boundaries implicitly
- execute unbounded traversal without explicit protection
- let ranking override declared deterministic ordering in strict mode
- bypass policy because a caller is internal
- return results without enough context for downstream trust-aware use

---

# 43. Conclusion

The AASL Query Engine is the subsystem that turns the Atrahasis semantic graph into something navigable, inspectable, and operationally useful.

It is not merely a convenience layer. It is the retrieval contract that every serious Atrahasis capability depends on:

- memory reuse
- agent reasoning
- provenance inspection
- verification-aware answer generation
- tool and API access
- federated semantic exchange

If the runtime is the living semantic substrate of AASL, the query engine is the disciplined interface through which that substrate becomes actionable knowledge.
