# C32 — Simplification Review
**Role:** Simplification Agent | **Tier:** OPERATIONAL
**Date:** 2026-03-12

---

## Question: What is the simplest version of C32 that preserves the novel claims?

### Core Novel Claims (must preserve)
1. Metamorphic Re-attestation Protocol (MRP) — identity continuity through agent transformation
2. Identity Continuity Kernel (ICK) — invariant anchor set
3. Canonical AgentID derivation — SHA-256(Ed25519_pubkey)
4. Lifecycle state machine — PROBATION → ACTIVE → CHRYSALIS → ACTIVE → RETIRED
5. Credential Composition Query API — unified identity view

### Components Reviewed

| Component | Essential? | Recommendation |
|-----------|-----------|----------------|
| Identity Anchor Service (IAS) | YES | Core — AgentID derivation and key verification |
| ICK Store | YES | Core — the invariant anchor record |
| Lifecycle State Machine (LSM) | YES | Core — defines metamorphic transitions |
| MRP | YES | Core novel claim #1 |
| Registration Protocol | YES | Fills critical gap — but keep minimal |
| CCQA | YES but SIMPLIFY | Make advisory/optional, not a required intermediary. Consumers can query sources directly. Reduce to a convenience library function, not a service. |
| IPT (Identity Presentation Tokens) | SIMPLIFY | Remove from CausalStamp (hot path). Instead, log IPTs once per epoch as a periodic health check, not per-interaction. This preserves forensic value while eliminating per-operation overhead. |
| Concurrent-Use Detection (CUD) | SIMPLIFY | Leverage existing C7 Gate 1 signature validation. Add a signature nonce cache (simple HashMap) rather than a full CUD subsystem. The detection logic is ~20 lines, not a component. |
| Social Recovery Protocol | DEFER | Pre-Mortem recommends it, but it's complex and addresses a LOW-likelihood scenario. Define the interface (SRP exists as an extension point) but defer the full protocol to a future task. |
| Chrysalis cooldown | ADD | Pre-Mortem's recommendation. Simple parameter: CHRYSALIS_COOLDOWN_EPOCHS. Minimal complexity, addresses HIGH-severity risk. |
| Work Product Chain | SIMPLIFY | Hash chain of epoch summaries is fine, but don't over-specify the summary format. Define it as `SHA-256(previous_summary_hash || epoch || work_product_count || aggregate_credibility)`. Four fields. |

### Simplification Recommendations

1. **CCQA → library function, not service.** Remove the "API" framing. It's a composition function that any consumer can call. No separate deployment, no availability concerns.

2. **IPT → epoch-level, not per-interaction.** Reduces IPT generation from ~1000/epoch to 1/epoch. Still detects undeclared model changes (model_hash comparison across epochs).

3. **CUD → inline at Gate 1.** Not a separate subsystem. A nonce-based duplicate check in C7's existing admission pipeline. ~20 lines of pseudocode.

4. **Social Recovery → extension point only.** Define `SRP_ENABLED = false` parameter and a placeholder interface. Full protocol is a separate task if needed.

5. **Remove `identity_health` composite signal from CCQA.** The `trust_level` composite is useful (it resolves conflicts between credential sources). The `identity_health` metric is vague — it duplicates what individual sources already provide. Cut it.

### Result: Simplified Component Count

| Original | Simplified |
|----------|-----------|
| 7 components (IAS, ICK, LSM, MRP, Registration, CCQA, IPT, CUD) | 4 components (IAS, ICK+LSM, MRP, Registration) + 2 inline features (IPT as epoch check, CUD as Gate 1 extension) + 1 library function (CCQA) |

### What Was NOT Cut
- MRP: cannot be simplified without losing the core claim
- ICK: minimal already (6 fields + references)
- Registration protocol: already minimal (5 steps)
- Lifecycle FSM: 4 states is already minimal for the semantics required
- AgentID derivation: one function, cannot simplify

**Conclusion:** The architecture is already fairly lean for a cross-cutting identity system. The main simplifications are: demoting CCQA from service to function, reducing IPT frequency from per-interaction to per-epoch, and inlining CUD into existing Gate 1 logic.
