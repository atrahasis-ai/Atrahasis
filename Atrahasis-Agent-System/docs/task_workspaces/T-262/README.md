# T-262 Workspace

## Title

AACP SDK Architecture

## Scope

This workspace defines the canonical five-module SDK architecture for native
`AACP` consumers and producers across Python, TypeScript, and Rust.

The task covers:

- stable logical module boundaries,
- `AACPClient` and `AACPServer` surfaces,
- typed message-builder and canonicalization helpers,
- manifest and registry discovery clients,
- `C40` security and replay-handling helpers,
- conformance vector execution and certification-bundle builders,
- generated-SDK overlay rules for downstream `C36` receptor exports.

This task does not redefine:

- transport/session/message semantics already owned by `C38` and `C39`,
- manifest object truth already owned by `C41`,
- tool lifecycle semantics already owned by `C42`,
- or the `T-280` CLI, inspector, and editor-tooling layer.

## Deliverables

1. `SWARM_PROPOSAL.md`
2. `SDK_ARCHITECTURE_SPEC.md`
