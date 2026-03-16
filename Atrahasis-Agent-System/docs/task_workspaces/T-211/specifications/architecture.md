# C39 Architecture Notes

## Core architecture statement

LCML defines the L4 message-layer contract for Alternative B:
- 23 normalized legacy classes remain canonical,
- 19 new classes are added,
- the resulting 42-class inventory is organized by bounded capability families.

## The message lattice

Each new class is positioned by:
1. capability family,
2. interaction mode,
3. lineage rule.

This keeps the expansion explicit without turning every delivery variation into a new class.

## Class economy rule

A new response or notification class is justified only when the reply:
- has materially different downstream semantic consequences,
- needs distinct validation rules,
- or needs distinct retention/provenance treatment.

Otherwise, request and response share one class with `interaction_mode` differentiating direction.

## Count-preservation rule

Push is represented through stream-family delivery modes instead of dedicated push-only message classes. Resource update delivery similarly rides stream or operational status channels rather than adding duplicate update classes.

## Result

`T-211` becomes the message-inventory authority for:
- `T-214` Agent Manifest messaging,
- `T-240` tool messaging,
- `T-241` resource messaging,
- `T-242` prompting/clarification messaging,
- `T-243` stream/push mechanics,
- `T-244` sampling messaging.
