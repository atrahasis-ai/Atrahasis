# T-201 Draft Policy

## Title
AASL Type Registry Extension Policy for `TL{}`, `PMT{}`, and `SES{}`

## Task
Define the governance policy for adding `TL{}`, `PMT{}`, and `SES{}` to the AASL type registry, including ontology versioning impact and forward-compatibility rules.

## Governing Context
- Alternative B requires native replacement of MCP tools, prompt templates, and session/state surfaces with AASL-native semantics.
- The Alternative B strategy packet identifies `TL`, `PMT`, and `SES` as new required AASL types.
- Under ADR-042, old ASV/C4 materials remain historical baseline only for `T-200+` protocol design work; they are not normative design authority for this policy.
- Existing AASL governance rules already require namespace discipline, pinned registry snapshots, explicit compatibility classes, non-ambient term invention, and lifecycle-aware validator behavior.

## Proposed Decision
Approve a formal extension policy that governs admission of `TL{}`, `PMT{}`, and `SES{}` into the canonical AASL registry.

### 1. Placement and authority
- `TL`, `PMT`, and `SES` SHALL be admitted as canonical registry terms through the existing ontology registry and governance process, not by ad hoc implementation extension.
- These terms SHALL live in the canonical Atrahasis-controlled namespace and module structure defined by the registry maintainers, not in partner, private, or experimental namespaces once accepted for stable Alternative B use.
- This task defines policy authority only. Final structural field definitions and canonical forms remain downstream design work for `T-212`.

### 2. Change classification
- `TL`, `PMT`, and `SES` admissions SHALL be treated as at least `additive-sensitive` governance changes and SHALL receive compatibility class `C1` or `C2`, not `C0`.
- If any proposed field set or semantics changes validator behavior, compiler mapping behavior, or runtime interpretation beyond additive optionality, the proposal SHALL be escalated to `C2` or higher with explicit migration metadata.
- No proposal in this family may be treated as editorial.

### 3. Required proposal contents
Every admission proposal for `TL`, `PMT`, or `SES` SHALL include:
- target namespace and module
- semantic rationale tied to Alternative B
- overlap analysis against existing AASL types and modules
- compatibility analysis against pinned registry snapshots
- validator impact
- compiler impact
- runtime and tooling impact
- examples and anti-examples
- lifecycle state request
- migration and coexistence guidance where applicable

### 4. Snapshot and versioning discipline
- All three types SHALL be admitted against explicit registry snapshots; no implementation may treat them as ambient latest-state features.
- The first stable release that contains these types SHALL mint a new canonical registry snapshot and module-version boundary.
- Validators, compilers, runtimes, and developer tooling SHALL record the exact registry snapshot used when resolving these types.
- Future revisions to `TL`, `PMT`, or `SES` SHALL be measured snapshot-to-snapshot using the existing `C0-C5` compatibility classes.

### 5. Forward-compatibility and unknown-type handling
- Implementations that do not recognize `TL`, `PMT`, or `SES` MUST NOT silently reinterpret them as older known types.
- Unknown-type handling SHALL follow existing AASL registry rules: explicit failure, warning, or profile-gated admission based on lifecycle state and declared profile, not heuristic guessing.
- Stable production profiles that do not support these types SHALL reject or quarantine objects that require them, while preserving enough metadata for explainable diagnostics.
- Sandbox or experimental profiles MAY accept pre-stable variants only through explicit registry/profile enablement.

### 6. Backward-compatibility and coexistence
- Admission of these new types SHALL NOT by itself redefine existing core AASL types.
- Existing documents that do not use `TL`, `PMT`, or `SES` remain valid under prior compatible snapshots unless another change explicitly alters their admissibility.
- If later work supersedes older workaround patterns using existing types, the registry SHALL publish coexistence windows and formal replacement mappings rather than forcing silent breakage.

### 7. Lifecycle policy
- `TL`, `PMT`, and `SES` MAY begin as `experimental` only if the registry maintainers judge their semantics not yet stable enough for direct canonical admission.
- Experimental admission MUST include expiration or renewal windows and MUST NOT silently promote to `stable`.
- Once Alternative B treats these types as required upstream inputs for downstream tasks, the canonical expectation is `stable` lifecycle status before broad production-profile reliance.

### 8. Namespace and anti-fragmentation policy
- No parallel unofficial spellings or synonym families for tool, prompt-template, or session semantics may bypass registry governance.
- Partner or private namespaces MAY define local refinements or adjunct terms, but MUST NOT masquerade as canonical `TL`, `PMT`, or `SES`.
- Compiler alias handling and migration assistance SHALL be driven by published registry alias/replacement tables only.

### 9. Downstream dependency rule
- `T-212` may define field schemas, canonical forms, and ontology placement only after this policy is accepted.
- `T-210` remains the upstream architectural authority for how these types fit into the five-layer protocol model.
- If `T-210` or later protocol tasks discover that these three types are insufficient, the response is a new registry-policy or extension task, not silent schema growth.

## Rationale
- The Alternative B packet already identifies these three types as required, so the governance gap is not whether new types are needed but how to admit them without breaking semantic closure.
- Existing AASL governance material already provides the right primitives: namespace classes, proposal intake, compatibility classes, coexistence windows, lifecycle-aware validator behavior, and a ban on silent unknown-term invention.
- This policy keeps `T-201` at the governance layer and avoids inventing the actual `TL` / `PMT` / `SES` schema content that belongs to `T-212`.

## Key Impacts
- Unblocks `T-210` as the next root protocol-architecture task.
- Establishes the governance envelope required by `T-212`.
- Prevents downstream tasks from treating provisional type ideas as canonical registry truth.

## Source Notes
- The legacy desktop paths named in the Alternative B packet were not present, but equivalent AASL source documents were found under `C:\Users\jever\Atrahasis\Atrahasis Conception Documentation\`.
- Relevant baseline rules came from:
  - `AASL_SPECIFICATION.md` sections on safe extensibility, namespaces, types, and versioning/compatibility
  - `Atrahasis_AASL_Ontology_Registry_and_Governance_Operations.md` sections on namespace classes, proposal intake, compatibility classes, lifecycle, validator behavior, and tooling integration
  - `AASL_PRIMER.md` guidance on unknown extensions and avoiding fabricated semantics
