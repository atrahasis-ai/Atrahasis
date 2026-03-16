# T-210 Pre-Ideation Quick Scan

## Task
Design the root AACP v2 five-layer protocol architecture that replaces the old `C4 ASV + A2A/MCP` end-state assumption with a sovereign Atrahasis-native stack.

## Immediate authorities
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replacement_Strategy.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_Council_Briefing.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_AAS_Tasks.md`
- `docs/task_workspaces/T-201/POLICY_DRAFT.md`
- `docs/specifications/C4/MASTER_TECH_SPEC.md`

## Problem compression

Atrahasis already has:
- a semantic-accountability baseline in `C4 ASV`,
- a settlement, verification, memory, coordination, runtime, federation, and interface stack in `C3/C5/C6/C7/C8/C23/C24/C36/C37`,
- an Alternative B program that explicitly wants protocol sovereignty.

What it does not yet have is the root communication architecture that says:
- what belongs to transport versus session versus security versus messaging versus semantics,
- what can evolve independently,
- where canonical hashes originate,
- where identities bind,
- how bridges fit without becoming the permanent center of gravity,
- how the rest of the Atrahasis stack consumes the new communication layer without ambiguous authority boundaries.

## Known solution families

### 1. Monolithic sovereign super-protocol
- One giant envelope that folds transport, handshake, auth, routing, and semantic payload rules into a single spec body.
- Benefit: fewer explicit boundaries.
- Risk: layer coupling, painful upgrades, hard conformance story, unclear substitution rules.

### 2. Contracted layered stack
- Separate layer responsibilities with explicit upward/downward contracts.
- Benefit: independent upgradeability, testability, and transport substitution.
- Risk: more specification discipline required; bad contracts can create leaks or duplication.

### 3. Compatibility overlay
- Keep A2A/MCP transport assumptions and treat AACP as the semantic overlay plus bridge bundle.
- Benefit: simpler near-term rollout.
- Risk: fails the sovereignty goal and preserves the semantic-integrity break at the old protocol boundary.

### 4. Shared semantic memory bus
- Replace most message transport with shared-state mutation and event observation.
- Benefit: powerful long-term direction for cumulative intelligence.
- Risk: too large a departure from the current Alternative B source packet; not the right first architecture task.

## Hard constraints for T-210

- Must remain compatible with the current Atrahasis stack; this is a new communication substrate, not a rewrite of verification, memory, settlement, or runtime.
- Must honor `T-201`: new semantic types live under governed AASL registry extension, not ambient schema invention.
- Must make bridges migration scaffolding, not normative architectural authority.
- Must preserve the ability to add future bindings and message classes without redoing the entire stack.
- Must not depend on deleting or forgetting `C4`; old materials remain historical baseline and retrofit reference.

## Seven concrete decisions T-210 must settle

1. Layer boundaries and layer ownership.
2. Cross-layer invariants that cannot be violated by future tasks.
3. Version-negotiation and downgrade rules.
4. Where canonical identity and hash authority lives.
5. Where authentication, authorization, and signatures bind.
6. How the messaging layer references semantic payloads without owning their meaning.
7. How the rest of Atrahasis integrates above the communication layer.

## Initial assessment

The right architecture is likely a contracted five-layer stack rather than a monolith or overlay. The hard part is not inventing five layer names; it is defining what each layer is forbidden to do, so downstream tasks cannot fill missing gaps with accidental coupling.
