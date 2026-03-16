# T-064 / C36 Assessment Council Transcript
**Agent:** Adapa (734bcdbf) | **Date:** 2026-03-12

---

## Council Composition
- **Advocate (Enshag):** Position — APPROVE
- **Skeptic (Lugalbanda):** Position — ADVANCE with conditions
- **Arbiter (Ninsun):** Position — APPROVE

## Round 1: Advocate (Enshag)

C36 fills the single largest architectural gap in the Atrahasis stack — 14+ specifications define internal behavior but none defines how any external entity interacts with any of it.

### Strengths

1. **Architectural clarity.** Four-component decomposition (Receptors, STE, IEC, PPE) is clean with distinct formal foundations: session types for receptors, Galois connections for translation, hash chains for evidence, non-interference for projections.

2. **Scope discipline.** Defines 35 receptors across 5 families with 3 detailed YAML exemplars. Resists Pre-Mortem Scenario #1 (scope explosion) by delivering receptor *contract* over receptor *catalog*.

3. **v1.0/v2.0 boundary.** NL translation deferred to v2.0 eliminates the largest feasibility risk. Structured-only constraint (REQ-09, REQ-17) keeps translation pipeline deterministic and composable.

4. **Integration density.** 18 inbound + 4 outbound integration points mapped to specific consuming/producing specs with claim class routing. Most integration-dense spec since C9.

5. **Security ordering invariant.** authenticate → validate → translate → authorize → dispatch with explicit "translation never confers authority" rule (REQ-11) is a meaningful security contribution.

## Round 2: Skeptic (Lugalbanda)

### Concerns

1. **Session type implementation risk.** Spec commits to Honda et al. session types (REQ-02, Appendix A), but Rust session type support is limited (unmaintained crate). MTS does not specify how session types will be enforced in the actual tech stack. *Monitoring flag needed.*

2. **Non-interference proof sketch is thin.** Appendix C relies on "authorize filter is a simple set intersection" and caveats cross-epoch authorization changes. Epoch-static mitigation is sound but proof needs strengthening. *Monitoring flag needed.*

3. **Evidence chain write-behind guarantees.** Section 6.6 claims epoch-boundary commitment with crash recovery from dispatch log. Dispatch log itself becomes critical unspecified dependency. *Monitoring flag needed.*

4. **Receptor composition side-effect analysis.** Excluding "receptors with side effects that modify state read by subsequent receptors" requires knowing owning spec internals. Constraint may be unenforceable without cooperation from owning specs. *Monitoring flag needed.*

5. **35 receptors, 3 exemplars.** Correct scope control strategy, but implementation gap is large. 32 unspecified receptors will require significant additional design work.

### Not blocking
- Transport binding coverage (6 transports) is reasonable
- Parameter ranges are sensible with consistent governance assignments
- Wave integration aligns with C22

## Round 3: Arbiter (Ninsun)

### Synthesis

The Advocate correctly identifies a genuine architectural gap. The Skeptic raises valid implementation-facing concerns, but none are spec-level defects:

1. **Session types** — implementation challenge, not specification error. C22 must address runtime enforcement.
2. **Non-interference** — honest caveat with sound epoch-static mitigation. Full proof is research, not spec.
3. **Write-behind** — dispatch log dependency should be monitored; standard distributed systems pattern.
4. **Composition side effects** — valid concern, recommend monitoring via C9 contract tests.
5. **Exemplar coverage** — by design. Receptor contract + 3 exemplars is correct abstraction level.

## Scores

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Novelty | 3.5/5 | Session-typed epistemic receptors + Galois translation with residual capture are novel in domain. Individual components from established theory. |
| Feasibility | 4.0/5 | All components implementable. Session type enforcement in Rust is main risk. NL deferral removes largest uncertainty. |
| Impact | 4.5/5 | Every external interaction depends on this layer. Highest integration density in the stack. |
| Risk | 4/10 MEDIUM | No fatal risks. 1 CRITICAL mitigated (membrane bypass). Session type implementation is primary concern. |

## Monitoring Flags

| ID | Flag | Trigger | Owner |
|----|------|---------|-------|
| MF-1 | Session type enforcement in Rust/TypeScript | W1 cannot achieve compile-time session type checking | C22 Implementation |
| MF-2 | Non-interference proof completeness | Cross-epoch authorization changes violate non-interference | Formal methods review |
| MF-3 | Write-behind evidence durability | Evidence loss between response emit and epoch boundary commit | Operations |
| MF-4 | Receptor composition side-effect detection | Composed chain produces inconsistent results from shared state mutation | C9 Contract Tests |
| MF-5 | Receptor specification coverage | >50% of receptors require significant redesign during implementation | C22 Implementation |

## Operational Conditions

| # | Condition | Gate |
|---|-----------|------|
| 1 | Session type enforcement strategy defined before W1 receptor implementation | W1 entry |
| 2 | Non-interference proof validated against all 5 persona families with concrete examples | W5 entry |
| 3 | Write-behind evidence recovery demonstrated in W1 integration tests | W2 entry |

## Verdict

**APPROVE** — C36 EMA-I is approved with 3 operational conditions and 5 monitoring flags.
