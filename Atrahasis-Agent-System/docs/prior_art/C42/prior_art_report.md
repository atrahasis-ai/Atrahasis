# C42 Prior Art Report - Lease-Primed Execution Mesh (LPEM)

Canonical source:
- `docs/task_workspaces/T-240/PRIOR_ART_REPORT.md`

## Summary

The relevant prior art comes from five directions:
- MCP for tool list/call/change baseline,
- JSON-RPC for generic message envelopes,
- gRPC and HTTP/2 for warm high-throughput channel patterns,
- LSP for progressive and partial-result long-lived workflows,
- SPIFFE for short-lived workload identity and rotation.

None of those sources, by themselves or in direct combination, define the full
composition `C42` is targeting:
- native semantic tool identity,
- explicit authority and provenance continuity,
- continuation/execution-ready contexts,
- and no-ambient-rights handoff into a downstream runtime lease model.

## Confidence

Confidence: `4/5`

Reason:
- strong prior art exists for every primitive,
- no direct match appears for the exact Atrahasis composition,
- novelty depends on integration discipline rather than new transport science.
