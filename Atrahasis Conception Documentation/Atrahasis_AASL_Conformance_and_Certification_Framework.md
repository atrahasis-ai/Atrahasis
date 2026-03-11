# Atrahasis AASL Conformance and Certification Framework

**Document ID:** ATR-AASL-CONFORMANCE-CERT-001  
**Status:** Canonical Draft  
**Version:** 1.0.0  
**Applies To:** AASL parsers, validators, runtimes, compilers, query engines, storage engines, tooling, adapters, governance services, and integrated Atrahasis execution environments  
**Authoritative Scope:** Defines the normative framework for determining whether an implementation, component, profile, or deployment is conformant with the Atrahasis Agent Semantic Language (AASL) ecosystem and whether it qualifies for formal certification.

---

## 1. Purpose

This document defines the authoritative conformance and certification model for the AASL ecosystem. Its purpose is to ensure that independently built AASL implementations behave consistently, exchange artifacts safely, preserve semantic meaning, and satisfy minimum guarantees required for interoperable operation inside the Atrahasis architecture.

The framework separates four related but distinct questions:

1. Whether an implementation is **syntactically conformant**.
2. Whether an implementation is **semantically conformant**.
3. Whether an implementation is **operationally safe and profile-compliant**.
4. Whether an implementation has passed the evidence and audit thresholds required for **certification**.

Conformance is a technical property. Certification is an attested status granted after structured evaluation.

---

## 2. Design Goals

The framework exists to achieve the following goals:

- Preserve cross-implementation semantic equivalence.
- Prevent ecosystem fragmentation caused by parser drift, ontology drift, or runtime divergence.
- Establish objective and repeatable pass/fail criteria.
- Allow multiple implementation languages and deployment models without sacrificing determinism.
- Support progressive maturity through profiles, levels, and capability classes.
- Provide a path for internal Atrahasis reference implementations and external third-party implementations to be judged against the same rules.
- Make failures diagnosable, reproducible, and appealable.
- Support both strict certification and lower-friction developer self-assessment.

---

## 3. Scope

This framework governs the following implementation classes:

- AASL parsers
- AASL validators
- AASL canonicalizers
- AASL runtimes
- AASC compilers
- Query engines
- Storage engines and indexers
- File readers and writers
- CLI tooling
- IDE/editor integrations
- Conversion adapters
- Governance registries
- Distributed execution or federation components
- Full-stack integrated AASL platforms

This framework does not replace the normative technical behavior defined in the language and subsystem specifications. Instead, it defines how compliance with those documents is measured.

---

## 4. Relationship to Other Canonical Documents

This framework derives its rules from the broader AASL document set, especially:

- `AASL_SPECIFICATION.md`
- `AASL_PRIMER.md`
- `AASL_TESTSET_Specification.md`
- `Atrahasis_AASL_Parser_Architecture.md`
- `Atrahasis_AASL_Runtime_Model.md`
- `Atrahasis_AASC_Compiler_Architecture.md`
- `Atrahasis_AASL_Validator_Architecture.md`
- `Atrahasis_AASL_Query_Engine_Specification.md`
- `Atrahasis_AASL_File_Infrastructure_Specification.md`
- `Atrahasis_AASL_Developer_Tooling_Specification.md`
- `Atrahasis_AASL_Conversion_Pipeline_Specification.md`
- `Atrahasis_AASL_Ontology_Registry_and_Governance_Operations.md`

If this document conflicts with a lower-level subsystem specification on implementation behavior, the subsystem specification governs behavior and this document governs assessment methodology.

---

## 5. Core Definitions

### 5.1 Conformance

Conformance means an implementation behaves in accordance with mandatory requirements applicable to its declared component class, capability set, and certification profile.

### 5.2 Certification

Certification is the formally attested status that a specific implementation build, version, and configuration has successfully satisfied the required conformance evaluation for a specified certification target.

### 5.3 Certification Target

A certification target is the exact object under review. It may be:

- a library release,
- a service deployment,
- a CLI binary,
- an IDE extension version,
- a hosted platform endpoint,
- or a complete integrated runtime stack.

### 5.4 Normative Requirement

A normative requirement is a requirement identified using mandatory language such as MUST, MUST NOT, REQUIRED, SHALL, or SHALL NOT.

### 5.5 Capability Claim

A capability claim is a declaration by the implementation owner that the implementation supports a named feature, profile, grammar subset, ontology set, transport, file format, or execution mode.

### 5.6 Certification Profile

A certification profile is a named bundle of required capabilities, restricted options, operational assumptions, and pass criteria.

### 5.7 Conformance Artifact

A conformance artifact is any evidence used during evaluation, including logs, traces, golden outputs, test reports, reproducibility scripts, build manifests, environment fingerprints, and signed declarations.

### 5.8 Reference Implementation

A reference implementation is an implementation maintained to exemplify intended behavior. Reference status does not automatically imply certification, though reference implementations are usually expected to pursue the highest certification tier.

---

## 6. Conformance Philosophy

AASL certification is based on the principle that interoperability requires more than successful parsing. An implementation is not meaningfully conformant unless it preserves the same semantic graph, validation outcomes, and operational commitments expected by the specifications.

Accordingly, conformance is assessed across multiple dimensions:

- **Lexical conformance**: tokenization, span handling, encoding rules.
- **Syntactic conformance**: grammar recognition and parse admissibility.
- **Structural conformance**: AST/CST shape, document object formation, canonical serialization.
- **Semantic conformance**: ontology binding, identity resolution, reference interpretation, validation semantics.
- **Behavioral conformance**: runtime execution, transaction semantics, query semantics, mutation rules.
- **Operational conformance**: safety controls, determinism claims, error handling, observability.
- **Profile conformance**: restrictions and feature guarantees tied to specific deployment classes.

An implementation that passes only one layer cannot advertise full AASL conformance unless the certification profile explicitly limits scope.

---

## 7. Conformance Dimensions

### 7.1 Syntax Conformance

An implementation claiming syntax conformance MUST:

- accept all valid documents within its declared grammar/profile scope,
- reject invalid documents with spec-compliant diagnostics,
- preserve required source spans and offsets,
- correctly implement lexical rules,
- correctly distinguish fatal syntax failures from recoverable issues where recovery is permitted.

### 7.2 Canonicalization Conformance

An implementation claiming canonicalization support MUST:

- produce canonical forms identical to the normative canonicalization rules,
- avoid semantically significant output drift,
- preserve stable ordering where required,
- generate equivalent hashes for semantically identical documents under the canonical profile.

### 7.3 Validation Conformance

A validator-conformant implementation MUST:

- apply the required validation passes in the specified order when order matters,
- assign severity levels correctly,
- produce admissibility decisions consistent with the spec,
- emit machine-readable diagnostics and evidence traces,
- distinguish schema failure, ontology failure, identity failure, integrity failure, and policy failure.

### 7.4 Runtime Conformance

A runtime-conformant implementation MUST:

- instantiate the required runtime object model,
- enforce object lifecycle and mutability rules,
- preserve semantic identity constraints,
- implement required transactional behavior,
- resolve references deterministically or emit correct uncertainty states,
- expose state transitions and execution outcomes in a spec-compliant way.

### 7.5 Compiler Conformance

A compiler-conformant implementation MUST:

- preserve source-to-semantic traceability,
- construct valid semantic graphs,
- emit ambiguity markers where semantic interpretation is not uniquely determined,
- support required provenance capture,
- avoid introducing unsupported inferred meaning without marking it explicitly.

### 7.6 Query Conformance

A query-conformant implementation MUST:

- parse and execute the declared query subset correctly,
- preserve result semantics under normative evaluation rules,
- implement ordering, filtering, graph traversal, and projection behavior consistently,
- distinguish no-result from invalid-query and inaccessible-scope states.

### 7.7 File and Transport Conformance

A file/transport-conformant implementation MUST:

- correctly read and write `.aas` documents,
- preserve encoding guarantees,
- honor integrity metadata rules,
- support required packaging and manifest constraints for its profile,
- reject corrupt or nonconformant artifacts with proper diagnostic codes.

### 7.8 Tooling Conformance

A tooling-conformant implementation MUST:

- present diagnostics consistently with the normative error model,
- avoid destructive or silent semantic rewrites,
- expose canonical formatting and validation behavior where claimed,
- respect profile restrictions and ontology registry rules.

### 7.9 Governance Conformance

A governance-conformant implementation MUST:

- correctly consume approved registry state,
- respect namespace and deprecation policies,
- distinguish stable, experimental, deprecated, and revoked entities,
- prevent invalid ontology assumptions from silently entering production flows.

---

## 8. Conformance Levels

AASL defines layered conformance levels so that implementations may certify at an appropriate scope.

### Level 0: Declared Compatibility

The implementation publishes a capability declaration and self-assessment but has not completed formal testing.

This level is not certified.

### Level 1: Syntax-Conformant

The implementation has passed syntax, lexical, and basic file handling requirements within a declared scope.

Typical targets:

- parser libraries,
- syntax highlighters,
- linting front ends,
- read-only viewers.

### Level 2: Semantic-Conformant

The implementation has passed syntax plus validation, ontology interpretation, canonicalization, and semantic graph consistency requirements.

Typical targets:

- validators,
- compilers,
- semantic processors,
- document analysis tools.

### Level 3: Runtime-Conformant

The implementation has passed Level 2 and runtime behavior requirements, including state lifecycle, transaction handling, reference resolution, and execution semantics.

Typical targets:

- agent runtimes,
- execution engines,
- integrated orchestration services.

### Level 4: Interoperability-Certified

The implementation has passed cross-implementation interoperability testing, differential execution analysis, and compatibility with the required reference fixtures and registry baselines.

Typical targets:

- production runtimes,
- distributed deployments,
- platform components intended for federation.

### Level 5: Mission-Critical Certified

The implementation has satisfied Level 4 plus additional requirements for reliability, security hardening, auditability, rollback safety, deterministic replay, and operational incident evidence.

Typical targets:

- critical Atrahasis production systems,
- regulated deployments,
- high-trust execution environments.

---

## 9. Certification Types

Certification is awarded by component class. An implementation may hold multiple certifications.

### 9.1 Parser Certification

Covers lexical analysis, grammar support, recovery behavior, AST/CST shape, spans, and canonical parse outcomes.

### 9.2 Validator Certification

Covers rule evaluation, severity assignment, admissibility determination, ontology checks, and repair guidance outputs.

### 9.3 Compiler Certification

Covers conversion from unstructured or semi-structured inputs to AASL semantic representations, provenance retention, confidence markers, and semantic preservation.

### 9.4 Runtime Certification

Covers execution semantics, graph materialization, state mutation behavior, transaction guarantees, concurrency controls, and observability.

### 9.5 Query Engine Certification

Covers query parsing, semantic evaluation, graph traversal correctness, result stability, and access-control-aware execution semantics.

### 9.6 File Infrastructure Certification

Covers file readers/writers, manifest handling, hash verification, canonical serialization, and package integrity.

### 9.7 Tooling Certification

Covers CLI tools, editors, formatters, visualizers, and developer automation.

### 9.8 Governance Service Certification

Covers ontology registry consumption, proposal state handling, namespace enforcement, compatibility checks, and deprecation/revocation behavior.

### 9.9 Platform Certification

Covers end-to-end integrated behavior across multiple component classes.

---

## 10. Certification Profiles

Profiles define what counts as enough for a given environment.

### 10.1 Core Profile

Minimum required for general AASL ecosystem participation.

Includes:

- syntax conformance,
- core ontology support,
- canonical serialization,
- base diagnostics,
- standard file integrity rules.

### 10.2 Developer Profile

For authoring and local development tools.

Includes:

- Core Profile,
- editor-grade diagnostics,
- formatter consistency,
- repair suggestions,
- local registry snapshot handling.

### 10.3 Runtime Profile

For live execution environments.

Includes:

- Core Profile,
- runtime lifecycle semantics,
- transaction handling,
- reference resolution,
- concurrency controls,
- audit event generation.

### 10.4 Federation Profile

For multi-node or cross-domain deployments.

Includes:

- Runtime Profile,
- interoperability fixtures,
- namespace governance,
- distributed identity compatibility,
- signature verification,
- clock-skew and replay handling.

### 10.5 Safety-Critical Profile

For systems where semantic errors or execution divergence create substantial operational or legal risk.

Includes:

- Federation Profile,
- deterministic replay,
- incident capture,
- stronger rollback guarantees,
- trace completeness,
- hardened policy enforcement.

### 10.6 Research Profile

Allows experimental capabilities so long as unstable features are clearly isolated.

Includes:

- explicit experimental namespace boundaries,
- feature flag disclosure,
- non-stable semantics labeling,
- prohibition on advertising stable conformance for experimental behavior.

---

## 11. Capability Declaration Model

Any implementation seeking certification MUST publish a machine-readable capability declaration.

The declaration MUST include:

- implementation name,
- implementation owner,
- version,
- build hash,
- target component class,
- supported certification profile(s),
- claimed conformance level,
- supported ontology versions,
- supported grammar versions,
- supported file formats,
- supported transports,
- supported optional features,
- unsupported normative features,
- known deviations or waivers,
- dependency manifest,
- test harness version used.

The declaration MUST be signed for formal certification submissions.

---

## 12. Normative Certification Requirements

An implementation MUST NOT be certified unless all of the following are true:

1. The certification target is unambiguously versioned.
2. The capability declaration is complete.
3. The test harness version is recorded.
4. The full required test suite for the requested profile has run.
5. Required evidence artifacts are present and verifiable.
6. No unresolved blocker defects remain in required conformance areas.
7. All waivers are explicitly documented and approved.
8. The evaluation environment is reproducible to the required degree.
9. The implementation has passed differential comparison against reference outcomes where mandated.
10. Security-sensitive claims are supported by evidence, not assertion alone.

---

## 13. Test Taxonomy

The certification process uses a layered taxonomy of tests.

### 13.1 Lexical Tests

Validate encoding, tokenization, whitespace handling, comments, delimiters, escape rules, span tracking, and invalid character behavior.

### 13.2 Grammar Tests

Validate parse acceptance/rejection, ambiguity handling, error recovery, nested constructs, and profile restrictions.

### 13.3 Canonicalization Tests

Validate stable serialization, ordering, hash equivalence, and round-trip normalization.

### 13.4 Structural Tests

Validate AST/CST nodes, object model mapping, document graph formation, schema presence, and manifest relationships.

### 13.5 Semantic Tests

Validate ontology binding, type interpretation, entity identity, reference resolution, provenance semantics, and ambiguity flags.

### 13.6 Validation Tests

Validate rule enforcement, severity mapping, admissibility outcomes, repair hints, and multi-pass diagnostics.

### 13.7 Runtime Behavior Tests

Validate state transitions, mutation semantics, transactions, event generation, rollback, and conflict handling.

### 13.8 Query Tests

Validate graph queries, projections, predicates, aggregation, scope restrictions, pagination, and deterministic result semantics.

### 13.9 Interoperability Tests

Validate exchange across multiple certified or candidate implementations using the same artifacts and expected outcomes.

### 13.10 Differential Tests

Run the same fixture through multiple implementations and compare semantic outputs, diagnostics, and state traces.

### 13.11 Adversarial Tests

Validate resilience to malformed input, ambiguous content, ontology poisoning attempts, invalid registry state, replay input, or corrupt manifests.

### 13.12 Performance Envelope Tests

Validate that the implementation remains correct while handling documents, graphs, and workloads at the scale required by its claimed profile.

### 13.13 Security and Integrity Tests

Validate signature checks, hash checks, trust boundaries, policy enforcement, privilege separation, and tamper detection.

### 13.14 Replay and Audit Tests

Validate whether significant actions can be reconstructed from emitted evidence.

---

## 14. Test Corpus Classes

The certification corpus MUST include the following fixture classes.

### 14.1 Positive Fixtures

Known-valid artifacts that MUST succeed.

### 14.2 Negative Fixtures

Known-invalid artifacts that MUST fail in a specific way.

### 14.3 Boundary Fixtures

Artifacts at size, depth, nesting, or complexity limits.

### 14.4 Ambiguity Fixtures

Artifacts intentionally designed to require uncertainty handling or explicit disambiguation.

### 14.5 Migration Fixtures

Artifacts spanning multiple ontology or grammar versions.

### 14.6 Interop Fixtures

Artifacts specifically chosen for cross-implementation comparison.

### 14.7 Corruption Fixtures

Artifacts containing invalid encoding, truncated sections, hash mismatches, or manifest inconsistencies.

### 14.8 Policy Fixtures

Artifacts used to test safety profile constraints, deprecation rules, restricted namespaces, and revocation handling.

---

## 15. Reference Outcomes

Each certification fixture class MUST have a reference outcome model appropriate to the test type.

Reference outcomes may include:

- parse acceptance/rejection,
- exact diagnostic codes,
- normalized AST/CST forms,
- canonical serialized outputs,
- semantic graph snapshots,
- admissibility decisions,
- runtime event traces,
- query result sets,
- audit logs,
- integrity verdicts.

Reference outcomes MUST specify whether equality is:

- byte-for-byte,
- structurally equivalent,
- semantically equivalent,
- order-insensitive,
- or tolerantly equivalent under declared rules.

---

## 16. Result Classes

All tests MUST yield one of the following result classes:

- **PASS**: requirement satisfied.
- **FAIL**: requirement violated.
- **XFAIL**: expected failure for a documented known limitation outside the requested certification scope.
- **WAIVED**: failure accepted by formal waiver.
- **INCONCLUSIVE**: result invalid due to harness or environment uncertainty.
- **BLOCKED**: required prerequisite unavailable.

Formal certification SHALL treat FAIL, unresolved INCONCLUSIVE, and unresolved BLOCKED outcomes in required areas as non-passing.

---

## 17. Failure Severity in Certification

Certification uses a severity model distinct from document validation severity.

### C0: Informational

Does not affect certification.

### C1: Minor Deviation

Small deviation with no semantic or interoperability impact. May be permitted in lower profiles with documentation.

### C2: Material Deviation

Affects diagnostics, tooling expectations, or non-critical behavior. Usually blocks strict certification unless waived.

### C3: Semantic Deviation

Changes semantic interpretation, admissibility, or cross-implementation behavior. Blocks certification.

### C4: Integrity or Safety Deviation

Affects trust, security, auditability, or safe operation. Blocks certification and may trigger advisory publication.

---

## 18. Evidence Requirements

Every certification submission MUST provide an evidence package.

The evidence package MUST contain:

- capability declaration,
- versioned binary or source reference,
- reproducible build instructions,
- dependency lockfile or equivalent,
- execution environment description,
- test harness version,
- raw test results,
- summarized pass/fail matrix,
- golden output comparisons,
- diagnostic logs,
- signed attestation by submitter,
- known limitation statement,
- waiver request file, if any.

For higher profiles, the evidence package MUST additionally include:

- interoperability comparison reports,
- replay audit traces,
- performance envelope results,
- security review artifacts,
- rollback and recovery evidence,
- incident simulation results.

---

## 19. Reproducibility Requirements

Certification MUST be reproducible to the degree required by the profile.

### 19.1 Core Reproducibility

For Core and Developer profiles, evaluators MUST be able to rerun the test suite and obtain materially identical results.

### 19.2 Runtime Reproducibility

For Runtime and Federation profiles, evaluators MUST be able to reproduce not only outcome status but also critical semantic traces and audit events within accepted variance bounds.

### 19.3 Safety-Critical Reproducibility

For Safety-Critical profiles, deterministic replay or functionally equivalent replay MUST be demonstrated for all required incident and execution fixtures.

---

## 20. Interoperability Requirements

Interoperability certification requires more than passing a local test suite.

An implementation seeking interoperability certification MUST:

- import artifacts generated by certified peer implementations where applicable,
- export artifacts consumable by peer implementations,
- preserve semantic equivalence across exchange boundaries,
- tolerate version-negotiated compatibility rules,
- correctly reject unsupported or unsafe artifacts,
- document all known interop restrictions.

Differential analysis MUST compare:

- semantic graph outputs,
- admissibility decisions,
- canonicalized forms,
- key diagnostic classes,
- query results,
- runtime traces where relevant.

---

## 21. Security and Trust Requirements

Security-sensitive implementations MUST satisfy additional conformance checks.

These include, as applicable:

- signature verification,
- trust store correctness,
- registry authenticity handling,
- tamper-evident packaging,
- least-privilege execution boundaries,
- correct failure on invalid signatures or revoked artifacts,
- audit completeness,
- secure error handling that does not hide critical integrity failures.

No implementation may advertise Safety-Critical or Federation certification while silently accepting failed integrity checks.

---

## 22. Conformance Waivers

A waiver is a formal, time-bounded acceptance of a known deviation.

Waivers MAY be granted only if:

- the deviation is fully documented,
- the affected requirement is identified precisely,
- the risk is understood,
- the deviation does not create a prohibited semantic or safety failure for the requested profile,
- compensating controls exist where necessary,
- an expiration or review condition is defined.

Waivers MUST NOT be used to excuse:

- semantic corruption,
- false admissibility,
- integrity bypass,
- unsafe runtime behavior,
- fraudulent capability claims.

---

## 23. Certification Lifecycle

### 23.1 Registration

The candidate implementation is registered as a certification target.

### 23.2 Scope Declaration

The submitter declares component class, requested level, requested profiles, optional features, and known deviations.

### 23.3 Evidence Submission

The evidence package is submitted.

### 23.4 Static Review

Evaluators check completeness, reproducibility, and artifact integrity.

### 23.5 Harness Execution

The official certification harness executes required test suites.

### 23.6 Differential and Interop Review

Peer comparison and interoperability evaluation occur where required.

### 23.7 Finding Resolution

The submitter may respond to findings, correct defects, or withdraw scope claims.

### 23.8 Decision

A certification decision is issued: granted, granted with conditions, deferred, or denied.

### 23.9 Publication

A certification statement and public capability record are published according to disclosure policy.

### 23.10 Renewal or Revocation

Certification is renewed on new versions or revoked if later evidence shows material nonconformance.

---

## 24. Certification States

A certification target may occupy one of the following states:

- Draft
- Submitted
- Under Review
- Evidence Incomplete
- Test In Progress
- Findings Open
- Certified
- Certified with Conditions
- Suspended
- Revoked
- Expired
- Withdrawn

Only **Certified** and **Certified with Conditions** are active approval states.

---

## 25. Versioning Rules for Certification

Certification applies to a specific implementation version and relevant configuration constraints.

### 25.1 Patch Rule

A patch update may inherit certification only if the governing policy allows delta certification and evidence shows no affected normative surface area or the delta suite passes.

### 25.2 Minor Rule

A minor version generally requires partial recertification.

### 25.3 Major Rule

A major version requires full recertification unless explicitly exempted by the certification authority.

### 25.4 Configuration Rule

A materially different deployment configuration may require separate certification even if the code version is unchanged.

---

## 26. Profiles vs Optional Features

An implementation MUST distinguish between:

- required features of a certification profile,
- optional features supported by the implementation,
- experimental features,
- unsupported features,
- restricted features disabled by policy.

Optional feature support MUST NOT be advertised as core conformance unless it is part of the requested profile.

Experimental features MUST be isolated so they cannot silently affect certified stable behavior.

---

## 27. Certification Harness Architecture

The official certification harness SHOULD be implemented as a reproducible, versioned, modular system.

It SHOULD support:

- fixture loading,
- environment orchestration,
- target adapters,
- output normalization,
- semantic diffing,
- trace capture,
- evidence signing,
- report generation,
- profile-specific test selection,
- reproducibility scripts.

The harness itself MUST be versioned and its version recorded in every certification decision.

---

## 28. Differential Semantics Policy

Where exact byte equality is not required, certification SHALL compare outputs under a declared semantic equivalence policy.

This policy MUST specify:

- which fields are identity-critical,
- which ordering differences are irrelevant,
- which provenance differences are tolerated,
- which uncertainty annotations are mandatory,
- which derived fields must match exactly,
- how timestamps, environment fingerprints, or nondeterministic metadata are normalized.

No differential policy may hide a semantic mismatch in entity identity, admissibility, integrity status, or required policy outcome.

---

## 29. Auditability Requirements

Any implementation seeking Runtime, Federation, or Safety-Critical certification MUST provide audit evidence sufficient to reconstruct:

- input artifact identity,
- effective ontology and registry versions,
- validation outcomes,
- key execution transitions,
- mutation attempts,
- accepted and rejected operations,
- integrity checks,
- emitted outputs,
- error states,
- operator-relevant policy events.

Audit records MUST be tamper-evident or protected by equivalent integrity mechanisms where required by profile.

---

## 30. Performance and Resource Claims

Performance is not the primary determinant of conformance, but any explicit performance claim used to obtain profile approval MUST be supported by evidence.

Performance certification MAY include:

- fixture throughput,
- latency targets,
- memory usage bounds,
- graph size limits,
- concurrent query behavior,
- recovery time.

Performance optimization MUST NOT alter normative behavior unless a profile-specific approximation mode is explicitly allowed and clearly excluded from strict certification.

---

## 31. Human Review and Appeals

Formal certification requires a human decision layer in addition to automated testing.

### 31.1 Human Review Responsibilities

Reviewers evaluate:

- waiver appropriateness,
- evidence completeness,
- unresolved edge-case risk,
- consistency of capability claims,
- disclosure sufficiency.

### 31.2 Appeals

A submitter MAY appeal a denial or revocation.

An appeal MUST include:

- contested finding,
- supporting evidence,
- reason the original assessment is believed incorrect,
- any new artifacts.

Appeals MUST be resolved through a documented review path.

---

## 32. Revocation Conditions

Certification MAY be revoked if any of the following occurs:

- later evidence reveals material nonconformance,
- capability claims were false or misleading,
- a critical integrity or safety flaw invalidates prior certification assumptions,
- required registry or ontology compatibility is no longer maintained,
- the implementation is modified outside the certified configuration,
- required renewal is not completed.

Revocation SHOULD produce a signed decision record and affected-profile disclosure.

---

## 33. Disclosure Model

Certification records SHOULD be published in a registry containing at minimum:

- implementation name,
- owner,
- certified version,
- certification type,
- conformance level,
- profiles,
- certification date,
- expiration or renewal status,
- conditions or waivers,
- harness version,
- public report identifier.

Sensitive security details MAY be redacted, but redaction MUST NOT hide the existence of material conditions.

---

## 34. Self-Assessment vs Formal Certification

The framework supports three assessment modes.

### 34.1 Self-Assessment

The implementation owner runs the public conformance harness and publishes results.

### 34.2 Verified Assessment

A recognized evaluator reruns the evidence and verifies results.

### 34.3 Formal Certification

An authorized certification authority issues a formal certification decision.

Only Formal Certification may use the designated Atrahasis certification marks, unless policy explicitly allows verified-assessment badges.

---

## 35. Certification Marks and Claims

No implementation MAY claim or imply a certification broader than the exact granted scope.

For example:

- A parser-certified implementation may not claim full runtime certification.
- A Core-certified implementation may not imply Safety-Critical approval.
- A Research-profile implementation may not market itself as stable interoperability-certified unless separately approved.

All public claims MUST include:

- certified component class,
- conformance level,
- profile,
- certified version.

---

## 36. Minimum Certification Matrices

### 36.1 Parser Certification Minimum

Required:

- lexical tests,
- grammar tests,
- recovery behavior tests,
- span fidelity tests,
- canonical parse shape tests,
- negative fixtures.

### 36.2 Validator Certification Minimum

Required:

- parser certification or approved equivalent dependency,
- semantic tests,
- validation-pass tests,
- severity tests,
- admissibility tests,
- repair output tests.

### 36.3 Runtime Certification Minimum

Required:

- validator certification or approved equivalent dependency,
- lifecycle tests,
- transaction tests,
- reference resolution tests,
- concurrency/consistency tests,
- audit trace tests,
- rollback tests.

### 36.4 Query Certification Minimum

Required:

- query syntax tests,
- semantic selection tests,
- graph traversal tests,
- scope enforcement tests,
- deterministic result tests,
- differential comparison tests.

### 36.5 Platform Certification Minimum

Required:

- all relevant subsystem minima,
- interoperability tests,
- end-to-end fixture tests,
- operational safety checks,
- deployment evidence,
- failure and recovery tests.

---

## 37. Nonconformance Reporting

Any evaluator, user, or peer implementation owner MAY submit a nonconformance report against a certified target.

A report SHOULD include:

- target identity,
- affected version,
- reproduction steps,
- fixture or artifact involved,
- expected behavior,
- observed behavior,
- evidence.

Reported nonconformance MUST be triaged, classified, and either dismissed, tracked, or escalated to suspension/revocation review.

---

## 38. Conformance in Multi-Agent Atrahasis Systems

Because AASL is intended for agent-semantic coordination, certification for integrated multi-agent systems MUST pay special attention to emergent divergence.

In such systems, certification SHOULD additionally assess:

- state-sharing consistency,
- multi-agent ontology interpretation alignment,
- cross-agent identity stability,
- replay across orchestrated workflows,
- event ordering guarantees,
- task handoff integrity,
- semantic closure under distributed mutation,
- failure isolation between agents.

A platform may be subsystem-conformant yet still fail integrated platform certification if emergent behavior violates AASL guarantees.

---

## 39. Reference Profiles for Atrahasis Internal Use

The Atrahasis program SHOULD maintain at least the following internal reference profiles:

- **AASL-DEV-LOCAL**: fast-moving developer toolchain profile.
- **AASL-CI-STRICT**: continuous integration gate profile.
- **AASL-RUNTIME-PROD**: production runtime profile.
- **AASL-FEDERATED-TRUST**: cross-domain execution profile.
- **AASL-MISSION-CRITICAL**: highest assurance profile.

Each internal profile SHOULD define:

- required test buckets,
- mandatory evidence artifacts,
- allowed waivers,
- promotion gates,
- rollback requirements,
- renewal cadence.

---

## 40. Renewal Cadence

Certification SHOULD be renewed according to risk level.

Recommended defaults:

- Developer and Core profiles: every major version or 12 months.
- Runtime profile: every minor version or 6 months.
- Federation profile: every minor version or 6 months, plus after material trust-boundary changes.
- Safety-Critical profile: every material release and not less than every 3 months.

Immediate review SHOULD be triggered by:

- ontology registry major changes,
- security incidents,
- semantic divergence reports,
- platform architecture changes,
- trust model changes.

---

## 41. Conformance Deliverables

A fully certified implementation SHOULD produce the following deliverables:

- certification statement,
- signed capability declaration,
- versioned conformance report,
- evidence archive,
- differential analysis summary,
- interoperability matrix,
- waiver register,
- renewal schedule,
- public disclosure entry.

---

## 42. Implementation Guidance

Implementation owners pursuing certification should follow this sequence:

1. Declare supported profiles conservatively.
2. Run the public conformance harness early.
3. Fix syntax and semantic drift before performance tuning.
4. Establish canonicalization stability before interop testing.
5. Generate audit traces before claiming runtime maturity.
6. Freeze dependencies for the certification target.
7. Produce reproducible build and run instructions.
8. Run differential tests against reference outcomes.
9. Document all deviations honestly.
10. Submit only after local evidence is complete.

---

## 43. Future Extensions

This framework is designed to support future additions including:

- benchmark tiers,
- certified approximation modes,
- domain-specific profile packs,
- sector-specific assurance overlays,
- machine-verifiable certification attestations,
- signed interop trust graphs,
- compliance mappings to external assurance standards.

Any such extensions MUST preserve the core distinction between semantic conformance and optional ecosystem features.

---

## 44. Summary of Normative Principles

The following principles are mandatory for the interpretation of this framework:

1. Certification is version-specific.
2. Capability claims must be explicit.
3. Syntax alone is insufficient for full conformance.
4. Semantic preservation is the center of AASL certification.
5. Interoperability must be demonstrated, not assumed.
6. Auditability is required for higher-trust profiles.
7. Safety and integrity failures cannot be waived into false compliance.
8. Experimental features must not contaminate stable certification claims.
9. Human review complements automated testing.
10. Revocation is part of the trust model, not an exception to it.

---

## 45. Canonical Outcome

With this framework in place, AASL gains a formal mechanism to determine whether any implementation is merely compatible in spirit, genuinely conformant in behavior, or trustworthy enough to participate in high-assurance Atrahasis environments.

This framework is therefore the bridge between specification and dependable ecosystem execution.

