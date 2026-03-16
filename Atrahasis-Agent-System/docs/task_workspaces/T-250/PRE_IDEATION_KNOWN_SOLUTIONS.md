# T-250 Pre-Ideation Known Solutions Scan

Scope note:
- This is the required shallow scan for ideation preparation, not the later
  deep prior-art stage.
- No external browsing or patent search was performed here. This scan uses the
  Alternative B packet, in-repo canonical specs, and broad known bridge and
  adapter patterns as orientation only.

Problem framing:
- `T-250` must define the generic bridge from `MCP` servers into `AACP`
  endpoints.
- It must translate `MCP` tool listing and tool invocation into `C39` tool
  message classes, respect `C40` trust ceilings, consume `C41` bridge posture
  disclosure, and avoid pretending that bridged outputs are native `C42`
  tool-authority artifacts.
- The strategy packet makes two requirements non-optional:
  1. automatic semantic enrichment of bridged results
  2. explicit native-versus-bridge provenance markers

## Obvious known solution families

### 1. Protocol translation gateways

Observed pattern:
- One protocol surface is exposed to clients while another is spoken
  downstream.
- Translation usually maps methods, fields, and status codes, then forwards the
  result.

Why it matters:
- This is the direct baseline for an `MCP` to `AACP` bridge.

Where it falls short for `T-250`:
- Generic gateways preserve syntax, not Atrahasis semantic accountability.
- They usually treat translated responses as equivalent to native ones.
- They rarely expose durable bridge posture or provenance-floor information.

### 2. Sidecar wrappers around plugin or tool ecosystems

Observed pattern:
- A wrapper process sits next to an existing tool host and presents a different
  outward API while reusing the original runtime.

Why it matters:
- A universal `MCP` bridge will often behave like a sidecar or facade in front
  of an existing `MCP` server.

Where it falls short for `T-250`:
- Sidecars often rely on deployment-local assumptions or hand-written adapters.
- They usually do not define a canonical discovery snapshot, semantic wrapper
  contract, or trust ceiling.

### 3. Schema-normalizing API adapters

Observed pattern:
- Adapter layers translate heterogeneous schemas into one normalized internal
  contract.

Why it matters:
- `T-250` must convert `MCP` tool descriptors and call payloads into pinned
  `AACP` discovery and invocation bundles.

Where it falls short for `T-250`:
- Schema normalization alone does not say how confidence, evidence, provenance,
  and bridge posture are generated or bounded.
- A naive normalizer can overstate semantic certainty when source metadata is
  weak.

### 4. Envelope enrichers and observability shims

Observed pattern:
- Systems add tracing, metadata, audit identifiers, or structured envelopes to
  calls crossing a boundary.

Why it matters:
- `T-250` must add `CLM + CNF + EVD + PRV` style wrapping around bridged tool
  results and preserve lineage through the translation boundary.

Where it falls short for `T-250`:
- Ordinary observability layers are not semantic accountability systems.
- They often annotate traffic after the fact rather than defining canonical
  translated artifacts with trust limitations.

### 5. Full-fidelity emulation layers

Observed pattern:
- A compatibility layer tries to make an old system appear fully native to the
  new one.

Why it matters:
- The temptation in `T-250` is to make bridged `MCP` servers look exactly like
  native `AACP` tool hosts for convenience.

Where it falls short for `T-250`:
- This violates the Alternative B authority boundary.
- `C40`, `C41`, and `C42` all require bridge posture to remain visible and
  policy-distinguishable from native behavior.
- Full-fidelity emulation risks false provenance, false trust posture, and
  unsound execution priming.

## Design pressures that appear immediately

1. Keep bridge honesty stronger than compatibility convenience.
- The bridge cannot silently promote `MCP` trust into native `AACP` trust.

2. Translate around stable snapshots, not ad hoc live calls.
- `C42` already establishes signed tool inventory snapshots as the native tool
  reuse surface. The bridge needs an equivalent bridged snapshot posture.

3. Enrichment must be bounded and source-aware.
- Bridged outputs should gain semantic wrapping, but the wrapper must preserve
  what was observed from `MCP` versus what the bridge inferred.

4. Zero per-server configuration is a hard design goal.
- If the bridge requires bespoke per-server mapping, the ecosystem migration
  story collapses.

5. Discovery, invocation, and result translation should be separate concerns.
- Tool inventory translation, call translation, and result enrichment should not
  collapse into one opaque adapter step.

6. Bridge outputs must remain useful to downstream native clients.
- `T-260`, `T-262`, `T-281`, and `T-307` will all depend on a coherent bridge
  contract rather than one-off wrapper behavior.

## Pre-ideation conclusion

The strongest invention direction is not a thin compatibility proxy. It is a
snapshot-aware, provenance-explicit bridge architecture that:
- ingests generic `MCP` tool inventories,
- emits bridge-scoped `AACP` discovery and invocation surfaces,
- enriches results into bounded semantic accountability bundles,
- preserves a visible trust/provenance ceiling,
- and gives downstream native `AACP` clients one coherent contract without
  falsely claiming native equivalence.
