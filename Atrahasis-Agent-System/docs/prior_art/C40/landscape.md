# C40 Landscape Analysis - Dual-Anchor Authority Fabric (DAAF)

## Current landscape

### A2A / MCP / conventional API security
- Strong on transport auth and practical ecosystem patterns.
- Weak on canonical semantic signing, native agent identity continuity, and
  protocol-visible bridge honesty.

### Legacy Atrahasis communication lineage
- Strong on semantics-first trust thinking and canonical-hash philosophy.
- Weak on unified sovereign protocol enforcement for mixed-principal security.

### Alternative B as of Wave 3
- `C38` defines L3 boundaries.
- `C39` defines the message inventory.
- `T-230` is now the missing security authority that must stabilize before
  manifests, tool connectivity, SDK design, conformance, and cross-layer
  integration can proceed cleanly.

## Strategic gap

No adopted design in the current repo provides all of the following together:
- sovereign native agent identity rooted in Atrahasis,
- standard federation and workload ingress for non-agent actors,
- message-level authority binding over canonical protocol identity,
- explicit operation-scoped capability grants,
- bounded treatment of bridge and API-key trust.

## Competitive reality

`T-230` does not compete by inventing a new auth primitive. It competes by
making the security story coherent across:
- agents,
- humans,
- services,
- bridges,
- downstream tool and manifest tasks.

## Landscape takeaway

The environment rewards a design that is:
- sovereign enough to keep native trust local,
- compatible enough to admit real-world non-agent actors,
- bounded enough to avoid collapsing into gateway centralization or runtime
  overreach.
