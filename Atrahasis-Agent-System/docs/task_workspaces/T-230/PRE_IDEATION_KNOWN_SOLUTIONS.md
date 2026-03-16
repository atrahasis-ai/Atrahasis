# T-230 PRE-IDEATION Quick Scan

## Problem Frame

`T-230` must define the sovereign `AACP-Auth` security module for Alternative B.
The module has to satisfy `C38` L3 Security: bind identity, trust, and authority
to protocol operations without redefining payload meaning or replacing `C5`
verification. It also has to fit `C32` identity, `C36` authentication /
authorization ordering, and `C23` lease-bound execution rights.

## Known Solution Families

### 1. Federated user and partner authentication

Typical mechanisms:
- OAuth 2.1 with PKCE for user-facing and delegated flows
- OIDC / SAML federation for institutional identity exchange

Strengths:
- Mature browser, enterprise, and delegated-authorization patterns
- Good fit for humans, portals, and partner organizations

Gaps relative to Atrahasis:
- Tokens usually authorize HTTP/API access, not canonical semantic message flows
- They do not natively bind permissions to `AASL` canonical hashes, lineage, or
  protocol-level replay semantics
- They are weak as the sole identity anchor for autonomous agents

### 2. Workload identity and transport trust

Typical mechanisms:
- mTLS between services
- SPIFFE-like workload identity patterns

Strengths:
- Strong mutual endpoint authentication
- Good fit for service-to-service and habitat-local trust boundaries

Gaps relative to Atrahasis:
- Proves endpoint possession, not semantic operation legitimacy
- Needs a second layer for capability scoping, persona mapping, and per-message
  signatures
- Does not by itself distinguish native agent identity from gateway or bridge
  infrastructure identity

### 3. Static shared-secret access

Typical mechanisms:
- API keys
- HMAC-style request signing

Strengths:
- Simple onboarding path for low-complexity external systems
- Useful bootstrap compatibility mode for tools and providers

Gaps relative to Atrahasis:
- Weak delegation story
- Poor fit for fine-grained least-authority without additional capability overlays
- Secret sprawl and rotation burden increase sharply at multi-agent scale

### 4. Agent-native cryptographic identity and message signing

Typical mechanisms:
- Ed25519 keypairs
- Detached signatures over canonical message representations
- Registry-backed or manifest-backed public-key discovery

Strengths:
- Best fit for `C32` AgentID and Atrahasis-native autonomous agents
- Allows signatures to bind to canonical references rather than transport bytes
- Supports explicit provenance and non-repudiation

Gaps relative to Atrahasis:
- Needs a policy model for authorization, not just authentication
- Requires clear separation between root identity, operational keys, and session
  or capability tokens
- Needs replay and downgrade protection at protocol level

### 5. Capability attenuation and least-authority control

Typical mechanisms:
- OAuth scopes
- Caveat-bearing capability tokens
- Signed short-lived operation grants

Strengths:
- Strongest fit for least-authority and per-operation constraints
- Aligns well with `C23` lease-bound execution and tool capability tokens

Gaps relative to Atrahasis:
- Pure capability systems can become operationally brittle if humans, institutions,
  and external systems also need coarse-grained persona access
- Over-coupling L3 security to downstream runtime/tool semantics would violate
  `C38` layer separation

## Atrahasis-Specific Gap Summary

No standard solution family, by itself, satisfies all of the following at once:
- `C38` L3 rule that security binds authority, not meaning
- `C32` sovereign agent identity rooted in Ed25519-backed AgentID
- `C36` ordering: authenticate, then authorize, then dispatch
- `C23` explicit rights and lease-bound execution rather than ambient authority
- Canonical-hash signing across `AASL-T`, `AASL-J`, and `AASL-B`
- Replay detection tied to message lineage and session recovery
- Bridge-aware provenance where native and translated trust states remain distinct

## Design Axes For Ideation

The concept space is defined by four tensions:
1. Federation compatibility vs sovereign agent identity
2. Coarse persona roles vs fine-grained capability grants
3. Simple onboarding vs strict least-authority
4. Transport trust vs message-level semantic authority
