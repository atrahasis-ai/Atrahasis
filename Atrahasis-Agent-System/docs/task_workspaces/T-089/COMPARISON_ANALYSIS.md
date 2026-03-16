# T-089: Communication Architecture Comparison
# ASV + A2A/MCP (Current) vs AASL + AACP (Original)

**Task ID:** T-089
**Type:** ANALYSIS
**Date:** 2026-03-12
**Agent:** Shamash (Claude Code, 6ecc7362)

---

## 1. Executive Summary

The Atrahasis Agent System's communication architecture underwent a fundamental redesign during the C4 pipeline (2026-03-10). The original approach — a custom scripting language (AASL) and custom wire protocol (AACP) — was replaced by a semantic vocabulary layer (ASV) that delegates transport to industry-standard protocols (A2A/MCP).

This document compares the two approaches across eight dimensions: scope, expressiveness, tooling, complexity, maintainability, ecosystem alignment, security, and architectural fit.

**Bottom line:** The pivot preserved AASL's genuine semantic innovations while eliminating approximately 18,000 lines of custom parser/runtime liability and a 187-line protocol sketch that would have required years of engineering to bring to production grade.

---

## 2. Architecture Comparison

### 2.1 Original Design: AASL + AACP

```
Application Logic
       │
  ┌────▼────┐
  │  AASL   │  Custom declarative language
  │ (18K+   │  - Agent, task, tool, workflow, policy types
  │  lines) │  - Custom syntax: AGT{id:ag.r1 role:research}
  │         │  - 7-layer processing pipeline (Source → Governance)
  │         │  - Custom parser required
  └────┬────┘
       │
  ┌────▼────┐
  │  AACP   │  Custom wire protocol
  │ (187    │  - No connection management
  │  lines) │  - No authentication
  │         │  - No error handling or versioning
  └────┬────┘
       │
    Network
```

**AASL scope:** Comprehensive declarative language covering agents, tasks, tools, workflows, semantic relationships, governance objects. Seven-layer processing pipeline from source text through governance validation.

**AACP scope:** Protocol sketch only. 187 lines. No production-grade features (connection management, authentication, error handling, versioning, retry logic, backpressure).

### 2.2 Current Design: ASV + A2A/MCP

```
Application Logic
       │
  ┌────▼────┐
  │ C4 ASV  │  Semantic vocabulary (JSON Schema + JSON-LD)
  │ (1,652  │  - 7 core types: CLM, CNF, EVD, PRV, VRF, AGT, SAE
  │  lines) │  - Claim classification taxonomy (9 classes)
  │         │  - Dual classification: speech-act + epistemic
  │         │  - CLM-CNF-EVD-PRV-VRF accountability chain
  └────┬────┘
       │
  ┌────▼────────────────▼────┐
  │  A2A                MCP  │  Industry-standard transport
  │  (Google/LF)   (Anthropic)│  - Agent-to-agent: A2A
  │  100+ enterprise    97M+ │  - Agent-to-tool: MCP
  │  partners       monthly  │  - Production-grade security,
  │                 SDK DLs  │    auth, error handling, versioning
  └──────────┬───────────────┘
             │
          Network
```

**ASV scope:** Vocabulary only. Defines *what* agents say semantically — typed claims, structured confidence, evidence linking, provenance chains, verification records. No transport, routing, connection management, or task lifecycle.

**A2A/MCP scope:** Full production transport. A2A handles agent-to-agent communication (discovery, authentication, streaming, task lifecycle). MCP handles agent-to-tool integration (capability discovery, resource access, structured content).

---

## 3. Dimension-by-Dimension Comparison

### 3.1 Scope

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Semantic content | Full type system (agents, tasks, tools, workflows, policies, claims) | Focused: 7 epistemic types (CLM, CNF, EVD, PRV, VRF, AGT, SAE) |
| Transport | 187-line sketch — no production features | A2A (agent-to-agent) + MCP (agent-to-tool) — production-grade |
| Serialization | Custom syntax (`AGT{id:ag.r1 role:research}`) | JSON Schema + JSON-LD |
| Processing | 7-layer pipeline (Source → Governance) | Validation only (schema + vocabulary) |

**Verdict:** ASV is narrower by design — it claims only the semantic layer that A2A/MCP explicitly leave unaddressed. AASL tried to own the entire stack from syntax through governance.

### 3.2 Expressiveness

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Claim classification | Supported (within AASL types) | 9 canonical classes (D/C/P/R/E/S/K/H/N) mapped to C5 |
| Confidence representation | Supported | Point, interval, and distribution with calibration metadata |
| Evidence linking | Supported | 5 quality classes (direct, inference, hearsay, computational, delegation) |
| Provenance | Custom format | W3C PROV-O extension (standard-compatible) |
| Accountability chain | Implicit in pipeline | Explicit: CLM → CNF → EVD → PRV → VRF |
| Agent/task/workflow types | Full coverage | Out of scope (handled by A2A task model) |
| Dual classification | Not present | Speech-act type + epistemic claim type simultaneously |

**Verdict:** AASL was broader (more object types). ASV is deeper on the epistemic dimension — the dual classification framework and structured confidence are genuinely novel contributions that AASL lacked. The "20% gap" (AASL semantics not captured by ASV) primarily covers non-epistemic types that A2A's task model and MCP's tool model already address.

### 3.3 Tooling & Ecosystem

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Parser | Custom (must build from scratch) | JSON Schema validators (every language) |
| LLM generation accuracy | ~0% (zero training data for custom syntax) | >95% for JSON with constrained decoding |
| Developer familiarity | None — novel syntax | Universal — JSON is lingua franca |
| Validation libraries | Must build | JSON Schema: mature libraries in Python, TypeScript, Go, Rust, Java |
| Transport libraries | Must build | A2A: 100+ enterprise partners, Linux Foundation governance. MCP: 97M+ monthly SDK downloads |
| IDE support | None | JSON/JSON-LD: universal IDE support |
| Testing infrastructure | Must build | JSON Schema test suites, A2A/MCP conformance tests exist |

**Verdict:** Decisive advantage for ASV + A2A/MCP. The custom syntax was identified by the C4 Ideation Council as a "strategic liability" — building parser, validator, IDE support, and LLM fine-tuning for a novel syntax is an enormous engineering cost with no semantic benefit over JSON.

### 3.4 Implementation Complexity

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Lines of specification | ~18,000+ (AASL) + 187 (AACP) | 1,652 (ASV) + 0 (transport specs are external) |
| Custom components to build | Parser, lexer, validator, runtime, protocol stack, connection manager, auth layer | JSON Schema files, JSON-LD context, validator library |
| Time to first integration | Months (parser + protocol must exist first) | 6 weeks (GATE-1: schema + validator + 3 integration examples) |
| Protocol modifications needed | N/A (building from scratch) | Zero — uses A2A/MCP existing extensibility |
| Estimated engineering effort | Years (full stack) | Weeks to months (vocabulary + validators) |

**Verdict:** Order-of-magnitude reduction in implementation complexity. ASV's Phase 1 kill gate is 6 weeks; AASL+AACP would require years before basic interoperability.

### 3.5 Maintainability

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Specification maintenance | 18,000+ lines of custom spec requiring internal expertise | 1,652-line vocabulary spec + external protocol specs maintained by Google/Anthropic |
| Breaking changes | Full control but full responsibility | Transport: managed by protocol owners. Vocabulary: managed by AAS |
| Versioning | Must design versioning system | JSON-LD @context versioning + A2A/MCP native versioning |
| Security patches | Must implement all transport security | Transport security maintained by A2A/MCP teams + communities |
| Backward compatibility | Must design migration paths | JSON Schema evolution rules + A2A/MCP backward compatibility guarantees |

**Verdict:** Strong advantage for ASV + A2A/MCP. The maintenance burden for transport security alone would require a dedicated team. Delegating transport means AAS engineers focus exclusively on the semantic layer where Atrahasis adds unique value.

### 3.6 Ecosystem Alignment

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Industry direction | Against — every production agent framework uses JSON | With — JSON + standard protocols |
| Regulatory alignment | Neutral — custom format has no regulatory standing | Favorable — EU AI Act, NIST framework expect standard formats |
| Interoperability | Zero — islands with other agent systems | Native — A2A interop with any A2A agent; MCP interop with any MCP tool |
| Adoption path | Must convince ecosystem to learn custom syntax | Zero learning curve for transport; vocabulary adoption is incremental |
| Competitive window | No window pressure (isolated system) | 12-18 month window — W3C community groups forming for epistemic metadata |

**Verdict:** AASL+AACP would create an isolated system. ASV+A2A/MCP positions Atrahasis to participate in the emerging agent ecosystem while contributing genuinely novel epistemic semantics.

### 3.7 Security Model

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Transport security | Must implement (AACP had none) | TLS 1.3 via A2A/MCP (already implemented) |
| Agent authentication | Must implement | A2A Agent Cards + MCP capability negotiation |
| Message integrity | Must implement | A2A message signing + MCP transport security |
| Epistemic integrity | Could implement in AASL | ASV CLM-CNF-EVD-PRV-VRF chain + C5 PCVM verification |
| Attack surface | Enormous (custom parser = custom vulnerabilities) | Reduced — JSON parsers are battle-tested; transport security is externalized |

**Verdict:** AACP's 187 lines had zero security features. Building production-grade transport security is a multi-year effort. A2A/MCP provide it out of the box.

### 3.8 Architectural Fit within AAS

| Dimension | AASL + AACP | ASV + A2A/MCP |
|-----------|-------------|---------------|
| Layer 1 positioning | AASL spans multiple layers (syntax → governance) | ASV is strictly Layer 1 — vocabulary only |
| C5 PCVM integration | Claim types must be mapped | 9 canonical claim classes (D/C/P/R/E/S/K/H/N) with deterministic `epistemic_class → claim_class` mapping |
| C8 DSF integration | Settlement metrics undefined | Stream 3 Communication Efficiency uses ASV protocol adherence + signal-to-noise ratio |
| C9 reconciliation | Would require reconciliation addendum | C4 authority cleanly defined: owns vocabulary, defers claim class authority to C5, defers settlement to C8 |
| C3 tidal coordination | AASL extension model | ASV types carried in C3 delta messages |
| Separation of concerns | Blurred — AASL handles syntax, semantics, and partial protocol | Clean — ASV (semantics), A2A/MCP (transport), C5 (verification), C8 (settlement) |

**Verdict:** ASV fits the AAS layered architecture cleanly. AASL's broad scope would have created authority conflicts with C5 (claim classification), C7 (task lifecycle), and C8 (settlement).

---

## 4. What Was Preserved from AASL

The pivot was not a rejection of AASL's ideas — it was a rejection of its delivery mechanism. C4 ASV explicitly extracts:

1. **Epistemic type system** — Claims as first-class semantic objects with typed confidence
2. **CLM-CNF-EVD-PRV-VRF accountability chain** — The core insight that every assertion should carry confidence, evidence, provenance, and verification status
3. **Claim classification taxonomy** — Observation, correlation, causation, inference, prediction, prescription (extended to 9 classes via C9)
4. **Confidence primitive** — Point, interval, and distribution representations with calibration metadata
5. **Governed semantic objects** — The AASL principle that "agent communications should be governed semantic objects, not transient text"

What was discarded:
- Custom syntax (`AGT{id:ag.r1 role:research}`)
- Custom parser and 7-layer processing pipeline
- Agent, task, tool, and workflow type definitions (covered by A2A task model)
- Policy type definitions (covered by AAS governance layer)
- ~18,000 lines of specification

---

## 5. What Was Lost

The comparison would be incomplete without acknowledging trade-offs:

| Lost Capability | Severity | Mitigation |
|----------------|----------|------------|
| Unified type system across agents, tasks, tools, workflows | LOW | A2A provides task/agent types; MCP provides tool types; ASV provides epistemic types. Coverage is complete but distributed. |
| Token compactness of custom syntax | NEGLIGIBLE | JSON overhead is marginal; LLM generation accuracy gains dominate. |
| Full-stack control | MEDIUM | AAS depends on Google (A2A) and Anthropic (MCP) for transport evolution. Mitigated by: (a) both are open standards with foundation governance, (b) ASV vocabulary layer is transport-agnostic and could adapt to future protocols. |
| 7-layer processing pipeline | LOW | ASV validation is simpler. The governance pipeline functionality moved to C7 RIF (intent routing) and C14 GTP (governance translation). |
| ~20% of AASL semantic coverage | LOW-MEDIUM | The "20% gap" (identified in C4 feasibility) covers edge-case AASL semantics not expressible in JSON Schema. Addressed by supplementary specification where needed. Risk: "AASL by another name" if the supplement grows too large. |

---

## 6. Risk Comparison

| Risk | AASL + AACP | ASV + A2A/MCP |
|------|-------------|---------------|
| Adoption failure (FIPA/KQML precedent) | VERY HIGH — custom syntax + custom protocol = maximum friction | MEDIUM — JSON removes syntax barrier; transport is already adopted; regulatory window creates demand |
| Engineering overrun | VERY HIGH — full stack from scratch | LOW — vocabulary + validators; transport is external |
| LLM incompatibility | CRITICAL — zero training data | LOW — >95% JSON generation accuracy |
| Protocol obsolescence | HIGH — single-implementer protocol | LOW — A2A (Linux Foundation) + MCP (Anthropic + community) have institutional backing |
| Semantic gap | NONE — full AASL coverage | LOW-MEDIUM — 20% gap, supplementary spec needed |
| Vendor dependency | NONE — fully internal | MEDIUM — depends on A2A/MCP trajectory. Mitigated by transport-agnostic vocabulary design |
| Security vulnerability | VERY HIGH — custom parser = custom CVEs | LOW — battle-tested JSON parsers + externalized transport security |

---

## 7. Quantitative Summary

| Metric | AASL + AACP | ASV + A2A/MCP | Delta |
|--------|-------------|---------------|-------|
| Lines of custom specification | ~18,187 | 1,652 | -91% |
| Custom components to build | ~8 (parser, lexer, validator, runtime, protocol, auth, connection mgr, versioning) | ~2 (schema files, validator library) | -75% |
| LLM generation accuracy | ~0% | >95% | +95pp |
| Time to first integration | Months-years | 6 weeks (GATE-1) | Order of magnitude |
| External ecosystem support | 0 partners | 100+ (A2A) + 97M monthly SDK DLs (MCP) | N/A |
| Transport security features | 0 | Full (TLS 1.3, agent auth, message signing) | Complete |
| Semantic expressiveness | Broader (agents, tasks, tools, workflows, policies, claims) | Deeper on epistemic dimension (dual classification, calibrated confidence) | Trade-off |

---

## 8. Conclusion

The AASL → ASV pivot was a **scope discipline decision**: AASL correctly identified that agent communication needs epistemic accountability, but incorrectly concluded that achieving this required owning the entire communication stack. ASV isolates the genuinely novel contribution (epistemic vocabulary) and delegates the commodity infrastructure (transport, security, connection management) to protocols with institutional backing and massive ecosystem adoption.

The trade-off — loss of full-stack control and ~20% of AASL's semantic breadth — is outweighed by:
- 91% reduction in custom specification
- LLM generation accuracy from ~0% to >95%
- Zero transport engineering burden
- Native interoperability with the emerging agent ecosystem
- 12-18 month window to establish reference vocabulary before protocol owners define competing epistemic metadata

The original AASL insight — "agent communications should be governed semantic objects, not transient text" — survives fully in ASV's CLM-CNF-EVD-PRV-VRF chain. The delivery mechanism changed; the core idea did not.

---

**References:**
- C4 MASTER_TECH_SPEC.md (v2.0, 1,652 lines) — `docs/specifications/C4/MASTER_TECH_SPEC.md`
- C4 architecture.md — `docs/specifications/C4/architecture.md` (AACP kill: ARCH-C4-007, line 923)
- C4 technical_spec.md — `docs/specifications/C4/technical_spec.md` (A2A/MCP integration schemas)
- C4 FEASIBILITY_VERDICT.md — `docs/invention_logs/C4_FEASIBILITY_VERDICT.md` (adversarial challenges)
- C9 MASTER_TECH_SPEC.md — `docs/specifications/C9/MASTER_TECH_SPEC.md` (cross-layer authority mapping)
- UNIFIED_ARCHITECTURE.md — `docs/specifications/UNIFIED_ARCHITECTURE.md` (Layer 1 positioning)

---

*Analysis by Shamash (Claude Code, 6ecc7362) — 2026-03-12*
