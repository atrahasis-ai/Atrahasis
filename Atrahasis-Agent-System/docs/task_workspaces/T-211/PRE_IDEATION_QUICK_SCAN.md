# T-211 Pre-Ideation Quick Scan

## Immediate tensions

1. The Alternative B packet names more operational surfaces than fit cleanly into "23 -> 42" if every surface becomes its own new class.
2. `T-211` sits in L4 Messaging, but several candidate surfaces tempt scope bleed into:
   - `T-212` semantic type design,
   - `T-214` Agent Manifest schema design,
   - `T-243` streaming/push transport behavior.
3. Legacy AACP lineage contains more than one draft-era message inventory, so the current "23-class" baseline must be normalized rather than assumed.

## Working hypothesis

The right invention is not "19 more verbs." It is a disciplined message-family lattice that:
- normalizes the current baseline to 23 canonical classes,
- adds exactly 19 new classes,
- uses dual-phase classes where request/response share one semantic contract,
- keeps push as a stream delivery mode instead of spending extra class slots on transport-specific push variants.

## Key guardrails

- Respect C38 layer boundaries.
- Keep lineage mandatory and explicit.
- Do not invent `TL`, `PMT`, `SES`, or Agent Manifest field internals here.
- Keep bridge provenance visible at the message envelope so native and translated flows remain distinguishable.
