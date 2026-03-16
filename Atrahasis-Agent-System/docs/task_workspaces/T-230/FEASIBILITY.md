# C40 Feasibility Report: Dual-Anchor Authority Fabric (DAAF)

**Invention:** C40 - Dual-Anchor Authority Fabric (DAAF)
**Stage:** FEASIBILITY
**Date:** 2026-03-12
**Status:** COMPLETE
**Input Documents:** `docs/task_workspaces/T-230/IDEATION_COUNCIL_OUTPUT.yaml`, `docs/task_workspaces/T-230/PRIOR_ART_REPORT.md`, `docs/task_workspaces/T-230/LANDSCAPE_REPORT.md`, `docs/task_workspaces/T-230/SCIENCE_ASSESSMENT.md`

---

## 1. Refined Concept

DAAF refines `T-230` into four bounded security components:

1. **Dual-anchor trust model**
   - native Atrahasis agents authenticate from `C32` AgentID and Ed25519-rooted
     keys,
   - non-agent actors authenticate from federation, mTLS, or bounded API-key
     anchors.

2. **Bounded security profile set**
   - a small set of negotiable L3 profiles that tell peers which anchor families,
     signing mode, and policy floor apply.

3. **Authority artifacts**
   - an authenticated `AuthorityContext` for role/persona admission,
   - explicit signed `CapabilityGrant` artifacts for sensitive operations.

4. **Canonical authority binding**
   - security-sensitive actions sign canonical message identity plus authority
     context,
   - replay, freshness, and downgrade checks fail closed.

## 2. Why this is feasible

### 2.1 The upstream contracts already exist
- `C38` defines L3 authority boundaries and `CMP-v1`.
- `C32` defines the native agent identity anchor.
- `C36` defines the pipeline ordering for external ingress.
- `C23` defines the no-ambient-rights runtime boundary.

### 2.2 The invention uses known primitives
- Ed25519,
- OAuth 2.1 / OIDC / SAML,
- mTLS,
- API-key admission,
- capability-style grants,
- replay windows and seen-message caches.

### 2.3 The task can stay bounded
DAAF does not need to specify:
- full Agent Manifest schema,
- tool invocation business semantics,
- runtime lease materialization,
- verification verdict logic.

### 2.4 The resulting design directly unblocks the backlog
- `T-214` gains supported auth and manifest-signing posture,
- `T-240` gains authority-binding and grant rules,
- `T-262` gains the `aacp.security` module shape,
- `T-281` gains a conformance target.

## 3. Adversarial analysis summary

### Attack A - Federation becomes the real trust root
- Risk: external IdPs or gateway credentials silently outrank native Atrahasis
  identity.
- Resolution: native agent identity remains rooted in `C32`; federation and mTLS
  are parallel ingress anchors for non-agent actors, not replacements.

### Attack B - Signatures still bind to bytes, not meaning
- Risk: transport-local signatures preserve channel integrity but not semantic
  identity.
- Resolution: security signs the canonical message projection defined by `C38`,
  plus explicit authority context.

### Attack C - Authentication becomes ambient authority
- Risk: once authenticated, a principal can do anything its connection can reach.
- Resolution: separate role/persona admission from short-lived
  operation-scoped capability grants, and pass concrete runtime enforcement to
  `C23`.

### Attack D - API keys and bridges become over-privileged
- Risk: low-trust bootstrap credentials gain native-equivalent authority.
- Resolution: bounded bridge/API-key profile, explicit degraded provenance, and
  hard blocks on native-only and high-trust operations.

## 4. Assessment council

### Advocate
This is the missing security invention that makes Alternative B feel like a
sovereign protocol instead of a transport plan with ad hoc auth bolted on later.

### Skeptic
The design fails if it becomes either:
- a centralized gateway with native identity as a decorative add-on, or
- a full runtime capability language pretending to be an L3 protocol module.

### Arbiter verdict

**Decision: ADVANCE**

| Dimension | Score | Notes |
|---|---|---|
| Novelty | 4.0 / 5 | Strong in the dual-anchor authority split and canonical authority binding |
| Feasibility | 4.0 / 5 | Mature primitives with manageable integration complexity |
| Impact | 5.0 / 5 | Foundational for manifests, tools, SDKs, conformance, and cross-layer integration |
| Risk | 6 / 10 | MEDIUM |

### Required actions for SPECIFICATION

1. Define the bounded security profiles explicitly.
2. Define the trust anchors and allowed anchor combinations.
3. Define authority binding, replay handling, and downgrade refusal.
4. Define capability-grant shape without pre-designing `T-240` or `C23`.
5. State cross-layer ownership boundaries clearly.

---

**Stage Verdict:** ADVANCE to DESIGN
