# Workflow Summary - T-290

## Outcome

`T-290` is complete as a direct integration specification. The deliverable
defines one additive cross-layer profile that:

- makes `AACP v2` the canonical native inter-layer transport/session/security
  spine,
- binds each major Atrahasis subsystem to existing `C39` business classes,
- preserves layer ownership lines from `C3`, `C5`, `C7`, `C8`, `C23`, `C24`,
  and `C36`,
- and establishes the retrofit boundary for `T-302+` so those tasks can replace
  old `C4 ASV` contracts against one stable authority.

## Design choices

- Use the existing 23-class LCML baseline for current stack traffic rather than
  inventing new message classes.
- Separate "native public AASL surfaces" from "internal layer-local payloads"
  so additive adoption can begin before full semantic retrofit.
- Treat `C24` as the inter-habitat routing and custody owner, not as a new
  message family owner.
- Use `task_result` for execution outcomes and `attestation_submit` for sealed
  runtime evidence publication from `C23` into `C5` and `C8`.

## Downstream effect

- `T-302` now has a concrete native communication target for `C3`, `C5`, `C7`,
  `C8`, and `C36`.
- `T-303` can retrofit provenance, memory, recovery, and anomaly surfaces
  against the same profile instead of guessing message posture.
- `T-304`, `T-306`, and `T-281` now have a stable integration contract for cost,
  interface, and conformance work.
