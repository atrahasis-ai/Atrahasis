# T-064 Research Reconciliation
**Agent:** Adapa | **Date:** 2026-03-12

## Assumption Validation

| Ideation Assumption | Research Finding | Status | Design Impact |
|---|---|---|---|
| "Typed receptor" is novel beyond middleware | F1: Only novel IF formalized via session types. Without it, just naming convention. | CONDITIONAL | Must commit to session types as formalism |
| Epistemic translation is feasible | F2: Feasible for structured path. NL path is inherently lossy (Galois connection). | PARTIALLY_VALIDATED | Split fast/slow paths. NL requires confirmation. |
| Complete evidence capture is possible | F3: Complete for mediated interactions. Covert channels are fundamental limit (Lampson 1973). | VALIDATED with caveat | Document coverage boundary. Use causal tracking. |
| Persona projections are consistent | F4: SOUND. View materialization + non-interference. | FULLY_VALIDATED | Bind to tidal epochs. Prove non-interference. |
| The architecture is performant at scale | F5: Fast path OK. NL path is bottleneck (100ms-1s). | PARTIALLY_VALIDATED | Explicit SLOs per path. Async evidence. |
| Membrane is defensible against attack | F6: Semantic confusion and prompt injection are real. | PARTIALLY_VALIDATED | Separate auth→translate→authorize. NL is untrusted. |
| Receptors compose safely | F7: Only for structured path. NL breaks composition. | CONDITIONAL | Restrict composition to fast path. |

## Key Research Findings That Change the Design

### 1. Two-Path Architecture (from F2, F5, F6, F7)
The NL translation path is fundamentally different from the structured path in terms of lossiness, performance, security, and composability. The design MUST formally separate these into two distinct interaction modes, not treat NL as "just another input format."

### 2. Session Types Are Required (from F1)
Without session types, the receptor model collapses to middleware + naming conventions. The spec must commit to session types as the formal receptor language. This is the single biggest design decision.

### 3. Galois Connection for Translation (from F2)
Translation between human-native and epistemic representations is inherently lossy. The spec must model this as a Galois connection, explicitly documenting what is lost in each direction and adding "translation residual" fields to evidence records.

### 4. Constitutional Governance Is Green-Field (from Landscape)
No DAO platform supports tiered constitutions, tribunals, or phased sovereignty. This is a genuine innovation space but also means no existing patterns to follow. Higher design risk.

### 5. MCP Gateway Convergence (from Landscape)
MCP gateways are evolving toward session-aware, context-routing interfaces. EMA-I's receptor model must differentiate from MCP by being epistemic-native (bound to claim classes and Subjective Logic), not just semantically-aware.

### 6. Emerging AI Commerce Protocols (from Landscape)
Mastercard/Visa/OpenAI are entering agentic commerce (2025-2026). EMA-I's marketplace receptor must differentiate by offering PCVM-grade verification, not just authorization verification.

## Revised Concept: EMA-I v1.1

Based on research reconciliation, the concept is refined:

1. **Typed Interaction Receptors** → formalized via session types (Honda et al.). 5 persona families. Versioning via session subtyping.
2. **Epistemic Translation Engine** → split into:
   - **Structured Translation** (fast path): deterministic claim-class mapping, composable, trusted
   - **Interpretive Translation** (slow path): NL/ambiguous input, produces ranked interpretations, untrusted, confirmation-required for high-consequence operations
3. **Interaction Evidence Chain** → causal tracking (not just temporal), cryptographic chaining, periodic PCVM commitments, explicit coverage boundary documentation
4. **Persona Projections** → bound to tidal epochs for consistency, non-interference proven across persona lattice, incremental view maintenance where monotone

### Scope Refinements
- The spec defines the architectural framework, NOT specific UI layouts or form fields
- OpenAPI/GraphQL/gRPC conformance as implementation requirements, not the core model
- Schema-driven SDK generation from receptor registry (absorbing IC-3)
- C22 Wave 3 earliest implementation target (requires C3, C5, C7, C8 operational)

### Removed / Deferred
- NL translation of governance votes: deferred to v2.0 (security risk too high for v1.0)
- Mobile-native receptor family: deferred (Web + CLI + SDK sufficient for initial deployment)
- Real-time streaming projections: deferred (epoch-boundary refresh sufficient)
