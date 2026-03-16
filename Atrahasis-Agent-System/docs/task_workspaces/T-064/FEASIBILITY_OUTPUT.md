# T-064 Feasibility Assessment: EMA-I v1.1
**Agent:** Adapa | **Date:** 2026-03-12

## Refined Scores

| Dimension | Score | Rationale |
|---|---|---|
| Novelty | 3.5/5 | Individual components (API gateway, RBAC, audit logs) are established. Novel combination: epistemic-native typed receptors via session types, Galois-connection translation, persona projections over epistemic state. Boundary object theory precedent exists but no implementation. |
| Feasibility | 4.0/5 | Session types are mature (20+ years). View materialization is solved. Structured translation path is deterministic. NL path deferred to v2.0. No unsolvable theoretical barriers. Main risk: session type tooling maturity for Rust/TypeScript. |
| Impact | 4.5/5 | Closes the interface gap for the entire Atrahasis stack (14+ specs). Enables C14 governance voting, C18 marketplace operations, C33 incident management, C22 developer tooling. Without this, no human can interact with the system. |
| Risk | 4/10 (MEDIUM) | No fundamental blockers. Risks: scope creep (5 personas × many specs = combinatorial surface), session type tooling gap, NL translation security, MCP gateway competitive convergence. |

## Adversarial Analysis (10 Scenarios)

| # | Attack | Severity | Mitigation |
|---|---|---|---|
| 1 | Semantic confusion: crafted input translates to unintended internal operation | HIGH | Three-stage pipeline: validate→translate→authorize. Translation produces descriptors, not executions. |
| 2 | Persona escalation: impersonate higher-privilege persona | HIGH | Authenticate persona BEFORE translation. MIA AgentID binding. |
| 3 | Evidence chain tampering: modify records after the fact | MEDIUM | Cryptographic hash chaining + periodic PCVM commitments. |
| 4 | Receptor version downgrade: force interaction through old, vulnerable receptor version | MEDIUM | Minimum version enforcement per receptor family. Sunset policy. |
| 5 | Translation oracle: probe translation engine to learn internal state | MEDIUM | Rate limiting per persona. Differential privacy on error messages. |
| 6 | Projection information leak: lower-persona projection leaks higher-persona data | MEDIUM | Non-interference proof required. Tidal epoch binding ensures frozen state. |
| 7 | DoS via slow-path flooding: overwhelm NL translation with volume | MEDIUM | Separate admission control for NL path. Queue depth limits. |
| 8 | Receptor composition chain bomb: deeply nested receptor compositions | LOW | Composition depth limit (configurable, default 3). |
| 9 | Schema injection: malformed C4 ASV objects bypass validation | LOW | JSON Schema validation at receptor entry. C4 conformance test suite. |
| 10 | Stale projection serving: serve outdated projections after state change | LOW | Epoch-boundary refresh guarantee. Projection timestamp in response. |

**Summary:** 0 FATAL, 2 HIGH (both mitigatable), 5 MEDIUM, 3 LOW. No showstoppers.

## Design Changes from Feasibility

1. **NL translation (slow path) deferred to v2.0** — security risk too high for v1.0. All v1.0 interactions are structured/typed.
2. **Receptor composition depth limited** — default max 3 to prevent chain bombs.
3. **Minimum version enforcement** — receptors have mandatory minimum version; old versions sunset.
4. **Separate admission control for NL queue** — when NL path added in v2.0.
5. **Non-interference proof required** — not just tested, but formally proven for the persona lattice.

## Hard Gates

| Gate | Status | Notes |
|---|---|---|
| No unsolvable theoretical barrier | PASS | All findings PARTIALLY_SOUND or SOUND |
| Integrates with existing specs without contradiction | PASS | Consumes C4 ASV, feeds C5 PCVM and C33 OINC |
| Implementable with C22 tech stack (Rust/Python/TypeScript) | PASS | Session types implementable in Rust (session-types crate). TypeScript for SDK. |
| Scope bounded to architectural framework | PASS | Spec defines receptor model, not UI layouts |
