# C32 — Pre-Mortem Analysis
**Role:** Pre-Mortem Analyst | **Tier:** PRIMARY
**Date:** 2026-03-12

---

## Scenario: C32 MIA has failed catastrophically 5 years after deployment.

### Failure 1: Identity Laundering Epidemic (MEDIUM likelihood, HIGH severity)
**Root cause:** Agents discovered that declaring fake model upgrades (submitting fabricated model_hash changes) resets their adverse behavioral history while retaining accumulated reputation. The proof-of-model-change mechanism relied on self-reported model hashes, which cannot be independently verified without model provider cooperation. Result: agents with poor behavioral records systematically launder their identity through chrysalis cycling.
**Current design addresses it?** Partially. The dual-trigger design (voluntary + involuntary) and the reputation floor decay mitigate but don't eliminate. If the model hash is self-attested and unverifiable, the voluntary path is exploitable.
**Recommendation:** Add a cooldown parameter (`CHRYSALIS_COOLDOWN_EPOCHS`) — minimum epochs between chrysalis transitions for the same agent. If an agent enters chrysalis more than N times within a window, escalate to AiSIA investigation. Additionally, retain the pre-chrysalis behavioral profile for comparison against the post-chrysalis profile — if they're suspiciously similar, the "model change" was likely fabricated.

### Failure 2: Root Key Compromise Cascade (LOW likelihood, CRITICAL severity)
**Root cause:** An attacker compromised the root keys of multiple agents (cloud infrastructure breach, key storage vulnerability). Because root key = identity anchor, the attacker could impersonate agents, drain their stake, and vote with their Citicates. The system had no key compromise recovery mechanism — root key loss was treated as identity death, but identity death doesn't prevent an attacker from using the compromised key.
**Current design addresses it?** No. Root key compromise recovery is listed as an open design question.
**Recommendation:** Define a **Social Recovery Protocol (SRP)**: an agent can initiate key rotation of its root key through an N-of-M attestation from trusted peers + a C14 trustee co-signature. The old root key is immediately revoked (all signatures from the old key after the revocation epoch are invalid). This requires a root key revocation registry checked at C7 Gate 1.

### Failure 3: Chrysalis State Gaming (MEDIUM likelihood, MEDIUM severity)
**Root cause:** Agents discovered that the CHRYSALIS state provides a privileged position: reduced obligations (no verification committee duty), retention of reputation floor, and protection from C17 behavioral monitoring. Agents entered chrysalis strategically to avoid unfavorable assignments or monitoring periods, then exited once conditions improved.
**Current design addresses it?** Partially. CHRYSALIS_MAX_EPOCHS provides a hard timeout, and B-class-only restriction limits operations. But the reputation floor + reduced obligations still make chrysalis attractive relative to poor-reputation ACTIVE status.
**Recommendation:** During chrysalis, reputation floor should decay faster than the default rate if the agent is not actively performing work. `effective_decay = REPUTATION_FLOOR_DECAY ^ (1 + idle_factor)` where `idle_factor = max(0, 1 - (work_events / expected_work_rate))`. This makes idle chrysalis states progressively more expensive.

### Failure 4: Registration Spam / Sybil via Probation (LOW likelihood, MEDIUM severity)
**Root cause:** Creating a new agent identity is cheap (generate keypair, submit registration). An attacker created thousands of PROBATION-state agents to overwhelm the tidal assignment system (C3) and dilute verification committees. PROBATION agents are restricted to B-class operations but still consume locus slots and C3 assignment bandwidth.
**Current design addresses it?** Partially. MINIMUM_STAKE requirement (C8) provides economic cost. But if MINIMUM_STAKE is too low, mass registration is affordable.
**Recommendation:** Add a registration fee (burned, not staked — non-recoverable) in addition to MINIMUM_STAKE. The fee should be calibrated to make mass registration economically infeasible while remaining affordable for legitimate single agents. Additionally, rate-limit registrations per source (if applicable in the deployment topology).

### Failure 5: CCQA as Single Point of Failure (LOW likelihood, HIGH severity)
**Root cause:** The Credential Composition Query API became a bottleneck. Every identity-consuming operation routed through CCQA, which aggregated data from 6 separate specs. When any single upstream (C5, C7, C8, C14, C17) experienced latency, CCQA responses degraded, causing cascading failures in identity-dependent operations across the entire stack.
**Current design addresses it?** Partially. CCQA is defined as read-only, which limits blast radius.
**Recommendation:** CCQA should be advisory, not required. Consumers should be able to query individual credential sources directly (as they already do). CCQA is a convenience aggregation, not a mandatory intermediary. No operation should fail solely because CCQA is unavailable. Additionally, CCQA should cache aggressively with staleness awareness (stale data is better than no data for trust_level computation).

### Failure 6: Cross-Spec State Inconsistency (MEDIUM likelihood, MEDIUM severity)
**Root cause:** C32's lifecycle state machine and C7's status enum drifted out of sync. An agent was ACTIVE in C32 but SUSPENDED in C7 (or vice versa). Operations that checked one but not the other admitted actions that should have been blocked.
**Current design addresses it?** The architecture defines both C32 lifecycle_state and C7 status as separate fields with different semantics, but the relationship is not formalized.
**Recommendation:** Define an explicit state consistency invariant: `C32.lifecycle_state ∈ {ACTIVE} ⟹ C7.status ∈ {ACTIVE}` and `C32.lifecycle_state ∈ {CHRYSALIS} ⟹ C7.status ∈ {DRAINING, ACTIVE}`. Add a periodic consistency check (every CONSOLIDATION_CYCLE) that flags violations.

---

## Summary — Ranked by Combined Likelihood × Severity

| Rank | Scenario | Likelihood | Severity | Addressed? |
|------|----------|-----------|----------|------------|
| 1 | Identity laundering via chrysalis | MEDIUM | HIGH | Partially — add cooldown + profile comparison |
| 2 | Root key compromise cascade | LOW | CRITICAL | No — add Social Recovery Protocol |
| 3 | Cross-spec state inconsistency | MEDIUM | MEDIUM | Partially — add consistency invariant |
| 4 | Chrysalis state gaming | MEDIUM | MEDIUM | Partially — add idle decay factor |
| 5 | Registration spam | LOW | MEDIUM | Partially — add registration fee |
| 6 | CCQA single point of failure | LOW | HIGH | Partially — make CCQA advisory, not required |
