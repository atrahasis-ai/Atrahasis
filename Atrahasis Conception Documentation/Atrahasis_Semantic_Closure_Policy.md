# Atrahasis Semantic Closure Policy
Version: 1.0.0  
Status: Canonical Implementation Policy  
Date: 2026-03-08  

---

# 1. Purpose

This policy defines the **semantic closure rule** for the Atrahasis runtime and the AASL ecosystem.

Its purpose is to prevent the most dangerous implementation failure mode in semantic agent systems:

> semantically meaningful behavior existing outside the formal AASL-governed system.

This policy ensures that Atrahasis remains an **AASL-native intelligence system**, rather than degrading into a hybrid architecture where meaning is split across:

- AASL
- raw prompts
- ad hoc JSON fields
- hidden service logic
- undocumented heuristics
- database-only flags
- manual operator conventions

This document is the formal guardrail against **semantic drift**.

---

# 2. Core Policy Statement

## 2.1 Primary Rule

Any data, rule, state, or decision that materially affects:

- semantic interpretation
- workflow routing
- agent behavior
- claim generation
- evidence evaluation
- verification outcome
- memory admission
- canonical identity
- trust tier
- federation behavior
- governance behavior

must exist in one of the following approved forms:

1. **AASL object**
2. **Formally defined AASL-adjacent contract field**
3. **Governed policy object explicitly linked to the semantic system**

If it affects the meaning or behavior of the system and is not represented in one of those forms, it is considered a **closure violation**.

---

# 3. Why Semantic Closure Matters

Atrahasis depends on AASL being the sovereign internal semantic substrate.

The architecture relies on these properties remaining true:

- canonicalization is authoritative
- verification compares formal semantics
- memory reuse depends on canonical semantic identity
- federation exchanges the full meaning
- governance evolves the formal system instead of hidden behavior
- inspection and debugging can reconstruct why the system behaved as it did

If behaviorally important meaning leaks outside the formal system, those guarantees collapse.

Semantic closure is therefore not an optional cleanliness standard.  
It is a foundational integrity requirement.

---

# 4. Definition of Semantic Drift

Semantic drift occurs when semantically meaningful behavior exists outside the formal AASL-governed architecture.

Examples include:

- prompt instructions that change trust behavior but are not modeled as policy
- hidden JSON fields that affect admission or routing
- code-level heuristics that bypass formal workflow logic
- memory decisions made by undocumented thresholds
- verification decisions based on untracked evaluator notes
- operator actions that change semantic state without formal representation

Semantic drift can exist even when the system “works.”

That is what makes it dangerous.

---

# 5. Scope of This Policy

This policy applies to all layers of the Atrahasis system, including:

- AASC compiler behavior
- parser and canonicalizer behavior
- runtime object handling
- coordinator routing logic
- research, analysis, verification, and memory agent behavior
- AACP message handling
- storage admission logic
- memory reuse logic
- verification and trust decisions
- export behavior
- operator tooling
- distributed federation
- governance and ontology evolution
- API-layer behavior that affects semantic outcomes

It applies to both human-written code and AI-generated implementation.

---

# 6. Approved Semantic Representation Forms

## 6.1 AASL Objects

The preferred form for semantically meaningful information is an AASL object or formally governed AASL document section.

Examples:

- `TSK` for tasks
- `CST` for constraints
- `CLM` for claims
- `EVD` for evidence
- `CNF` for confidence
- `PRV` for provenance
- `VRF` for verification
- `TIM` for explicit time metadata

If the meaning fits naturally into AASL, it should be represented there first.

## 6.2 AASL-Adjacent Contract Fields

Some operational metadata may need to exist outside direct AASL object syntax but still inside formal contract systems.

These may include:

- AACP header metadata
- bundle wrapper metadata
- API request envelope fields
- storage admission state fields
- workflow correlation identifiers

These fields are allowed only if they are:

- formally schema-defined
- versioned
- documented
- validated
- inspectable
- governed

## 6.3 Governed Policy Objects

When behavior must be controlled by policy rather than instance-level semantic objects, that policy must itself be formalized.

Examples:

- verification threshold policy
- trust admission policy
- memory promotion policy
- federation acceptance policy
- ontology/module acceptance policy

These policies must not exist only as hidden code or prompt text.  
They must exist as governed artifacts linked to the semantic runtime.

---

# 7. Prohibited Semantic Leakage

The following are prohibited when they materially affect system behavior:

## 7.1 Hidden Prompt Semantics

Prompts may guide language transformation or extraction behavior, but they must not be the only place where important operational semantics are defined.

Examples of prohibited prompt-only semantics:

- “If source is trustworthy, skip verification”
- “Prefer stronger causal claims for certain datasets”
- “Override normal trust rules for premium workflows”
- “Suppress ambiguous evidence if confidence seems high”

If a prompt changes behavior materially, the same behavior must be representable and inspectable as policy or semantic state.

## 7.2 Ungoverned JSON or Metadata Flags

Prohibited examples:

- `trust_boost`
- `skip_verify`
- `priority_override`
- `special_mode`
- `force_memory_accept`
- `semantic_similarity_override`

unless they are:

- formally defined
- governed
- versioned
- documented
- visible to inspection and audit tools

## 7.3 Untracked Code Heuristics

Prohibited examples:

- hardcoded routing shortcuts
- memory admission exceptions
- verification bypasses
- dataset-specific hidden logic
- undocumented fallback paths that change semantic interpretation

## 7.4 Operator-Only Semantic Overrides

Operators may manage systems, but they must not create hidden semantic truth through manual intervention without formal artifacts representing the change.

Any operator action that affects semantic outcomes must generate an inspectable and traceable system record.

---

# 8. Formal Closure Test

Every proposed feature, field, heuristic, or behavior must pass the following review test:

## 8.1 Semantic Closure Questions

1. What meaning does this introduce?
2. Does it affect interpretation, routing, trust, admission, or reuse?
3. Where does that meaning live formally?
4. Can it be represented in AASL or a governed adjacent schema?
5. Can it be validated?
6. Can it be stored?
7. Can it be queried?
8. Can it be inspected in operator tooling?
9. Can it be federated if needed?
10. Can it be governed across versions?

If the answer to these questions is “no” for a behaviorally meaningful element, implementation must stop until a formal representation is defined.

---

# 9. Semantic Closure Review Requirement

Every new feature affecting the runtime must undergo **semantic closure review** before implementation.

The review must explicitly answer:

- what new meaning is introduced
- whether the meaning affects execution or trust
- whether the meaning is represented in AASL, contracts, or policy objects
- whether it is inspectable and auditable
- whether it is versioned and governed

No semantically meaningful implementation change may bypass this review.

---

# 10. Prompt Governance Rules

Prompts are allowed, but only within strict bounds.

## 10.1 Allowed Prompt Roles

Prompts may be used for:

- extraction assistance
- language-to-semantic transformation
- summarization
- natural-language rendering
- semantic candidate generation
- non-authoritative explanation generation

## 10.2 Disallowed Prompt Roles

Prompts must not be the sole authority for:

- trust decisions
- memory admission rules
- workflow routing rules
- canonical identity logic
- ontology interpretation
- policy exceptions
- verification thresholds

If prompts influence these areas, that influence must be explicitly controlled by governed policy and represented in formal system state.

---

# 11. Service Logic Rules

Services may implement algorithms and workflow logic, but they may not become hidden semantic authorities.

Therefore:

- all routing decisions must be explainable from formal state and policy
- all admission decisions must be explainable from formal state and policy
- all verification decisions must be explainable from formal state and policy
- all semantic transformations must be attributable to formal rules or compiler behavior
- all exceptions must be represented as governed policy, not private code paths

This prevents services from becoming shadow ontologies.

---

# 12. Storage Closure Rules

The storage layer must preserve semantic closure.

This means:

- no behaviorally meaningful fields may exist in storage without schema ownership
- no trust-relevant decision may depend on undocumented storage flags
- no hidden DB-only states may influence memory admission or retrieval
- all tier transitions must be inspectable
- all duplicate/equivalence logic must be tied to canonical semantic identity, not hidden similarity metrics unless formally governed

Storage must not become a second hidden semantics system.

---

# 13. Memory Closure Rules

The Memory Agent and memory service are high-risk drift zones because they are tempting places to add heuristics.

The following rules apply:

- all reuse decisions must be explainable from query results, canonical identity, verification state, and formal admission policy
- all duplicate detection logic must be documented and schema-backed
- all admission results must be persisted formally
- all memory rejection and quarantine states must be visible and queryable

No hidden “smart cache logic” is allowed if it materially affects trust or reuse.

---

# 14. Verification Closure Rules

Verification must be anchored to formal semantics.

Therefore:

- verification compares canonical semantic artifacts, not only raw text
- verification status must be represented as `VRF` or governed verification records
- verification thresholds must be policy-controlled
- all disputes must be represented formally
- all verification methods must be explicit and inspectable

No hidden evaluator scores or undocumented reviewer logic may decide trust status silently.

---

# 15. API Closure Rules

API layers may translate between external formats and internal AASL, but they must not introduce hidden semantics.

Therefore:

- external API request convenience fields are allowed only if they are formally mapped into semantic or contract state
- API-only flags must not bypass runtime trust or routing policy
- API result shaping must not hide authoritative semantic state
- any client-visible status must correspond to real runtime semantic state

The API is a boundary adapter, not a semantic authority.

---

# 16. Operator Closure Rules

Operators may observe, inspect, and manage the system, but operator actions that change semantic outcomes must be formalized.

Examples:

- forcing bundle quarantine
- promoting bundle tiers
- resolving conflicts
- re-running verification
- approving policy exceptions

These actions must generate:

- auditable records
- explicit state changes
- provenance of intervention
- visible traces in inspection tooling

No invisible operator magic is allowed.

---

# 17. Federation Closure Rules

When knowledge leaves a node, all semantically relevant meaning required to interpret it must travel with it or be resolvable through governed shared registries.

Therefore:

- artifacts must not depend on node-local hidden assumptions
- ontology/module interpretation must be versioned and explicit
- trust decisions must be backed by exchangeable formal metadata
- synchronization must not rely on undocumented local heuristics

A node must not export incomplete semantic truth while keeping critical behavior hidden locally.

---

# 18. Governance Closure Rules

Governance must apply not only to the language but also to system behavior.

Therefore:

- all semantic-affecting policies must be versioned
- new behaviorally meaningful fields require review
- extensions require schema or ontology registration
- experimental semantics must use reserved namespaces
- deprecated behavior must be formally marked and phased out

This prevents “temporary” exceptions from silently becoming permanent hidden law.

---

# 19. Observability Requirements

To enforce closure, operator and developer tooling must expose the real reasons behind system behavior.

At minimum, tooling must allow inspection of:

- why a task was routed
- why memory was a hit or miss
- why a bundle was admitted or rejected
- why verification succeeded or failed
- which policy objects were applied
- what semantic artifacts drove the decision
- what human/operator interventions occurred

If the runtime cannot explain a behavior in inspectable formal terms, semantic closure may already be broken.

---

# 20. Allowed Exceptions

Very limited exceptions are permitted only under strict control.

An exception may exist temporarily if all of the following are true:

1. it is documented explicitly
2. it is time-bounded
3. it has an owner
4. it has a migration/removal plan
5. it does not change trust or semantic identity silently
6. it is visible in diagnostics or operator tooling

Temporary implementation scaffolding is not a license to create hidden semantic authority.

---

# 21. Closure Violation Severity Levels

Closure violations should be classified by severity.

## Level 1 — Minor Structural Drift
Meaning exists outside ideal AASL form, but does not yet affect trust, reuse, or interpretation materially.

## Level 2 — Semantic Drift
Meaning materially affects routing, interpretation, or storage behavior but remains partially inspectable.

## Level 3 — Trust Drift
Meaning materially affects verification, memory admission, or trust tier decisions without full formal representation.

## Level 4 — Sovereignty Failure
The real system behavior is primarily controlled by hidden prompts, hidden code, or hidden metadata rather than the formal semantic system.

Level 3 and Level 4 violations must be treated as architectural defects requiring immediate remediation.

---

# 22. Required Enforcement Mechanisms

This policy must be enforced through implementation mechanisms.

Required mechanisms include:

- semantic closure review in design process
- schema review for new contract fields
- policy review for new trust or routing rules
- CI checks for undocumented fields where possible
- code review templates that ask where meaning lives formally
- operator tooling that exposes policy and semantic traces
- validation/reporting that distinguishes formal vs hidden states

Without enforcement, the policy is only advisory and will eventually fail.

---

# 23. Implementation Checklist for Enforcing Closure

The first runtime should implement the following controls:

1. Add “semantic closure” as a required section in architecture and feature proposals.
2. Add code review checklist item: “Does this introduce meaning outside AASL/contracts/policy?”
3. Require schema definitions for all behaviorally meaningful new fields.
4. Require persisted admission/verification/routing traces.
5. Expose decision traces in operator APIs and tooling.
6. Forbid undocumented service-local flags in production paths.
7. Maintain a registry of governed policy objects affecting trust and routing.
8. Audit prompts for hidden operational semantics.
9. Audit storage schema for hidden behavioral fields.
10. Audit memory reuse logic for undocumented heuristics.

---

# 24. Policy Ownership

This policy should be jointly owned by:

- AASL maintainers
- runtime architects
- verification policy owners
- storage/memory owners
- governance maintainers

No one implementation team should be allowed to weaken it unilaterally.

---

# 25. Practical Decision Rule

When engineers or AI coding agents are unsure whether something is a closure violation, use this rule:

> If removing AASL, formal contracts, and governed policy objects would make the behavior impossible to explain or reconstruct, then that behavior is not formally closed and must not be accepted.

This is the fastest practical test.

---

# 26. Final Statement

Atrahasis is being built as a semantically sovereign intelligence system.

That means AASL is not merely a notation layer.  
It is the formal constitution of internal machine meaning.

This policy exists to ensure that the implementation does not quietly create an unwritten shadow constitution in:

- prompts
- heuristics
- service code
- undocumented metadata
- operator folklore

Any operationally important meaning that affects interpretation, trust, routing, reuse, or federation must be represented formally, governed explicitly, and made inspectable.

That is semantic closure.  
Without it, the architecture will drift.  
With it, Atrahasis remains truly AASL-native.
