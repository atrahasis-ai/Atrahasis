# Atrahasis AASL Ontology Registry and Governance Operations

**Document ID:** ATR-AASL-ONTOREG-001  
**Title:** Atrahasis AASL Ontology Registry and Governance Operations  
**Status:** Canonical Draft  
**Version:** 1.0.0  
**Authoring Context:** Atrahasis / AASL Core System  
**Last Updated:** 2026-03-08  
**Applies To:** ontology modules, namespace registration, term lifecycle management, schema-to-ontology alignment, extension admission, governance decision flows, compatibility policy, deprecation operations, trust controls, registry publishing, and ecosystem evolution.

---

## 1. Purpose

This document defines the canonical **ontology registry and governance operations layer** for the Atrahasis Agentic Semantic Language (AASL). It specifies how ontology terms, modules, namespaces, extensions, versions, and semantic policies are proposed, reviewed, admitted, published, deprecated, superseded, and retired.

AASL can only remain interoperable if shared meaning evolves through controlled, explicit, and reviewable mechanisms. Without a registry, independent implementers will create drifting concept vocabularies. Without governance, ontology expansion will fragment the ecosystem. Without operational procedures, even correct ontology ideas will become unmanageable at scale.

The purpose of this specification is to ensure that:

1. **Shared semantic meaning remains stable** across documents, tools, runtimes, and organizations.
2. **Ontology evolution is possible** without breaking the semantic closure guarantees of Atrahasis.
3. **Extensions remain auditable** and are admitted through explicit procedures rather than hidden convention.
4. **Compatibility is measurable** instead of hand-waved.
5. **Registry publication is deterministic** and versioned.
6. **Humans and agents can participate** in ontology operations without bypassing governance constraints.
7. **Safety, trust, and provenance requirements** apply to ontology growth the same way they apply to runtime behavior.

This document turns ontology management from an informal community activity into a formal operating subsystem.

---

## 2. Scope

This specification covers:

- ontology registry architecture
- namespace classes and namespace ownership
- ontology module structure
- term identity and canonical metadata
- schema and ontology registration contracts
- proposal submission and intake workflows
- review states and approval gates
- compatibility classes and release policy
- deprecation, supersession, and retirement operations
- registry publication formats
- governance roles and decision authority
- conflict handling and appeals
- experimental modules and sandbox namespaces
- trust, provenance, and signing requirements
- validator/runtime integration expectations
- ecosystem change management
- audit logs and traceability expectations

This specification does **not** redefine the full AASL syntax, parser internals, validator pass architecture, or compiler extraction logic, except where those systems depend on registry and governance decisions.

---

## 3. Why This Layer Exists

AASL is a semantic language, not merely a syntax format. Its long-term utility depends on the stability of the meanings attached to object classes, relation types, fields, enumerations, and semantic constraints.

Three failure modes justify a dedicated ontology registry and governance system:

### 3.1 Semantic drift

Different teams begin using the same surface token for different meanings, or different tokens for the same meaning, until interoperability becomes impossible.

### 3.2 Silent extension

Implementers add fields, object families, enums, or relation types in private deployments without formal registration, creating invisible ecosystem forks.

### 3.3 Version chaos

Ontology changes are released without compatibility classification, migration policy, or machine-readable registry snapshots, making validator and runtime behavior inconsistent.

The registry and governance layer exists to prevent all three.

---

## 4. Design Principles

The ontology registry and governance layer shall obey the following principles.

### 4.1 Explicitness over implication

No ontology meaning is official merely because it is used frequently. Terms become canonical only through explicit admission into the registry.

### 4.2 Stability over velocity

Ontology growth must be controlled. The cost of admitting a bad term is higher than the inconvenience of delaying a new one.

### 4.3 Versioned meaning over ambient interpretation

Every ontology reference must resolve against a declared registry snapshot or module version, not against vague community understanding.

### 4.4 Extension without fragmentation

The system must allow domain expansion, but only through mechanisms that preserve cross-implementation interoperability.

### 4.5 Traceable governance

Every accepted, rejected, deprecated, or retired ontology element must have a decision trace.

### 4.6 Machine readability

Governance outcomes must be publishable in machine-readable registry artifacts.

### 4.7 Semantic closure

Registry operations must honor the Atrahasis semantic closure policy. Nothing enters the trusted semantic substrate through undocumented side channels.

### 4.8 Reversible evolution where possible

Changes should be staged so that mistakes can be corrected through supersession and migration rather than ecosystem rupture.

---

## 5. Core Concepts

### 5.1 Registry

The **registry** is the canonical, versioned, signed publication of approved ontology modules, namespaces, terms, constraints, aliases, lifecycle states, compatibility metadata, and governance records.

### 5.2 Ontology module

An **ontology module** is a versioned package of semantically related definitions. Examples include:

- core semantic primitives
- reasoning and evidence concepts
- scientific knowledge modules
- economic and governance modules
- medical modules
- industrial process modules

### 5.3 Namespace

A **namespace** is a controlled identifier domain under which modules and terms are registered. Namespaces are governance boundaries.

### 5.4 Term

A **term** is a canonical semantic unit within the registry, such as:

- object class
- relation type
- attribute key
- enum member
- constraint label
- semantic role
- event type
- unit family

### 5.5 Registry snapshot

A **registry snapshot** is an immutable published state of the registry at a point in time. Validators, compilers, runtimes, and tooling must be able to bind behavior to a specific snapshot.

### 5.6 Governance record

A **governance record** is the formal trace of a registry decision, including proposal inputs, reviewers, rationale, classification, vote or approval outcome, and resulting registry mutation.

---

## 6. Registry Objectives

The registry must provide:

1. a single canonical source of ontology truth,
2. stable identifiers for semantic elements,
3. deterministic machine-readable exports,
4. lifecycle state tracking,
5. compatibility metadata,
6. discoverability for tooling and authors,
7. provenance and signature support,
8. governance auditability,
9. support for experimental isolation,
10. clear migration paths when terms evolve.

---

## 7. Registry Architecture Overview

```text
Proposal Intake
   ↓
Normalization + Completeness Check
   ↓
Technical Review
   ├─ semantic coherence review
   ├─ overlap/collision review
   ├─ compatibility review
   ├─ validator/runtime impact review
   └─ safety/governance review
   ↓
Decision Layer
   ├─ approve
   ├─ approve with conditions
   ├─ return for revision
   ├─ reject
   └─ escalate
   ↓
Registry Build + Signing
   ↓
Snapshot Publication
   ↓
Validator / Compiler / Runtime / Tooling Consumption
```

The registry must function as an operational system, not just a documentation repository.

---

## 8. Namespace Model

### 8.1 Namespace classes

Namespaces shall be categorized into classes.

| Namespace Class | Purpose | Admission Standard | Default Trust Level |
|---|---|---|---|
| `core` | foundational universal concepts | highest | fully trusted |
| `system` | platform-internal operational concepts | high | trusted |
| `domain` | domain-specific official modules | high | trusted |
| `partner` | formally recognized external contributor modules | moderate-high | bounded trust |
| `experimental` | trial concepts under controlled review | lower | restricted |
| `private` | local/private deployment extensions | local only | untrusted by default |
| `deprecated` | legacy namespace state marker | none for new additions | not for new authoring |

### 8.2 Namespace ownership

Every non-core namespace must declare:

- namespace owner
- governing authority
- contact or service identity
- publication key identity
- admission rules
- review quorum requirements
- deprecation authority

### 8.3 Namespace immutability of identity

A namespace identifier, once published, must never be silently repurposed. If stewardship changes, ownership metadata may change, but the semantic identity of the namespace must remain continuous or be retired.

### 8.4 Namespace collision rules

Namespace names must be globally unique within the registry. Registration must fail on exact collision and be flagged for review on near collision.

---

## 9. Ontology Module Structure

Every ontology module must contain canonical metadata.

### 9.1 Required module metadata

Each module shall declare at minimum:

- module identifier
- namespace identifier
- module name
- semantic summary
- version
- lifecycle state
- maintainers/governing body
- compatibility baseline
- dependency declarations
- exported term list
- constraint set references
- changelog reference
- provenance reference
- signature or signing envelope reference

### 9.2 Optional module metadata

Modules may additionally declare:

- alias packs
- localization labels
- usage notes
- migration recipes
- known conflicts
- experimental flags
- deprecation timeline
- recommended profiles
- domain evidence basis

### 9.3 Module types

Canonical module types should include:

- primitive
- structural
- reasoning
- evidence
- governance
- scientific-domain
- industrial-domain
- protocol
- unit-system
- interop-bridge

---

## 10. Term Model

### 10.1 Required term metadata

Every registered term must include:

- stable term identifier
- module identifier
- canonical label
- term kind
- human-readable definition
- machine-readable semantic summary
- allowed parent context or usage scope
- lifecycle state
- version introduced
- provenance reference
- compatibility notes

### 10.2 Optional term metadata

Terms may additionally include:

- aliases
- forbidden synonyms
- examples
- anti-examples
- expected relations
- allowed cardinality patterns
- unit compatibility
- domain restrictions
- recommended validation rules
- migration targets

### 10.3 Term kinds

The registry shall at minimum support these kinds:

- object class
- relation type
- attribute key
- enum set
- enum value
- evidence type
- claim type
- constraint
- role
- event type
- unit family
- scalar type extension
- provenance tag

### 10.4 Stable identifiers

A term identifier must be opaque enough to remain stable across label edits, but structured enough to be resolvable.

Illustrative pattern:

```text
term://core.reasoning/claim.supports
term://domain.medical/condition.diagnosis
term://system.governance/proposal.status
```

Identifier format may evolve, but stability semantics may not.

---

## 11. Lifecycle States

Ontology modules and terms shall move through explicit lifecycle states.

| State | Meaning | Allowed for Production Authoring | Allowed for Validation | Allowed for New Dependency |
|---|---|---|---|---|
| draft | not admitted | no | only in sandbox | no |
| proposed | under review | no | only in review tools | no |
| experimental | admitted with restrictions | profile-dependent | yes, with policy | limited |
| stable | canonical and recommended | yes | yes | yes |
| deprecated | still resolvable, discouraged | no for new authoring | yes with warning | no |
| superseded | replaced by newer construct | no | yes with migration guidance | no |
| retired | no longer supported for new processing except legacy replay | no | legacy-only | no |
| rejected | not admitted | no | no | no |

Lifecycle state transitions must be logged through governance records.

---

## 12. Registry Publication Artifacts

The registry must publish canonical artifacts.

### 12.1 Required artifacts

At minimum, every registry snapshot must include:

- module index
- namespace index
- term index
- lifecycle index
- compatibility manifest
- dependency graph manifest
- alias/redirect manifest
- deprecation manifest
- governance record index
- signing manifest
- changelog summary

### 12.2 Machine-readable formats

The canonical transport format may be JSON, AASL-native, or both, but it must be deterministic and schema-versioned.

Suggested publication set:

- `registry.snapshot.json`
- `registry.modules.json`
- `registry.terms.json`
- `registry.aliases.json`
- `registry.lifecycle.json`
- `registry.compatibility.json`
- `registry.governance-log.json`
- `registry.signatures.json`

### 12.3 Human-readable artifacts

Human-readable companion artifacts should include:

- release notes
- admitted proposals summary
- rejected proposal summary
- compatibility impact summary
- migration advisories
- deprecation notices

---

## 13. Governance Roles

The governance system shall define roles with bounded authority.

### 13.1 Registry maintainers

Registry maintainers administer publication mechanics, completeness checks, release packaging, and audit integrity. They do not have unilateral authority to redefine core semantics outside the approved governance process.

### 13.2 Ontology editors

Ontology editors review structure, terminology quality, overlap, naming discipline, semantic clarity, and internal consistency.

### 13.3 Domain stewards

Domain stewards evaluate whether domain-specific modules reflect valid disciplinary use and whether definitions are sufficiently bounded.

### 13.4 Compatibility reviewers

Compatibility reviewers assess ecosystem impact, migration burden, downstream validator/compiler/runtime consequences, and profile breakage risk.

### 13.5 Safety and constitutional reviewers

These reviewers ensure that ontology changes do not bypass semantic closure, trust controls, policy boundaries, or governance constraints defined elsewhere in Atrahasis.

### 13.6 Release authority

Release authority signs and publishes an approved registry snapshot. This may be a role, quorum, or hybrid approval mechanism depending on deployment scale.

### 13.7 Appeals authority

Appeals authority handles disputes, escalations, re-reviews, and contested semantic classifications.

---

## 14. Governance Decision Classes

Not all ontology changes require the same governance burden. Changes must be classified.

| Change Class | Examples | Required Review Intensity |
|---|---|---|
| editorial | typo fixes, clarifications with no semantic change | low |
| additive-safe | new optional term with no conflicts | moderate |
| additive-sensitive | new relation, new object class, new enum affecting behavior | moderate-high |
| interpretive | definition tightening or changed scope | high |
| compatibility-affecting | change that may alter validation or runtime meaning | high |
| deprecating | beginning retirement of existing constructs | high |
| breaking | incompatible removal or redefinition | highest |
| constitutional | changes affecting core semantic closure or governance boundaries | highest + escalation |

Decision class must be recorded per proposal.

---

## 15. Proposal Intake

### 15.1 Proposal requirement

No ontology mutation shall enter the canonical registry without a proposal record.

### 15.2 Required proposal fields

Every proposal must include:

- proposal identifier
- submitter identity
- target namespace/module
- requested operation
- semantic rationale
- full proposed definitions
- overlap analysis
- compatibility analysis
- migration assessment
- validator impact assessment
- compiler impact assessment
- runtime/tooling impact assessment
- examples and anti-examples
- requested lifecycle state
- supporting references or provenance

### 15.3 Operation types

The registry must support proposals for:

- create namespace
- create module
- add term
- amend metadata
- add alias
- deprecate term
- supersede term
- retire term
- merge modules
- split modules
- revise constraints
- register experimental extension
- transfer stewardship

### 15.4 Intake validation

Before substantive review, intake must verify:

- structural completeness,
- namespace legitimacy,
- duplicate detection,
- required analysis presence,
- schema validity,
- author identity or authorized service identity,
- signature validity where required.

Incomplete proposals shall be returned without entering substantive review.

---

## 16. Review Pipeline

### 16.1 Review stages

Canonical review stages should include:

1. intake validation,
2. semantic normalization,
3. overlap and collision analysis,
4. technical review,
5. compatibility review,
6. governance/safety review,
7. final decision,
8. publication scheduling.

### 16.2 Semantic normalization

Submitted labels, aliases, examples, and definitions should be normalized into registry form for comparison without altering the proposal’s intended meaning.

### 16.3 Overlap analysis

The review process must explicitly evaluate whether the proposal:

- duplicates an existing term,
- conflicts with an existing term,
- should instead be modeled as an alias,
- belongs in a different module,
- violates existing ontological boundaries,
- introduces ambiguous class boundaries.

### 16.4 Compatibility review

Compatibility review must classify the proposal impact at minimum as:

- non-breaking,
- warning-inducing,
- migration-required,
- profile-gated,
- breaking.

### 16.5 Review outcomes

Each stage may yield:

- pass,
- pass with required conditions,
- revision requested,
- reject,
- escalate.

---

## 17. Decision Rules

### 17.1 Approval prerequisites

A proposal may be approved only if:

- the semantic definition is sufficiently bounded,
- collision risks are acceptably resolved,
- compatibility classification is explicit,
- migration path is defined when needed,
- validator/compiler/runtime implications are documented,
- provenance is adequate,
- lifecycle state is justified,
- required reviewers have approved.

### 17.2 Conditional approval

Conditional approval is allowed when the change is acceptable in principle but publication requires edits such as:

- naming normalization,
- alias restructuring,
- stronger examples,
- lifecycle downgrade to experimental,
- added migration notes,
- added usage constraints.

### 17.3 Rejection conditions

Common rejection causes include:

- semantic duplication,
- insufficient definitional clarity,
- hidden breaking impact,
- policy or constitutional conflict,
- misuse of namespace scope,
- unverifiable provenance,
- domain overreach,
- need for implementation evidence before admission.

### 17.4 Escalation

Escalation is mandatory for:

- core namespace changes,
- breaking changes to stable widely used terms,
- governance boundary changes,
- term disputes with ecosystem-wide impact,
- constitutional semantic closure issues.

---

## 18. Compatibility Policy

Compatibility must be a first-class registry concern.

### 18.1 Compatibility classes

Registry changes shall be labeled using compatibility classes.

| Class | Meaning |
|---|---|
| C0 | editorial only, no semantic impact |
| C1 | additive and backward-compatible |
| C2 | backward-compatible with warnings or new optional constraints |
| C3 | migration recommended |
| C4 | migration required for some profiles |
| C5 | breaking change |

### 18.2 Required metadata for non-C0 changes

For any change above C0, the registry record must include:

- affected modules/terms,
- impacted validator behaviors,
- impacted query semantics,
- impacted compiler mappings,
- required migration steps,
- rollback or coexistence strategy,
- effective date or snapshot boundary.

### 18.3 Coexistence windows

For deprecations and supersessions, the registry should define coexistence windows during which both old and new terms remain resolvable.

### 18.4 Snapshot discipline

Compatibility is measured between snapshots, not against vague latest-state assumptions.

---

## 19. Deprecation, Supersession, and Retirement

### 19.1 Deprecation

Deprecation means the term remains valid for resolution and historical interpretation but should not be used for new authoring.

Required metadata:

- deprecation reason,
- deprecation snapshot,
- recommended replacement if any,
- migration notes,
- removal or retirement conditions if anticipated.

### 19.2 Supersession

Supersession means one construct has been formally replaced by another construct or pattern.

A supersession record must define:

- source term/module,
- target term/module,
- exact semantic relationship,
- one-to-one, one-to-many, or conditional mapping,
- migration recipe,
- incompatibility notes.

### 19.3 Retirement

Retirement is stronger than deprecation. A retired construct is no longer active for ordinary processing except legacy replay or explicit archival profiles.

Retirement requires high review burden and must not occur without a coexistence and migration history unless the term was experimental-only.

---

## 20. Experimental and Sandbox Governance

AASL must support innovation without contaminating the stable semantic substrate.

### 20.1 Experimental namespaces

Experimental namespaces allow limited admission of concepts that are promising but not yet ready for stable canonical inclusion.

### 20.2 Experimental constraints

Experimental content must:

- be explicitly marked,
- be disallowed from silent promotion to stable,
- carry stricter provenance requirements,
- be blocked or warned in stable production profiles unless explicitly enabled,
- have review expiration or renewal windows.

### 20.3 Sandbox registries

Private or sandbox registries may exist for local development. They must not be confused with the canonical registry and must not be treated as globally trusted without explicit federation rules.

---

## 21. Trust, Identity, and Signing

### 21.1 Registry trust model

The registry is part of the trusted semantic substrate. Therefore, publication must support:

- signer identity,
- signature verification,
- artifact integrity,
- provenance chain,
- release attestations,
- tamper-evident audit logging.

### 21.2 Signed snapshots

Every canonical snapshot must be signed by the designated release authority or quorum mechanism.

### 21.3 Proposal identity

Proposal origin must be attributable to a human, organization, or approved agent identity. Anonymous mutations must not reach canonical publication.

### 21.4 Agent participation

Agents may assist with proposal drafting, overlap analysis, migration planning, or review summarization. Agents must not bypass approval authority. Agent-authored recommendations must remain attributable and reviewable.

---

## 22. Registry Audit Log

The registry must maintain an append-only governance audit log.

### 22.1 Audit events

The log should include events such as:

- proposal submitted,
- intake failed,
- review started,
- review comment added,
- proposal revised,
- approved,
- conditionally approved,
- rejected,
- escalated,
- snapshot published,
- snapshot revoked,
- term deprecated,
- term retired,
- stewardship transferred.

### 22.2 Required audit metadata

Each event should record:

- timestamp,
- actor identity,
- event type,
- affected registry elements,
- prior state,
- resulting state,
- rationale reference,
- signature or integrity reference where applicable.

### 22.3 Audit immutability

Published audit records must be immutable except through explicit correction records.

---

## 23. Validator Integration

The validator depends on the registry as the authoritative source of semantic admissibility.

### 23.1 Registry resolution contract

The validator must be able to resolve against:

- a pinned snapshot,
- a pinned module version,
- an approved profile-defined registry bundle,
- an offline cache of the above.

### 23.2 Validation outcomes tied to lifecycle

Validator behavior should reflect lifecycle state:

- `stable` → normal admission rules,
- `experimental` → profile-gated admission or warnings,
- `deprecated` → warning or policy failure for new authoring,
- `superseded` → warning plus migration suggestion,
- `retired` → failure outside legacy profiles,
- `rejected` → hard failure.

### 23.3 No ambient term invention

The validator must not silently accept unknown terms based on heuristic similarity. Unknown terms require explicit registry recognition or approved sandbox policy.

---

## 24. Compiler Integration

The compiler uses the registry as the target semantic vocabulary.

### 24.1 Mapping discipline

The compiler must map extracted semantics to registered terms and record the exact registry snapshot used.

### 24.2 Ambiguity handling

If multiple registry terms could plausibly fit extracted semantics, the compiler must record ambiguity rather than silently choosing a strong ontology commitment.

### 24.3 Alias handling

Compiler alias expansion must be driven by registry alias tables, not private synonym dictionaries that bypass governance.

---

## 25. Runtime and Query Integration

### 25.1 Runtime

The runtime must interpret semantic objects against the declared registry snapshot or profile-defined registry set.

### 25.2 Query layer

The query engine should expose registry-aware introspection such as:

- list modules,
- list terms in namespace,
- show lifecycle state,
- show aliases,
- show supersession targets,
- show compatible replacements,
- show snapshot diff.

### 25.3 Explainability

When the runtime or query layer surfaces ontology-based interpretation, it should reference the registry definitions that governed the interpretation.

---

## 26. Tooling Integration

Developer tooling should provide registry-aware capabilities.

### 26.1 Authoring assistance

Tools should support:

- namespace-aware autocompletion,
- lifecycle-aware warnings,
- alias and replacement suggestions,
- term definition hover,
- snapshot pinning visibility,
- module dependency inspection.

### 26.2 Migration support

Tools should support automatic or semi-automatic migration when registry records provide formal replacement mappings.

### 26.3 Registry diff visualizations

Tools should expose human-readable diffs between snapshots, especially for:

- new terms,
- changed definitions,
- changed lifecycle states,
- new deprecations,
- new incompatibilities.

---

## 27. Federation and Multi-Registry Environments

Atrahasis may need to operate across multiple organizations and trust domains.

### 27.1 Canonical registry vs federated registries

The canonical registry is the default shared semantic authority. Federated registries may exist, but federation must be explicit.

### 27.2 Federation requirements

Federated registry interoperability requires:

- declared trust relationship,
- namespace collision policy,
- snapshot identity,
- signing verification,
- explicit import policy,
- local override restrictions,
- conflict resolution policy.

### 27.3 Imported module status

Imported modules should carry origin metadata and local trust classification.

### 27.4 No silent federation

A runtime or validator must never merge external registries into trusted resolution scope without an explicit federation configuration.

---

## 28. Operational Workflows

### 28.1 New module admission workflow

1. Submit module proposal.  
2. Complete intake validation.  
3. Run duplication and overlap analysis.  
4. Review module scope and namespace placement.  
5. Review compatibility and implementation consequences.  
6. Approve as experimental or stable.  
7. Publish in next registry snapshot.  
8. Update tooling and migration indexes.

### 28.2 New term admission workflow

1. Draft term with definition, examples, and usage boundary.  
2. Compare against existing registry terms.  
3. Determine whether term is truly new, alias-worthy, or redundant.  
4. Review compatibility, validator, compiler, and runtime consequences.  
5. Approve or revise lifecycle state.  
6. Publish term with stable identifier and metadata.

### 28.3 Deprecation workflow

1. Submit deprecation proposal.  
2. Document reason and replacement path.  
3. Review ecosystem usage and migration burden.  
4. Approve coexistence window.  
5. Publish deprecation metadata.  
6. Surface warnings through tooling and validation.

### 28.4 Breaking change workflow

1. Submit proposal with explicit breaking classification.  
2. Provide migration strategy and impact report.  
3. Escalate to higher governance review.  
4. Publish transition plan.  
5. Release in major snapshot boundary only.  
6. Maintain historical resolution support where feasible.

---

## 29. Registry Quality Gates

Before publishing a snapshot, the release process should verify:

- all admitted proposals are represented,
- no duplicate stable identifiers exist,
- alias targets resolve,
- supersession graphs are acyclic where required,
- deprecation metadata is complete,
- dependency graphs resolve,
- lifecycle states are valid,
- compatibility manifest is complete,
- signatures verify,
- machine-readable exports pass schema validation,
- changelog summaries match actual registry deltas.

A failed quality gate must block publication.

---

## 30. Anti-Patterns

The following behaviors are prohibited or strongly disallowed:

- silently inventing ontology terms in runtime or tooling,
- using private synonym maps to bypass registry review,
- reusing deprecated terms for new meanings,
- changing definitions without a new governance record,
- shipping unversioned ontology bundles,
- treating experimental modules as stable by convention,
- allowing parser/validator/compiler disagreement over registry state,
- publishing unsigned or unaudited canonical snapshots,
- embedding hidden ontology extensions inside application code,
- using natural-language documentation as the only source of semantic truth.

---

## 31. Minimal Canonical Data Model

Illustrative registry term entry:

```json
{
  "term_id": "term://core.reasoning/claim.supports",
  "module_id": "module://core.reasoning/v1",
  "canonical_label": "claim.supports",
  "kind": "relation_type",
  "definition": "Indicates that one claim or evidence object provides supporting weight for another claim under a declared reasoning context.",
  "lifecycle_state": "stable",
  "introduced_in": "snapshot-2026.03.08-core1",
  "aliases": ["supports_claim"],
  "supersedes": [],
  "deprecated_by": null,
  "compatibility_notes": "Backward-compatible additive relation.",
  "provenance_ref": "govrec://proposal-1842"
}
```

Illustrative governance record:

```json
{
  "governance_record_id": "govrec://proposal-1842",
  "proposal_id": "proposal-1842",
  "decision_class": "additive-sensitive",
  "outcome": "approved",
  "effective_snapshot": "snapshot-2026.03.08-core1",
  "reviewers": [
    "role:ontology-editor",
    "role:compatibility-reviewer",
    "role:release-authority"
  ],
  "rationale": "Approved because relation fills a core reasoning gap and does not collide with existing entailment or provenance relations.",
  "signed": true
}
```

These examples are illustrative. Final wire formats may differ, but the semantics are mandatory.

---

## 32. Security and Abuse Considerations

Ontology governance is a security surface.

Potential abuse patterns include:

- malicious redefinition of trusted terms,
- namespace squatting,
- ambiguity injection,
- alias poisoning,
- registry tampering,
- unsigned unofficial snapshot distribution,
- mass proposal flooding by autonomous agents,
- covert policy bypass through “temporary” private terms.

Mitigations must include:

- signing,
- rate controls and intake controls,
- reviewer separation where necessary,
- auditability,
- explicit trust classifications,
- restricted promotion from experimental/private to stable,
- deterministic snapshot publication.

---

## 33. Relationship to the Atrahasis Semantic Closure Policy

This document operationalizes semantic closure in the ontology domain.

Concretely, it means:

- ontology meaning enters the trusted substrate only through registered artifacts,
- extension is allowed only through visible governance channels,
- validator and runtime behavior must resolve against explicit registry state,
- undocumented semantic behavior is non-canonical,
- “everyone knows what this means” is not a governance mechanism.

The ontology registry is therefore one of the principal enforcement mechanisms for semantic closure across the AASL ecosystem.

---

## 34. Conformance Requirements

An implementation claiming conformance with this specification must, at minimum:

1. support versioned registry snapshots,  
2. support stable term and module identifiers,  
3. publish lifecycle state for registered elements,  
4. require proposal records for canonical mutations,  
5. record governance outcomes in an audit trail,  
6. expose compatibility metadata for non-editorial changes,  
7. provide signed or otherwise verifiable canonical snapshot publication,  
8. prevent silent acceptance of unknown terms in trusted validation mode,  
9. expose deprecation and supersession metadata to downstream systems,  
10. preserve traceability from published ontology element back to governance decision.

---

## 35. Recommended Initial Deliverables

To operationalize this specification, the Atrahasis implementation roadmap should produce:

1. **Registry Schema Package**  
   Canonical schemas for namespaces, modules, terms, lifecycle metadata, compatibility manifests, and governance records.

2. **Registry Builder**  
   Deterministic build system that assembles raw governance-approved inputs into signed snapshot artifacts.

3. **Governance Proposal Templates**  
   Standardized machine-readable and human-readable proposal forms.

4. **Registry Diff Engine**  
   Tooling that compares snapshots and emits semantic, lifecycle, and compatibility deltas.

5. **Validator Registry Resolver**  
   A pinned-snapshot resolver used by the validator and query engine.

6. **Compiler Mapping Resolver**  
   Registry-aware alias and term resolution component for AASC.

7. **Migration Advisory Engine**  
   Emits upgrade hints based on deprecation and supersession records.

8. **Federation Policy Module**  
   Defines how external registries can be imported under controlled trust.

---

## 36. Final Statement

The ontology registry and governance layer is the semantic constitution-in-operation for AASL evolution. Syntax can be parsed without it. Documents can be written without it. Experiments can even proceed without it. But a durable, interoperable, auditable semantic ecosystem cannot exist without it.

This specification defines the mechanism by which Atrahasis preserves shared meaning while still allowing growth. It prevents ontology drift, constrains extension, enforces versioned semantic identity, and gives validators, compilers, runtimes, tooling, and federated systems a common semantic source of truth.

In practical terms, this is the layer that keeps AASL from fragmenting as soon as multiple teams, multiple agents, multiple domains, and multiple deployments begin extending it at once.
