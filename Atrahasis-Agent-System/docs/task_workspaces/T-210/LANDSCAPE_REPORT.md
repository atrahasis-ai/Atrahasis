# T-210 Landscape Report

## Current repo landscape

Alternative B is active, but only two upstream tasks exist today:
- `T-201` completed the type-registry extension policy.
- `T-301` is auditing where the old `ASV + A2A/MCP` assumption still exists across the repo.

That makes `T-210` the root architectural authority for the new communication stack.

## Downstream dependency surfaces

### Wave 2 consumers
- `T-211` needs the message-layer contract and layer ownership.
- `T-212` needs the semantics-layer contract plus the `T-201` governance boundary.
- `T-213` needs the session-layer scope.
- `T-215` needs lineage placement and canonicalization authority.

### Wave 3 consumers
- `T-220` to `T-223` need transport-binding boundaries.
- `T-230` needs the security-layer authority boundary.
- `T-214` needs the architectural place of the agent manifest.

### Wave 4+ consumers
- `T-240` and bridge tasks need the messaging/semantics split to stay precise.
- `T-290` and retrofit tasks need a stable cross-layer integration model.

## Existing Atrahasis stack obligations

### C3 Tidal Noosphere
- Needs routing, scheduling, and parcel/locus coordination to remain above the communication stack.

### C5 PCVM
- Needs the new communication layer to preserve verification-grade provenance, signatures, and message lineage.

### C6 EMA
- Needs semantic payload stability and canonical identity so messages can become durable knowledge artifacts.

### C7 RIF
- Needs message classes and session rules that can carry decomposition and execution coordination.

### C8 DSF
- Needs payment-grade settlement messages and accountable provenance.

### C23 SCR / C24 FHF
- Need the communication layer to work across runtime cells, habitats, and federation edges without external protocol dependence.

### C36 EMA-I / C37 EFF
- Need a stable boundary for external ingress and advisory message publication.

## Architectural risks in the current landscape

1. If T-210 is vague, downstream tasks will improvise missing authority boundaries.
2. If T-210 over-specifies future tasks, it will crowd out the real work assigned to them.
3. If T-210 treats bridges as first-class architecture rather than migration tooling, Alternative B collapses back into dependency.
4. If T-210 lets messaging or transport reinterpret semantic meaning, the semantic-integrity argument fails.

## Landscape conclusion

T-210 must be the narrow waist of Alternative B:
- wide enough to anchor every later task,
- narrow enough to avoid consuming those later tasks.
