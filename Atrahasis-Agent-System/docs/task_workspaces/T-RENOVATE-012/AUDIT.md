# T-RENOVATE-012 Audit

## Scope

This audit reviewed the membrane and external-assumption posture across the repo surfaces that actually exist for the `C19-C42` tranche:

- `C19`
- `C20`
- `C21`
- `C22`
- `C23`
- `C24`
- `C31`
- `C32`
- `C33`
- `C34`
- `C35`
- `C36`
- `C38`
- `C39`
- `C40`
- `C41`
- `C42`

The task definition names `C19-C42`, but the current repository does not contain `C25-C30` or `C37`. Those absent surfaces were recorded and excluded from direct audit action.

## Audit Rule

The audit separated two conditions:

1. Stale assumptions that still imply open marketplace dependence, uncontrolled public API exposure, or unresolved protocol-selection authority.
2. Bounded compatibility posture that remains acceptable because it is explicitly subordinate to the native `AACP/AASL` stack and does not grant authority to uncontrolled external systems.

## Findings Summary

### No Patch Required

The following audited surfaces already matched the renovated doctrine closely enough to remain unchanged:

- `C19`
- `C20`
- `C21`
- `C23`
- `C24`
- `C31`
- `C32`
- `C33`
- `C34`
- `C36`
- `C38`
- `C39`
- `C40`
- `C41`
- `C42`

These specifications either already described internal-only membranes and bounded compatibility bridges, or they did not rely on public-marketplace or uncontrolled external-API assumptions in a way that conflicted with the closed-capability doctrine.

### Patched Surfaces

#### C22 Implementation Planning

Stale assumptions found:

- Marketplace and token or reference-rate framing still appeared in implementation-planning sections.
- Historical `MCP` and `A2A` protocol-selection language could be read as still-open architectural authority.
- Generic provider-API abstraction language was broader than the current leased-cognition and native-runtime posture.

Applied fix:

- Added an explicit renovation note near the top of the spec clarifying that historical `ASV`, `A2A`, and `MCP` language is compatibility or reference scaffolding only.
- Replaced open protocol-selection language with native `AACP/AASL` wording plus bounded compatibility harnesses.
- Reframed compute and commercial assumptions around internal compute allocation, Foundry or enterprise revenue routing, and admitted leased-cognition providers with native fallback.

#### C35 Seismographic Sentinel

Stale assumptions found:

- The cluster-membership surface was still described in several places as a public or externally-facing API.

Applied fix:

- Rewrote those references as an authenticated internal service surface for attested downstream consumers.
- Preserved the API contracts, cross-spec integrations, and performance assumptions while removing the implication of uncontrolled public exposure.

## Residual Future Work

- `C22` still contains broader historical `C4 ASV` planning structure. That material is now explicitly non-authoritative where it conflicts with native `AACP/AASL`, but full implementation-plan replacement belongs to the Alternative C retrofit sequence rather than this audit pass.
- `C38-C42` retain compatibility-bridge language that is still acceptable at this stage because it is bounded, subordinate, and no longer described as open protocol authority.
