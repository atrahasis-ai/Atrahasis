# T-230 Domain Translator Brief

## 1. Border Control: Passport + Visa + Customs Manifest

Source domain:
- International border processing

Structural parallel:
- Identity proof alone is not enough; the traveler also needs permission for a
  specific purpose and a declaration of what is crossing the boundary.

Design insight:
- Separate three checks:
  1. who are you,
  2. what authority do you have,
  3. what are you trying to bring or do.
- For `T-230`, that argues for distinct identity anchors, authorization grants,
  and message/content handling rules instead of one undifferentiated auth token.

Where the analogy breaks:
- Human border control is slow, discretionary, and often opaque; AACP needs
  machine-verifiable, low-latency, deterministic policy surfaces.

## 2. Container Shipping: Bill of Lading + Tamper Seal

Source domain:
- Maritime logistics and cargo custody

Structural parallel:
- The shipping record describes what should be in transit, while the tamper seal
  attests whether the container changed unexpectedly in transit.

Design insight:
- Separate content meaning from custody/integrity evidence.
- For `T-230`, signatures should bind to canonical references and declared message
  identity, while higher layers retain authority over semantic meaning.

Where the analogy breaks:
- Physical tamper seals say little about the truthfulness of the cargo manifest.
  That mirrors `C38`: L3 can prove authority and integrity, but not substitute for
  `C5` verification.

## 3. Operating Room Safety: Role Credential + Procedure-Specific Time-Out

Source domain:
- Surgical process control

Structural parallel:
- A licensed surgeon still must be authorized for the specific patient, procedure,
  site, and tool set before action proceeds.

Design insight:
- Identity and professional standing are necessary but insufficient.
- High-consequence operations need contextual authorization and explicit
  confirmation of the exact action surface.
- For `T-230`, this supports persona-level access plus operation-scoped capability
  checks, especially before tool use, verification requests, or governance actions.

Where the analogy breaks:
- Human teams can fall back to tacit knowledge and verbal correction. Protocols
  cannot rely on unmodeled social repair.

## 4. Letters of Credit: Trusted Issuer, Narrow Purpose, Expiry

Source domain:
- Trade finance

Structural parallel:
- A trusted issuer creates a bounded promise that is only valid for a named
  counterparty, narrow purpose, and expiry window.

Design insight:
- Capability grants should be attenuable, time-bounded, and verifiable by the
  receiving party without granting general ambient trust.
- For `T-230`, short-lived signed authority artifacts are more aligned with
  sovereign least-authority than broad long-lived bearer tokens alone.

Where the analogy breaks:
- Financial instruments assume discrete transactions. AACP also needs session
  continuity, replay handling, and streaming-safe semantics.

## 5. T-Cell Co-Stimulation: Identity Alone Must Not Trigger Action

Source domain:
- Adaptive immunology

Structural parallel:
- Recognizing a target is not enough for activation; the system requires a second
  co-stimulatory signal to avoid dangerous false activation.

Design insight:
- For `T-230`, authentication should not automatically imply execution authority.
- Sensitive actions should require identity plus an explicit capability or policy
  context before dispatch.
- This is the strongest analogy for keeping L3 fail-closed under incomplete or
  downgraded security posture.

Where the analogy breaks:
- Biology adapts probabilistically and tolerates false positives/negatives. AACP
  needs explicit, inspectable rules with deterministic failure behavior.

## Net Synthesis

The cross-domain pattern is consistent:
- identity is not enough,
- authority must be narrow and contextual,
- integrity evidence must be separate from semantic truth,
- and dangerous actions should require a second bounded authorization signal.

That pattern favors an AACP security design with:
- sovereign agent identity anchors,
- federation-aware external identity ingress,
- operation-scoped capability grants,
- canonical-reference signatures,
- and explicit fail-closed downgrade / replay handling.
