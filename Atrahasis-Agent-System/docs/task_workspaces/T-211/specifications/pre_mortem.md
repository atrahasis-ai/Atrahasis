# C39 Pre-Mortem

## Failure mode 1 - Inventory inflation returns immediately

Cause:
- downstream tasks add dedicated classes for every update, acknowledgment, or transport variation.

Mitigation:
- explicit class-economy rules in the spec,
- requirement that inventory growth beyond 42 requires later governance review.

## Failure mode 2 - T-211 pre-designs downstream semantic objects

Cause:
- this task defines `TL`, `PMT`, `SES`, or Agent Manifest field internals.

Mitigation:
- payload contracts use semantic placeholders and bundle obligations only,
- downstream ownership is called out explicitly in the master spec.

## Failure mode 3 - Push becomes transport leakage

Cause:
- message classes are defined in terms of HTTP webhook mechanics or WebSocket-specific behavior.

Mitigation:
- define only messaging-layer response-channel semantics here,
- defer transport realization to `T-243` and binding specs.

## Failure mode 4 - Legacy baseline is contested

Cause:
- old draft-era AACP inventories are treated as equally canonical.

Mitigation:
- document the normalization rule and state which legacy classes remain canonical under the current repo baseline.
