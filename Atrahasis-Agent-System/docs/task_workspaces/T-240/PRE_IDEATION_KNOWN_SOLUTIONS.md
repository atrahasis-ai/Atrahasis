# T-240 Pre-Ideation Known Solutions Scan

Scope note:
- This is the required shallow scan for ideation preparation, not the later
  deep prior-art stage.
- Per current AAS HITL rules, no external browsing or patent search was
  performed here. This scan uses the Alternative B packet, in-repo canonical
  specs, and broad known protocol patterns as orientation only.

Problem framing:
- `T-240` must define a sovereign tool-connectivity protocol for `AACP v2`.
- It must replace the useful parts of `MCP` tool workflows while binding tool
  operations to `AASL` typing, `C39` lineage rules, `C40` authorization, and
  automatic accountability wrapping (`CLM + CNF + EVD + PRV`).

## Obvious known solution families

### 1. MCP-style tool catalogs and tool calls

Observed pattern:
- One server exposes a tool list plus a tool-call surface.
- Tool inputs and outputs are usually schema-described, but semantics are mostly
  application-defined and accountability/provenance are thin.

Why it matters:
- This is the direct baseline replacement target named in the Alternative B
  packet.

Where it falls short for `T-240`:
- No native `AASL` object discipline.
- No required canonicalization or ontology-resolution boundary.
- No built-in `C39` lineage model for discovery, invocation, result, and change
  notifications.
- No default requirement that results become explicit semantic accountability
  bundles.

### 2. Schema-first API protocols (`OpenAPI`, `JSON-RPC`, `gRPC`)

Observed pattern:
- Typed request/response contracts, method names, and service catalogs are
  common.
- These systems are good at stable invocation contracts and client generation.

Why it matters:
- `T-240` also needs typed invocation surfaces and durable discoverability.

Where it falls short for `T-240`:
- Tools become generic remote procedures rather than accountable semantic acts.
- Capability policy, provenance, and result verification are not first-class.
- Session, trust, and semantic bundle rules remain external or optional.

### 3. Graph- or query-oriented access models

Observed pattern:
- Rich typed selection and partial responses can be negotiated through one
  schema-centric contract.

Why it matters:
- Tool discovery may need structured filtering and inventory snapshots instead
  of flat name lists.

Where it falls short for `T-240`:
- The model is optimized for data retrieval, not executable tool actions.
- Side effects, policy gates, and execution accountability are not naturally
  expressed.

### 4. Agent framework function-calling registries

Observed pattern:
- Tool registries are often attached to one agent runtime, planner, or vendor
  stack.
- Invocation tends to be conversation-centric and transport-specific.

Why it matters:
- `T-240` must interoperate with agent runtimes and later bridges.

Where it falls short for `T-240`:
- These designs are usually runtime-local, not sovereign protocol standards.
- Tool identity, type resolution, and evidence/provenance wrapping are not
  durable across vendors or transports.

### 5. Capability-scoped execution systems

Observed pattern:
- Some systems require explicit grants or leases before sensitive execution.

Why it matters:
- `C40` already requires explicit grants for tool invocation across trust
  boundaries and forbids ambient authority.

Where it falls short for `T-240`:
- Most known designs do not combine capability discipline with a typed tool
  catalog, semantic result wrapping, and protocol-native lineage.

## Design pressures that appear immediately

1. Keep tool connectivity distinct from manifests and runtime execution.
- `C41` can disclose tool capability surfaces, but it should not absorb the full
  invocation protocol.
- `C23` enforces runtime leases, but `T-240` should not redesign runtime
  execution semantics.

2. Bind invocation to an explicit, resolvable contract.
- `TL{}` identity, version, provider, schema references, and declared permission
  hints already exist in `T-212`; invocation should pin to that surface rather
  than rely on ambient local agreement.

3. Make tool results accountable by default.
- The Alternative B packet explicitly requires automatic semantic wrapping for
  every tool result.
- The minimum wrapper contract must stay bounded enough for real adoption.

4. Support native and bridge cases without conflating them.
- `T-250` will need a generic `MCP` bridge, so the native protocol should expose
  provenance markers and translation posture cleanly instead of treating bridge
  traffic as indistinguishable from native execution.

5. Allow inventory evolution without forcing manifest churn.
- `tool_change_notification` exists as its own `C39` message class, which argues
  for a stable tool-lifecycle surface separate from one static manifest fetch.

## Pre-ideation conclusion

The most credible invention direction is not "tool calling" in the abstract.
It is a sovereign, capability-aware, semantically typed tool protocol that:
- discovers `TL{}` surfaces cleanly,
- invokes them against canonical schemas,
- binds authorization explicitly,
- returns deterministic semantic accountability bundles,
- and can later support bridges and server frameworks without custom per-tool
  glue.
