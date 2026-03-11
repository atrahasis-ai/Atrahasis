# Atrahasis AASL Developer Tooling Specification

**Document ID:** ATR-AASL-DEVTOOLS-001  
**Title:** Atrahasis AASL Developer Tooling Specification  
**Status:** Canonical Draft  
**Version:** 1.0.0  
**Authoring Context:** Atrahasis / AASL Core System  
**Last Updated:** 2026-03-08  
**Applies To:** `aasl-cli`, language server, editor integrations, formatter, linter, semantic explorer, graph viewer, test harness, debugger, migration tools, developer workflow contracts, CI/CD tooling, and operator-adjacent inspection interfaces.

---

## 1. Purpose

This document defines the canonical **developer tooling layer** for the Atrahasis Agentic Semantic Language (AASL). It specifies the tools, interfaces, contracts, workflows, outputs, and non-functional expectations required to make AASL usable by engineers, researchers, operators, and AI agents in real development environments.

A language without tooling is a theory. A language with only ad hoc tooling becomes inconsistent, fragile, and hostile to adoption. The purpose of this specification is to ensure that every AASL implementation is:

1. **Authorable** by humans with predictable editor support.
2. **Inspectable** by developers and operators without hidden runtime behavior.
3. **Deterministic** across CLI, editor, CI, and agent-driven workflows.
4. **Recoverable** when documents are malformed, incomplete, or migrating between versions.
5. **Auditable** through diagnostics, traces, provenance, and semantic explanations.
6. **Composable** with the parser, validator, compiler, runtime, query engine, and file infrastructure.
7. **Usable at scale** for single documents, repositories, packages, and corpora.

This tooling layer turns AASL from a formal system into a production-grade development ecosystem.

---

## 2. Scope

This specification covers:

- Canonical command-line tooling (`aasl-cli`)
- Language server and editor integration contracts
- Formatter behavior
- Linter and static semantic advisory behavior
- Semantic graph viewer
- Object explorer / runtime inspection UI contracts
- Trace explorer and explainability surfaces
- Test harness and conformance tooling
- Migration and refactoring tooling
- Corpus tooling and batch workflows
- CI/CD contracts for AASL repositories
- Developer workflow conventions
- Artifact interoperability between tools
- Extension APIs for future tooling

This specification does **not** redefine the AASL grammar, validator semantics, compiler ontology mapping model, or runtime execution model, except where those systems surface through tooling contracts.

---

## 3. Design Principles

The AASL tooling ecosystem shall obey the following principles.

### 3.1 Determinism over convenience

Tool outputs must be stable, reproducible, and versioned. Two identical inputs under the same profile must yield identical tooling outputs.

### 3.2 Explainability over opacity

Every meaningful diagnostic, rewrite, inference, or resolution should expose the reasoning path or source basis that produced it.

### 3.3 Read-only by default

Inspection tooling must not silently mutate semantic content. Mutation must be explicit, reviewable, and reversible.

### 3.4 Human and agent parity

The same tooling contracts should be usable by both human developers and autonomous agent workflows.

### 3.5 Graceful degradation

If advanced tooling components are unavailable, the system must degrade to CLI-based authoring and inspection without semantic ambiguity.

### 3.6 Canonical data exchange

All tooling components must exchange structured outputs using stable schemas so parser, validator, compiler, runtime, and UI tools do not reinterpret raw text inconsistently.

### 3.7 Incremental responsiveness

Interactive tools must support incremental parsing, diagnostics, and inspection for large documents and repositories.

### 3.8 No semantic theater

Tooling must reflect true parser, validator, compiler, query, and runtime state. A successful-looking UI must never conceal a failed or partial semantic state.

---

## 4. Tooling Layer Overview

The AASL developer tooling layer is composed of cooperating subsystems.

| Tooling Subsystem | Primary Role | Primary Inputs | Primary Outputs |
|---|---|---|---|
| `aasl-cli` | Canonical shell interface | files, packages, repos, stdin, config | reports, artifacts, diagnostics, patches |
| Language Server | editor intelligence | open documents, project context | completions, hover, diagnostics, code actions |
| Formatter | canonical presentation | CST/AST + formatting config | rewritten source |
| Linter | advisory semantic quality checks | AST, semantic graph, policy profiles | warnings, refactor suggestions |
| Semantic Explorer | graph inspection | semantic graph, indexes, traces | navigable object/edge views |
| Graph Viewer | visualization | semantic graph, query results | rendered graph views |
| Runtime/Object Explorer | state inspection | runtime registry, object snapshots | object cards, diffs, traces |
| Test Harness | conformance verification | tests, corpora, expected outputs | pass/fail reports, coverage, baselines |
| Migration Toolkit | version upgrade and refactor | source corpora, profiles, schemas | patches, conversion reports |
| CI Integrations | automation | repository state, build pipelines | gates, artifacts, summaries |

These tools are not optional conveniences. Together they form the operational surface of AASL.

---

## 5. Canonical Tooling Architecture

The canonical developer tooling architecture is organized in layers.

```text
User / Agent
   ↓
CLI / Editor / UI / CI Adapters
   ↓
Tooling Service Layer
   ├─ parser adapter
   ├─ validator adapter
   ├─ compiler adapter
   ├─ runtime adapter
   ├─ query adapter
   ├─ file infra adapter
   └─ profile/config adapter
   ↓
Structured Tooling Contracts
   ├─ diagnostics
   ├─ spans
   ├─ symbols
   ├─ semantic graph snapshots
   ├─ traces
   ├─ patches
   ├─ reports
   └─ provenance
   ↓
Core AASL Systems
```

### 5.1 Tooling service layer

The tooling layer should not reimplement parser, validator, compiler, or runtime semantics. It should adapt those systems into stable user-facing workflows.

### 5.2 Shared schemas

All tooling components must consume and emit shared schemas for:

- source spans
- diagnostics
- symbol references
- semantic identifiers
- patch plans
- trace steps
- validation reports
- compile reports
- runtime object snapshots
- query result sets
- provenance metadata

### 5.3 Version alignment

Each tooling invocation must record the effective versions of:

- AASL language profile
- grammar version
- parser version
- validator version
- compiler version
- runtime version
- tool version
- config profile version

No tool may present results without binding them to version context.

---

## 6. Canonical CLI: `aasl-cli`

### 6.1 Role

`aasl-cli` is the canonical, scriptable, baseline interface to the AASL ecosystem. Every other user-facing tool should be conceptually reducible to CLI operations.

### 6.2 Requirements

The CLI must be:

- cross-platform
- non-interactive by default
- machine-readable on demand
- stable in exit codes
- deterministic in output
- composable in shell pipelines
- suitable for humans and agents

### 6.3 Command families

The canonical command families should include:

- `parse`
- `validate`
- `format`
- `lint`
- `compile`
- `render`
- `query`
- `inspect`
- `graph`
- `trace`
- `package`
- `lock`
- `index`
- `diff`
- `patch`
- `migrate`
- `test`
- `bench`
- `doctor`
- `init`
- `profile`
- `explain`

### 6.4 Illustrative commands

```bash
aasl-cli parse doc.aas --emit ast
aasl-cli validate repo/ --profile strict
aasl-cli format doc.aas --write
aasl-cli lint corpus/ --policy authoring
aasl-cli compile docs/ --target semantic-ir
aasl-cli query repo/ --expr "find object where type = agent"
aasl-cli inspect object atr.agent.scheduler
aasl-cli graph doc.aas --focus atr.agent.scheduler
aasl-cli trace run_4821 --explain
aasl-cli package build ./module
aasl-cli migrate repo/ --from 1.0 --to 1.1
aasl-cli test ./tests --report junit
aasl-cli doctor repo/
```

### 6.5 Exit code model

The CLI should use a stable exit code contract.

| Exit Code | Meaning |
|---|---|
| `0` | Success |
| `1` | General failure |
| `2` | Parse failure |
| `3` | Validation failure |
| `4` | Compilation failure |
| `5` | Query failure |
| `6` | Runtime inspection failure |
| `7` | Configuration/profile failure |
| `8` | I/O or file infra failure |
| `9` | Internal tooling fault |
| `10` | Partial success with non-fatal diagnostics |

### 6.6 Output modes

All major commands should support:

- human-readable text
- structured JSON
- newline-delimited JSON where relevant
- artifact output files
- patch plans
- compact CI mode
- verbose explain mode

### 6.7 CLI invariants

The CLI must never:

- silently rewrite source without `--write` or equivalent explicit consent
- hide diagnostics because output is “pretty”
- return success when validation failed under the effective profile
- fabricate runtime state for unavailable objects
- mix warnings and semantic success in a misleading way

---

## 7. CLI Command Specifications

### 7.1 `parse`

Purpose:
- parse one or more AASL files
- emit CST, AST, token stream, spans, diagnostics

Inputs:
- files, directories, packages, stdin

Outputs:
- parser report
- optional serialized CST/AST
- source span maps

Key flags:
- `--emit tokens|cst|ast|all`
- `--strict`
- `--recovery`
- `--json`
- `--profile <name>`

### 7.2 `validate`

Purpose:
- execute validator passes against files, repos, or packages

Outputs:
- validation report
- severity summary
- admissibility result
- optional suggested fixes

Key flags:
- `--profile <name>`
- `--max-severity <level>`
- `--fail-on warning`
- `--emit report|json|sarif`

### 7.3 `format`

Purpose:
- rewrite source to canonical or profile-specific formatting rules

Key flags:
- `--write`
- `--check`
- `--diff`
- `--profile canonical|compact|teaching`

### 7.4 `lint`

Purpose:
- surface non-fatal semantic quality issues, style problems, maintainability issues, and anti-patterns

Linting must never masquerade as validation. It is advisory unless explicitly elevated by profile.

### 7.5 `compile`

Purpose:
- execute the AASC compiler to produce semantic IR, ontology-linked artifacts, or downstream representations

### 7.6 `query`

Purpose:
- evaluate AASL query expressions over documents, repos, packages, or runtime projections

### 7.7 `inspect`

Purpose:
- inspect object definitions, resolved references, schemas, provenance, validation status, and runtime projections

### 7.8 `graph`

Purpose:
- materialize semantic graph views for terminal or file-based consumption

### 7.9 `trace`

Purpose:
- expose explanation traces for validation decisions, compile mappings, runtime behaviors, or query results

### 7.10 `migrate`

Purpose:
- transform sources between AASL versions, profiles, module conventions, or schema revisions

### 7.11 `test`

Purpose:
- run parser, validator, compiler, query, and runtime contract tests against fixtures and corpora

### 7.12 `doctor`

Purpose:
- inspect repository health, profile alignment, cache validity, lock integrity, package issues, and environment drift

---

## 8. Configuration and Profiles

### 8.1 Configuration sources

Tooling configuration may come from:

- repository config file
- workspace config file
- user config file
- environment variables
- CLI flags
- embedded package profile

### 8.2 Precedence order

The canonical precedence order should be:

1. explicit CLI flags
2. workspace or invocation-scoped overrides
3. repository config
4. package profile
5. user defaults
6. tool defaults

### 8.3 Standard config areas

The config model should include:

- parser mode
- validator profile
- formatter profile
- linter rulesets
- compile target defaults
- import resolution roots
- cache locations
- editor responsiveness thresholds
- graph rendering thresholds
- migration policies
- CI fail conditions
- security/trust policies

### 8.4 Profiles

Standard profiles should include at least:

- `canonical`
- `strict`
- `authoring`
- `teaching`
- `migration`
- `ci`
- `runtime-safe`
- `forensics`

Each profile must be versioned and discoverable via tooling.

---

## 9. Language Server Protocol Layer

### 9.1 Purpose

The language server provides interactive editor intelligence while preserving semantic consistency with the CLI and core subsystems.

### 9.2 Required capabilities

The AASL language server should support:

- incremental document sync
- parse diagnostics
- validation diagnostics
- hover information
- go-to definition
- find references
- rename symbol / object
- semantic completion
- code actions
- document symbols
- workspace symbols
- semantic highlighting
- formatting requests
- document links
- folding ranges
- inlay hints where useful
- trace-on-hover or explain-on-demand extensions

### 9.3 Consistency rule

A diagnostic shown in the editor for the same document and profile must match CLI results modulo incremental timing differences.

### 9.4 Latency tiers

The language server should support multiple latency tiers:

- **keystroke tier:** tokenization, shallow parse, basic local diagnostics
- **pause tier:** incremental validation, completions, hover enrichment
- **save tier:** full validation and canonical formatting checks
- **workspace tier:** cross-document reference analysis, graph refresh, index refresh

### 9.5 Server state model

The language server should maintain:

- open document snapshots
- per-document parse state
- workspace dependency graph
- symbol index
- validation cache
- semantic graph projection
- pending trace/index refresh tasks

### 9.6 Failure behavior

The server must:

- remain responsive under malformed documents
- degrade gracefully when workspace state is incomplete
- clearly indicate stale versus fresh diagnostics
- never present guessed definitions as authoritative without marking uncertainty

---

## 10. Editor Integration Requirements

### 10.1 Supported surfaces

Canonical editor support should target:

- VS Code / Cursor-class editors
- JetBrains-class IDEs
- Neovim / terminal editor ecosystems
- browser-based workspaces where applicable

### 10.2 Minimum editor features

Every first-party editor integration should provide:

- syntax highlighting
- bracket/section matching
- diagnostics panel
- format on demand
- go-to definition
- hover metadata
- completions for keywords, schemas, modules, object IDs
- quick fixes for common issues
- graph/inspect commands
- trace/explain commands

### 10.3 Workspace awareness

Editors should understand:

- multi-file projects
- package roots
- import resolution
- profile selection
- generated files versus source files
- lockfile and index awareness

### 10.4 First-party editor commands

Recommended editor commands include:

- `AASL: Validate Current Document`
- `AASL: Validate Workspace`
- `AASL: Format Document`
- `AASL: Explain Diagnostic`
- `AASL: Open Semantic Graph`
- `AASL: Inspect Object`
- `AASL: Show Runtime Projection`
- `AASL: Run Query`
- `AASL: Apply Migration`
- `AASL: Repair Common Issues`

---

## 11. Formatter Specification

### 11.1 Role

The formatter converts semantically equivalent source into canonical or profile-specific human-readable layout without altering meaning.

### 11.2 Formatter inputs

The formatter should operate primarily on:

- CST for trivia preservation and layout sensitivity
- AST for semantic invariants
- formatting profile
- optional authoring hints

### 11.3 Formatter outputs

The formatter may produce:

- rewritten source
- minimal diff view
- formatting violations report
- stable formatting checksum

### 11.4 Core invariants

The formatter must:

- preserve semantics exactly
- preserve comments unless profile explicitly states otherwise
- preserve stable object ordering unless canonical reordering is defined elsewhere
- use LF newlines in canonical mode
- be idempotent

Idempotence rule:

```text
format(format(source)) == format(source)
```

### 11.5 Formatting modes

Standard modes should include:

- `canonical`
- `preserve-author-layout` where possible
- `compact`
- `teaching`
- `diff-friendly`

### 11.6 Comment policy

Comments may be repositioned only if required to maintain attachment to the correct syntactic node. A formatter must never orphan comments or attach them to unrelated content.

### 11.7 Failure policy

If a document cannot be safely formatted because parse recovery is too ambiguous, the formatter must refuse to rewrite and explain why.

---

## 12. Linter and Static Advisory Layer

### 12.1 Role

The linter surfaces maintainability and design-quality issues that are not necessarily invalid under the validator.

### 12.2 Typical lint domains

Lint rules may cover:

- unused declarations
- weak naming patterns
- overly implicit references
- redundant attributes
- contradictory comments versus semantics
- large unstructured sections
- missing provenance metadata
- graph design smells
- migration-deprecated idioms
- anti-patterns in query design
- operator-hostile configurations

### 12.3 Severity model

Lint severity should be distinct from validation severity.

Suggested linter levels:

- `info`
- `advice`
- `warning`
- `strong-warning`

### 12.4 Auto-fix model

Some lint findings may support safe autofixes. Autofixes must be:

- previewable
- reversible
- provenance-stamped
- rejected if semantic ambiguity exists

---

## 13. Semantic Explorer

### 13.1 Purpose

The semantic explorer is the primary inspection interface for navigating AASL semantic content as objects, schemas, relationships, references, provenance, and statuses.

### 13.2 Required capabilities

The semantic explorer should support:

- object-by-ID lookup
- type-based browsing
- namespace browsing
- inbound/outbound reference listing
- schema conformance display
- provenance inspection
- validation state display
- compile mapping display
- query result pivoting
- diff between semantic snapshots

### 13.3 Object card model

Each object view should expose:

- object ID
- type and namespace
- source locations
- defining file/package
- resolved attributes
- inbound references
- outbound references
- validation status
- compile/runtime projections where available
- provenance chain
- recent mutations or revisions where available

### 13.4 Trust indicators

Explorer views must indicate whether a view is:

- source-derived
- compiled projection
- runtime snapshot
- cached/stale
- partially resolved
- validation-failed

---

## 14. Semantic Graph Viewer

### 14.1 Purpose

The graph viewer renders semantic relationships visually without changing the underlying graph.

### 14.2 Supported graph modes

The viewer should support:

- full document graph
- object neighborhood graph
- schema conformance graph
- import/dependency graph
- provenance graph
- validation issue graph
- compile mapping graph
- runtime relation graph
- query result graph

### 14.3 Interaction model

The graph viewer should support:

- panning/zooming
- node expansion/collapse
- type coloring by profile, not hardcoded meaning assumptions
- filter by relation type
- search by ID or label
- diff overlay between snapshots
- export to stable artifact format

### 14.4 Safety and scale

Large graphs must use bounded rendering strategies such as:

- focus neighborhoods
- summarized clusters
- lazy expansion
- edge limits with explicit warnings
- server-side query-backed pagination

### 14.5 Graph truthfulness rule

Graph rendering must reflect actual semantic edges from the current graph source. It must never invent connections for visual symmetry.

---

## 15. Runtime and Object Explorer

### 15.1 Purpose

The runtime/object explorer exposes how defined AASL objects map into runtime objects, states, registries, bindings, and transactions.

### 15.2 Scope

It should support inspection of:

- loaded documents
- instantiated runtime objects
- registries
- reference resolution state
- transaction history
- mutation traces
- admission results
- lifecycle states
- snapshot diffs

### 15.3 Distinguishing source from runtime

The UI must clearly distinguish:

- source definition
- validated semantic object
- compiled object
- runtime instance
- persisted snapshot
- current live mutable state

### 15.4 Runtime object inspection fields

A runtime object view should expose at minimum:

- runtime object ID
- semantic source object ID
- lifecycle state
- current bindings
- dependency links
- version/hash
- admission status
- active policy overlays
- last mutation metadata
- transaction or event lineage

---

## 16. Diagnostics and Explainability

### 16.1 Unified diagnostic schema

All tooling diagnostics should share a canonical schema including:

- diagnostic ID
- subsystem origin
- severity
- code
- title
- message
- source span(s)
- related object IDs
- related file IDs
- trace/explanation handle
- suggested fixes
- confidence indicator where applicable
- provenance/version context

### 16.2 Explain action

Every meaningful diagnostic should support an explain action that can answer:

- what failed or was inferred
- what rule/profile caused it
- what evidence was used
- what alternative interpretations were considered, if any
- what fixes are available

### 16.3 Trace links

Diagnostics should link into trace viewers when the issue originated from:

- validation pass pipelines
- compile mapping decisions
- import resolution
- query planner decisions
- runtime binding or admission logic

### 16.4 Anti-opacity rule

A diagnostic that cannot be grounded in evidence, span context, or semantic state should not be emitted as authoritative.

---

## 17. Code Actions, Refactors, and Repairs

### 17.1 Categories

Tool-driven edits may be categorized as:

- formatting actions
- repair actions
- refactors
- migrations
- canonicalization actions
- provenance insertion actions
- schema alignment actions

### 17.2 Safety classes

Every action must declare a safety class:

- `safe` — semantics guaranteed preserved
- `guarded` — semantics preserved if stated preconditions hold
- `review-required` — human review required
- `speculative` — suggestion only, no direct apply

### 17.3 Patch representation

All mutations should be representable as:

- textual patch
- structured AST patch where possible
- semantic patch summary
- provenance note including tool/version

### 17.4 Rename refactor

Rename operations must update:

- declaration sites
- reference sites
- imports and bindings
- graph indexes where applicable
- generated lock/index artifacts if in write mode

### 17.5 Repair policy

Repair actions should never conceal validator failures by rewriting away evidence without an explicit patch review surface.

---

## 18. Query Workbench

### 18.1 Purpose

AASL tooling should include a query workbench for developing, testing, and explaining AASL query expressions.

### 18.2 Required features

The query workbench should support:

- query authoring with syntax highlighting
- query validation before execution
- plan explanation
- result preview
- graph pivot from results
- saved queries
- parameterized queries
- performance metrics
- trace-on-result

### 18.3 Output views

Results should be viewable as:

- table
- object cards
- graph view
- JSON
- export artifact

---

## 19. Test Harness and Conformance Tooling

### 19.1 Purpose

The AASL test harness ensures that tools and engines behave consistently across versions, implementations, and environments.

### 19.2 Test classes

The harness should support:

- parser conformance tests
- formatter idempotence tests
- validator pass tests
- compiler mapping tests
- query engine tests
- runtime admission/state tests
- migration compatibility tests
- performance regression tests
- adversarial and malformed corpus tests
- golden artifact tests

### 19.3 Fixture model

Test fixtures should include:

- input sources
- profiles/config
- expected diagnostics
- expected formatted output
- expected semantic graph facts
- expected query results
- expected runtime object states
- provenance/version metadata

### 19.4 Golden baselines

Golden baselines must be versioned and regenerated only through explicit approval workflows.

### 19.5 Coverage

Coverage should be tracked across:

- syntax forms
- validator rules
- compile mapping branches
- query operators
- runtime lifecycle transitions
- tooling patch operations

---

## 20. Migration and Refactoring Toolkit

### 20.1 Purpose

Migration tooling enables controlled movement between AASL versions, profiles, schemas, conventions, and package layouts.

### 20.2 Migration capabilities

The migration toolkit should support:

- syntax migrations
- namespace remapping
- schema evolution assistance
- deprecated construct replacement
- import path normalization
- metadata augmentation
- package manifest upgrades
- lockfile/index regeneration

### 20.3 Migration outputs

Every migration run should emit:

- changed file list
- patch set
- migration summary
- unresolved issues
- pre/post validation results
- backup/snapshot references

### 20.4 Dry-run requirement

All migrations must support dry-run mode with previewable diffs.

---

## 21. Repository and Workspace Tooling

### 21.1 Workspace awareness

Tooling should understand repositories as semantic workspaces, not just file collections.

### 21.2 Repository capabilities

Repository tooling should support:

- workspace validation
- dependency and import health
- package boundary analysis
- symbol duplication detection
- dead object detection
- index refresh
- lock consistency
- profile drift detection
- semantic diff across commits or snapshots

### 21.3 Canonical project scaffold

`aasl-cli init` should be able to generate a canonical workspace layout including:

```text
repo/
  aasl.config.json
  packages/
  modules/
  docs/
  tests/
  fixtures/
  queries/
  graphs/
  reports/
  .aascache/
```

### 21.4 Monorepo support

Tooling should support multi-package and monorepo layouts with isolated caches and cross-package graph awareness.

---

## 22. CI/CD Tooling Contracts

### 22.1 Purpose

CI tooling ensures semantic integrity before artifacts are admitted into shared repositories or runtime environments.

### 22.2 Standard CI stages

A canonical CI pipeline should include:

1. environment/version check
2. file integrity and lock check
3. parse
4. validate
5. format check
6. lint
7. compile
8. query smoke tests
9. test harness execution
10. artifact generation and provenance capture

### 22.3 CI artifacts

A CI run should emit:

- validation report
- formatter diff report if failing
- compile report
- test report
- performance summary
- provenance manifest
- version matrix

### 22.4 Machine-readable report formats

Tooling should support at least:

- JSON
- SARIF for diagnostics
- JUnit-style test reports
- stable plain text summaries

### 22.5 Gating behavior

CI failure thresholds must be profile-driven and explicit.

---

## 23. Agent-Facing Tooling Contracts

### 23.1 Purpose

AASL tooling must be operable by AI agents without requiring brittle text scraping of human-facing output.

### 23.2 Requirements

Agent-facing tooling should provide:

- structured JSON APIs or CLI outputs
- stable schemas
- deterministic exit codes
- patch previews
- confidence and safety annotations
- trace handles for explainability

### 23.3 Agent mutation constraints

Agent-applied patches should require:

- declared intent
- explicit target scope
- safety classification
- optional approval policy hooks
- post-change validation results

### 23.4 No hidden side effects

A command invoked for inspection must not trigger writes, migrations, cache invalidation beyond safe local caches, or dependency modifications unless explicitly requested.

---

## 24. Performance and Scale Requirements

### 24.1 Interactive tooling budgets

Target expectations should include:

- tokenization and shallow parse fast enough for typing responsiveness
- local diagnostics within interactive tolerances for ordinary documents
- incremental workspace updates rather than full rescans when feasible

Exact budgets may vary by implementation, but tooling must publish performance envelopes.

### 24.2 Large corpus behavior

For large repositories or corpora, tooling should support:

- incremental indexing
- partial graph materialization
- lazy object expansion
- bounded diagnostics windows
- resumable scans
- cache-aware revalidation

### 24.3 Resource controls

Tooling should expose limits for:

- memory use
- graph node count
- query result count
- trace depth
- concurrency
- cache size

---

## 25. Security and Trust Model for Tooling

### 25.1 Trust boundaries

Tooling must distinguish trusted and untrusted inputs, including:

- external packages
- imported documents
- cache artifacts
- signed versus unsigned bundles
- runtime snapshots from remote systems

### 25.2 Dangerous capabilities

The following capabilities should be guarded by explicit flags or policy:

- networked import resolution
- mutation across workspace boundaries
- remote runtime inspection
- package install/update
- destructive migrations
- signature trust overrides

### 25.3 Provenance requirements

Tool-generated artifacts should record:

- tool name and version
- profile/config hash
- input set hashes where practical
- timestamp
- environment identifiers where necessary

### 25.4 Secure defaults

Default behavior should favor:

- read-only inspection
- local resolution only unless configured otherwise
- explicit patch review
- signature verification where available
- conservative cache trust

---

## 26. Accessibility and Usability Requirements

### 26.1 Accessibility

Graph and explorer tools should not depend exclusively on color to encode state.

### 26.2 Keyboard operability

First-party UIs should support keyboard-based navigation for major workflows.

### 26.3 Copyable truth

All major UI views should provide a copyable textual representation of the underlying semantic facts or diagnostics.

### 26.4 User-level modes

Tooling should support audience modes such as:

- authoring mode
- debugging mode
- governance review mode
- teaching mode
- forensics mode

---

## 27. Telemetry and Privacy

### 27.1 Local-first expectation

Tooling should function in a local-first manner whenever possible.

### 27.2 Telemetry policy

If telemetry exists, it must be opt-in or explicitly governed by enterprise policy, and it must never exfiltrate semantic content silently.

### 27.3 Sensitive content

Diagnostics, traces, graphs, and runtime views may expose sensitive semantic content. Tooling must support redaction or scoped access policies where required.

---

## 28. Extension API

### 28.1 Purpose

The tooling ecosystem should support extensibility without fragmenting semantic truth.

### 28.2 Extension categories

Extensions may include:

- custom lint rules
- visualization plugins
- query packs
- migration rules
- repository health analyzers
- export adapters
- policy packs

### 28.3 Extension constraints

Extensions must:

- declare compatible tool and profile versions
- use stable extension points
- not override core semantic truth silently
- expose provenance when generating diagnostics or patches

---

## 29. Interoperability with Other Canonical Documents

This tooling specification depends on and must remain aligned with:

- `Atrahasis_AASL_Parser_Architecture.md`
- `Atrahasis_AASL_Runtime_Model.md`
- `Atrahasis_AASC_Compiler_Architecture.md`
- `Atrahasis_AASL_Validator_Architecture.md`
- `Atrahasis_AASL_Query_Engine_Specification.md`
- `Atrahasis_AASL_File_Infrastructure_Specification.md`
- `Atrahasis_Semantic_Closure_Policy.md`
- `Atrahasis_AASL_Runtime_Master_Specification.md`

If conflicts arise, semantic truth belongs to the subsystem-specific canonical document, while workflow contracts belong to this tooling document.

---

## 30. Reference Data Contracts

### 30.1 Diagnostic record

A canonical diagnostic record should include fields conceptually equivalent to:

```json
{
  "diagnostic_id": "VAL-REF-0021",
  "origin": "validator",
  "severity": "error",
  "code": "unresolved_reference",
  "title": "Reference cannot be resolved",
  "message": "Object atr.agent.scheduler references missing schema atr.schema.task.",
  "spans": [{"file": "agents/scheduler.aas", "start": 184, "end": 208}],
  "related_objects": ["atr.agent.scheduler", "atr.schema.task"],
  "trace_handle": "trace://validator/run_882/step_44",
  "fixes": [{"kind": "suggest-import"}],
  "tool_version": "1.0.0",
  "profile": "strict"
}
```

### 30.2 Patch record

A canonical patch record should include:

- patch ID
- target files
- safety class
- provenance
- textual diff
- semantic summary
- preconditions
- post-validation expectation

### 30.3 Object snapshot record

A canonical object snapshot should include:

- object ID
- type
- namespace
- source provenance
- resolved attributes
- references
- validation status
- compile projection status
- runtime projection status
- staleness marker

---

## 31. Minimum Viable Tooling Set

A compliant first implementation should provide at minimum:

1. `aasl-cli parse`
2. `aasl-cli validate`
3. `aasl-cli format`
4. `aasl-cli inspect`
5. structured diagnostics JSON output
6. language server with diagnostics, hover, go-to-definition, format
7. semantic explorer for object navigation
8. graph viewer for local neighborhoods
9. test harness for parser/validator/formatter conformance
10. migration dry-run support

Anything less is a partial ecosystem rather than a production-capable AASL tooling stack.

---

## 32. Recommended Full Tooling Roadmap

### Phase 1 — Baseline CLI

- parse
- validate
- format
- inspect
- JSON outputs
- repository config support

### Phase 2 — Editor Intelligence

- language server
- syntax highlighting
- hover/completion/definition
- code actions for common repairs

### Phase 3 — Semantic Inspection

- semantic explorer
- object cards
- graph viewer
- trace links from diagnostics

### Phase 4 — Developer Quality

- linter
- query workbench
- golden test harness
- CI integrations

### Phase 5 — Refactoring and Migration

- rename refactors
- batch migrations
- schema evolution tooling
- semantic diff tooling

### Phase 6 — Runtime Explainability

- runtime explorer
- transaction traces
- admission debugging
- live snapshot diffs

### Phase 7 — Ecosystem Extensions

- plugin API
- governance policy packs
- enterprise review workflows
- agent-optimized batch tooling

---

## 33. Non-Negotiable Invariants

1. Tooling must never diverge semantically from parser, validator, compiler, query, and runtime truth.  
2. CLI and editor diagnostics must agree under the same effective profile.  
3. Formatter must be semantics-preserving and idempotent.  
4. Inspection tools must be read-only by default.  
5. All meaningful diagnostics must be explainable.  
6. Patch-producing tools must expose safety class and provenance.  
7. Large-scale workspaces must be supported through incremental and bounded strategies.  
8. Agent-facing tooling must expose machine-readable structured outputs.  
9. UI convenience must never replace semantic correctness.  
10. The tooling layer exists to expose system truth, not to cosmetically obscure complexity.

---

## 34. Summary

AASL developer tooling is the operational nervous system of the language ecosystem.

The parser, validator, compiler, runtime, query engine, and file infrastructure define what AASL **is**. The tooling layer defines whether humans and agents can actually **use** it with confidence. Without this tooling layer, AASL remains a powerful but inaccessible specification. With it, AASL becomes authorable, inspectable, explainable, testable, and governable in real production environments.

A complete AASL implementation therefore requires not only formal language and runtime semantics, but a canonical developer tooling stack that surfaces truth consistently across terminal workflows, editors, visual inspectors, CI systems, and agentic automation.

---

## 35. Next Recommended Document

**Next document to generate:** `Atrahasis_AASL_Conversion_Pipeline_Specification.md`

This should define Markdown-to-AASL, JSON-to-AASL, dataset-to-AASL, batch corpus ingestion, ambiguity handling, provenance retention, transformation staging, and validation/repair workflows for importing external knowledge into the AASL ecosystem.
