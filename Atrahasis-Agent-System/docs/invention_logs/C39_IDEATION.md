# C39 IDEATION - Lineage-Bearing Capability Message Lattice (LCML)

**Invention:** C39 - Lineage-Bearing Capability Message Lattice (LCML)
**Parent Task:** T-211
**Stage:** IDEATION
**Date:** 2026-03-12
**Status:** COMPLETE

---

## Problem statement

Alternative B needs 19 new message classes for discovery, tools, resources, prompting, streaming, and sampling, but the repo lacks a canonical message-layer design explaining how those additions fit the current 23-class baseline without class sprawl, hidden transport leakage, or semantic-scope overreach.

## Concepts considered

### IC-1 - Universal Verb Envelope
- Strength: minimal visible class count.
- Weakness: shifts too much meaning into payload conventions.

### IC-2 - Lineage-Bearing Capability Message Lattice (LCML)
- Strength: explicit family structure, bounded growth, and lineage discipline.
- Weakness: requires a defended normalization of the old baseline.

### IC-3 - Capability Patch Table
- Strength: fastest additive route.
- Weakness: likely exceeds the 42-class target and leaves poor boundaries.

## Selection

**Selected concept: IC-2 - Lineage-Bearing Capability Message Lattice (LCML).**

## Rationale

LCML is the only concept that:
- preserves C38's L4 authority boundary,
- keeps the Alternative B inventory at the required 42 classes,
- gives downstream tasks an explicit message substrate instead of a loose feature list.

## Stage verdict

**ADVANCE to RESEARCH**

Open questions for RESEARCH:
- what normalized 23-class baseline is defensible against the live repo lineage,
- which responses need distinct classes versus dual-phase reuse,
- how push should be represented without creating transport-bound duplicate classes.
