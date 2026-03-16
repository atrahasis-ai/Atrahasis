# C38 Simplification Review

## Why five layers is the minimum useful split

- Fewer than five collapses session/security or messaging/semantics and reintroduces ambiguity.
- More than five would create bookkeeping layers without strong evidence that they deserve separate lifecycle authority.

## What the spec intentionally does not do

- It does not define the 42 message classes.
- It does not define the new `TL{}`, `PMT{}`, or `SES{}` fields.
- It does not define the exact handshake schema.
- It does not define transport-binding wire formats.
- It does not define bridge internals.

## Simplification verdict

The architecture remains minimal because it specifies only:
- ownership,
- invariants,
- upgrade boundaries,
- integration posture.
