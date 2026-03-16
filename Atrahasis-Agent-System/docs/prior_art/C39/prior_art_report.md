# C39 Prior Art Report - Lineage-Bearing Capability Message Lattice (LCML)

## Scope

This report evaluates prior art relevant to `T-211`: message-taxonomy extension for discovery, tool connectivity, resource access, prompting, streaming, and sampling under Alternative B.

## Primary comparison set

1. Google A2A
2. Anthropic MCP
3. JSON-RPC request/response and notification patterns
4. gRPC unary and streaming RPC families
5. Existing Atrahasis/AASL/AACP lineage documents

## Findings

### 1. A2A proves discovery and long-running work need explicit surface area

A2A separates agent discovery, task lifecycle, and streaming/status behaviors instead of collapsing them into generic opaque payloads. This supports the `T-211` conclusion that discovery and streaming deserve visible message-layer treatment.

### 2. MCP proves tool, resource, prompt, and sampling capabilities are distinct interaction families

MCP's split among tools, resources, prompts, and sampling shows these are operationally different enough to warrant separate contracts. However, MCP does not carry Atrahasis-style lineage, canonical payload identity, or bridge-provenance posture.

### 3. Generic RPC patterns are necessary but not sufficient

JSON-RPC and gRPC show how request/response and notification flows can be modeled compactly, but they do not answer:
- which messages deserve distinct semantic result classes,
- how mandatory lineage survives multi-hop workflows,
- how native and bridge provenance should be exposed at the envelope layer.

### 4. The Atrahasis lineage already values fixed message classes

The original AASL/AACP corpus rejected ad hoc message naming and required fixed `message_class` values, mandatory four-field lineage, and bundle-centered payload contracts. `T-211` extends that discipline rather than inventing message fixity from scratch.

### 5. No direct prior art was found for a family-bounded message lattice tied to governed semantic payloads

The closest systems either:
- provide explicit operation families without deep semantic payload governance, or
- provide semantic payload governance without a unified sovereign message-family design across discovery, tools, resources, prompting, streaming, and sampling.

## Prior-art conclusion

The individual ingredients are established:
- request/response families,
- notifications,
- tool and resource protocol surfaces,
- message headers with identifiers.

The differentiator in `C39` is the composition:
- normalized legacy baseline,
- exactly bounded 19-class extension,
- lineage-bearing family rules,
- class-economy criteria that keep push and some result flows from inflating the inventory,
- envelope-level native-versus-bridge provenance posture.

## Confidence

Confidence: `4/5`

Reason:
- Strong evidence exists for the component patterns.
- No direct match was found for the exact Atrahasis synthesis.
- Novelty remains architectural/integrative rather than based on wholly new transport primitives.
