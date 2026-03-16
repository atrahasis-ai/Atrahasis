# T-262 Swarm Proposal

- Task: `T-262`
- Title: `AACP SDK Architecture`
- Agent: `Ninkasi (Codex)`
- Status: `CLAIMED`
- Date: `2026-03-14`

## Governing Inputs

- `C38` FSPA plus `T-213` / `T-215` for transport-agnostic protocol and session
  contracts
- `C40` DAAF for security profiles, authority contexts, grants, signatures, and
  replay handling
- `C41` LSCM for manifest fetch, parse, and negotiation surfaces
- `C42` LPEM for tool snapshot caching, continuation invalidation, and runtime
  handoff lifecycle
- `C45` ASCF for language-native server ergonomics
- `T-261` for registry-client and trust-vector response structure
- `C36` EMA-I for generated-SDK posture and membrane-metadata preservation
- `C38` conformance framework for vector execution and certification bundles

## Lead Architect

Define one canonical SDK architecture with stable nouns across Python,
TypeScript, and Rust.

Baseline shape:

- message and canonicalization helpers,
- security helpers for profiles, contexts, grants, signatures, and replay,
- discovery helpers for manifests, registry lookups, and capability negotiation,
- runtime surfaces for `AACPClient` and `AACPServer`,
- and a conformance surface for vector execution.

The SDK must remain native-first, generated-SDK-friendly, and subordinate to the
existing protocol specifications rather than re-inventing them.

## Visionary

Do not ship a thin transport wrapper. Ship a sovereign protocol operating kit.

The SDK should make these first-class:

- deterministic message builders instead of raw JSON hand-assembly,
- manifest and registry negotiation that can choose binding, encoding, and
  security profile coherently,
- reusable continuation and snapshot handles for high-speed tool flows,
- certification and vector-running surfaces that let every language stack prove
  conformance without separate ad hoc tooling.

That turns the SDK from a convenience layer into the default implementation
substrate for native AACP ecosystems.

## Systems Thinker

The exact five-module shape should be:

1. `aacp.protocol`
   Own message builders, canonicalization helpers, codecs, and session tuples.

2. `aacp.security`
   Own `C40` profile objects, authority-context builders, capability-grant
   helpers, signature envelopes, and replay controls.

3. `aacp.discovery`
   Own manifest fetch/parse, capability negotiation, registry search, trust
   vectors, and tool-snapshot caching.

4. `aacp.runtime`
   Own `AACPClient`, `AACPServer`, transport adapters, framework bindings, and
   continuation/runtime-handoff lifecycle glue.

5. `aacp.conformance`
   Own vector execution, interoperability harnesses, certification-bundle
   builders, and certification artifact serialization.

This preserves the five-module constraint while still giving `AACPClient` and
`AACPServer` explicit top-level surfaces inside `aacp.runtime`.

## Critic

Non-negotiable constraints:

- generated endpoint SDKs must not fork protocol or security logic,
- manifest parsing and registry search must fail closed on trust conflict rather
  than papering over bad state,
- runtime convenience must not bypass `C40` or `C23` authority boundaries,
- bridge compatibility helpers must stay outside the default native path,
- conformance tooling must reuse canonical vectors and certification-bundle
  shapes instead of inventing a second test dialect.

## Final Proposal

Write `T-262` as a direct specification for a five-module native AACP SDK stack:

- `aacp.protocol`
- `aacp.security`
- `aacp.discovery`
- `aacp.runtime`
- `aacp.conformance`

with cross-language naming consistency, language-specific packaging rules,
generated-SDK overlays above the core modules, and explicit `AACPClient`,
`AACPServer`, message-builder, registry, manifest, replay, vector-runner, and
certification-bundle surfaces.
