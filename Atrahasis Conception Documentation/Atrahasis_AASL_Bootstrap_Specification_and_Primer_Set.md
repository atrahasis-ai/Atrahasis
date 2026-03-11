# Atrahasis AASL Bootstrap Specification and Primer Set

**Document ID:** ATR-AASL-BOOTSTRAP-SPEC-001  
**Status:** Canonical  
**Version:** 1.0.0  
**Owner:** Atrahasis Language and Runtime Architecture Council  
**Scope:** Defines the bootstrap documentation, training corpus, primer set, test assets, packaging rules, and conformance expectations required to make AASL learnable, teachable, transferable, and operationally adoptable by humans, AI systems, toolchains, and federated runtime environments.

---

## 1. Purpose

AASL cannot become a durable, interoperable language ecosystem through runtime and compiler specifications alone. A language becomes real when new authors can learn it quickly, tools can ingest it consistently, models can internalize it reliably, and implementations can verify that the same document means the same thing across environments.

This document establishes the canonical bootstrap layer for AASL.

The bootstrap layer is the minimum complete knowledge-and-verification package required to:

1. teach AASL to humans,
2. teach AASL to language models and agents,
3. validate that implementations interpret AASL identically,
4. provide authoritative examples of correct authoring,
5. distinguish normative rules from explanatory guidance,
6. anchor future training, certification, and ecosystem growth.

The bootstrap set is not optional documentation. It is part of the language system.

---

## 2. Bootstrap Layer Objectives

The AASL bootstrap layer SHALL satisfy the following objectives:

### 2.1 Learnability
A first-time engineer, architect, analyst, or agent author SHALL be able to understand core AASL concepts, document structure, object semantics, identity rules, link behavior, and queryable structure without reading the entire master runtime specification first.

### 2.2 Normative Clarity
The ecosystem SHALL have a clearly distinguished normative source of truth for syntax, semantics, conformance, validation classes, and portability guarantees.

### 2.3 Model Conditioning
The ecosystem SHALL provide compact, canonical, machine-ingestible artifacts that enable LLMs and agent systems to:

- understand what AASL is,
- produce valid AASL,
- reason about object relationships,
- avoid hallucinated syntax,
- identify invalid constructions,
- explain their reasoning in terms aligned to the actual specification.

### 2.4 Interoperable Testing
All serious AASL implementations SHALL have access to a common test corpus and expected outputs so parser, compiler, validator, query engine, and runtime behavior can be compared across implementations.

### 2.5 Incremental Onboarding
The bootstrap set SHALL support multiple onboarding depths:

- executive/conceptual,
- authoring/basic,
- engineering/implementation,
- model/bootstrap ingestion,
- conformance/certification.

### 2.6 Durable Evolution
The bootstrap layer SHALL be versioned, diffable, forward-maintainable, and able to evolve without introducing ambiguity about which artifacts are authoritative for a given AASL release line.

---

## 3. Canonical Bootstrap Set

The canonical bootstrap set SHALL contain the following top-level artifacts.

### 3.1 `AASL_SPECIFICATION.md`
The compact normative specification for the language.

This file is the authoritative source for the minimum complete statement of:

- core syntax,
- canonical document structure,
- normative keywords,
- identity and reference rules,
- object categories,
- linkage semantics,
- validation requirements,
- canonicalization expectations,
- compatibility and versioning constraints,
- conformance requirements.

This document is normative.

### 3.2 `AASL_PRIMER.md`
The human-and-agent-friendly introduction to the language.

This file explains:

- what AASL is for,
- why it exists,
- how to think in AASL,
- how to read AASL,
- how to write minimal valid AASL,
- common authoring patterns,
- common mistakes,
- practical examples.

This document is explanatory and instructional, but SHALL remain strictly aligned to normative rules.

### 3.3 `AASL_TESTSET/`
The conformance corpus for language implementations.

This directory contains:

- valid documents,
- invalid documents,
- ambiguous source materials,
- canonicalized outputs,
- expected AST/IR snapshots,
- validation diagnostics,
- query fixtures,
- compiler fixtures,
- round-trip fixtures,
- federation and namespace fixtures,
- migration fixtures.

This set is normative for conformance testing where expected outputs are explicitly specified.

### 3.4 `AASL_BOOTSTRAP_MANIFEST.json`
A machine-readable manifest describing the exact contents of the bootstrap bundle.

This manifest SHALL include:

- bootstrap bundle version,
- targeted AASL version,
- artifact hashes,
- normative/explanatory classification,
- test corpus version,
- dependency declarations,
- integrity metadata,
- optional signatures.

### 3.5 `AASL_QUICKSTART.aas`
A minimal canonical example document written in actual AASL.

This file SHALL be the smallest practical real document that demonstrates:

- document header,
- namespace declaration,
- a small object graph,
- references,
- relations,
- annotations,
- basic queryability.

### 3.6 `AASL_BOOTSTRAP_PROFILE.md`
A concise operational guide defining what a tool, agent, or model must ingest to claim “bootstrap-complete” awareness of AASL.

This profile SHALL define minimum ingestion requirements for:

- model prompting,
- embedded toolchains,
- editor integrations,
- gateway validators,
- runtime hosts,
- certification harnesses.

---

## 4. Classification of Bootstrap Artifacts

Each artifact in the bootstrap set SHALL be classified into one of the following categories.

### 4.1 Normative
Normative artifacts define binding requirements.

Violations of normative content constitute implementation non-conformance.

Examples:

- `AASL_SPECIFICATION.md`
- explicit expected outputs in parts of `AASL_TESTSET/`
- bootstrap manifest version bindings

### 4.2 Explanatory
Explanatory artifacts teach, clarify, or provide guidance without altering normative meaning.

Examples:

- `AASL_PRIMER.md`
- diagrams or walkthroughs
- commentary files in example directories

### 4.3 Reference
Reference artifacts provide sanctioned examples, templates, snippets, or sample corpora.

Examples:

- quickstart document
- style guide samples
- annotated example collections

### 4.4 Conformance
Conformance artifacts define expected behavior of implementations for verification purposes.

Examples:

- parser fixture inputs and expected AST outputs
- validator fixture outputs
- canonicalized form snapshots
- query result expectations

### 4.5 Training
Training artifacts are optimized for model conditioning and agent bootstrapping while remaining traceable to normative rules.

Examples:

- distilled grammar cards
- anti-pattern sets
- prompt-safe summaries
- structured concept maps

No training artifact may contradict any normative artifact.

---

## 5. `AASL_SPECIFICATION.md` Requirements

The compact specification SHALL exist as a standalone, canonical document distinct from the larger master system specification.

### 5.1 Role
Its purpose is to serve as the shortest complete normative expression of AASL.

It is the document an implementer or model should ingest when they need authoritative language rules without the broader Atrahasis architectural narrative.

### 5.2 Required Sections
The specification SHALL contain, at minimum:

1. Scope and goals
2. Conformance language and normative keyword definitions
3. Language model and conceptual overview
4. Lexical and structural conventions
5. Document anatomy
6. Namespace and module semantics
7. Object kinds and fields
8. Identity rules
9. Reference and relation semantics
10. Annotation and metadata semantics
11. Validation classes and admissibility
12. Canonicalization requirements
13. Compatibility and versioning rules
14. Security and trust considerations
15. Minimum implementation requirements
16. Conformance statement template
17. Glossary

### 5.3 Normative Style Rules
The compact specification SHALL:

- use explicit normative terminology,
- avoid motivational prose except where needed for disambiguation,
- maintain stable section numbering,
- isolate examples from rules,
- identify each example as informative unless otherwise specified,
- define terms before first normative use,
- include cross-references to the full master spec when deeper context exists.

### 5.4 Size Constraint
The compact specification SHOULD be significantly shorter than the master AASL runtime/master specification while still remaining complete enough for implementation.

Target design principle:

- complete, not encyclopedic,
- normative, not tutorial,
- portable, not Atrahasis-internal.

### 5.5 Machine Alignment
The specification SHALL be authored so that LLMs and static tooling can reliably segment it into atomic normative statements.

Recommended patterns include:

- single-rule paragraphs,
- explicit MUST/SHOULD/MAY usage,
- bounded list structures,
- stable section IDs,
- formal examples with labels.

---

## 6. `AASL_PRIMER.md` Requirements

### 6.1 Role
The primer is the first-contact document for humans and general-purpose AI systems.

Its purpose is to make AASL intuitive before the reader enters deeper normative material.

### 6.2 Audience Classes
The primer SHALL support at least these audiences:

- first-time human readers,
- technical writers,
- software engineers,
- ontology designers,
- LLM-based authoring agents,
- code assistants and document transformation tools.

### 6.3 Required Sections
The primer SHALL include:

1. What AASL is
2. Why AASL exists
3. Core mental model
4. Smallest valid AASL document
5. Documents, objects, identities, links, and namespaces
6. How to read an AASL file top to bottom
7. Common authoring patterns
8. Common mistakes and why they fail
9. From informal text to structured AASL
10. Querying and inspecting AASL
11. How validation works
12. How canonicalization works
13. How AASL relates to the compiler/runtime/tooling stack
14. Next steps and where to go deeper

### 6.4 Pedagogical Requirements
The primer SHALL:

- introduce one concept at a time,
- use complete worked examples,
- pair examples with explanations,
- show invalid examples and their corrections,
- explain the reasoning behind identity and linkage rules,
- remain consistent with the compact specification,
- avoid unexplained jargon.

### 6.5 Agent-Friendly Formatting
The primer SHOULD include sections designed for fast machine grounding, such as:

- concept summary cards,
- valid/invalid pairs,
- compact rule summaries,
- anti-hallucination notes,
- transformation examples from prose to AASL.

### 6.6 Explicit Non-Authority Clause
The primer SHALL state clearly that it is not the final authority when explanatory language and normative language appear to conflict. The compact specification and full master specification govern.

---

## 7. `AASL_TESTSET/` Requirements

### 7.1 Role
The testset is the executable truth layer for AASL interoperability.

It exists to prove whether implementations actually behave according to the language, not merely whether they claim to.

### 7.2 Top-Level Structure
The testset SHOULD contain structured directories such as:

```text
AASL_TESTSET/
  parser/
  validator/
  canonicalization/
  compiler/
  runtime/
  query/
  federation/
  migrations/
  roundtrip/
  security/
  examples/
  metadata/
```

### 7.3 Fixture Classes
The corpus SHALL include the following classes of fixtures.

#### 7.3.1 Valid Syntax Fixtures
Documents that are syntactically and structurally valid.

#### 7.3.2 Invalid Syntax Fixtures
Documents that MUST fail parsing.

#### 7.3.3 Structurally Invalid Fixtures
Documents that parse but violate language structure rules.

#### 7.3.4 Semantically Invalid Fixtures
Documents that are syntactically well-formed but violate semantic invariants.

#### 7.3.5 Canonicalization Fixtures
Documents with expected canonicalized normalized output.

#### 7.3.6 Compiler Fixtures
Source material plus expected compiled AASL or expected ambiguity reports.

#### 7.3.7 Runtime Fixtures
Object graphs and operations with expected runtime behaviors.

#### 7.3.8 Query Fixtures
Input documents, queries, and expected result sets.

#### 7.3.9 Federation Fixtures
Multi-namespace or cross-boundary examples with expected resolution behavior.

#### 7.3.10 Migration Fixtures
Documents that test version upgrades, deprecations, or compatibility adapters.

#### 7.3.11 Security Fixtures
Hostile or malformed inputs that verify safe failure behavior.

#### 7.3.12 Round-Trip Fixtures
Fixtures proving stability across parse, canonicalize, serialize, and reparse cycles.

### 7.4 Fixture Metadata
Every fixture SHALL include machine-readable metadata describing:

- fixture ID,
- targeted AASL version,
- category,
- objective,
- expected result kind,
- severity if invalid,
- dependent modules or namespaces,
- notes on ambiguity where relevant.

### 7.5 Expected Outputs
For any fixture intended as a conformance fixture, expected outputs SHALL be explicit and version-bound.

Examples include:

- parser success/failure,
- AST snapshots,
- canonicalized document snapshots,
- validator diagnostic arrays,
- compiler ambiguity classifications,
- query results,
- runtime state transitions.

### 7.6 Stability Rules
Conformance fixtures SHALL be immutable once released for a given bootstrap bundle version, except via formally versioned correction.

### 7.7 Goldens and Diffs
The testset SHOULD use stable golden outputs with deterministic serialization so cross-implementation diffs are meaningful.

---

## 8. Bootstrap Manifest Specification

The bootstrap manifest provides machine-verifiable integrity and bundle semantics.

### 8.1 Required Fields
The manifest SHALL include:

- `bootstrap_bundle_version`
- `target_aasl_version`
- `release_date`
- `artifacts`
- `normative_artifacts`
- `conformance_artifacts`
- `training_artifacts`
- `hash_algorithm`
- `artifact_hashes`
- `compatibility_window`
- `signatures` if signing is enabled

### 8.2 Artifact Entry Requirements
Each artifact entry SHALL include:

- logical name,
- path,
- category,
- status,
- version,
- hash,
- human-readable description,
- dependency references,
- whether the artifact is mandatory for bootstrap-complete ingestion.

### 8.3 Example Shape
```json
{
  "bootstrap_bundle_version": "1.0.0",
  "target_aasl_version": "1.0.0",
  "artifacts": [
    {
      "name": "AASL_SPECIFICATION.md",
      "category": "normative",
      "required": true,
      "hash": "sha256:..."
    }
  ]
}
```

### 8.4 Trust Model
If signatures are present, consumers SHOULD verify signatures before treating the bootstrap bundle as authoritative.

---

## 9. Quickstart Artifact Requirements

### 9.1 Purpose
`AASL_QUICKSTART.aas` is the “hello world” of the language.

It is designed for immediate inspection by humans and immediate ingestion by models and tools.

### 9.2 Content Requirements
It SHALL demonstrate:

- a valid header,
- a declared module or namespace,
- at least one entity/object,
- at least one relation,
- at least one annotation or metadata block,
- at least one resolvable reference,
- a simple queryable structure.

### 9.3 Non-Requirements
It need not demonstrate every advanced capability. Its goal is minimal comprehensibility.

### 9.4 Companion Walkthrough
The primer SHALL include a section that line-by-line explains the quickstart artifact.

---

## 10. Bootstrap Profile Requirements

### 10.1 Purpose
The bootstrap profile defines what it means for a tool, model, or runtime to claim it has ingested the AASL bootstrap layer.

### 10.2 Profiles
The ecosystem SHALL define, at minimum, the following bootstrap profiles.

#### 10.2.1 Reader Profile
Can read and explain AASL correctly at a high level.

Required ingestion:

- primer,
- quickstart artifact,
- compact specification summary sections.

#### 10.2.2 Author Profile
Can produce simple valid AASL documents.

Required ingestion:

- primer,
- quickstart artifact,
- syntax and validation sections of the compact specification,
- selected valid/invalid examples.

#### 10.2.3 Implementer Profile
Can implement or maintain parser, validator, or tooling features.

Required ingestion:

- full compact specification,
- targeted subsystem specs,
- testset metadata,
- canonicalization fixtures.

#### 10.2.4 Runtime Profile
Can host or execute against AASL graphs safely.

Required ingestion:

- compact specification,
- runtime model spec,
- validation architecture,
- query engine specification,
- runtime fixtures.

#### 10.2.5 Model Bootstrap Profile
A language model or agent can reason about AASL with grounded terminology and reduced hallucination risk.

Required ingestion:

- compact specification,
- primer,
- anti-pattern set,
- valid/invalid pairs,
- quickstart artifact,
- selected test fixtures.

---

## 11. Model and Agent Conditioning Design

AASL is intended to be used by agent systems and language models, not just by human engineers. Therefore the bootstrap set SHALL contain content optimized for machine conditioning while remaining traceable to normative rules.

### 11.1 Conditioning Objectives
Model-facing bootstrap materials SHALL help models:

- preserve exact terminology,
- avoid inventing unsupported syntax,
- distinguish object identity from display labels,
- understand that namespaces and modules are governance-relevant,
- treat validation failures as meaningful categories,
- recognize the difference between parse-valid and semantically valid documents,
- understand canonicalization as a stability operation rather than a cosmetic formatter.

### 11.2 Recommended Model Assets
The bootstrap set SHOULD additionally include:

- `AASL_RULE_CARDS.md`
- `AASL_VALID_INVALID_PAIRS.md`
- `AASL_COMMON_FAILURES.md`
- `AASL_CONCEPT_MAP.json`
- `AASL_BOOTSTRAP_PROMPTING_GUIDE.md`

These may be explanatory or training artifacts but SHALL not supersede the normative specification.

### 11.3 Hallucination Prevention Patterns
Bootstrap materials SHOULD explicitly warn against the following model failure modes:

- inventing undeclared keywords,
- treating examples as exhaustive rules,
- collapsing identity and label fields,
- skipping namespace declarations,
- introducing JSON-like assumptions into native AASL syntax without basis,
- assuming every free-form note is semantically binding,
- misclassifying compiler ambiguity as validator failure.

### 11.4 Traceability Rule
Every training-oriented concept summary SHOULD map back to the section IDs of the normative specification.

---

## 12. Human Onboarding Ladder

The bootstrap set SHALL be designed as a progressive onboarding ladder.

### 12.1 Level 0: Conceptual Familiarity
Target audience:

- executives,
- architects,
- reviewers,
- adjacent system designers.

Artifacts:

- primer overview sections,
- one-page concept summary,
- quickstart explanation.

### 12.2 Level 1: Basic Authoring
Target audience:

- analysts,
- technical writers,
- prompt engineers,
- junior implementers.

Artifacts:

- primer,
- valid/invalid examples,
- quickstart,
- authoring checklist.

### 12.3 Level 2: Structural Competence
Target audience:

- engineers,
- schema designers,
- integration developers.

Artifacts:

- compact specification,
- validator architecture,
- file infrastructure spec,
- testset examples.

### 12.4 Level 3: Implementation Competence
Target audience:

- parser/compiler developers,
- query engine developers,
- runtime maintainers.

Artifacts:

- full compact specification,
- subsystem specs,
- conformance fixtures,
- canonicalization goldens.

### 12.5 Level 4: Governance and Ecosystem Stewardship
Target audience:

- standards owners,
- ontology maintainers,
- ecosystem certifiers.

Artifacts:

- ontology registry operations spec,
- compatibility and migration fixtures,
- release governance policies,
- bootstrap manifest rules.

---

## 13. Versioning Rules for the Bootstrap Set

### 13.1 Independent but Bound Versioning
The bootstrap bundle SHALL have its own bundle version, but it SHALL declare the AASL language version it targets.

### 13.2 Compatibility Declaration
Each bootstrap bundle SHALL declare one of the following statuses relative to a target AASL version:

- exact-match,
- backward-compatible,
- forward-guidance-only,
- deprecated.

### 13.3 Artifact Drift Prevention
If the compact specification changes in a way that affects meaning, then:

- relevant primer sections SHALL be reviewed,
- impacted fixtures SHALL be revised or version-frozen,
- the manifest SHALL be updated,
- the release notes SHALL identify semantic deltas.

### 13.4 Immutable Release Principle
Published bootstrap bundle versions SHOULD be immutable. Corrections SHALL be handled via patch releases, not silent replacement.

---

## 14. Release Packaging Model

### 14.1 Bundle Form
The bootstrap set SHOULD be distributable as a canonical package such as:

- source repository directory,
- signed release archive,
- embedded toolchain bundle,
- model bootstrap package,
- documentation portal export.

### 14.2 Required Release Contents
A bootstrap release SHALL include:

- compact specification,
- primer,
- quickstart artifact,
- bootstrap manifest,
- testset,
- release notes,
- checksum file,
- conformance notes.

### 14.3 Recommended Release Additions
A bootstrap release SHOULD additionally include:

- human-readable changelog,
- example gallery,
- anti-pattern guide,
- migration notes,
- model bootstrap assets.

---

## 15. Conformance and Certification Usage

### 15.1 Implementation Claims
No implementation SHALL claim full AASL conformance unless it can be tested against the relevant conformance portions of the bootstrap set.

### 15.2 Certification Profiles
The ecosystem MAY define certification levels such as:

- Parser-Conformant,
- Validator-Conformant,
- Canonicalization-Conformant,
- Query-Conformant,
- Runtime-Conformant,
- Bootstrap-Complete Tooling,
- Bootstrap-Complete Model Integration.

### 15.3 Evidence Requirements
Certification evidence SHOULD include:

- bootstrap bundle version used,
- executed fixture set,
- pass/fail summaries,
- exceptions or unsupported features,
- implementation version,
- environment metadata.

---

## 16. Security and Integrity Considerations

### 16.1 Artifact Authenticity
Bootstrap artifacts SHOULD be hash-verified and optionally signature-verified.

### 16.2 Poisoning Resistance
Because models may be conditioned on bootstrap artifacts, the distribution chain MUST protect against artifact tampering, substitution, or unofficial forks being mistaken for canonical release material.

### 16.3 Example Safety
Examples included in the primer or testset SHOULD avoid patterns that normalize unsafe parser behavior, silent mutation, trust-boundary confusion, or namespace spoofing.

### 16.4 Hostile Fixture Segregation
Malicious-input fixtures SHALL be clearly identified and isolated so production pipelines do not accidentally ingest them as ordinary examples.

---

## 17. Documentation Quality Rules

All bootstrap artifacts SHALL adhere to the following quality rules:

1. consistent terminology across all files,
2. stable identifiers for sections and fixtures,
3. explicit distinction between rule and example,
4. no contradiction with normative specs,
5. deterministic example formatting,
6. clear change history,
7. suitability for both human reading and AI ingestion.

Additionally, explanatory prose SHOULD prefer precision over marketing language.

---

## 18. Reference Directory Layout

A recommended canonical directory layout is shown below.

```text
AASL_BOOTSTRAP/
  AASL_SPECIFICATION.md
  AASL_PRIMER.md
  AASL_QUICKSTART.aas
  AASL_BOOTSTRAP_PROFILE.md
  AASL_BOOTSTRAP_MANIFEST.json
  RELEASE_NOTES.md
  CHECKSUMS.txt
  training/
    AASL_RULE_CARDS.md
    AASL_VALID_INVALID_PAIRS.md
    AASL_COMMON_FAILURES.md
    AASL_CONCEPT_MAP.json
    AASL_BOOTSTRAP_PROMPTING_GUIDE.md
  examples/
    minimal/
    intermediate/
    advanced/
  AASL_TESTSET/
    parser/
    validator/
    canonicalization/
    compiler/
    runtime/
    query/
    federation/
    migrations/
    security/
    metadata/
```

This layout is informative but strongly recommended.

---

## 19. Bootstrap Production Workflow

The canonical workflow for producing a bootstrap release SHOULD follow this sequence:

1. finalize targeted AASL language version,
2. update compact specification,
3. reconcile primer with normative changes,
4. update quickstart artifact if needed,
5. regenerate or validate conformance fixtures,
6. refresh machine-readable manifest,
7. run release integrity checks,
8. execute certification test matrix,
9. publish release notes,
10. publish signed bundle.

No release should be considered canonical until integrity, consistency, and conformance checks complete.

---

## 20. Bootstrap Governance

### 20.1 Ownership
The bootstrap set SHALL be stewarded by the Atrahasis language governance function or its designated successor.

### 20.2 Change Control
Bootstrap artifacts SHALL be subject to change review proportional to their category.

- Normative changes require formal review.
- Conformance fixture changes require expected-output review.
- Explanatory changes require alignment review.
- Training asset changes require traceability review.

### 20.3 Dispute Resolution
Where explanatory material appears inconsistent with normative material, the normative material prevails and the explanatory material SHALL be corrected in the next patch release.

---

## 21. Minimum Initial Deliverables

To declare the bootstrap layer operational for AASL v1, the following minimum deliverables SHALL exist:

1. `AASL_SPECIFICATION.md`
2. `AASL_PRIMER.md`
3. `AASL_QUICKSTART.aas`
4. `AASL_BOOTSTRAP_MANIFEST.json`
5. a first conformance-capable `AASL_TESTSET/`
6. `AASL_BOOTSTRAP_PROFILE.md`
7. release notes and checksums

Without these artifacts, AASL may be specified architecturally, but it is not yet bootstrap-complete.

---

## 22. Recommended Future Extensions

The following additions are recommended after the initial bootstrap release:

- multilingual primer variants,
- interactive tutorial pack,
- executable notebook walkthroughs,
- schema visualization assets,
- ontology authoring workbooks,
- certification dashboards,
- model fine-tuning micro-corpus derived from canonical examples,
- differential fixture packs for version migration training,
- domain-specific example suites.

---

## 23. Canonical Position

The AASL bootstrap layer is the bridge between specification and adoption.

Without it, AASL remains an architecture known mainly to its designers.
With it, AASL becomes teachable, testable, portable, and reproducible across humans, tools, runtimes, and agent systems.

This document therefore declares the bootstrap set a first-class architectural requirement of the AASL ecosystem.

---

## 24. Summary of Required Artifact Set

For convenience, the bootstrap layer REQUIRED artifact inventory is summarized below:

- `AASL_SPECIFICATION.md` — compact normative language spec
- `AASL_PRIMER.md` — human/agent onboarding guide
- `AASL_TESTSET/` — conformance corpus
- `AASL_BOOTSTRAP_MANIFEST.json` — machine-readable release manifest
- `AASL_QUICKSTART.aas` — minimal canonical example
- `AASL_BOOTSTRAP_PROFILE.md` — ingestion/completeness profile
- `RELEASE_NOTES.md` — release-specific change disclosures
- `CHECKSUMS.txt` — integrity validation support

These artifacts, taken together, constitute the canonical AASL bootstrap set.

---

## 25. Final Requirement

Any future Atrahasis AASL release program SHALL treat bootstrap completeness as a release gate, not as optional post-release documentation.

A language that cannot be bootstrapped reliably cannot be federated reliably.
A language that cannot be tested reliably cannot be governed reliably.
A language that cannot be taught reliably cannot become infrastructure.

For AASL, bootstrap completeness is therefore part of language correctness.
