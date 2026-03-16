# T-280 Direct Specification Draft

## Title

AACP Developer Tooling Suite

## Task

Specify the canonical developer tooling suite for native `AACP`, including
`aacp-cli`, `AACP Inspector`, Forge-management CLI, and editor or tooling
support for message flows and semantic visualization.

This task defines:

- the product boundaries of the tooling suite,
- the shared artifact formats used across CLI, inspector, Forge, and editor
  workflows,
- command and interaction surfaces for protocol, registry, conformance, and
  Forge operations,
- semantic-visualization and developer-diagnostic rules above the canonical SDK.

This task does not redefine:

- `T-262` SDK module authority,
- `T-261` registry authority,
- `C38` conformance truth,
- `C39` message semantics,
- `C40` trust semantics,
- `C45` runtime execution authority,
- or `C47` Forge quarantine and promotion rules.

## Governing Context

- `T-262` already defines the canonical five-module SDK architecture and leaves
  CLI, inspector, and editor tooling to this task.
- `T-261` already defines the registry query, trust-vector, and
  usage-documentation shapes that tooling must consume directly.
- The `C38` conformance framework explicitly requires `T-280` to build CLI and
  inspector affordances around the vector corpus and interoperability matrix.
- `C39` defines the message classes and lineage fields that semantic
  visualization must display rather than reinterpret.
- `C41` defines manifest capability truth and discovery posture.
- `C42` defines snapshot, continuation, and runtime-handoff lifecycles that the
  tooling must visualize and debug.
- `C45` defines the server-side runtime posture that CLI and inspector surfaces
  may interrogate but not replace.
- `C47` defines the locus/model Forge lifecycle that the Forge-management CLI
  must expose faithfully.

## 1. Design Goal

`T-280` establishes one coherent tooling suite above the canonical SDK:

1. `aacp-cli`
2. `AACP Inspector`
3. `forgectl`
4. `AACP Language Server + Editor Pack`

These are separate products, but they are not separate truth systems. They all
consume one shared artifact plane so developers can move from command-line
automation to visual inspection to editor diagnostics without losing semantic,
trust, or conformance fidelity.

## 2. Design Principles

1. **SDK-first, not side-channel-first**
   Tooling must consume the `T-262` SDK and admitted artifacts rather than
   inventing ad hoc protocol clients.

2. **Readable but truthful**
   Visualization and UX may simplify navigation, but they must preserve
   membrane, trust, quarantine, and conformance warnings.

3. **Local-first developer workflow**
   All tools should operate against local artifact captures as well as live
   endpoints so debugging and review do not depend on persistent online access.

4. **One artifact, many views**
   Captures, semantic graphs, vector workspaces, and Forge operations must have
   stable machine-readable formats shared across the suite.

5. **Policy-visible operations**
   Convenience commands must surface profile floors, trust posture, quarantine
   state, and certification scope rather than hiding them.

6. **No bypass tooling**
   Tooling may orchestrate, inspect, and request. It may not create a privileged
   shortcut around `C40`, `C45`, `C47`, or downstream governance surfaces.

## 3. Suite Topology

The tooling suite is composed of four products over one shared artifact plane.

| Product | Primary role | Primary upstream dependencies |
|---|---|---|
| `aacp-cli` | command-line control plane for discovery, runtime probing, conformance, and artifact export | `T-262`, `T-261`, `C38`, `C41`, `C42` |
| `AACP Inspector` | interactive inspection of manifests, trust vectors, message flows, semantic lineage, and certification evidence | `T-262`, `T-261`, `C38`, `C39`, `C41`, `C42` |
| `forgectl` | Forge lifecycle control and audit surface for locus and model operations | `T-262`, `C47`, `C41`, `C45` |
| `AACP Language Server + Editor Pack` | authoring, diagnostics, completions, graph previews, and code actions in editors | `T-262`, `C39`, `C41`, `T-261` |
| Shared artifact plane | stable machine-readable artifacts used by all four products | all of the above |

### 3.1 Why separate products

The suite is intentionally split because the workflows differ:

- `aacp-cli` is automation-first,
- `AACP Inspector` is analysis-first,
- `forgectl` is lifecycle-operations-first,
- editor tooling is authoring-first.

The split is acceptable only because all four consume the same canonical
artifacts and SDK surfaces.

## 4. Shared Artifact Plane

### 4.1 `FlowCaptureBundle`

`FlowCaptureBundle` is the canonical captured-session artifact used by the CLI,
Inspector, and editor previews.

```text
FlowCaptureBundle := {
  capture_id,
  captured_at,
  subject_ref?,
  manifest_snapshot_ref?,
  registry_subject_ref?,
  negotiated_session_ref?,
  authority_context_ref?,
  message_refs[],
  packet_trace_refs[],
  continuation_context_refs[],
  runtime_handoff_refs[],
  warnings[],
  source_tool
}
```

Semantics:

- `message_refs[]` preserve canonical message identity and lineage.
- `packet_trace_refs[]` may record binding-local traces, but those are adjuncts
  to canonical message identity rather than replacements for it.
- `source_tool` records whether the bundle came from `aacp-cli`, Inspector, or
  editor tooling.

### 4.2 `SemanticFlowGraph`

`SemanticFlowGraph` is the normalized graph view used for semantic
visualization.

```text
SemanticFlowGraph := {
  graph_id,
  source_capture_id,
  node_set[],
  edge_set[],
  membrane_annotations[],
  trust_annotations[],
  continuation_annotations[],
  validation_warnings[]
}
```

The graph must preserve at least four overlays:

- message lineage,
- semantic payload identity,
- membrane class,
- trust or provenance warnings.

### 4.3 `VectorWorkspace`

`VectorWorkspace` is the canonical interoperability and conformance work artifact.

```text
VectorWorkspace := {
  workspace_id,
  target_matrix[],
  selected_suites[],
  selected_vectors[],
  result_refs[],
  manifest_snapshot_ref?,
  certification_bundle_ref?,
  created_by
}
```

This artifact lets `aacp-cli`, Inspector, and future automation exchange vector
results without inventing separate formats.

### 4.4 `ForgeOperationRecord`

`ForgeOperationRecord` is the canonical local view over Forge lifecycle events.

```text
ForgeOperationRecord := {
  operation_id,
  lane,
  subject_ref?,
  artifact_hash,
  lifecycle_state,
  quarantine_state?,
  promotion_scope?,
  manifest_ref?,
  evidence_refs[],
  created_at,
  updated_at
}
```

It is a tooling projection, not a second Forge authority ledger.

## 5. `aacp-cli`

`aacp-cli` is the general developer and automation control plane for native
`AACP`.

### 5.1 Command families

| Command family | Purpose |
|---|---|
| `manifest` | fetch, validate, diff, and summarize `C41` manifests |
| `registry` | search subjects, inspect trust vectors, fetch usage docs, and resolve tool matches |
| `session` | negotiate, inspect, resume, and close sessions against live endpoints |
| `message` | build, lint, encode, decode, send, and capture canonical messages |
| `tool` | discover tools, pin snapshots, invoke tools, and inspect continuations |
| `vector` | run conformance vectors and interoperability matrices |
| `cert` | build, verify, and inspect certification evidence bundles |
| `capture` | record, import, export, summarize, and diff `FlowCaptureBundle` artifacts |
| `project` | initialize local tooling metadata, vector workspaces, and editor settings |

### 5.2 Behavioral rules

- `aacp-cli` must use `T-262` SDK imports rather than bespoke wire clients.
- `manifest` and `registry` commands must surface trust conflicts and profile
  mismatches as explicit failures or warnings.
- `message` commands may emit binding-local packets for diagnostics, but the
  canonical message identity remains primary.
- `vector` and `cert` commands must reuse the `C38` vector and
  certification-bundle shapes.
- capture export must emit `FlowCaptureBundle`, not an unstructured text log.

### 5.3 Representative commands

Examples of required affordances:

- `aacp manifest fetch <subject-or-url>`
- `aacp registry search --native-only --type TL --tool-tag filesystem`
- `aacp session negotiate <subject>`
- `aacp message build tool_invocation --schema tl.fs.read`
- `aacp vector run --tier C2 --target local-server`
- `aacp cert bundle create --workspace ws-001`
- `aacp capture export --session s-001`

The exact flag syntax is not normative; the command-family coverage is.

## 6. `AACP Inspector`

`AACP Inspector` is the interactive analysis surface for local and live
artifacts.

### 6.1 Required panes

| Pane | Purpose |
|---|---|
| Manifest and trust pane | inspect manifest sections, trust posture, registry agreement, lifecycle, and trust-vector factors |
| Session timeline pane | inspect handshake, resume, heartbeat, message ordering, and transport-local traces |
| Semantic flow pane | visualize message lineage, semantic payload identity, membrane overlays, and trust annotations |
| Vector and certification pane | inspect suite coverage, pass/fail results, interoperability matrix cells, and certification scope |
| Forge and quarantine pane | inspect Forge-derived subject state, quarantine evidence, promotion scope, and manifest lineage |

### 6.2 Input sources

The Inspector must accept:

- local `FlowCaptureBundle`,
- local `VectorWorkspace`,
- local `ForgeOperationRecord`,
- manifest snapshots,
- registry results,
- live endpoint sessions through the canonical SDK.

### 6.3 Visualization rules

- Graphs must show membrane boundaries clearly.
- Quarantine or trust warnings must be visually attached to the relevant nodes,
  edges, or panes.
- Inspector views must be exportable back into the shared artifact plane rather
  than becoming screenshot-only dead ends.
- Binding-local traces may be shown, but they must remain secondary to canonical
  message identity and semantic lineage.

## 7. `forgectl`

`forgectl` is the dedicated Forge-management CLI for `C47`.

### 7.1 Command families

| Command family | Purpose |
|---|---|
| `locus` | inspect or submit locus-conversion jobs and manifests |
| `model` | inspect model-intake, license, provenance, and adaptation state |
| `quarantine` | inspect quarantine status, evidence, and blocked promotions |
| `promotion` | request or inspect membrane-scoped promotion decisions |
| `artifact` | inspect hashed intake artifacts and generated outputs |
| `evidence` | export quarantine, conformance, and promotion evidence bundles |

### 7.2 Hard boundaries

`forgectl` may:

- submit requests,
- inspect status,
- package evidence,
- and prepare promotion requests.

`forgectl` may not:

- bypass license or provenance gates,
- suppress quarantine state,
- promote a Forge output directly into Sanctum,
- or impersonate runtime or governance authority.

### 7.3 Representative commands

- `forgectl locus submit <repo>`
- `forgectl model intake <artifact>`
- `forgectl quarantine status <operation-id>`
- `forgectl promotion request <subject> --scope ENTERPRISE`
- `forgectl evidence export <operation-id>`

## 8. `AACP Language Server + Editor Pack`

The editor surface is the authoring and diagnosis layer for manifests, message
bundles, capture metadata, and local project wiring.

### 8.1 Core components

| Component | Purpose |
|---|---|
| `aacp-language-server` | diagnostics, hover, completion, definition, and code actions |
| schema and ontology packs | local validation packs for manifests, message bundles, and tooling artifacts |
| flow-preview extension | render `SemanticFlowGraph` previews and trust overlays inside the editor |
| project integration adapter | map local workspaces to CLI, Inspector, and vector artifacts |

### 8.2 Required capabilities

- validate manifests, message bundles, and shared tooling artifacts,
- autocomplete `C39` message classes and common builder fields,
- show hover help for trust profiles, manifest sections, and lineage fields,
- render local semantic-flow previews using the shared graph model,
- offer code actions that generate builder stubs or update references from
  canonical SDK nouns,
- surface trust, lifecycle, or conformance warnings inline.

### 8.3 Non-goals

The editor pack must not:

- become a second runtime client,
- emit non-canonical manifests or message payloads silently,
- or hide trust or conformance errors behind weak lint severity.

## 9. Cross-Tool Workflow Contracts

### 9.1 Local development loop

1. Editor tooling validates and previews local manifests or flow artifacts.
2. `aacp-cli` negotiates sessions, captures flows, or runs vectors.
3. Inspector opens the resulting captures and vector workspaces.
4. Certification bundles or Forge evidence exports return to the CLI or Inspector
   for packaging and review.

### 9.2 Registry and manifest workflow

1. `aacp-cli registry search` or Inspector search queries use `T-261` directly.
2. The selected subject opens in Inspector or editor preview through
   `ManifestView`.
3. Any capture or certification workspace binds back to the exact manifest
   snapshot under test.

### 9.3 Forge workflow

1. `forgectl` submits or inspects a Forge operation.
2. Quarantine and promotion state are recorded as `ForgeOperationRecord`.
3. Inspector opens the record and related conformance evidence.
4. Exported evidence flows back through CLI or archive workflows without
   inventing a second evidence structure.

## 10. Packaging and Deployment Model

The tooling suite may be delivered as separate installables, but it must follow
one packaging discipline:

- `aacp-cli` and `forgectl` are command-line distributions,
- `AACP Inspector` is a local-first inspection surface,
- the editor pack is a language-server-backed extension set,
- all products must consume the canonical SDK and shared artifact plane.

Optional read-only HTTP mirrors from `T-261` may be used as convenience inputs,
but the authoritative semantics remain those already defined by the registry,
manifest, SDK, and conformance specs.

## 11. Formal Requirements

| ID | Requirement | Priority |
|---|---|---|
| TOOL-R01 | The tooling suite MUST expose four first-class products: `aacp-cli`, `AACP Inspector`, `forgectl`, and `AACP Language Server + Editor Pack` | P0 |
| TOOL-R02 | All tooling products MUST consume the canonical `T-262` SDK modules rather than implementing a conflicting protocol stack | P0 |
| TOOL-R03 | The suite MUST use stable shared artifact formats for flow capture, semantic graphs, vector workspaces, and Forge operations | P0 |
| TOOL-R04 | `aacp-cli` MUST provide command families for manifest, registry, session, message, tool, vector, certification, capture, and project workflows | P0 |
| TOOL-R05 | `AACP Inspector` MUST provide manifest-trust, session timeline, semantic flow, vector-certification, and Forge-quarantine panes | P0 |
| TOOL-R06 | `forgectl` MUST expose Forge locus, model, quarantine, promotion, artifact, and evidence command families without bypassing `C47` gates | P0 |
| TOOL-R07 | The editor pack MUST provide diagnostics, completions, hover help, code actions, and semantic-flow preview for canonical artifacts | P0 |
| TOOL-R08 | Tooling visualizations MUST preserve membrane, trust, quarantine, and conformance warnings rather than flattening them away | P0 |
| TOOL-R09 | Registry and manifest tooling MUST consume `T-261` and `C41` surfaces directly and MUST NOT invent alternate trust-vector or manifest truth models | P0 |
| TOOL-R10 | Vector and certification tooling MUST consume the `C38` corpus, interoperability matrix, and certification-bundle posture without inventing a second certification dialect | P0 |
| TOOL-R11 | `FlowCaptureBundle` exports MUST preserve canonical message identity and lineage even when binding-local packet traces are included | P1 |
| TOOL-R12 | `SemanticFlowGraph` views MUST expose message lineage, semantic payload identity, membrane overlays, and trust annotations as separate inspectable layers | P1 |
| TOOL-R13 | `forgectl` MUST surface quarantine and promotion evidence explicitly for Forge-derived subjects and MUST NOT present hidden or implied promotion state | P0 |
| TOOL-R14 | Editor and inspector surfaces MUST be able to open locally saved artifacts without requiring live endpoint access | P1 |
| TOOL-R15 | Tooling convenience commands MUST fail closed or emit explicit warnings when trust posture, lifecycle, or conformance scope is unresolved | P0 |
| TOOL-R16 | The tooling suite MUST remain local-first and MUST NOT require public registry mirrors, bridge infrastructure, or external runtime dependencies to function on canonical artifacts | P1 |

## 12. Parameters

| Parameter | Meaning | Initial guidance |
|---|---|---|
| `TOOLING_LOCAL_CAPTURE_DEFAULT` | whether local artifact capture is enabled by default | `true` |
| `TOOLING_SEMANTIC_GRAPH_EXPORT_ALLOWED` | whether graph exports are first-class artifacts | `true` |
| `TOOLING_INSPECTOR_LIVE_ATTACH_ALLOWED` | whether Inspector may attach to live sessions through the canonical SDK | `true` |
| `TOOLING_EDITOR_FLOW_PREVIEW_ENABLED` | whether editor flow preview is a first-wave feature | `true` |
| `TOOLING_FORGE_PROMOTION_REQUEST_ALLOWED` | whether `forgectl` may submit promotion requests | `true` |
| `TOOLING_FORGE_DIRECT_PROMOTION_ALLOWED` | whether tooling may bypass Forge promotion gates | `false` |
| `TOOLING_VECTOR_WORKSPACE_PERSIST_DEFAULT` | whether vector workspaces persist by default | `true` |
| `TOOLING_PACKET_TRACE_EXPORT_ALLOWED` | whether binding-local packet traces may be stored alongside canonical captures | `true` |
| `TOOLING_HTTP_MIRROR_CONVENIENCE_ALLOWED` | whether read-only HTTP mirrors may be consumed as convenience inputs | `true` |

## 13. Downstream Contracts

| Task | `T-280` provides |
|---|---|
| `T-291` | a concrete CLI and Inspector surface for exercising the justification and vector corpus |
| `T-300` | practical developer-facing surfaces that the supersession boundary policy must classify as native-first and compatibility-bounded |
| `T-305` | implementation-planning input for delivery sequencing across CLI, inspector, Forge ops, and editor integrations |
| `T-306` | the canonical developer and operator touchpoints that later interface-retrofit work must preserve |

## 14. Conclusion

`T-280` defines the native AACP tooling suite as a unified workbench rather than
isolated helper tools.

Its key architectural move is simple:

- separate the products by workflow,
- unify them by shared canonical artifacts,
- and keep all of them subordinate to the SDK, registry, conformance, runtime,
  and Forge authorities that already exist.
