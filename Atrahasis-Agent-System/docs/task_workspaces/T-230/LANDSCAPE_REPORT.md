# T-230 Landscape Report

## Current repo landscape

Alternative B now has:
- `C38` as the root five-layer authority,
- `C39` as the bounded message inventory,
- `T-212` as the new AASL type-extension surface,
- `T-213` and `T-215` as the session and canonicalization refinements.

What it still lacks is a concrete L3 security invention. That makes `T-230` the
authority boundary for every downstream task that needs to know what "secure"
means in native AACP.

## Immediate downstream consumers

### Wave 3
- `T-214` needs supported auth schemes, manifest signing posture, and native vs
  federated identity rules.

### Wave 4
- `T-240` needs explicit capability-grant and authority-binding rules for tool
  invocation.
- `T-231` needs a concrete attack surface for replay, downgrade, spoofing, and
  bridge-mediated injection.

### Wave 6
- `T-262` needs the `aacp.security` SDK shape.
- `T-281` needs a conformance target for profile negotiation, signature
  validation, and replay handling.
- `T-290` needs cross-layer contracts into C32, C23, C36, C5, and the rest of
  the stack.

## Existing Atrahasis stack obligations

### C32 MIA
- Must remain the authoritative native agent identity substrate.
- `T-230` can consume MIA anchors but must not replace MIA lifecycle rules.

### C23 SCR
- Must remain the runtime enforcement layer.
- `T-230` can define capability grants and no-ambient-rights expectations, but
  runtime isolation and lease materialization stay with `C23`.

### C36 EMA-I
- Must remain the boundary/integration membrane for human and external-system
  ingress.
- `T-230` must align with its authenticate -> validate -> authorize -> dispatch
  ordering and persona-aware admission flow.

### C5 PCVM
- Must remain verification authority.
- `T-230` may deliver stronger signed provenance and trust context but may not
  issue verification verdicts.

## Landscape risks

1. If `T-230` recenters trust in a conventional gateway or IdP, Alternative B
   loses its sovereign native-agent claim.
2. If `T-230` overdesigns capability semantics, it will pre-empt `T-240` and
   `C23`.
3. If API keys and bridge credentials are treated as equal to native identity,
   downstream trust surfaces will blur.
4. If message-level authority still binds to transport-local bytes rather than
   canonical meaning, the semantic-integrity story collapses.

## Landscape conclusion

`T-230` must be the narrow waist of AACP security:
- wide enough to admit native agents, federated humans, services, and bridges,
- narrow enough to keep semantics, verification, translation, and runtime
  enforcement in their existing owners.
