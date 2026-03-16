# T-230 Prior Art Report

## Scope

Assess the security, identity, and authorization patterns relevant to `T-230`
and determine where a sovereign AACP security invention is genuinely additive.

## Compared baselines

### 1. OAuth 2.1 / OpenID Connect / SAML
- Contribution: mature federation for humans and institutions.
- Limitation: issuer-centric identity and bearer/session semantics do not
  natively bind to canonical semantic message identity.
- Relevance: necessary ingress mechanism for non-agent actors.

### 2. SPIFFE/SPIRE-style workload identity and mTLS
- Contribution: strong service-to-service identity, certificate rotation, and
  transport-bound authentication.
- Limitation: transport identity alone does not explain semantic lineage,
  capability grants, or Atrahasis-native agent continuity.
- Relevance: strong system/workload anchor for provider and infrastructure paths.

### 3. API key systems
- Contribution: simple bounded admission for local tooling, bootstrap, and legacy
  integrations.
- Limitation: weak provenance, weak non-repudiation, poor fit for high-trust or
  long-lived sovereign identity.
- Relevance: useful only as low-trust bounded ingress.

### 4. Ed25519 message signing and content-addressed systems
- Contribution: stable asymmetric signatures, canonical-hash binding, and
  portable authenticity over meaning-bearing payloads.
- Limitation: signatures alone do not decide who is allowed to act.
- Relevance: foundation for canonical message authority in AACP.

### 5. Object-capability systems and attenuable tokens
- Contribution: explicit least-authority, non-ambient rights, time-bounded
  delegation.
- Limitation: pure capability designs often assume the rest of the runtime model
  already exists.
- Relevance: informs operation-scoped grants without forcing a full runtime-first
  redesign in `T-230`.

### 6. Existing AASL security architecture
- Contribution: the seven security layers already exist conceptually:
  integrity, authenticity, provenance trust, transport/exchange, storage
  admission, access/policy, and runtime safety.
- Limitation: those layers were not yet promoted into one sovereign protocol
  security module with explicit profile negotiation and message-level authority
  binding.
- Relevance: direct architectural lineage.

### 7. Existing Atrahasis substrate specs
- `C32` contributes the native agent anchor (`AgentID = SHA-256(Ed25519_pubkey)`).
- `C23` contributes the no-ambient-rights runtime boundary.
- `C36` contributes the authenticate -> validate -> authorize -> dispatch
  ordering discipline.
- `C38` contributes the L3 authority boundary and `CMP-v1` canonical message
  identity.

## What is not novel in T-230

- using OAuth/OIDC/SAML,
- using mTLS,
- using API keys,
- using Ed25519 signatures,
- using capability-style grants,
- using replay windows and seen-message caches.

## What is novel enough to justify the task

The invention is the Atrahasis-specific composition:

1. native agents remain rooted in `C32` sovereign identity rather than a foreign
   IdP,
2. non-agent actors can still enter through federation, mTLS, or bounded API-key
   paths,
3. security-sensitive authority binds to canonical protocol identity instead of
   transport bytes alone,
4. role/persona admission and operation-scoped capability grants stay distinct,
5. the seven historical AASL security layers are promoted into protocol
   enforcement without stealing verification or runtime ownership from `C5` and
   `C23`.

## Prior-art destruction attempt

### Claim: "This is just OAuth plus signatures"
- Rebuttal: OAuth solves non-agent federation, not sovereign native agent
  identity, canonical semantic signing, or bridge-honest capability enforcement.

### Claim: "This is just SPIFFE with extra metadata"
- Rebuttal: workload identity does not preserve Atrahasis-native identity
  continuity, semantic hash binding, or operation-scoped authority artifacts.

### Claim: "This is just capability security"
- Rebuttal: the design is explicitly dual-anchor, not pure capability-first; it
  preserves role admission, federated identity ingress, and bounded downstream
  authority boundaries.

## Conclusion

`T-230` is justified if it stays narrow:
- define the bounded profile set,
- define trust anchors and authority artifacts,
- define canonical signature and replay rules,
- hand runtime/tool/detail surfaces to downstream tasks.

It is not justified if it turns into a complete runtime authorization language or
tries to replace `C5`, `C23`, or `C36`.
