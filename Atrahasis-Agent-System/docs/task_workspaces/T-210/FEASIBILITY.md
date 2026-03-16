# C38 Feasibility Report: Five-Layer Sovereign Protocol Architecture (FSPA)

**Invention:** C38 - Five-Layer Sovereign Protocol Architecture (FSPA)
**Stage:** FEASIBILITY
**Date:** 2026-03-12
**Status:** COMPLETE
**Input Documents:** `docs/task_workspaces/T-210/IDEATION_COUNCIL_OUTPUT.yaml`, `docs/task_workspaces/T-210/PRIOR_ART_REPORT.md`, `docs/task_workspaces/T-210/LANDSCAPE_REPORT.md`, `docs/task_workspaces/T-210/SCIENCE_ASSESSMENT.md`

---

## 1. Refined Concept

FSPA refines the root Alternative B architecture into five bounded protocol layers:

1. **Transport Layer** - moves framed bytes across HTTP, gRPC, WebSocket, or stdio bindings.
2. **Session Layer** - negotiates capabilities, versions, encodings, liveness, and recovery.
3. **Security Layer** - binds identity, authentication, authorization, signatures, and replay defense.
4. **Messaging Layer** - defines the message envelope, lineage, class taxonomy, and routing semantics.
5. **Semantics Layer** - governs AASL objects, canonicalization, ontology versioning, and payload meaning.

The architectural center is the **semantic integrity chain**:
- Semantics defines canonical meaning.
- Messaging packages that canonical payload into a lineage-bearing envelope.
- Security signs canonical meaning and authorizes its movement.
- Session negotiates which layer capabilities are active for a connection.
- Transport carries opaque frames without semantic authority.

## 2. Why this is feasible

### 2.1 It composes known primitives rather than inventing new science
- layering,
- canonicalization,
- signatures,
- capability negotiation,
- resumable sessions,
- transport bindings.

### 2.2 It matches the existing task program
- `T-210` sets root contracts,
- `T-211` through `T-215` refine message and semantics surfaces,
- `T-220+` refine transport,
- `T-230` refines security,
- later tasks consume the boundaries rather than guessing them.

### 2.3 It preserves current Atrahasis authority boundaries
- C3 still coordinates placement and scheduling.
- C5 still verifies claims.
- C6 still owns knowledge metabolism.
- C7 still orchestrates decomposition.
- C8 still settles.
- C23/C24 still own runtime and federation execution concerns.

## 3. Adversarial analysis summary

### Attack A - Decorative layering
- Risk: the spec names five layers but leaves authority ambiguous.
- Resolution: each layer must include explicit owned responsibilities and explicit forbidden behaviors.

### Attack B - Hashes bind to the wrong thing
- Risk: signatures or canonical hashes bind to transport bytes or encoding artifacts instead of semantic meaning.
- Resolution: canonical authority must originate in the Semantics layer and be carried upward as a stable reference.

### Attack C - Bridges become the real architecture
- Risk: MCP/A2A bridges quietly become the default deployment path and native AACP remains theoretical.
- Resolution: architecture marks bridges as degraded-but-supported migration scaffolding with explicit provenance markers.

### Attack D - Session and security collapse into each other
- Risk: future tasks mix handshake, authentication, authorization, and lifecycle into one uncontrolled surface.
- Resolution: session negotiates and maintains connection state; security proves and constrains authority. They cooperate but do not merge.

## 4. Assessment council

### Advocate
This closes the single most important Alternative B gap: the repo has a program, but not the root architectural authority that every later communication task should inherit.

### Skeptic
The spec is only valid if it stays at architecture level. If it starts writing the detailed contents of `T-211`, `T-212`, `T-213`, or `T-230`, it becomes self-invalidating.

### Arbiter verdict

**Decision: ADVANCE**

| Dimension | Score | Notes |
|---|---|---|
| Novelty | 4.0 / 5 | Novel in the Atrahasis-specific integrity composition and contract model |
| Feasibility | 4.0 / 5 | Uses established primitives with manageable integration complexity |
| Impact | 5.0 / 5 | Root authority for almost the entire Alternative B backlog |
| Risk | 6 / 10 | MEDIUM |

## 5. Required actions for DESIGN / SPECIFICATION

1. Define per-layer ownership and forbidden behaviors.
2. Specify the semantic integrity chain explicitly.
3. Provide upgrade boundaries and downgrade refusal rules.
4. Define bridge status as migration scaffolding only.
5. Keep the architecture above field-level detail that belongs to later tasks.

---

**Stage Verdict:** ADVANCE to DESIGN
