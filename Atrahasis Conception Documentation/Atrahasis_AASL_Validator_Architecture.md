# Atrahasis AASL Validator Architecture

Version: 1.0  
Status: Canonical Subsystem Specification  
Scope: AASL document admissibility, semantic integrity, policy conformance, repair guidance, and runtime-safe acceptance into the Atrahasis knowledge fabric

---

## 1. Purpose

This document defines the canonical validator architecture for AASL (Atrahasis Agentic Semantic Language). The validator is the trust boundary between authored, compiled, imported, federated, or machine-generated AASL artifacts and the rest of the Atrahasis runtime.

Its role is not merely to determine whether a document is “valid.” Its job is to determine whether an AASL artifact is:

1. syntactically well-formed,
2. structurally coherent,
3. semantically admissible,
4. referentially resolvable,
5. policy compliant,
6. safe to store,
7. safe to index,
8. safe to execute against,
9. safe to federate,
10. and safe to expose to agents, workflows, and downstream inference systems.

The validator therefore acts as:

- the document gatekeeper,
- the semantic integrity checker,
- the policy enforcement surface,
- the repair hint generator,
- the normalization verifier,
- and the basis of trust scoring for every admitted artifact.

---

## 2. Design Goals

The validator must satisfy the following design goals.

### 2.1 Deterministic Outcomes

Given identical input, schema set, ontology registry, policy bundle, and runtime context, validation must produce the same result, findings, and admissibility decision.

### 2.2 Layered Validation

Validation must occur in ordered passes so that errors are classified close to their origin and higher-order checks only run once lower-order guarantees exist.

### 2.3 Explainability

Every finding must include:

- stable rule identifier,
- severity,
- source location,
- affected node/object/path,
- human-readable explanation,
- machine-readable metadata,
- and suggested repair where possible.

### 2.4 Partial Tolerance

The validator must support strict and permissive modes. Some workflows require hard rejection for any deviation; others require soft admission with quarantining, annotation, or deferred repair.

### 2.5 Runtime Safety

The validator must prevent malformed or hostile AASL from destabilizing storage, index, federation, execution, or agent reasoning layers.

### 2.6 Canonical Integration

The validator must operate consistently across:

- hand-authored `.aas` files,
- compiled AASC outputs,
- imported datasets,
- externally federated artifacts,
- runtime patch operations,
- and policy-triggered revalidation events.

### 2.7 Repairability

Validation should not stop at failure. The validator must, where possible, emit structured repair guidance and machine-actionable rewrite recommendations.

### 2.8 Incrementality

The validator must support validating the entire document, a changed subgraph, a patch delta, or a newly imported dependency without requiring unnecessary full-graph recomputation.

---

## 3. What the Validator Validates

The validator evaluates AASL artifacts across multiple assurance domains.

### 3.1 Lexical and Parse-Derived Integrity

The validator confirms that the parser output being received is complete, internally consistent, and structurally traversable.

### 3.2 Structural Integrity

The validator checks the presence and arrangement of required sections, object kinds, field shapes, list forms, block nesting, and document envelope constraints.

### 3.3 Type Integrity

The validator checks scalar types, composite types, enums, unions, optionality, nullability policy, and custom semantic types.

### 3.4 Identity Integrity

The validator checks identifier uniqueness, namespace admissibility, ID format constraints, stable key requirements, and collision rules.

### 3.5 Referential Integrity

The validator checks that links, references, imports, pointers, anchors, and foreign keys resolve according to scope rules.

### 3.6 Ontological Integrity

The validator checks that declared entity kinds, relation predicates, schemas, modules, and semantic annotations are registered, compatible, and admissible.

### 3.7 Constraint Integrity

The validator checks business rules, cardinality limits, invariant rules, lifecycle restrictions, and cross-field consistency requirements.

### 3.8 Policy Integrity

The validator checks security policy, visibility policy, governance restrictions, semantic closure policy, safety constraints, federation rules, and execution guardrails.

### 3.9 Canonicalization Integrity

The validator checks whether the normalized or canonical form is faithful, stable, reproducible, and compliant with ordering and serialization rules.

### 3.10 Runtime Admissibility

The validator determines whether the artifact may enter:

- primary storage,
- graph indexes,
- vector or hybrid retrieval layers,
- federation exchange,
- execution or planning layers,
- or only quarantine.

---

## 4. Position in the Atrahasis Pipeline

The validator sits between parse/compile and storage/runtime admission.

Canonical flow:

1. Input artifact received.
2. Parser produces CST/AST and source map.
3. Canonicalizer produces normalized intermediate representation.
4. Validator executes ordered passes.
5. Findings are aggregated.
6. Admissibility engine determines acceptance state.
7. Repair engine proposes automated or operator-assisted correction.
8. Admission controller either:
   - accepts,
   - accepts with annotations,
   - quarantines,
   - or rejects.
9. Accepted artifacts proceed to runtime registry, storage, indexing, and federation publication.

The validator is therefore upstream of persistence but downstream of syntax parsing. It also participates in post-admission lifecycle events when revalidation is triggered by policy, ontology, schema, or dependency changes.

---

## 5. Core Architectural Components

The validator subsystem is composed of the following canonical components.

## 5.1 Validation Orchestrator

The orchestrator runs ordered validation passes, manages dependency sequencing, collects findings, and produces a final validation report.

Responsibilities:

- select validation profile,
- determine applicable passes,
- manage pass dependencies,
- preserve deterministic pass order,
- short-circuit when configured,
- collect timing and telemetry,
- emit final report and admissibility status.

## 5.2 Validation Context Builder

The context builder assembles the full validation environment.

Inputs include:

- AST or canonical IR,
- source map,
- module registry,
- ontology registry,
- schema registry,
- current runtime namespace state,
- identity registry,
- policy bundle,
- federation trust profile,
- execution mode,
- previous validation cache,
- and requested strictness profile.

## 5.3 Pass Engine

The pass engine provides a standard interface for individual validation passes.

Each pass declares:

- pass identifier,
- prerequisites,
- input assumptions,
- applicable object kinds,
- whether it is blocking,
- whether it supports incremental operation,
- and whether it can emit repairs.

## 5.4 Rule Registry

The rule registry stores all validation rules with stable identifiers and metadata.

Each rule entry must include:

- rule ID,
- title,
- description,
- severity default,
- category,
- rationale,
- machine condition,
- repair availability,
- compatibility scope,
- deprecation state,
- and policy override behavior.

## 5.5 Findings Collector

The findings collector aggregates all findings across passes and deduplicates or groups related findings into coherent issue chains.

## 5.6 Admissibility Engine

The admissibility engine maps raw findings into final disposition.

Possible dispositions:

- accepted,
- accepted_with_warnings,
- accepted_with_annotations,
- deferred_acceptance,
- quarantined,
- rejected,
- superseded_by_repair.

## 5.7 Repair Engine

The repair engine generates structured remediation suggestions, rewrite candidates, field substitutions, missing-reference recovery proposals, and auto-fix patches where allowed.

## 5.8 Dependency Resolver

The dependency resolver provides the validator with imported modules, referenced objects, foreign namespaces, schema definitions, and ontology declarations needed to evaluate integrity.

## 5.9 Validation Cache

The validation cache stores pass results, hash-based subgraph checks, and dependency signatures to enable incremental revalidation.

## 5.10 Report Serializer

The report serializer emits human-readable and machine-readable validation reports for CLI, API, CI, governance review, and agent tooling.

---

## 6. Canonical Validation Pass Model

Validation is not a single function. It is a sequence of passes with increasing semantic depth.

### Pass 0: Input Integrity Pass

Purpose:
Confirm that the validator has received a complete artifact, parser output, source map, and required context.

Checks include:

- artifact not truncated,
- parser status success or acceptable recovery status,
- source ranges are attached,
- canonical IR present,
- mandatory context registries loaded,
- version handshake compatibility.

Failure here is generally fatal.

### Pass 1: Structural Envelope Pass

Purpose:
Validate top-level document organization.

Checks include:

- document header presence,
- version declaration,
- module/namespace declarations,
- required sections,
- ordering constraints where relevant,
- top-level object block admissibility,
- unsupported root forms.

### Pass 2: Shape and Type Pass

Purpose:
Validate field presence, field type, list shape, map shape, scalar constraints, and schema conformance.

Checks include:

- required fields present,
- illegal fields absent,
- scalar types valid,
- enum values permitted,
- unions correctly discriminated,
- nested object shape matches schema,
- cardinality constraints respected.

### Pass 3: Identity and Namespace Pass

Purpose:
Validate local and global object identity.

Checks include:

- object IDs present where required,
- IDs correctly formatted,
- namespace prefixes valid,
- no duplicate IDs in scope,
- no forbidden shadowing,
- stable key derivation valid,
- identity reservation conflicts.

### Pass 4: Reference Resolution Pass

Purpose:
Validate that all references resolve according to scope rules.

Checks include:

- local references resolve,
- imported references resolve,
- namespace references resolve,
- anchors exist,
- relation endpoints exist,
- cyclic reference constraints obeyed,
- external reference trust boundaries observed.

### Pass 5: Ontology and Schema Semantics Pass

Purpose:
Validate semantic declarations against registered ontology and schema resources.

Checks include:

- object kinds registered,
- predicate names registered,
- entity-role compatibility,
- inheritance rules obeyed,
- schema version compatibility,
- semantic annotation admissibility,
- deprecated concept use flagged,
- experimental concept use policy checked.

### Pass 6: Invariant and Cross-Field Logic Pass

Purpose:
Validate multi-field and multi-object logical coherence.

Checks include:

- temporal intervals valid,
- mutually exclusive fields not both populated,
- dependency rules satisfied,
- lifecycle states consistent,
- start/end ordering valid,
- quantity and unit coherence,
- relation symmetry or asymmetry rules obeyed,
- ownership/authority constraints satisfied.

### Pass 7: Policy and Security Pass

Purpose:
Apply security, privacy, governance, closure, and runtime safety rules.

Checks include:

- classification tags present,
- visibility policies valid,
- restricted fields not exposed improperly,
- execution-affecting directives allowed,
- semantic closure policy compliant,
- prohibited imports blocked,
- trust-domain rules observed,
- federation export constraints satisfied,
- unsafe embedded instructions flagged.

### Pass 8: Canonicalization Consistency Pass

Purpose:
Ensure the canonical representation is stable and round-trippable.

Checks include:

- key ordering rules obeyed,
- normalized values consistent,
- deterministic serialization form preserved,
- hash material stable,
- canonical IDs unchanged after normalization,
- formatting-only differences ignored,
- normalization side effects detected.

### Pass 9: Runtime Admissibility Pass

Purpose:
Determine whether the artifact is safe to admit into active runtime systems.

Checks include:

- all blocking findings resolved,
- dependency completeness meets threshold,
- trust score above minimum,
- quarantine conditions absent,
- required metadata present for indexing,
- execution guardrails satisfied,
- federation or storage profile compatible.

### Pass 10: Repair and Recommendation Pass

Purpose:
Generate fix plans, patch suggestions, repair bundles, and prioritization guidance.

Checks include:

- can issue be auto-fixed,
- can issue be safely downgraded,
- should reference be deferred,
- can missing ontology be stubbed,
- is operator review required,
- can artifact be admitted after targeted patch.

---

## 7. Validation Modes

The validator must support multiple operational modes.

### 7.1 Strict Mode

Used for:

- canonical production admission,
- signed releases,
- governance-approved registry updates,
- cross-domain federation.

Behavior:

- all blocking errors reject,
- most warnings elevated where policy says so,
- unresolved externals typically reject,
- deprecated semantics may fail depending on policy.

### 7.2 Standard Mode

Used for:

- internal authoring,
- default CI,
- normal storage admission.

Behavior:

- errors reject,
- warnings annotate,
- some unresolved optional dependencies may defer.

### 7.3 Permissive Mode

Used for:

- ingestion of noisy corpora,
- recovery scenarios,
- exploratory compilation,
- migration tooling.

Behavior:

- allows soft admission with quarantine tags,
- maximizes finding emission and repair guidance,
- may admit partial graphs into staging only.

### 7.4 Incremental Patch Mode

Used for:

- document edits,
- runtime mutations,
- patch application,
- agent-authored updates.

Behavior:

- validates changed region plus dependency neighborhood,
- reuses cached pass results,
- escalates to full validation if affected invariants are global.

### 7.5 Federation Intake Mode

Used for:

- externally received AASL,
- partner exchanges,
- inter-cluster synchronization.

Behavior:

- enforces trust-domain policy,
- validates signature and provenance metadata,
- may disallow some executable or privileged constructs,
- may quarantine unknown ontology extensions.

### 7.6 Lint/Authoring Mode

Used for:

- editor feedback,
- CLI preflight,
- developer ergonomics.

Behavior:

- fast,
- partial,
- highly repair-oriented,
- tolerant of incomplete drafts.

---

## 8. Findings Model

Every validation issue must be represented by a canonical finding object.

### 8.1 Required Fields

Each finding includes:

- `finding_id`: stable unique instance identifier,
- `rule_id`: stable rule identifier,
- `category`: syntax|structure|type|identity|reference|ontology|constraint|policy|canonicalization|runtime,
- `severity`: info|warning|error|critical,
- `blocking`: boolean,
- `message`: concise human summary,
- `details`: longer explanation,
- `document_id`,
- `object_id` if applicable,
- `path`: semantic path within the document,
- `source_span`: line/column offsets if available,
- `related_findings`: list of IDs,
- `repair_candidates`: optional,
- `evidence`: machine-readable context,
- `pass_id`,
- `timestamp`,
- `policy_override_state` if applicable.

### 8.2 Severity Semantics

#### Info
Non-problematic or advisory condition.

#### Warning
Potential problem, not inherently admission-blocking.

#### Error
Normative rule violation; normally blocks admission in standard and strict modes.

#### Critical
Severe integrity or safety violation. Must block admission and may trigger quarantine or security review.

### 8.3 Blocking vs Non-Blocking

Severity and blocking are related but not identical. Policy may elevate a warning to blocking or downgrade an error under controlled permissive modes.

---

## 9. Admissibility Decision Model

After passes complete, findings are mapped to a final disposition.

### 9.1 Accepted

Artifact has no blocking issues and is safe for full runtime admission.

### 9.2 Accepted with Warnings

Artifact is admissible, but non-blocking issues are attached as annotations.

### 9.3 Accepted with Annotations

Artifact is admitted with explicit caveats, partial trust restrictions, or runtime limitations.

Example:

- allowed into storage,
- disallowed from federation publication,
- excluded from some planning workflows.

### 9.4 Deferred Acceptance

Artifact is not fully admissible but may become admissible after dependencies resolve or repairs apply.

### 9.5 Quarantined

Artifact is stored in isolation for review, repair, provenance verification, or security triage.

### 9.6 Rejected

Artifact is not stored in active systems and is returned with findings.

### 9.7 Superseded by Repair

Validator-generated or approved repair bundle replaces the original admission candidate.

---

## 10. Repair Architecture

Validation must support remediation, not only rejection.

### 10.1 Repair Categories

The repair engine may emit:

- lexical repair hints,
- missing field suggestions,
- enum correction suggestions,
- type coercion suggestions,
- reference correction candidates,
- namespace rewrite proposals,
- deprecated-to-current ontology migrations,
- inferred default insertion proposals,
- patch bundles,
- and quarantine release requirements.

### 10.2 Repair Safety Levels

Repairs must be classified by safety.

#### Safe Auto-Fix
Deterministic fix with negligible semantic ambiguity.

Examples:

- canonical key ordering,
- whitespace normalization,
- trivially recoverable enum case normalization.

#### Guarded Auto-Fix
Likely correct, but should be recorded and optionally require approval.

Examples:

- inserting missing default visibility tag,
- upgrading deprecated namespace alias to current alias.

#### Human Review Required
Fix affects semantics or trust.

Examples:

- selecting among multiple possible references,
- inferring ontology type from weak evidence.

#### Non-Repairable
Issue must be resolved at source.

Examples:

- missing provenance for privileged external artifact,
- irreconcilable policy violation.

### 10.3 Repair Bundle Structure

A repair bundle should contain:

- issue targets,
- proposed edits,
- confidence score,
- rationale,
- safety level,
- reversible patch representation,
- revalidation requirements.

---

## 11. Rule Taxonomy

Validation rules must be organized into stable taxonomic groups.

### 11.1 Syntax-Derived Rules

Rules derived from parser guarantees or parser recovery states.

### 11.2 Structural Rules

Rules about document composition and block admissibility.

### 11.3 Type Rules

Rules for scalar, composite, and domain-specific type correctness.

### 11.4 Identity Rules

Rules for IDs, namespace allocation, and key stability.

### 11.5 Reference Rules

Rules for resolution and dependency graph integrity.

### 11.6 Ontology Rules

Rules for semantic class, relation, annotation, and schema compatibility.

### 11.7 Invariant Rules

Rules requiring broader graph or lifecycle reasoning.

### 11.8 Policy Rules

Rules for security, privacy, governance, closure, and federation.

### 11.9 Canonicalization Rules

Rules ensuring normalized equivalence and serialization stability.

### 11.10 Runtime Safety Rules

Rules for execution, storage, and operational risk admissibility.

---

## 12. Source Mapping and Explainability

Every finding must map back to both syntax and semantics.

### 12.1 Source Span Mapping

Findings should point to:

- line and column,
- token range,
- original source excerpt when allowed,
- enclosing object or section.

### 12.2 Semantic Path Mapping

Findings should also point to semantic paths such as:

- namespace/object/field,
- relation endpoint path,
- import chain,
- graph subcomponent ID.

### 12.3 Causal Chains

When one issue causes many others, the validator must be able to designate:

- primary cause,
- dependent findings,
- likely minimal repair target.

This prevents overwhelming users or agents with hundreds of derivative messages.

---

## 13. Dependency-Aware Validation

AASL is inherently graph-oriented. Validation therefore must account for dependencies.

### 13.1 Internal Dependencies

Examples:

- local object references,
- section-local anchors,
- same-document imports,
- cross-object lifecycle rules.

### 13.2 External Dependencies

Examples:

- ontology modules,
- imported schemas,
- referenced namespace registries,
- external federation objects,
- shared vocabularies.

### 13.3 Missing Dependency Strategy

When dependencies are missing, validator behavior depends on mode and policy.

Possible outcomes:

- hard fail,
- soft fail with deferred acceptance,
- quarantine,
- stub resolution with warning,
- admit into staging only.

### 13.4 Dependency Trust

External dependencies must be validated not only for existence, but for:

- signature status,
- source trust profile,
- version compatibility,
- revocation status,
- and policy allowlist membership.

---

## 14. Incremental Revalidation Model

AASL documents and graphs evolve. Full validation on every mutation is too expensive.

### 14.1 Revalidation Triggers

Incremental revalidation may be triggered by:

- field edit,
- object insertion,
- object deletion,
- relation endpoint change,
- import target change,
- schema update,
- ontology registry update,
- policy bundle change,
- dependency version update,
- federation trust reclassification.

### 14.2 Validation Scope Expansion

For each change, the validator computes the impacted subgraph and runs the minimal necessary pass subset.

Example:

- editing a label may only need type/canonicalization checks,
- editing an ID may require identity, reference, invariant, runtime admissibility, and downstream index rechecks.

### 14.3 Cache Invalidation Rules

Cached pass results must be invalidated when:

- upstream assumptions changed,
- dependency hashes changed,
- rule set version changed,
- policy or ontology version changed,
- or affected node neighborhood expanded beyond cached bounds.

---

## 15. Policy Integration

The validator is one of the main enforcement surfaces for Atrahasis policy.

### 15.1 Security Policy

Checks may include:

- secret-bearing field restrictions,
- privilege-bearing object controls,
- action or execution intent restrictions,
- high-risk directive blocking,
- unsafe embedded payload detection.

### 15.2 Semantic Closure Policy

Checks may include:

- unsupported open-world ambiguity,
- unresolved placeholder constructs,
- claims lacking closure evidence,
- dangling semantic declarations.

### 15.3 Governance Policy

Checks may include:

- module registration status,
- ontology proposal state,
- deprecation schedule enforcement,
- namespace ownership.

### 15.4 Federation Policy

Checks may include:

- export eligibility,
- inbound trust class,
- partner-specific field suppression,
- signature/provenance requirements,
- sovereign namespace restrictions.

### 15.5 Storage Policy

Checks may include:

- metadata completeness,
- retention class assignment,
- record immutability flags,
- hashing and signing requirements.

---

## 16. Validator Interfaces

The subsystem must expose canonical interfaces for all main integration surfaces.

## 16.1 CLI Interface

Example operations:

- validate file,
- validate directory,
- validate incremental patch,
- emit JSON report,
- emit human report,
- apply safe repairs,
- compare before/after validation state.

## 16.2 Library Interface

The validator library should expose functions roughly equivalent to:

- `validate_document(input, profile)`
- `validate_ir(ir, context, profile)`
- `validate_patch(base, patch, profile)`
- `revalidate_impacted(graph, change_set, profile)`
- `suggest_repairs(report)`

## 16.3 Service Interface

For distributed systems, validator-as-a-service may support:

- synchronous admission precheck,
- asynchronous bulk validation,
- CI and governance hooks,
- policy-triggered revalidation jobs,
- federated intake screening.

## 16.4 Editor/LSP Interface

The validator must support low-latency partial diagnostics for authoring workflows.

Capabilities include:

- live diagnostics,
- hover explanations,
- quick-fix actions,
- semantic rule links,
- severity filtering,
- diff-aware validation.

---

## 17. Validation Profiles

Validation behavior should be configurable by named profiles.

Examples:

### 17.1 `production_strict`

For release-grade artifacts.

### 17.2 `authoring_default`

For editor and CLI workflows.

### 17.3 `ingestion_permissive`

For noisy imported material.

### 17.4 `federation_intake_high_trust`

For trusted partner exchanges.

### 17.5 `federation_intake_low_trust`

For unknown or partially trusted domains.

### 17.6 `migration_legacy`

For upgrading older AASL versions or transitional schemas.

Profiles specify:

- enabled passes,
- rule overrides,
- severity overrides,
- repair permissions,
- admissibility thresholds,
- quarantine policy,
- external dependency policy.

---

## 18. Versioning and Compatibility

The validator itself is versioned and must reason about version compatibility.

### 18.1 Validator Version

The subsystem must expose its own version so reports can be reproduced.

### 18.2 Rule Set Version

Rules are versioned independently from runtime binaries when possible.

### 18.3 Schema and Ontology Version Compatibility

Validation must consider:

- artifact declared version,
- current supported version matrix,
- migration path availability,
- deprecation window,
- policy-required minimum versions.

### 18.4 Backward Compatibility Handling

Older valid AASL may still be admissible under legacy profiles, while being flagged for migration.

---

## 19. Trust, Provenance, and Signatures

For federated or privileged artifacts, validation includes trust verification.

### 19.1 Provenance Metadata Checks

Required where applicable:

- source issuer,
- creation timestamp,
- signing key or certificate reference,
- compilation provenance,
- transformation lineage,
- custody chain.

### 19.2 Signature Verification

Where signatures exist, validator must confirm:

- signature format valid,
- signing key trusted,
- signed material hash matches,
- signature not revoked,
- algorithm permitted.

### 19.3 Trust Scoring

Validator may contribute to a trust score used by admission control.

Possible factors:

- artifact source class,
- prior source reliability,
- repair burden,
- ontology compatibility,
- signature strength,
- unresolved ambiguity level.

---

## 20. Quarantine Model

Not every invalid artifact should simply vanish. Some should be isolated.

### 20.1 Reasons for Quarantine

Examples:

- unresolved privileged references,
- suspected hostile content,
- provenance failure,
- severe policy violation pending review,
- partially reparable imported corpus item.

### 20.2 Quarantine Properties

Quarantined artifacts must:

- be isolated from active runtime reasoning,
- remain inspectable,
- retain validation reports,
- support repair workflows,
- support provenance investigation,
- support eventual release or purge.

### 20.3 Quarantine Release

Release from quarantine requires:

- successful repair and revalidation,
- policy or security approval where required,
- and updated admission report.

---

## 21. Performance Requirements

The validator must be robust at scale.

### 21.1 Deterministic Cost Discipline

Passes should declare expected complexity characteristics.

### 21.2 Partial Evaluation

Authoring and patch workflows must avoid unnecessary whole-document recomputation.

### 21.3 Parallelism

Independent passes or independent subgraphs may validate in parallel provided determinism of final report ordering is preserved.

### 21.4 Large Graph Handling

For very large AASL graphs, validator should support:

- chunked traversal,
- streamed dependency checks,
- bounded-memory report construction,
- progressive result emission.

### 21.5 Telemetry

Validator should record:

- pass timings,
- rule hit frequencies,
- cache hit rates,
- common repair types,
- rejection rates by profile,
- quarantine reasons.

---

## 22. Security Considerations

The validator itself is part of the attack surface.

### 22.1 Defensive Parsing Assumption

Validator must assume input may be malformed, adversarial, oversized, cyclic, deceptive, or intentionally expensive to process.

### 22.2 Resource Exhaustion Guards

Protections should exist for:

- excessive nesting,
- pathological graph expansion,
- import storms,
- reference loops,
- huge literal payloads,
- rule-trigger amplification.

### 22.3 Sandbox Boundaries

Validation must not execute embedded instructions or side-effectful hooks while determining admissibility.

### 22.4 Trust Boundary Separation

External lookups used for validation must be mediated through safe dependency interfaces, not arbitrary code execution.

### 22.5 Finding Sanitization

Reports intended for lower-trust contexts must avoid leaking protected source content or secrets.

---

## 23. Testing Strategy

The validator requires extensive test coverage.

### 23.1 Unit Tests

Per-rule and per-pass deterministic tests.

### 23.2 Golden Corpus Tests

Canonical valid and invalid AASL fixtures with expected reports.

### 23.3 Mutation Tests

Small edits introduced into valid fixtures to ensure rules catch each defect class.

### 23.4 Differential Tests

Compare full validation vs incremental validation on the same effective state.

### 23.5 Fuzz Tests

Adversarial malformed inputs, edge-case graphs, namespace collisions, cyclic dependency scenarios.

### 23.6 Policy Matrix Tests

Same artifact under different profiles to confirm rule override and admissibility behavior.

### 23.7 Federation Tests

Cross-domain artifacts with signatures, trust classes, and external ontology dependencies.

### 23.8 Repair Round-Trip Tests

Validate, repair, revalidate, confirm stable admissible output and reversible patch behavior.

---

## 24. Failure Modes

The validator must explicitly guard against common failure modes.

### 24.1 Over-Rejection

Rejecting too aggressively can block useful ingestion and evolution. Profiles and repair pathways mitigate this.

### 24.2 Silent Under-Validation

Permissive modes must not silently admit dangerous artifacts without strong annotation and isolation.

### 24.3 Cascading Duplicate Findings

Root-cause grouping is necessary to prevent unusable reports.

### 24.4 Policy Drift

If policies change without corresponding revalidation, stored artifacts may become unsound. Revalidation triggers must exist.

### 24.5 Non-Deterministic Resolution

Reference or ontology lookup ambiguity must not produce unstable validation outcomes.

### 24.6 Repair-Induced Semantic Drift

Auto-fix systems must not change meaning invisibly. All guarded or semantic repairs must be logged and reviewable.

---

## 25. Canonical Report Formats

The validator must emit at least two canonical forms.

### 25.1 Human Report

Designed for developers, operators, and governance reviewers.

Should include:

- summary counts,
- disposition,
- grouped findings,
- source excerpts,
- repair suggestions,
- next steps.

### 25.2 Machine Report

Designed for CI, APIs, editors, and automation.

Should include structured fields for:

- findings,
- pass outputs,
- metrics,
- profile,
- rule versions,
- repair bundles,
- disposition,
- trust metadata.

---

## 26. Integration with Other AASL Subsystems

The validator interacts closely with the rest of the AASL stack.

### 26.1 Parser

Consumes AST/source maps and parser recovery metadata.

### 26.2 Runtime Model

Checks object lifecycle, registry admissibility, mutation legality, and active namespace coherence.

### 26.3 Compiler

Validates compiler output and helps distinguish source ambiguity from emitted semantic defects.

### 26.4 Query Engine

Ensures indexed/queryable artifacts meet shape and semantic guarantees.

### 26.5 Storage Layer

Provides admission outcome, retention flags, and quarantine routing.

### 26.6 Federation Layer

Provides export/import admissibility and trust-boundary enforcement.

### 26.7 Governance Layer

Enforces registry rules, deprecations, namespace ownership, and proposal maturity requirements.

### 26.8 Tooling Layer

Provides diagnostics and repair pathways to CLI, editor, CI, and operator interfaces.

---

## 27. Minimal Canonical APIs

The following logical interfaces should exist, regardless of implementation language.

### 27.1 Validate Whole Document

Input:

- document,
- profile,
- context.

Output:

- validation report,
- disposition,
- normalized artifact reference,
- repair bundle candidates.

### 27.2 Validate Patch

Input:

- base artifact,
- patch,
- profile.

Output:

- impacted scope,
- findings,
- patch admissibility,
- required revalidation breadth.

### 27.3 Revalidate on Policy Change

Input:

- stored artifact set,
- policy delta.

Output:

- affected artifacts,
- new findings,
- quarantine/release actions.

### 27.4 Generate Repair Suggestions

Input:

- validation report.

Output:

- ranked repair candidates.

### 27.5 Explain Finding

Input:

- finding ID.

Output:

- full rationale,
- source context,
- related rules,
- likely repair steps.

---

## 28. Implementation Phasing

The validator should be implemented in stages.

### Phase 1: Core Structural Validator

Includes:

- input integrity,
- structural envelope,
- type and shape validation,
- human and machine reports.

### Phase 2: Identity and Reference Validation

Includes:

- namespace checks,
- ID uniqueness,
- reference resolution,
- dependency graph basics.

### Phase 3: Ontology and Invariant Validation

Includes:

- schema compatibility,
- ontology registry integration,
- cross-field invariants,
- lifecycle logic.

### Phase 4: Policy and Runtime Admissibility

Includes:

- security and governance policy,
- semantic closure checks,
- quarantine and admission engine.

### Phase 5: Repair and Incremental Validation

Includes:

- auto-fix suggestions,
- diff-aware validation,
- cache and revalidation support,
- LSP/editor integration.

### Phase 6: Federation and Trust Validation

Includes:

- provenance,
- signature verification,
- trust scoring,
- cross-domain policy profiles.

---

## 29. Non-Goals

The validator is not responsible for:

- free-form content truth adjudication in the epistemic sense,
- executing workflows to see whether they “work,”
- performing arbitrary business logic not encoded as AASL rules or policy,
- replacing governance judgment for novel ontology admissions,
- silently mutating user content without an audit trail.

---

## 30. Canonical Acceptance Criteria

The validator architecture is considered complete when Atrahasis can do all of the following reliably:

1. validate an authored `.aas` file deterministically,
2. validate AASC compiler output deterministically,
3. emit source-mapped findings with stable rule IDs,
4. distinguish blocking vs non-blocking defects,
5. produce final admissibility state,
6. generate repair suggestions,
7. support strict, standard, permissive, patch, and federation modes,
8. revalidate incrementally after localized edits,
9. quarantine high-risk artifacts,
10. enforce policy and trust boundaries before runtime admission.

---

## 31. Recommended Next Document

The next canonical document to generate after this one is:

**Atrahasis_AASL_Query_Engine_Specification.md**

Reason:
Once parser, runtime, compiler, and validator are defined, the next missing subsystem is the mechanism by which validated semantic graphs are retrieved, traversed, filtered, reasoned over, and served to agents and applications.

---

## 32. Final Statement

The AASL validator is the formal semantic gatekeeper of the Atrahasis system. It converts AASL from a flexible authoring and compilation medium into a trusted substrate for storage, retrieval, governance, execution, and federation.

Without this subsystem, AASL can be parsed, authored, and compiled, but it cannot yet be safely admitted. With this subsystem, every artifact can be evaluated against structure, meaning, trust, and policy before it becomes part of the live semantic fabric.

That is what allows Atrahasis to scale from documents to dependable intelligence infrastructure.
