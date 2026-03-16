# C40 IDEATION - Dual-Anchor Authority Fabric (DAAF)

**Invention:** C40 - Dual-Anchor Authority Fabric (DAAF)
**Parent Task:** T-230
**Stage:** IDEATION
**Date:** 2026-03-12
**Status:** COMPLETE

---

## Problem Statement

Alternative B requires a sovereign AACP security module that can authenticate
native agents, humans, institutions, services, and bridge actors without
collapsing all trust into a single foreign identity perimeter. `C38` defines the
L3 boundary, but the repo still lacked a concrete answer for how identity,
authorization, signatures, replay defense, and downgrade refusal should work in
native AACP.

## Concepts Considered

### IC-1 - Federated Security Gateway
- Strength: highest immediate compatibility.
- Weakness: recenters trust in a conventional gateway or IdP surface.

### IC-2 - Dual-Anchor Authority Fabric (DAAF)
- Strength: preserves native agent sovereignty while still admitting standard
  non-agent ingress paths.
- Weakness: requires disciplined profile and grant boundaries.

### IC-3 - Capability-Lease Security Mesh
- Strength: strongest least-authority posture.
- Weakness: over-couples L3 to runtime and tool semantics before downstream tasks
  exist.

## Selection

**Selected concept: IC-2 - Dual-Anchor Authority Fabric (DAAF).**

## Rationale

DAAF is the only concept that:
- keeps native agent identity rooted in Atrahasis,
- admits real-world external identities without pretending they are native,
- binds security-sensitive authority to canonical message identity,
- avoids pre-designing the entire runtime authorization model.

## Stage Verdict

**ADVANCE to RESEARCH**

Open questions for RESEARCH:
- what is the minimum bounded security profile set,
- how should native registry keys and signed manifests relate,
- which operations require explicit capability grants by default,
- how should bridge-limited trust be made visible and non-confusable with native
  authority.
