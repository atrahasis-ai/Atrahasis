# C41 Ideation Log

**Invention:** C41 - Layered Semantic Capability Manifest (LSCM)
**Task:** T-214
**Agent:** Inanna (Codex)
**Date:** 2026-03-12

## Selected concept

- Approved concept: `IC-2`
- Approval artifact: `docs/task_workspaces/T-214/HITL_APPROVAL.md`
- User approval text: `IC-2 proceed`

## Concept summary

LSCM defines a signed, endpoint-scoped manifest for Alternative B with bounded
sections for:
- subject identity and trust posture,
- transport and discovery endpoints,
- security profiles and auth schemes,
- supported message families,
- supported `AASL` semantic surfaces and ontology snapshots,
- capability references and manifest supersession.

## Why selected

It preserves the strongest qualities of a discovery manifest without collapsing
runtime telemetry, registry behavior, or downstream protocol internals into the
same document.
