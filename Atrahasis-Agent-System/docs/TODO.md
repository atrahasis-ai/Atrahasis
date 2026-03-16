# AAS TODO List
**Owner:** Chronicler
**Purpose:** Track pending tasks, future work, and deferred items.
**Source:** Gap analysis of original 15-layer Atrahasis architecture vs 19 AAS Master Tech Specs (2026-03-11).

---

## Active / In Progress

### The Sovereign Custody Redesign (Renovation Backlog)
These tasks supersede the previous buildout.

The Sovereign Custody Redesign backlog is complete.
Next dispatchable canonical tranche: `PARALLEL` - `T-303` + `T-306` + one of `T-305 / T-307`.

See docs/specifications/STRATEGY/RENOVATION_TASKS.md for full details.

#### Renovation Status

| ID | Target | Status | Notes |
|----|--------|--------|-------|
| `T-RENOVATE-001` | `C14 AiBC` | `DONE` | Constitutional rewrite completed and claim closed. |
| `T-RENOVATE-002` | `C15 AIC` | `DONE` | Economic rewrite completed and claim closed. |
| `T-RENOVATE-003` | `C18 Funding` | `DONE` | Closed-capability publication posture rewrite completed. |
| `T-RENOVATE-004` | `C22 Implementation` | `DONE` | Implementation resequencing completed and claim closed. |
| `T-RENOVATE-005` | `C3 Noosphere` | `DONE` | Osmosis boundary and quarantine filter retrofit completed. |
| `T-RENOVATE-006` | `C36 EMA-I` | `DONE` | Four-membrane interface isolation rewrite completed. |
| `T-RENOVATE-007` | `C40 Security` | `DONE` | Sanctum trust-anchor exclusion hardening completed. |
| `T-RENOVATE-008` | `C44 / C45` | `DONE` | Leased-cognition envelope formalization completed. |
| `T-RENOVATE-009` | `C47 Forge` | `DONE` | Native model adaptation expansion completed. |
| `T-RENOVATE-010` | `C48 Glass Vault` | `DONE` | New transparency-ledger spec completed. |
| `T-RENOVATE-011` | `C1 - C13` | `DONE` | Audit completed; canonical membrane mapping lives in `T-RENOVATE-011/MEMBRANE_AUDIT.md` and `C9 v2.0.1`. |
| `T-RENOVATE-012` | `C19 - C42` | `DONE` | Audit completed; stale marketplace and uncontrolled API assumptions were patched in `C22` and `C35`. |

No active canonical tasks at the moment. `T-302` and `T-304` closeout are complete, and the next dispatchable tranche is listed above.
System note: Master Prompt v2.2 model routing policy has been applied. No follow-up TODO item is required for this governance update.

---

## AAS Pipeline Required (New System Design)

These are genuinely missing subsystems that need task-scoped invention work - IDEATION through ASSESSMENT.

Policy note:
- `T-xxx` entries below are task / problem-space IDs, not preassigned invention IDs.
- A task may mint zero, one, or multiple `C-xxx` inventions after IDEATION selection.
- For any `FULL PIPELINE` task, Ideation Council output is advisory only. The assigned agent must stop after `IDEATION`, obtain explicit user concept approval, and record it in `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md` before minting any `C-xxx` invention ID or creating per-invention artifacts.

### CRITICAL - Referenced by existing specs but never specified

(No remaining CRITICAL items â€” T-060 completed as C35 Seismographic Sentinel.)

### HIGH - Core architectural gaps

(No remaining HIGH items â€” T-062 completed as C34 BSRF.)

### MEDIUM - Needed for deployment but not blocking architecture

(No remaining MEDIUM items â€” T-064 completed as C36 EMA-I.)

### LOW - Architectural completeness, not blocking

(No remaining LOW items â€” T-067 completed as C37 Epistemic Feedback Fabric.)

---

## AACP/AASL Full Replacement (Alternative C)

These tasks activate the sovereign Atrahasis communication stack described in the March 12, 2026 source packet under `C:\Users\jever\Atrahasis\AACP-AASL\`. The source packet used the Alternative B label; the repo's canonical shared state now tracks this program as Alternative C.

Policy notes:
- `T-200` through `T-291` are the protocol buildout tasks derived directly from the Alternative C strategy packet, historically introduced under the Alternative B source-packet label.
- `T-300` through `T-309` are mandatory retrofit tasks for the rest of the Atrahasis repo, because large parts of the current system assume `C4 ASV + A2A/MCP`.
- A2A/MCP bridges remain allowed as migration scaffolding, not as the intended end-state architecture.
- `C4 ASV` and related materials are retained as the historical baseline and compatibility reference; they are not normative design authority for `T-200`+ protocol-design tasks.
- Direct use of ASV-era materials is expected for supersession, audit, retrofit, migration, and compatibility tasks (`T-300`+), or when a task explicitly requires comparison against the old stack.
- Do not delete or archive ASV materials out of the working repo until the Alternative C retrofit program is complete.

### Dependency Safety Rules

- The `Dependencies` column is a hard gate, not a hint. If a listed prerequisite is not complete, the downstream task must stop rather than invent missing architecture.
- `FULL PIPELINE` tasks establish upstream design authority. `DIRECT SPEC`, `Governance`, `Analysis`, and `Packaging` tasks must consume those upstream artifacts instead of fabricating placeholders.
- `FULL PIPELINE` tasks must also honor the ideation approval gate: `recommended_concepts` are not self-approving, and no promoted invention may be minted without `docs/task_workspaces/T-<ID>/HITL_APPROVAL.md`.
- If a task discovers that its declared prerequisites are insufficient, the correct action is to add or assign a prerequisite task, not to fill the gap with speculative details.
- `T-301` is intentionally early. It audits the old `ASV + A2A/MCP` footprint so later retrofit tasks do not miss stale assumptions.
- Parallel-capacity notes below are **surface-safe dispatch ceilings**, not just dependency counts. They assume one writer per canonical surface.
- A task may be dependency-ready but still blocked if another active claim owns the same primary write surface: the same spec file, the same future `C` master spec, the same governance/shared-doc surface, or the same external AASL corpus.
- When a wave contains multiple direct-spec tasks on one primary surface, only one of those tasks may run at a time even if every dependency is complete.
- Claim files remain authoritative. If a task's concrete `scope.safe_zone_paths` overlap a live claim, stop and wait even if the wave note says capacity remains.
- The wave counts below are conservative planning numbers for delegation. If a claim reveals broader overlap than the table assumed, use the smaller number.

### Dispatch Lane Rules

- Treat the lane notes under each wave as the actual assignment rule. If two tasks appear on the same lane, they are mutually exclusive and must serialize.
- Do not assign two direct-spec tasks in the same wave unless they sit on different named lanes.
- For `FULL PIPELINE` tasks, the lane is the task workspace before approval and the minted `C-xxx` safe zone after approval. Two different `FULL PIPELINE` tasks are parallel-safe only if they are on different lanes and the ideation approval gate is respected.
- If a lane note says "broad existing-stack surface" or "shared governance/docs surface", assume overlap unless a fresh claim review proves otherwise.
- When in doubt, dispatch fewer tasks and let the claim review expand capacity instead of assuming the larger wave count is safe.

### Wave 1 - Foundation (Sequential)

These tasks should run first and in order.
Surface-safe dispatch ceiling: 1 task at a time.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|

### Wave 1A - Early Audit (Can Run After T-200)

Surface-safe dispatch ceiling: 1 additional task. This wave can overlap with Wave 1 after `T-200`, so the early global ceiling is 2 concurrent tasks (`T-301` plus one Wave 1 task).

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|

### Wave 2 - Core Protocol (After T-210, Can Parallelize)

Surface-safe dispatch ceiling: no open tasks. Wave 2 is complete.

(No remaining open Wave 2 tasks - `T-211`, `T-212`, `T-213`, and `T-215` are complete. Historical note: `T-213` and `T-215` serialized because both refined the `C38` master spec surface.)

### Wave 3 - Transport, Auth, and Manifest (After Wave 2, Can Parallelize)

Surface-safe dispatch ceiling: no open tasks. Wave 3 is complete.
Dispatch lanes:
- Historical note: the serialized `C38` transport lane (`T-220` -> `T-221` -> `T-222` -> `T-223`) is complete.
- Historical note: `T-214` completed as `C41`, so downstream tasks now consume the canonical manifest authority surface rather than dispatching the invention lane.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
(No remaining open Wave 3 tasks - the serialized C38 transport lane is complete.)

### Wave 4 - Tool Connectivity and Operational Semantics (After T-211, T-212, T-230)

Surface-safe dispatch ceiling: no open tasks. Wave 4 is complete.
Dispatch lanes:
- `Tool invention lane`: complete as `C42` Lease-Primed Execution Mesh (LPEM); downstream tasks now consume the canonical tool-authority surface.
- `C39 message-semantics lane`: complete through `T-243` and `T-244`; `C39` now defines both the concrete stream/push operational surface (`v1.0.3`) and the canonical sampling contract (`v1.0.4`).
- `Security addendum lane`: complete as the `C40 v1.0.1` semantic-poisoning defense addendum; downstream tasks now consume the bounded admission-gate and manifest anti-spoofing surface.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
(No remaining open Wave 4 tasks - `T-241`, `T-242`, `T-243`, and `T-244` are complete.)

### Wave 5 - The Cross-Compilation Forge (After T-240)

Surface-safe dispatch ceiling: no open tasks. Wave 5 is complete.
Dispatch lanes:
- `Forge lane`: complete as `C47` AACP Automated Cross-Compilation Forge; downstream tasks now consume the canonical tool ingestion surface.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
(No remaining open Wave 5 tasks - `T-252` is complete.)

### Wave 6 - Ecosystem and Cross-Layer Integration (After Wave 5)

Surface-safe dispatch ceiling: no open tasks. Wave 6 is complete.
Dispatch lanes:
- `Ecosystem lane`: complete through `T-280`; downstream interface work now consumes the canonical tooling surface.
- `Conformance lane`: complete through `T-281`; downstream work now consumes the canonical certification authority surface.
- `Cross-layer integration lane`: complete through `T-290`; downstream retrofit and governance work now consume `AXIP-v1` as the native integration target.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
(No remaining open Wave 6 tasks - `T-262`, `T-280`, `T-281`, and `T-290` are complete.)

### Wave 7 - Validation, Governance, and Supersession Boundary (After Wave 6)

Surface-safe dispatch ceiling: no open tasks. Wave 7 is complete.
Dispatch lanes:
- `Validation lane`: complete through `T-291`; downstream work now consumes the canonical justification-test authority.
- `Governance/shared-doc lane`: complete through `T-300`; downstream retrofit planning now uses the canonical C4 supersession boundary.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
(No remaining open Wave 7 tasks - `T-291` and `T-300` are complete.)

### Wave 8 - Repo-Wide Retrofit (After Boundary and Integration Artifacts Exist)

These follow-on tasks revise the rest of the Atrahasis repo after the Alternative C architecture stabilizes.
Surface-safe dispatch ceiling: 3 concurrent tasks.
Dispatch lanes:
- `Core retrofit lane`: `T-303`. The remaining verification/communication retrofit still touches the `C5`-side core surfaces.
- `Governance retrofit lane`: `T-305`, `T-307`. These must serialize because both edit shared planning/governance docs.
- `Interface retrofit lane`: `T-306`. Unblocked now that `T-302` and `T-280` are complete; it may overlap with `T-303` and one governance task if claim review confirms no shared file collision.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
| T-303 | Verification, Memory, and Provenance Retrofit | DIRECT SPEC | HIGH | T-301, T-240, T-252, T-290 | Align C5, C6, C34, and C35 trust boundaries and provenance handling. Remove all legacy 'bridged provenance' caveats. |
| T-305 | Implementation Plan and Wave Sequencing Rewrite | Governance | HIGH | T-301, T-210, T-230, T-240, T-260, T-290 | Replace the current implementation roadmap with Alternative C sequencing, staffing, rollout gates, and ownership splits. |
| T-306 | Interface and Developer Experience Retrofit | DIRECT SPEC | MEDIUM | T-302, T-260, T-280 | Update EMA-I, developer/operator touchpoints, and tool assumptions for native AACP/AASL workflows. |
| T-307 | Sub-Agent Loci Conversion Strategy | Governance | HIGH | T-300, T-252, T-291 | Define the strategic roadmap for converting the top 50 required external capabilities into native Sub-Agent Loci via the Cross-Compilation Forge. |

### Wave 9 - Cleanup and Publication

Surface-safe dispatch ceiling: 1 task launch from the Alternative C tranche. `T-308` starts first; `T-309` remains blocked until `T-308` is complete.
Dispatch lane:
- `Publication lane`: `T-308`, `T-309`. Serialize these; `T-309` remains blocked on `T-308`.

| ID | Task | Type | Priority | Dependencies | Notes |
|----|------|------|----------|--------------|-------|
| T-308 | Repo-Wide Terminology and Reference Sweep | Packaging | MEDIUM | T-300, T-301, T-302, T-307 | Replace stale ASV/A2A/MCP/Bridge language across read-first docs, spec introductions, and cross-references. |
| T-309 | External Review Package Refresh | Packaging | LOW | T-304, T-305, T-308 | Repackage the repo for external reviewers after the communication-architecture shift, including funding and implementation narrative updates. Absorbs the former `T-011` packaging scope. |

---

## Direct Spec Edits (No AAS Pipeline)

These are gaps that can be closed by adding sections to existing specs.

### HIGH Priority

| ID | Task | Type | Target Spec | Notes |
|----|------|------|-------------|-------|
(No remaining HIGH direct edit items â€” T-074 completed as C5 Section 10.5 Membrane Certificate Engine, T-076 completed as C14 Section 7.6 Governance Directive Registry.)

### MEDIUM Priority

| ID | Task | Type | Target Spec | Notes |
|----|------|------|-------------|-------|
(No remaining MEDIUM direct edit items â€” T-080 completed as C6 Section 4.6 Four-Tier Memory Model, T-083 completed as C14 Section 4.4 Trustee Ratification Interface, T-084 completed as C5 Section 10.6 Contestable Reliance Membrane.)

### LOW Priority

| ID | Task | Type | Target Spec | Notes |
|----|------|------|-------------|-------|
(No remaining LOW direct edit items. Legacy packaging task `T-011` has been folded into `T-309`.)

---

## Out of Scope (No Action Needed)

These items are not active work for the current AAS backlog:

- Physical planetary network deployment remains deferred beyond current AAS specification scope; current work stops at the architecture/specification layer.
- Legacy Verichain, CIOS, and Knowledge Cortex continuation work is out of scope as standalone lines because C5, C7, and C6 replaced them.

## User Dispatch Order (Simple)

Use this section for assignment order. It is intentionally simplified and already accounts for the known non-conflict lanes.
When a task listed here is completed, remove its task ID from this section as part of shared-state closeout. During parallel execution, queue that removal in the handoff rather than editing the UDO live.

1. `PARALLEL` - `T-303` + `T-306` + one of `T-305 / T-307`
2. `SOLO after T-307` - `T-308`
3. `SOLO after T-308` - `T-309`

Completed tasks are archived in [COMPLETED.md](COMPLETED.md) (124 tasks).

---

*Last updated: 2026-03-15 (T-302 shared-state closeout - Tishpak)*
