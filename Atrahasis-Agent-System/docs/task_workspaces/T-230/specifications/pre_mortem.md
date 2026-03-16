# C40 Pre-Mortem

## Failure mode 1 - A gateway quietly becomes the real trust root

Cause:
- federated identity and bridge credentials are treated as superior to or
  equivalent with native `C32` identity.

Mitigation:
- keep native agent trust rooted in MIA,
- treat federation and bridge paths as parallel ingress anchors,
- reject silent equivalence.

## Failure mode 2 - Session signing is under-bound

Cause:
- federated or workload sessions can sign messages without a tight binding to the
  negotiated authority context and expiry window.

Mitigation:
- bind all session-attested signing keys to one authority context and one
  expiration boundary,
- fail closed on context mismatch.

## Failure mode 3 - API keys become ambient admin authority

Cause:
- API keys are accepted for high-trust operations because they are convenient.

Mitigation:
- bound API-key use to the limited bridge/bootstrap profile,
- require stronger anchors and explicit grants for high-consequence actions.

## Failure mode 4 - Capability grants eat downstream task scope

Cause:
- `T-230` tries to fully define every future tool/resource/prompt authorization
  shape.

Mitigation:
- define only the generic grant envelope now,
- let downstream tasks refine target selectors and operation semantics.
