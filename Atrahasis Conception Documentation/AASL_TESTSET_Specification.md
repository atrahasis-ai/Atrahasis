# AASL_TESTSET Specification

**Document ID:** AASL-BOOTSTRAP-TESTSET-001  
**Status:** Canonical Bootstrap Artifact Specification  
**Version:** 1.0.0  
**Applies To:** Atrahasis AASL Runtime, Parser, Validator, Compiler, Query Engine, Tooling, and Conformance Infrastructure  
**Primary Audience:** Runtime engineers, parser/compiler engineers, validator engineers, ontology authors, tooling developers, agent-system integrators, QA and verification teams  

---

## 1. Purpose

`AASL_TESTSET` is the canonical conformance and stress-testing corpus for the Atrahasis Agentic Artifact Specification Language (AASL). It exists to ensure that all compliant AASL implementations parse, validate, canonicalize, compile, query, store, render, and exchange AASL artifacts with identical observable behavior under controlled conditions.

The testset is not merely a parser fixture library. It is the authoritative verification substrate for the entire AASL ecosystem. Its purpose is to:

1. prove cross-implementation semantic equivalence,
2. detect ambiguity in the language or ontology model,
3. prevent silent drift between the specification and implementations,
4. provide a regression baseline for every subsystem,
5. supply training-grade exemplars for agent authoring and repair loops,
6. certify that runtime behavior matches canonical AASL expectations, and
7. support formal admission, interoperability, and release gating.

`AASL_TESTSET` is therefore both a product artifact and a governance artifact.

---

## 2. Scope

This specification defines:

- the purpose and structure of the AASL test corpus,
- test categories and required coverage,
- directory and manifest layout,
- normative metadata for every test case,
- expected outputs and oracle formats,
- conformance levels,
- execution modes,
- pass/fail semantics,
- cross-version stability rules,
- ontology-specific and profile-specific test overlays,
- fuzz, mutation, adversarial, and scale test classes,
- certification workflows for AASL implementations.

This specification does **not** define the language itself; it defines how the language is tested.

---

## 3. Design Principles

`AASL_TESTSET` SHALL be governed by the following principles:

### 3.1 Deterministic Observability

A test must define expected behavior in a form that is machine-checkable and implementation-neutral.

### 3.2 Layer Isolation

Tests must isolate parser, validator, compiler, runtime, query, storage, and rendering responsibilities wherever practical.

### 3.3 Semantic Priority

Superficial textual differences do not matter unless they affect canonicalization or observable semantics.

### 3.4 Failure Explicitness

Every invalid or rejected case must specify exactly why it fails and which layer is responsible.

### 3.5 Progressive Depth

The corpus must include beginner-readable cases, production-grade cases, and pathological stress cases.

### 3.6 Ecosystem Portability

A compliant implementation in any language must be able to consume the testset without hidden assumptions.

### 3.7 Anti-Overfitting

The testset must not reward brittle implementations that merely memorize fixture strings; it must include parametric, generated, and mutation-based cases.

---

## 4. Conformance Objectives

The testset SHALL verify the following objectives.

### 4.1 Syntax Conformance

The implementation correctly lexes and parses valid AASL syntax and rejects invalid syntax with correct diagnostics.

### 4.2 Structural Conformance

The implementation constructs the correct CST, AST, and semantic graph shape for valid inputs.

### 4.3 Validation Conformance

The implementation performs all mandatory validation passes and emits the required issue classes, codes, and severities.

### 4.4 Canonicalization Conformance

The implementation produces the canonical normalized form required by the AASL specification.

### 4.5 Compilation Conformance

When given supported non-AASL source inputs, the implementation produces semantically correct AASL outputs and trace metadata.

### 4.6 Runtime Conformance

The runtime resolves references, identities, versions, inheritance, closures, and mutability boundaries correctly.

### 4.7 Query Conformance

The query engine returns the correct bindings, result ordering, nullability behavior, and explanation metadata.

### 4.8 Storage and Admission Conformance

Artifact ingestion, storage, and retrieval preserve canonical identity, content integrity, provenance, and version semantics.

### 4.9 Federation Conformance

Remote exchange and replicated evaluation produce stable outcomes across nodes.

### 4.10 Security and Robustness Conformance

Malicious, oversized, malformed, or ambiguity-inducing inputs are handled safely and predictably.

---

## 5. Testset Layers

The complete testset is divided into ten normative layers.

### 5.1 L0: Bootstrap Readability Cases

Small human-readable examples used by developers, documentation, tutorials, and model prompts.

### 5.2 L1: Parser Cases

Focused tests for tokenization, grammar productions, precedence, spans, comments, literals, blocks, lists, declarations, anchors, references, and error recovery.

### 5.3 L2: Validator Cases

Schema, ontology, semantic, admissibility, closure, provenance, permission, and lifecycle validation tests.

### 5.4 L3: Canonicalization Cases

Formatting, ordering, normalization, whitespace, key ordering, identifier normalization, and equivalent-source convergence tests.

### 5.5 L4: Compiler Cases

Conversion from markdown, JSON, structured corpora, and external representations into AASL.

### 5.6 L5: Runtime Cases

Identity resolution, link traversal, overlay composition, mutation semantics, inheritance, multi-document state, and transaction behavior.

### 5.7 L6: Query Cases

Selection, filters, joins, binding, graph navigation, derived predicates, aggregation, windowing, and explain plans.

### 5.8 L7: Interop Cases

Cross-implementation roundtrip, serialization fidelity, remote handoff, federation, and storage portability.

### 5.9 L8: Adversarial Cases

Malformed payloads, ambiguity bombs, recursion traps, resource exhaustion, duplicate identity attacks, provenance forgery, malicious references, and decompression-style input expansion.

### 5.10 L9: Scale and Endurance Cases

Large corpora, long-lived sessions, high object counts, high reference density, deep module chains, and repeated query loads.

---

## 6. Normative Repository Layout

A canonical distribution of `AASL_TESTSET` SHALL conform to the following layout.

```text
AASL_TESTSET/
  README.md
  MANIFEST.aasl
  VERSION
  LICENSE
  profiles/
    core/
    strict/
    educational/
    runtime/
    federation/
    security/
  ontologies/
    core/
    domain-*/
  fixtures/
    l0-bootstrap/
    l1-parser/
    l2-validator/
    l3-canonicalization/
    l4-compiler/
    l5-runtime/
    l6-query/
    l7-interop/
    l8-adversarial/
    l9-scale/
  generators/
  mutation/
  fuzz/
  oracle/
  schemas/
  scripts/
  reports/
  certification/
```

### 6.1 README.md

Human-readable overview of the corpus, execution modes, and compatibility notes.

### 6.2 MANIFEST.aasl

The canonical machine-readable index of all tests, categories, required implementations, expected outcomes, and artifact hashes.

### 6.3 VERSION

The version of the testset itself, independent from implementation versions.

### 6.4 profiles/

Profile-specific overlays that enable subsets or stricter requirement sets.

### 6.5 ontologies/

Ontology-specific tests that validate semantics beyond the language core.

### 6.6 fixtures/

The primary test cases grouped by layer.

### 6.7 generators/

Programs or declarative specs that generate parametric and large-scale tests.

### 6.8 mutation/

Fixtures produced by controlled mutation of valid seeds.

### 6.9 fuzz/

Randomized or guided fuzz campaigns and retained minimization outputs.

### 6.10 oracle/

Expected outputs, diagnostics, canonical forms, and result bindings.

### 6.11 certification/

Release gating policies, implementation scorecards, and signed conformance records.

---

## 7. Test Case Unit Model

Every test case SHALL be represented as a directory or grouped artifact package with the following minimum components.

```text
<test-id>/
  case.aasl            # or source input such as case.md / case.json
  metadata.aasl
  expected/
    outcome.aasl
    diagnostics.aasl
    canonical.aasl
    ast.json
    graph.json
    query-results.aasl
    explain.aasl
  notes.md
```

Not every case requires every expected artifact, but every case must declare which outputs are normative.

---

## 8. Required Metadata Fields

Each test case SHALL define at least the following metadata.

```aasl
@test {
  id: "L2-VAL-0042"
  title: "Reject duplicate stable IDs within same namespace"
  layer: validator
  profile: core
  status: normative
  source-format: aasl
  feature-tags: [identity, namespace, duplicate-detection]
  required-capabilities: [parse, validate]
  expected-outcome: reject
  oracle-set: [diagnostics]
  minimum-spec-version: "1.0.0"
}
```

### 8.1 Field Definitions

- `id`: globally unique stable test identifier.
- `title`: concise human-readable name.
- `layer`: primary test layer.
- `profile`: applicable conformance profile.
- `status`: `normative`, `informative`, `experimental`, or `deprecated`.
- `source-format`: input format under test.
- `feature-tags`: searchable capability labels.
- `required-capabilities`: capabilities an implementation must expose to run the test.
- `expected-outcome`: `accept`, `reject`, `repair`, `warn`, `canonicalize`, `compile`, `query`, `roundtrip`, or `stress-pass`.
- `oracle-set`: expected result bundles that are normative for the case.
- `minimum-spec-version`: minimum AASL spec version required.

### 8.2 Optional Fields

- `maximum-spec-version`
- `ontology`
- `security-class`
- `mutation-parent`
- `generator`
- `seed`
- `nondeterminism-policy`
- `resource-budget`
- `expected-runtime-class`
- `federation-mode`
- `notes`

---

## 9. Oracle Types

An oracle is the normative expected result against which an implementation is evaluated.

### 9.1 Diagnostic Oracle

Expected validation or parsing issues, including:

- issue code,
- severity,
- phase,
- subject identity,
- source span,
- normalized message class,
- repair availability.

### 9.2 Canonicalization Oracle

The exact canonical AASL form expected after normalization.

### 9.3 AST Oracle

A normalized abstract syntax tree representation used only for parser conformance.

### 9.4 Semantic Graph Oracle

A normalized graph form representing resolved objects, links, attributes, inferred defaults, provenance, and closure state.

### 9.5 Query Result Oracle

Expected query bindings, ordering, null semantics, aggregates, and explanation metadata.

### 9.6 Roundtrip Oracle

Expected equivalence after parse → canonicalize → serialize → parse and related cycles.

### 9.7 Performance Oracle

Expected budget class or threshold for scale tests.

### 9.8 Security Oracle

Expected safe handling class, such as reject, sandbox, abort, quarantine, or bounded degrade.

---

## 10. Outcome Semantics

A test case SHALL declare exactly one primary expected outcome and may declare secondary expected properties.

### 10.1 Accept

The input is valid and admissible for the requested profile.

### 10.2 Reject

The input must not be accepted, stored, or executed in the requested context.

### 10.3 Repair

The input is invalid but machine-repairable under a defined repair policy. Repair must emit repair trace metadata.

### 10.4 Warn

The input is valid but requires warnings.

### 10.5 Canonicalize

The implementation must converge the input to a specific canonical form.

### 10.6 Compile

The implementation must transform a non-AASL source into a semantically correct AASL artifact with traceability.

### 10.7 Query

The implementation must execute one or more queries and return the normative bindings.

### 10.8 Roundtrip

The implementation must preserve semantics over declared transformation cycles.

### 10.9 Stress-Pass

The implementation must complete the test within the declared safety and resource constraints.

---

## 11. Conformance Profiles

The testset SHALL support the following minimum profiles.

### 11.1 Core Profile

Required for all compliant AASL implementations.

Includes:
- basic parsing,
- validation,
- canonicalization,
- identity handling,
- stable serialization,
- essential diagnostics.

### 11.2 Strict Profile

Adds stronger determinism, stricter diagnostics, mandatory canonical spans, and narrower ambiguity tolerance.

### 11.3 Educational Profile

Smaller and more readable corpus intended for onboarding, tutorials, and agent prompting.

### 11.4 Runtime Profile

Adds runtime state, transactions, multi-document operations, overlays, and mutation rules.

### 11.5 Federation Profile

Adds transport and multi-node consistency cases.

### 11.6 Security Profile

Adds adversarial, malicious, forged, oversized, and denial-style inputs.

No implementation may claim profile conformance unless it passes all required normative tests for that profile.

---

## 12. Required Coverage Matrix

The following capability families SHALL have explicit test coverage.

### 12.1 Lexical Coverage

- identifiers,
- quoted strings,
- multiline strings,
- numeric forms,
- booleans,
- null-like semantics if supported,
- comments,
- escaping,
- reserved keywords,
- unicode handling policy where applicable,
- byte-order and encoding rejection behavior.

### 12.2 Grammar Coverage

- declarations,
- nested blocks,
- lists,
- maps,
- annotations,
- imports/includes,
- references,
- anchors,
- version declarations,
- ontology attachments,
- query forms if inline.

### 12.3 Validation Coverage

- required fields,
- type mismatch,
- duplicate identity,
- unknown ontology terms,
- forbidden mutation,
- missing provenance,
- unresolved references,
- closure violations,
- namespace collisions,
- illegal lifecycle state transitions.

### 12.4 Canonicalization Coverage

- key ordering,
- default elision or inclusion policy,
- stable indentation,
- normalized quoting,
- list ordering policy,
- identifier casing policy,
- deterministic serialization of semantically equivalent inputs.

### 12.5 Runtime Coverage

- object creation,
- update,
- deprecation,
- replacement,
- overlay resolution,
- inheritance resolution,
- transaction rollback,
- snapshot consistency,
- multi-document merge semantics.

### 12.6 Query Coverage

- graph traversal,
- filtering,
- joins,
- aggregates,
- path navigation,
- empty result handling,
- duplicate suppression,
- deterministic ordering,
- explanation trees.

### 12.7 Interop Coverage

- cross-language serialization,
- cross-node exchange,
- signed artifact portability,
- version negotiation,
- downgrade and upgrade behavior.

### 12.8 Security Coverage

- malformed structure,
- deeply nested recursion,
- fake provenance,
- duplicate hash collisions,
- path traversal style references,
- expansion bombs,
- oversized literals,
- cyclic include attacks,
- partial signature tampering.

---

## 13. Test Classes

### 13.1 Golden Tests

Hand-authored fixtures with exact expected outputs.

### 13.2 Differential Tests

The same input executed against multiple implementations to detect divergence.

### 13.3 Parametric Tests

Generated from templates with controlled variable sets.

### 13.4 Mutation Tests

Produced by applying controlled corruptions to valid source cases.

### 13.5 Fuzz Tests

Randomized or grammar-guided inputs, generally used for robustness rather than normative exact output.

### 13.6 Corpus Tests

Realistic multi-file projects simulating developer or agent workflows.

### 13.7 Scenario Tests

Multi-step tests spanning compile, validate, store, query, mutate, and federate operations.

### 13.8 Endurance Tests

Long-run stability tests with repeated operations or sustained load.

---

## 14. Naming Conventions

Test IDs SHALL use the following canonical pattern:

```text
L<layer>-<domain>-<number>
```

Examples:

- `L1-PARSE-0007`
- `L2-VAL-0141`
- `L3-CANON-0022`
- `L6-QUERY-0099`
- `L8-SEC-0015`

Mutation-derived tests may append suffixes:

- `L2-VAL-0141-M03`
- `L1-PARSE-0007-FUZZ-R214`

---

## 15. Manifest Specification

`MANIFEST.aasl` SHALL enumerate every test artifact and its properties.

Minimum manifest fields:

- test id,
- file paths,
- artifact hashes,
- profile inclusion,
- layer,
- ontology dependencies,
- expected outcome,
- oracle bundle,
- normative status,
- version compatibility,
- generator reference if applicable.

Example:

```aasl
@testset-manifest {
  version: "1.0.0"
  tests: [
    {
      id: "L1-PARSE-0001"
      path: "fixtures/l1-parser/L1-PARSE-0001/"
      hash: "sha256:..."
      profile: core
      outcome: accept
      oracle-set: [ast, canonical]
    }
  ]
}
```

---

## 16. Execution Model

A conforming test harness SHALL support the following execution phases.

### 16.1 Discovery

Load the manifest, resolve profile and version filters, verify file integrity.

### 16.2 Capability Matching

Determine whether the implementation under test supports the required capability set.

### 16.3 Preparation

Load ontologies, seed storage, initialize runtime state, provision federation peers if needed.

### 16.4 Execution

Invoke parser, validator, compiler, runtime, query engine, or external transport as required by the case.

### 16.5 Observation

Capture diagnostics, canonical outputs, query bindings, runtime traces, and performance metrics.

### 16.6 Normalization

Normalize outputs into oracle-comparable form.

### 16.7 Comparison

Compare the implementation outputs to the oracle set.

### 16.8 Reporting

Emit machine-readable and human-readable pass/fail records.

---

## 17. Pass/Fail Rules

### 17.1 Normative Tests

A normative test passes only if all declared required oracles match within the allowed comparison policy.

### 17.2 Informative Tests

Informative tests do not affect profile conformance but should still be reported.

### 17.3 Experimental Tests

Experimental tests may be run for forward compatibility but must not block certification.

### 17.4 Partial Support

If an implementation lacks a required capability for a profile it claims, the relevant tests are failures, not skips.

### 17.5 Skips

Skips are allowed only for features outside the declared conformance profile.

---

## 18. Comparison Policies

Every oracle comparison SHALL declare one of the following policies.

### 18.1 Exact Text Match

Used for canonical serialization outputs.

### 18.2 Structural Equivalence

Used for AST and graph outputs where field ordering is irrelevant after normalization.

### 18.3 Set Equivalence

Used when output ordering is defined as semantically irrelevant.

### 18.4 Ordered Binding Equivalence

Used for query results when deterministic ordering is required.

### 18.5 Threshold Compliance

Used for bounded performance or resource tests.

### 18.6 Class Match

Used for security handling classes and other category-based outcomes.

---

## 19. Diagnostics Normalization

Because implementations may differ in wording while still matching semantically, diagnostic comparison SHALL be based on normalized issue records rather than raw free-text messages.

Each normalized record SHALL include:

- issue code,
- severity,
- phase,
- path or subject identity,
- stable message class,
- optional source span,
- optional suggested repair class.

Raw messages may be preserved for humans but are not the primary oracle unless explicitly required.

---

## 20. Canonical Seed Corpus

The testset SHALL include a seed corpus of small, medium, and large hand-authored artifacts that collectively demonstrate all core language features.

Minimum seed groups:

1. identity and reference examples,
2. ontology attachment examples,
3. lifecycle and mutation examples,
4. provenance and signature examples,
5. queryable graph examples,
6. multi-file import and include examples,
7. compiler input/output examples,
8. federation and synchronization examples.

These seeds are the parent material for mutation and fuzz campaigns.

---

## 21. Mutation Framework

The mutation subsystem SHALL produce invalid, borderline, and ambiguity-inducing variants of valid seeds.

Mutation families should include:

- deletion of required fields,
- duplicate insertion,
- reference corruption,
- span corruption,
- nesting explosion,
- type substitution,
- namespace collision,
- ordering perturbation,
- signature tampering,
- provenance erasure,
- invalid lifecycle transitions.

Every mutation-generated case SHALL record:

- source parent,
- mutation operator,
- mutation parameters,
- intended failure mode.

---

## 22. Fuzzing Strategy

The testset SHALL support both retained fuzz artifacts and reproducible fuzz campaigns.

### 22.1 Grammar-Guided Fuzzing

Preferred for parser and validator discovery.

### 22.2 Semantic Fuzzing

Generates syntactically valid but semantically stressful artifacts.

### 22.3 Query Fuzzing

Exercises edge cases in filters, paths, joins, and aggregations.

### 22.4 Runtime State Fuzzing

Perturbs operation sequences to discover illegal state transitions or rollback defects.

Every retained fuzz artifact must be minimized and assigned a stable test ID when promoted into the canonical corpus.

---

## 23. Adversarial Security Corpus

The security corpus SHALL include tests specifically designed to validate safe failure behavior.

Required families include:

- deeply recursive artifacts,
- oversized string and blob handling,
- malicious include graphs,
- forged provenance chains,
- partial signature mismatch,
- duplicate stable IDs with divergent content,
- ontology shadowing attacks,
- alias confusion attacks,
- reference cycles used for resource exhaustion,
- parser recovery abuse inputs.

Security tests must specify expected handling classes such as:

- reject,
- quarantine,
- bounded parse failure,
- bounded validation failure,
- resource abort,
- sandbox isolate.

---

## 24. Scale Benchmarks

The scale layer SHALL contain reproducible corpora sized across graduated classes.

Suggested normative classes:

- `S1`: up to 100 objects,
- `S2`: up to 1,000 objects,
- `S3`: up to 10,000 objects,
- `S4`: up to 100,000 objects,
- `S5`: implementation-defined research scale.

Benchmarks shall measure:

- parse throughput,
- validation throughput,
- canonicalization stability,
- query latency bands,
- memory footprint classes,
- rollback integrity under mutation bursts.

The specification does not require fixed absolute numeric performance targets across all environments, but it does require deterministic reporting and bounded safety behavior.

---

## 25. Cross-Version Compatibility Rules

The testset SHALL evolve independently while preserving traceable version semantics.

### 25.1 Version Triples

Both the AASL spec and the testset must use semver-like version identifiers.

### 25.2 Backward Stability

A patch-level testset release may add clarifications and new informative cases, but must not silently change expected outcomes of existing normative tests without explicit changelog entry.

### 25.3 Outcome Change Protocol

If the expected result of a normative test changes, the test ID must either:

1. receive a new version-qualified replacement, or
2. be retained with explicit deprecated outcome notes and changelog.

### 25.4 Spec Binding

Each test must declare the minimum supported AASL spec version and optional maximum version.

---

## 26. Ontology-Specific Extensions

AASL core conformance is separate from ontology-specific conformance.

Ontology packs may add tests for:

- required domain classes,
- term compatibility,
- domain invariants,
- semantic closure expectations,
- specialized query vocabularies,
- profile-specific admissibility rules.

Ontology packs must not weaken core language invariants.

---

## 27. Certification Workflow

`AASL_TESTSET` SHALL support formal implementation certification.

### 27.1 Certification Levels

- **Bronze:** Core parser and validator conformance.
- **Silver:** Core + canonicalization + runtime/query basics.
- **Gold:** Core + runtime + query + interop + security profile.
- **Platinum:** Full profile set including federation, scale, and deterministic release reproducibility.

### 27.2 Certification Inputs

An implementation seeking certification shall provide:

- implementation identifier,
- version,
- supported profiles,
- runtime environment metadata,
- capability declaration,
- test harness version,
- signed results bundle.

### 27.3 Certification Outputs

The certification pipeline shall emit:

- pass/fail summary,
- per-profile coverage,
- divergence records,
- waivers if any,
- signed attestation artifact.

---

## 28. Reporting Formats

A conforming harness SHALL emit reports in both human-readable and machine-readable forms.

Minimum report artifacts:

- `summary.json`
- `summary.aasl`
- `failures.json`
- `coverage.json`
- `certification-record.aasl`

Report dimensions should include:

- total tests,
- executed tests,
- skipped tests,
- passed tests,
- failed tests,
- flaky detections if any,
- profile coverage,
- feature-tag coverage,
- runtime resource notes.

---

## 29. Flakiness Policy

Normative tests must not be flaky.

If a test exhibits nondeterministic outcomes across repeated execution under stable conditions, it must be removed from the normative set or redesigned. Nondeterministic research tests may exist only under explicit experimental status.

---

## 30. Release Gating Rules

A reference implementation release SHALL NOT be marked conformant unless:

1. all required normative tests for its declared profile set pass,
2. no unresolved severity-critical security corpus failures remain,
3. no canonicalization divergence exists in declared deterministic modes,
4. testset version and implementation version are recorded together.

---

## 31. Agent-Oriented Use of the Testset

Because AASL is intended for agentic systems, the testset SHALL also support model and agent workflows.

This includes:

- prompt-ready examples for valid authoring,
- invalid examples paired with correct diagnostics,
- repair cases showing before/after transformations,
- query examples with explanations,
- compiler examples mapping source text to AASL outputs.

These materials may be derived from the same canonical cases, but tutorial packaging must never modify the normative oracle itself.

---

## 32. Minimum Canonical Starter Corpus

The first release of `AASL_TESTSET` SHALL include at minimum:

### 32.1 Parser

- 50 valid syntax cases,
- 50 invalid syntax cases,
- 20 recovery cases.

### 32.2 Validator

- 75 semantic validity cases,
- 75 semantic rejection cases,
- 25 warning-only cases,
- 25 repairable cases.

### 32.3 Canonicalization

- 40 equivalence convergence cases,
- 20 stable serialization cases.

### 32.4 Compiler

- 25 markdown compilation cases,
- 25 JSON compilation cases,
- 10 ambiguous-source trace cases.

### 32.5 Runtime

- 40 resolution and mutation cases,
- 20 transaction and rollback cases.

### 32.6 Query

- 50 query behavior cases,
- 20 explain-plan cases.

### 32.7 Security

- 40 adversarial rejection cases,
- 10 bounded degradation cases.

### 32.8 Interop and Roundtrip

- 30 roundtrip equivalence cases,
- 15 multi-node exchange cases.

These are minimums, not targets.

---

## 33. Example Minimal Test Case

### 33.1 Input

```aasl
@artifact {
  id: "demo.alpha"
  type: concept
  title: "Alpha"
}
```

### 33.2 Metadata

```aasl
@test {
  id: "L1-PARSE-0001"
  title: "Parse minimal artifact declaration"
  layer: parser
  profile: core
  status: normative
  source-format: aasl
  required-capabilities: [parse]
  expected-outcome: accept
  oracle-set: [ast, canonical]
  minimum-spec-version: "1.0.0"
}
```

### 33.3 Expected Canonical Output

```aasl
@artifact {
  id: "demo.alpha"
  title: "Alpha"
  type: concept
}
```

### 33.4 Expected Outcome

- parse succeeds,
- no diagnostics,
- canonical output matches oracle.

---

## 34. Example Rejection Case

### 34.1 Input

```aasl
@artifact {
  id: "demo.alpha"
  id: "demo.beta"
  type: concept
}
```

### 34.2 Expected Diagnostics

```aasl
@diagnostics {
  issues: [
    {
      code: "VAL_DUPLICATE_FIELD"
      severity: error
      phase: validator
      subject: "demo.alpha"
    }
  ]
}
```

### 34.3 Expected Outcome

- parser may accept,
- validator must reject,
- artifact is inadmissible.

---

## 35. Governance of the Testset

`AASL_TESTSET` is a controlled artifact and SHALL be governed under the AASL ontology and governance framework.

Changes to the normative corpus must follow:

1. proposal,
2. review,
3. reference implementation verification,
4. changelog entry,
5. version increment,
6. signed publication.

Major governance events include:

- adding a new normative profile,
- changing an oracle format,
- deprecating a test family,
- changing outcome semantics,
- introducing a certification threshold.

---

## 36. Changelog Requirements

Every published version of the testset SHALL include a changelog with:

- added tests,
- removed tests,
- deprecated tests,
- changed expected outcomes,
- new profiles,
- new ontology overlays,
- security additions,
- certification policy changes.

---

## 37. Implementation Guidance

Although not normative, implementers are strongly advised to:

- separate parser tests from validator tests in code,
- retain normalized intermediate representations for debugging,
- support single-test execution by ID,
- support profile-based filtering,
- store historical certification reports,
- run mutation and fuzz campaigns continuously,
- treat every divergence from the canonical corpus as a release blocker until triaged.

---

## 38. Non-Goals

The testset is not intended to:

- replace the AASL language specification,
- define product-specific business rules beyond ontology packs,
- enforce a single implementation architecture,
- guarantee performance portability across all hardware,
- serve as the only source of training examples.

---

## 39. Acceptance Criteria for This Specification

This specification is complete when the Atrahasis program can generate and maintain a canonical `AASL_TESTSET` repository that:

1. covers all mandatory AASL subsystem behaviors,
2. supports profile-based conformance evaluation,
3. uses stable manifests and oracle bundles,
4. detects parser, validator, compiler, runtime, query, interop, and security regressions,
5. enables certification of independent implementations,
6. supports both human developers and agentic authoring systems.

---

## 40. Final Normative Statement

No AASL implementation may claim full language conformance on the basis of parser success alone. Conformance exists only when the implementation passes the required normative portions of `AASL_TESTSET` for its declared profile set and does so with reproducible, auditable, oracle-matching behavior.

`AASL_TESTSET` is therefore a first-class component of the AASL ecosystem and must be maintained with the same rigor as the language specification itself.
