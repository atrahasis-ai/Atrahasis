# T-280 Swarm Proposal

- Task: `T-280`
- Title: `AACP Developer Tooling Suite`
- Agent: `Ninkasi (Codex)`
- Status: `CLAIMED`
- Date: `2026-03-14`

## Governing Inputs

- `T-262` SDK module architecture and public nouns
- `T-261` registry discovery and trust-vector surfaces
- `C38` conformance framework and certification evidence posture
- `C39` message-family inventory and lineage structure
- `C41` manifest fetch and capability disclosure truth
- `C42` continuation, snapshot, and runtime-handoff lifecycle
- `C45` server-framework ergonomics
- `C47` Forge quarantine and promotion lifecycle

## Lead Architect

Define a bounded tooling suite that sits above the canonical SDK and gives
developers practical ways to:

- inspect manifests and registry results,
- negotiate and exercise sessions,
- run vectors and build certification bundles,
- inspect message flows and semantic lineage,
- and operate the Forge lifecycle without bypassing policy.

The baseline suite should include:

- one general CLI,
- one inspection surface,
- one Forge-management CLI,
- and one editor-integration surface.

## Visionary

Do not stop at command wrappers. Build an observability and reasoning cockpit for
the sovereign protocol stack.

The tooling should let a developer:

- see message lineage, semantic payload identity, membrane posture, and trust
  overlays in one graph,
- move from registry search to manifest inspection to live session capture
  without changing tools,
- inspect vector outcomes and certification scope visually,
- and manage quarantine and promotion evidence for Forge outputs as a first-class
  developer workflow.

That turns `T-280` into the native ecosystem workbench rather than a grab bag of
helper scripts.

## Systems Thinker

The suite should be organized as four products over one shared artifact plane:

1. `aacp-cli`
   General command-line orchestration for discovery, runtime probing,
   conformance, and capture export.

2. `AACP Inspector`
   Interactive local inspection surface for manifests, trust posture, packet and
   session timelines, semantic flow graphs, and certification evidence.

3. `forgectl`
   Dedicated Forge-management CLI for locus and model lifecycle, quarantine,
   promotion requests, and audit export.

4. `AACP Language Server + Editor Pack`
   Editor diagnostics, completions, code actions, and live semantic-flow
   previews for manifests, message bundles, and project wiring.

Shared artifact plane:

- `FlowCaptureBundle`
- `SemanticFlowGraph`
- `VectorWorkspace`
- `ForgeOperationRecord`

No new prerequisite task is required. `T-280` can consume `T-262`, `T-261`,
`C38`, and `C47` directly.

## Critic

Non-negotiable constraints:

- tooling must not invent a second protocol dialect or trust model,
- inspector and editor views must be projections from canonical artifacts rather
  than speculative reinterpretations,
- CLI convenience must not bypass `C40`, `C45`, or `C47` policy gates,
- Forge tooling must not hide quarantine state or promotion evidence,
- semantic visualization must preserve membrane and trust warnings instead of
  flattening them into pretty but misleading graphs.

## Final Proposal

Write `T-280` as a direct specification for a four-product tooling suite over
the canonical SDK and artifact plane:

- `aacp-cli`
- `AACP Inspector`
- `forgectl`
- `AACP Language Server + Editor Pack`

with one shared set of capture, graph, vector-workspace, and Forge-operation
artifacts so every surface can move between command-line, visual inspection, and
editor workflows without inventing incompatible metadata.
