# C40 Prior Art Report - Dual-Anchor Authority Fabric (DAAF)

## Scope

This report evaluates prior art relevant to `T-230`: sovereign protocol security,
identity, signature binding, replay defense, and authorization under Alternative B.

## Primary comparison set

1. OAuth 2.1 / OpenID Connect / SAML federation
2. SPIFFE/SPIRE-style workload identity and mTLS
3. API-key admission systems
4. Ed25519 canonical signing and content-addressed trust systems
5. Object-capability and attenuable delegation systems
6. Existing AASL security architecture
7. Existing Atrahasis substrate specs (`C32`, `C23`, `C36`, `C38`)

## Findings

### 1. Federation patterns are valid but not sufficient

OAuth 2.1, OIDC, and SAML are mature for human and institutional identity, but
they do not define native agent identity continuity or canonical message
authority over semantic protocol objects.

### 2. Workload identity solves transport trust, not semantic trust

mTLS and workload certificates provide strong service identity, but transport
identity does not answer:
- who owns native Atrahasis agent continuity,
- how authority binds to canonical message identity,
- how operation-scoped rights are represented.

### 3. API keys are useful only as bounded ingress

API keys remain practical for local tooling, bridges, and bootstrap cases, but
their prior-art profile is weak for non-repudiable high-trust actions.

### 4. Canonical signing is necessary

Ed25519 and content-addressed systems validate the principle that signatures
should bind to canonical identity rather than uncontrolled bytes. This directly
supports the `C38` security goal.

### 5. Capability systems support the least-authority half of the design

Macaroons and object-capability systems show that attenuable rights are practical,
but they do not by themselves solve the mixed-principal world `T-230` must serve.

### 6. The seven-layer AASL security lineage already exists

The old AASL corpus already names seven security layers:
- integrity,
- authenticity,
- provenance trust,
- transport/exchange,
- storage admission,
- access/policy,
- runtime safety.

`C40` promotes that security lineage into protocol enforcement instead of leaving
it as a conceptual note.

## Prior-art conclusion

The component patterns are established. The novelty in `C40` is their bounded
Atrahasis-native synthesis:
- dual-anchor trust model,
- bounded security profiles,
- canonical authority binding,
- explicit capability grants,
- bridge-honest trust posture,
- preservation of `C32`, `C23`, `C36`, and `C5` authority boundaries.

## Confidence

Confidence: `4/5`

Reason:
- strong prior art exists for each primitive,
- no direct match was found for the exact Atrahasis composition,
- novelty is architectural/integrative rather than cryptographically
  foundational.
