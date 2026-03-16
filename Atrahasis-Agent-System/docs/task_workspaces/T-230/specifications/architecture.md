# C40 Architecture Notes

## Core architecture statement

DAAF defines the L3 security contract for Alternative B:
- one sovereign native-agent anchor rooted in `C32`,
- one federation/workload ingress family for non-agent actors,
- a bounded set of negotiable security profiles,
- canonical authority binding for security-sensitive messages,
- explicit capability grants for sensitive operations.

## The dual-anchor model

The invention does not force every principal through one auth perimeter.

Instead it separates:
1. **native Atrahasis identity** for agents that are part of the sovereign stack,
2. **external ingress identity** for humans, institutions, systems, bridges, and
   local tools that must still interact with the stack.

Both anchor families enter the same L3 module, but they do not become
interchangeable.

## Canonical authority binding

DAAF makes the security-binding unit:
- canonical message identity from `C38`,
- authenticated authority context,
- optional capability-grant references.

This is the security-side equivalent of refusing to sign opaque transport bytes.

## Result

`T-230` becomes the security authority for:
- `T-214` manifest auth advertisement and signing,
- `T-240` operation-scoped tool authorization,
- `T-262` SDK security module shape,
- `T-281` conformance targets,
- `T-290` cross-layer security integration.
