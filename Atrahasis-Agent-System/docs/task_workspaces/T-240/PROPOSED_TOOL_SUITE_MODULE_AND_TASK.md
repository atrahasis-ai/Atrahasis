# Proposed Atrahasis Tool Suite Module And Task

Purpose:
- define the missing downstream layer for concrete first-party Atrahasis tools
- capture the proposal inside the `T-240` workspace without editing shared
  backlog/state files live

Status:
- proposal only
- not yet added to `docs/TODO.md`
- intended for later serialized closeout or future dispatch planning

## Why this is needed

Current Alternative B work defines:
- what a tool is (`TL{}` via `T-212`)
- how tool messages exist (`C39`)
- how tool authority works (`C40`)
- how manifests disclose capability surfaces (`C41`)
- how the native tool protocol should behave (`T-240`)
- how native tool servers should be exposed (`T-260`)

What is still missing is a module dedicated to the actual Atrahasis-built tool
library: the concrete first-party tools that agents will use for search,
verification, retrieval, transformation, governance, external interaction, and
cross-layer system operations.

That layer should not be overloaded into `T-240`. `T-240` defines the protocol.
The missing module defines the actual tool suite that rides on that protocol.

## Proposed module

Module name:
- `Atrahasis First-Party Tool Suite`

Module role:
- the canonical first-party library of native `AACP` tools authored and
  maintained by Atrahasis
- built on top of the `T-240` tool protocol and the `T-260` native server
  framework

Module boundaries:
- IN SCOPE:
  - first-party tool families and package boundaries
  - canonical tool descriptors and packaging strategy
  - tool trust/provenance expectations
  - capability profiles for high-consequence tools
  - cross-layer tool families that expose Atrahasis-native system functions
  - release and conformance expectations for official tools
- OUT OF SCOPE:
  - redefining the `AACP` tool protocol (`T-240`)
  - redefining the native server framework (`T-260`)
  - bridge semantics for non-native tool servers (`T-250`)
  - public registry format (`T-261`)
  - SDK core architecture (`T-262`)

Primary module objectives:
1. Define the official Atrahasis tool families.
2. Standardize how first-party tools expose schemas, permissions, and result
   accountability.
3. Identify which tools are core platform tools versus optional packs.
4. Define how first-party tools map into existing Atrahasis layers such as
   `C5`, `C23`, `C24`, `C36`, and later retrofit work.
5. Create a path from protocol design to concrete usable tool inventory.

## Proposed tool families

Core platform packs:
- `Knowledge and Retrieval Pack`
  - search, retrieval, corpus query, document fetch, ontology lookup
- `Verification and Evidence Pack`
  - evidence assembly, provenance inspection, verification request helpers,
    trust-boundary inspection
- `Transformation and Extraction Pack`
  - parsing, conversion, extraction, schema normalization, canonicalization
- `Execution and Runtime Pack`
  - bounded runtime invocation helpers, lease-aware execution launchers,
    continuation inspection where permitted
- `Governance and Coordination Pack`
  - policy lookup, rule evaluation, governance action helpers, agent-manifest
    inspection, registry query utilities
- `External Systems Pack`
  - API connector scaffolds, database/query tools, file/document tools, web and
    system adapters implemented as first-party native tools where strategically
    justified

## Proposed task

Task label:
- `T-TBD: Atrahasis First-Party Tool Suite`

Recommended type:
- `FULL PIPELINE`

Why FULL PIPELINE:
- this is not a small direct edit
- it likely requires concept selection about what a first-party tool suite
  should be, how broad it should be, what families are canonical, and how it
  should integrate with the rest of the stack

Recommended timing:
- after `T-240`, `T-260`, `T-262`, and `T-290`

Recommended dependencies:
- `T-240` `AACP Tool Connectivity Protocol`
- `T-260` `AACP Native Server Framework`
- `T-262` `AACP SDK Architecture`
- `T-290` `AACP v2 Cross-Layer Integration with Atrahasis Stack`

Rationale for timing:
- `T-240` defines how tool interactions work
- `T-260` defines how tools are authored and served
- `T-262` shapes the client/server developer surface
- `T-290` clarifies where tools intersect with the existing Atrahasis layers

Proposed task objective:
- design the official first-party Atrahasis tool suite as a native `AACP`
  capability layer, including tool-family architecture, packaging, trust
  posture, capability classes, and initial release set

Expected deliverables:
- module architecture
- first-party tool taxonomy
- canonical tool package boundaries
- trust and permission model for official tools
- initial official tool inventory and release waves
- guidance for what should be native versus bridged versus external-only
- roadmap for later implementation and packaging work

## Downstream implications

Likely later follow-on tasks after this module is defined:
- actual implementation backlog for first-party tool packs
- certification/conformance backlog for official tools
- registry/indexing additions for official Atrahasis tools
- operator/developer packaging and distribution plan

## Relationship to current T-240 ideation

If `T-240` selects a more advanced concept with continuation contexts, rich
session profiles, or lease-aware execution handoff, that may materially shape
the first-party tool suite design.

That is acceptable:
- `T-240` should define the tool protocol authority first
- the future tool-suite module should then build on that authority
- if `T-240` spills into later task surfaces, the later tasks can be updated at
  their own execution time rather than forcing `T-240` to stay artificially
  narrow now

## Serialized closeout note

Because shared-state files are currently protected in parallel mode, this
proposal should be treated as a queued candidate for later insertion into:
- `docs/TODO.md`
- future handoff notes
- any implementation-roadmap rewrite that follows `T-240` / `T-260`
