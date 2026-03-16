# T-230 Science and Engineering Assessment

## Verdict

No scientific impossibility is present. `T-230` is a protocol-security
composition problem built from established primitives.

## Sound principles involved

### Canonical-hash signing
- Established and directly compatible with `C38` canonical message identity.
- Appropriate for binding authority to meaning rather than presentation syntax.

### Public-key and federated authentication
- Ed25519, OAuth 2.1, OIDC/SAML, mTLS, and hashed API-key admission are all
  mature engineering patterns.
- Appropriate when principal types differ materially.

### Capability-style authorization
- Time-bounded, attenuable grants are well established.
- Appropriate for avoiding ambient authority in a tool-rich agent system.

### Replay detection with freshness windows
- Seen-message caches and bounded freshness checks are standard.
- Appropriate for AACP because message lineage and session resume already exist.

## Real engineering challenges

1. **Profile sprawl**
   - Too many security profiles would make negotiation and conformance brittle.

2. **Authority confusion**
   - If roles, capability grants, session state, and runtime leases blur
     together, downstream layers will duplicate enforcement.

3. **Bridge equivalence**
   - Migration scaffolding can quietly become trusted-as-native unless bridge
     posture remains explicit and policy-visible.

4. **Key-distribution conflict**
   - Native key registry data and signed manifest data must not disagree silently.

## Feasibility assessment

- Technical feasibility: HIGH
- Integration complexity: MEDIUM-HIGH
- Novelty source: bounded Atrahasis-specific composition, not unknown
  cryptographic primitives

## Recommendation

Advance, with one discipline rule:
- define the minimum bounded security profile set and authority artifacts now,
  and leave downstream object details, tool rights, and runtime materialization
  to their owning tasks.
