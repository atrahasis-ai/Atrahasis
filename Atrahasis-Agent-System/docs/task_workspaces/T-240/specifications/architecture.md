# C42 Architecture Notes

## Core architecture statement

LPEM defines the native Alternative B tool fabric as a five-part governed
sequence:

1. discover signed tool inventory state,
2. invoke a specific tool against pinned semantic state,
3. emit an accountable result,
4. optionally mint a bounded continuation or execution-ready context,
5. hand runtime work to `C23` only through an explicit downstream lease path.

## Architectural layers inside the invention

### 1. Discovery snapshot layer
- publishes signed inventory snapshots for `TL{}` surfaces
- enables high-speed reuse without repeated full discovery
- carries expiry and invalidation boundaries

### 2. Authority-bound invocation layer
- pins invocation to tool identity, snapshot identity, and explicit authority
- preserves the cheap immediate path for simple calls
- allows richer priming modes only when requested

### 3. Continuation context layer
- lets a result issue a bounded follow-on context for multi-step or long-running
  work
- keeps that context policy-visible, expiring, and provenance-bound

### 4. Runtime handoff layer
- provides structured handoff data that `C23` can consume when runtime work is
  needed
- does not become a substitute for an actual execution lease

### 5. Accountability layer
- preserves `tool_result` as the distinct accountable artifact
- requires `CLM + CNF + EVD + PRV` wrapping even when continuation or execution
  priming occurs

## Important boundaries

LPEM does:
- define tool inventory reuse,
- define invocation priming levels,
- define continuation contexts,
- define runtime-handoff semantics,
- define native-versus-bridge posture for those contexts.

LPEM does not:
- redefine `C39` message classes,
- redefine `TL{}` fields,
- redefine `C41` manifests,
- redefine `T-243` stream carriage,
- redefine `C23` runtime enforcement internals.

## Result

`T-240` becomes the tool authority for:
- `T-250` native-vs-bridge tool translation posture,
- `T-260` continuation-aware server framework behavior,
- `T-262` client/server context-management SDK design,
- `T-290` integration with runtime, verification, and external boundary layers,
- and a future Atrahasis first-party tool suite built on native `AACP`.
