# AAS TODO List
**Owner:** Chronicler
**Purpose:** Track pending tasks, future work, and deferred items.
**Source:** Gap analysis of original 15-layer Atrahasis architecture vs 19 AAS Master Tech Specs (2026-03-11).

---

## Active / In Progress

| ID | Task | Status | Priority | AAS | Notes |
|----|------|--------|----------|-----|-------|
| — | No active tasks | — | — | — | — |

---

## AAS Pipeline Required (New System Design)

These are genuinely missing subsystems that need full invention — IDEATION through ASSESSMENT.

### CRITICAL — Referenced by existing specs but never specified

| ID | Task | Priority | Notes |
|----|------|----------|-------|
| T-060 | C23 — Sentinel Graph (Security & Anomaly Detection) | CRITICAL | Referenced by 10+ specs (C3, C5, C6, C8, C11, C12, C13, C14, C17) as critical infrastructure for anomaly detection, behavioral clustering, and infrastructure fingerprinting. Most-referenced unspecified component in the entire system. No dedicated spec exists. |

### HIGH — Core architectural gaps

| ID | Task | Priority | Notes |
|----|------|----------|-------|
| T-061 | C24 — Agent Execution Runtime | HIGH | The system orchestrates agents (C7 RIF), schedules them (C3), and verifies their output (C5) — but never specifies how agents actually run. No agent types, no execution runtime, no inference provisioning, no cell execution layer. C22 Wave 1 assumes this exists. |
| T-062 | C25 — Recovery & State Assurance | HIGH | No snapshot layer, delta journal, witness system, or state reconstruction engine. C3 has Emergency Tidal Rollback and C8 has deterministic EABS, but no unified recovery architecture across all 6 layers. Critical for production deployment. |
| T-063 | C26 — Identity & Citizenship Registry | HIGH | Identity is scattered: C7 RIF has Agent Registry, C5 PCVM has Credibility Engine, C8 DSF has Capability-Weighted Stake, C14 has Citicate. No unified identity system. Missing: role history tracking, domain expertise profiles, unified eligibility engine. |

### MEDIUM — Needed for deployment but not blocking architecture

| ID | Task | Priority | Notes |
|----|------|----------|-------|
| T-064 | C27 — Human & External Interface Layer (Website / Mobile / API / SDK / CLI) | MEDIUM | No spec defines how humans or external systems interact with Atrahasis. Humans need: website, mobile apps, API access, developer SDKs, CLI tooling. C4 ASV defines message schemas but no REST/gRPC/WebSocket API surface. C14 trustees need governance interfaces. C16 institutional partners need access points. C22 mentions TypeScript schemas but no interface spec. |
| T-065 | C28 — Infrastructure & Federation | MEDIUM | No compute topology, cluster architecture, or cross-region federation. C3 explicitly defers federation to Phase 4. C22 specifies technology stack (Rust/Python/NATS/PostgreSQL) but not deployment architecture. |
| ~~T-068~~ | ~~C31 — Agent Organizational Topology~~ | ~~COMPLETE~~ | ~~Moved to COMPLETED.md~~ |
| T-066 | C29 — Operational Monitoring & Incident Response | MEDIUM | No governance health dashboard, incident response playbooks, or runtime security audit layer. C14 defines CFI metric and AiSIA monitoring conceptually, but no operational tooling spec exists. Needed for production operations. |

### LOW — Architectural completeness, not blocking

| ID | Task | Priority | Notes |
|----|------|----------|-------|
| T-067 | C30 — Cognitive Control & Meta-Cognition | LOW | No learning loops, reasoning templates, strategy feedback, or system optimization. The system verifies reasoning (C5 R-class claims) but doesn't guide it. May be intentionally out of scope — Atrahasis is infrastructure, not agent internals. Needs scoping decision: is this in-scope or explicitly excluded? |

---

## Direct Spec Edits (No AAS Pipeline)

These are gaps that can be closed by adding sections to existing specs.

### HIGH Priority

| ID | Task | Type | Target Spec | Notes |
|----|------|------|-------------|-------|
| T-070 | Specify Capsule Epoch Protocol | Missing section | C3 | C3 TOC line 259 explicitly lists "Fusion Capsule Epoch Protocol" as excluded/deferred. Needs specification for complete coordination layer. |
| T-071 | Specify Cut Commit Fallback | Missing section | C3 | No "cut commit" recovery pattern specified. C3 has ETR but needs a general-purpose fallback for partial epoch failures. |
| T-072 | Unify Attestation Engine references | Cross-reference | C5 | Attestation logic distributed across C5 Sections 6-7. Add a named subsection consolidating the attestation flow. |
| T-073 | Specify Contradiction Lattice | Missing section | C6 | C6 Section 7 has Coherence Graph with CONTRADICTION edges but no dedicated lattice data structure. Original Noosphere spec had detailed contradiction lattice. |
| T-074 | Add Membrane Certificate Engine spec | Missing section | C5 | C3 references "Membrane Certificate (MCT)" in data flow. C5 Section 10 produces admission/rejection decisions. Need explicit MCT format and lifecycle. |
| T-075 | Define Proposal System lifecycle | Missing section | C14 | C3 Section 7.1 has G-class consensus and C14 has governance taxonomy, but no formal proposal lifecycle (submission → debate → voting → ratification → execution). |
| T-076 | Define Governance Directive Registry | Missing section | C14 | C14 defines governance decision taxonomy (GTP) but no persistent registry for active directives, their status, and enforcement state. |

### MEDIUM Priority

| ID | Task | Type | Target Spec | Notes |
|----|------|------|-------------|-------|
| T-077 | Name Scoped Replica Groups in C3 | Terminology | C3 | C3's parcels + loci function as scoped replica groups. Add explicit naming and cross-reference to align with original architecture terminology. |
| T-078 | Add Claim Family Graph to C5/C6 | Missing section | C5, C6 | C5 Credibility Engine tracks claim dependencies. C6 Coherence Graph has derivation edges. Need explicit "claim family" grouping and graph structure. |
| T-079 | Add Semantic Index to C6 | Missing section | C6 | C6 EMA Section 9 has retrieval interfaces but no dedicated semantic index for knowledge discovery. Need indexing strategy for epistemic quanta. |
| T-080 | Define Four-Tier Memory Model | Missing section | C6 | C3 Section 1.2 defers this to Noosphere Spec Sections 23-25. C6 has metabolic lifecycle states but the original four-tier model (working/short-term/long-term/archival) is never formally specified. |
| T-081 | Add Archive Layer to C6 | Missing section | C6 | C6 catabolism handles knowledge retirement (quarantine → dissolution) but no long-term archival. Need archive specification for historical knowledge preservation. |
| T-082 | Specify Governance Audit Layer | Missing section | C14 | C14 Section 16 defines AiSIA conceptually. Need runtime audit specification: what's logged, retention, query interface, compliance reporting. |
| T-083 | Add Manual Ratification Interface to C14 | Missing section | C14 | C14 defines trustee voting thresholds but no interface spec for how human trustees interact with governance decisions in practice. |
| T-084 | Specify Contestable Reliance Membrane | Missing section | C5 | Original Verichain spec had this concept — a mechanism for agents to contest verification results they rely on. Not carried forward into PCVM. |

### LOW Priority

| ID | Task | Type | Target Spec | Notes |
|----|------|------|-------------|-------|
| T-085 | Add Heuristic Family Store to C6 | Missing section | C6 | H-class claims exist in C5 taxonomy but heuristics are not grouped into "families" for tracking, versioning, or retirement. |
| T-086 | Add Super-Verification Layer to C5 | Missing section | C5 | C5 has deep-audit (7% random full replication) but no escalation path for contested high-stakes verification. Original spec had a "super-verification" concept. |
| T-087 | Specify Bundle Compaction Engine | Missing section | C6 | C6 catabolism handles retirement. Need specification for compacting related knowledge bundles without information loss. |
| T-088 | Specify Canonicalizer service | Missing section | C4 | C4 ASV provides JSON-LD context for semantic normalization but no dedicated canonicalization service for deduplication and normalization of equivalent representations. |
| T-011 | External review preparation | Packaging | All | Package specs for external review or publication |

---

## Deprecated / Out of Scope (No Action Needed)

These components from the original 15-layer list are either deprecated, replaced, or absorbed:

| Original Component | Status | Replacement |
|----|--------|-------------|
| AASC Compiler | DEPRECATED | C4 ASV — JSON Schema replaces custom compiler |
| AASL Parser | DEPRECATED | C4 ASV — standard JSON Schema validation |
| AASL Validator | DEPRECATED | C4 ASV — standard JSON Schema validators |
| AASL Runtime Workspace | DEPRECATED | Concept eliminated — ASV is vocabulary, not runtime |
| AACP Envelope Layer | DEPRECATED | C4 ASV Speech-Act Envelope (SAE) + A2A/MCP integration |
| CIOS | DEPRECATED | C7 RIF — fully replaces CIOS |
| Knowledge Cortex | DEPRECATED | C6 EMA — fully replaces Knowledge Cortex |
| Collective Intelligence Kernel (CIK) | ABSORBED | Distributed across C7 RIF, C3, C6 EMA |
| Global Intelligence Control Plane | ABSORBED | C7 RIF Section 10.2 — Global Executive (GE) |
| Trinity Structures | RESOLVED by C31 | CAT generalizes the tetrahedral motif — DAN of 4 in MEDIUM safety IS a tetrahedral cell |
| Tetrahedral Clusters | RESOLVED by C31 | CAT preserves the concept as Deterministic Affinity Neighborhoods (DANs) of 3-5 agents |
| Lattice Clusters | RESOLVED by C31 | Crystal Structure (informational layer) provides lattice-like inter-DAN connectivity |
| Planetary Intelligence Network | DEFERRED | C3 targets planetary scale; physical network deferred |
| Planning Agents | ABSORBED | C7 RIF Section 8.2 — System 4 Strategic Intelligence |
| Routing Policy Engine | ABSORBED | C7 RIF Section 8.1 — System 3 Operational Control + C3 hash-ring scheduling |
| Resource Strategy Engine | ABSORBED | C7 RIF Section 6.4-6.5 + C8 DSF Section 8 Capacity Market |
| Coordinator Agents | ABSORBED | C7 RIF architectural roles (GE, LD, PE) |
| Verification Liaison Agents | ABSORBED | C5 PCVM VRF-selected committees handle verification directly |
| Memory Liaison Agents | ABSORBED | C6 EMA system service handles knowledge metabolism |
| Human Interface | MOVED TO T-064 | Elevated to AAS Pipeline task C27 — website, mobile apps, API, SDK, CLI |
| Verichain | DEPRECATED | C5 PCVM — fully replaces Verichain |

---

## Summary

| Category | Count |
|----------|-------|
| AAS Pipeline Required | 8 new inventions (C23-C30) + C31 COMPLETE |
| Direct Spec Edits — HIGH | 7 tasks |
| Direct Spec Edits — MEDIUM | 8 tasks |
| Direct Spec Edits — LOW | 5 tasks |
| Deprecated / Out of Scope | 18 components (no action) + 3 under review |
| **Total open tasks** | **29** + T-011 |

*Completed tasks archived in [COMPLETED.md](COMPLETED.md) (56 tasks)*

---

*Last updated: 2026-03-11*
