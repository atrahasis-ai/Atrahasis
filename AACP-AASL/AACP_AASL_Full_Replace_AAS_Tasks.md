You are operating the Atrahasis Agent System (AAS) to execute a series of tasks that will produce the complete AACP/AASL Full Replacement protocol stack.

## Context

The Atrahasis project has decided (per the Council Briefing dated March 12, 2026) to pursue Alternative B: Full Replacement of Google A2A and Anthropic MCP with a sovereign AACP v2 / AASL protocol stack. This decision reverses the previous out-of-scope designation in TODO.md.

The justification is quantified:
- 53% session cost reduction on Opus 4.6 ($93 → $43 per session)
- 94% thinking overhead reduction (6,250 → 390 tokens per complex task)
- 6x multi-hop reasoning, 10x cross-doc synthesis, 10x verification assessment
- 5 hallucination categories structurally eliminated
- $537M/yr savings at 10K agent scale

## Your Operating Rules

1. **Read the AAS Master Prompt** at `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md` before starting any task. Follow its rules exactly.

2. **Read the Full Replacement Strategy** at `AACP_AASL_Full_Replacement_Strategy.md` (in project files) — this is the canonical architecture document for all AACP v2 work.

3. **Read the Council Briefing** at `AACP_AASL_Full_Replace_Council_Briefing.md` (in project files) — this contains the quantified justification and reasoning quality analysis.

4. **Each task below is scoped for one AAS pipeline run.** Tasks marked "FULL PIPELINE" go through IDEATION → RESEARCH → FEASIBILITY → DESIGN → SPECIFICATION → ASSESSMENT. Tasks marked "DIRECT SPEC" are additions to existing specifications and skip the ideation/research stages.

5. **Task IDs are T-xxx format.** Invention IDs (C-xxx) are minted only when concepts advance past IDEATION. One task may produce zero, one, or multiple inventions.

6. **Execute tasks in the order specified by the user.** The user will tell you which task(s) to start. Do not skip ahead.

7. **Update TODO.md** after each task completes — move the task from Active to the completed section, following the existing pattern in COMPLETED.md.

8. **Update AGENT_STATE.md** with the new invention entries as they are created.

9. **Critical architectural constraint:** Every specification produced must be compatible with the existing Atrahasis stack (C3 Tidal Noosphere, C5 PCVM, C6 EKMF, C7 RIF, C8 DSF, C9 Reconciliation, C23 SCR, C24 FHF, C32 MIA, C34 BSRF, C35 Seismographic Sentinel, C36 EMA-I, C37 EFF). AACP v2 is a new communication/transport layer, not a replacement of the epistemic architecture.

10. **The existing AASL specification** (`AASL_System.txt`, `AASL_SPECIFICATION.md`, `AASL_PRIMER.md`) and all `Atrahasis_AASL_*.md` files are the foundation. AACP v2 extends AASL, it does not replace it.

## First Action

Update `TODO.md`:
- Remove the out-of-scope entries for AACP and AASL
- Add an ADR to `DECISIONS.md` recording the decision to pursue Full Replacement (Alternative B)
- Add all tasks from Part 2 of this document to TODO.md under a new section "AACP/AASL Full Replacement (Alternative B)"
- Set AGENT_STATE.md stage to "ACTIVE" with status "AACP_V2_BUILDOUT"

Then await user direction on which task to execute first.



## PART 2: TASK LIST

### Governance Tasks (execute first)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-200 | ADR: Approve Full Replacement Strategy | Governance | CRITICAL | None | Record the decision to pursue Alternative B. Reverse the out-of-scope designation for AACP/AASL in TODO.md. Reference the Council Briefing and Advantage Analysis documents. |
| T-201 | ADR: AASL Type Registry Extension Policy | Governance | HIGH | T-200 | Establish the policy for adding TL{}, PMT{}, SES{} to the AASL type registry. Define backward compatibility rules, ontology versioning impact, and forward-compatibility behavior for agents that don't understand new types. |

### Phase 1 — Core Protocol Architecture (Weeks 1-14)

These tasks define the foundational protocol architecture. They must complete before transport bindings or tool connectivity.

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-210 | AACP v2 Five-Layer Protocol Model | FULL PIPELINE | CRITICAL | T-200 | Design the unified 5-layer protocol architecture (Transport, Session, Security, Messaging, Semantics). Define layer contracts, interaction rules, and independent upgradeability. This is the master architecture for everything that follows. Produces a Master Tech Spec. |
| T-211 | AACP Message Class Extension (23 → 42) | FULL PIPELINE | CRITICAL | T-210 | Design all 19 new message classes organized by function: Agent Discovery (3), Tool Connectivity (4), Resource Access (3), Elicitation/Prompting (4), Streaming/Push (3), Sampling (2). Define header extensions, payload schemas, lineage tracking, and canonical forms. Produces a Master Tech Spec. |
| T-212 | AASL New Types: TL, PMT, SES | DIRECT SPEC | HIGH | T-201, T-210 | Specify three new AASL primitive types: TL{} (Tool), PMT{} (Prompt Template), SES{} (Session). Define fields, canonical forms, validation rules, ontology placement, and AASC compiler extensions. Extends AASL_SPECIFICATION.md. |
| T-213 | AACP Handshake & Session Management Protocol | DIRECT SPEC | HIGH | T-210 | Specify the connection lifecycle: handshake_request/handshake_response message format, capability exchange, version negotiation, encoding selection (AASL-T/AASL-J/AASL-B), PING/PONG heartbeat, graceful shutdown, reconnection with workflow recovery, stateless mode. |
| T-214 | Atrahasis Agent Manifest Specification | FULL PIPELINE | HIGH | T-210, T-211 | Design the Agent Manifest replacing A2A Agent Cards. Includes semantic capabilities (supported AASL types, ontology versions, verification methods), endpoint URLs, supported encodings, auth schemes. Published at /.well-known/atrahasis.json. Produces a Master Tech Spec. |
| T-215 | AACP Lineage & Canonicalization Extension | DIRECT SPEC | HIGH | T-210 | Formalize the 4-field mandatory lineage (message_id, parent_message_id, conversation_id, workflow_id) at the AACP v2 transport level. Define canonical hash computation for AACP messages across all three encodings (AASL-T, AASL-J, AASL-B). Specify cross-encoding semantic identity rules. |

### Phase 2A — Transport Layer (Weeks 10-20)

Each transport binding is a separate task. They can be executed in parallel.

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-220 | AACP-HTTP Transport Binding | DIRECT SPEC | CRITICAL | T-210, T-213 | Specify the HTTP binding: endpoint structure (POST /aacp/message, GET /aacp/manifest, POST /aacp/stream, POST /aacp/handshake), Content-Type headers for each encoding, TLS 1.3 mandate, HTTP/2 multiplexing, HTTP/3 QUIC support, HSTS requirements, SSE streaming integration. |
| T-221 | AACP-gRPC Transport Binding | DIRECT SPEC | HIGH | T-210, T-213 | Specify the gRPC binding: .proto definitions for all 42 message classes, AACPService RPC definitions (SendMessage, StreamMessages, BiStream, Handshake, GetManifest, DiscoverTools, InvokeTool), AASL-B to protobuf mapping, gRPC health checking, bidirectional streaming. |
| T-222 | AACP-WebSocket Transport Binding | DIRECT SPEC | HIGH | T-210, T-213 | Specify the WebSocket binding: binary frame support for AASL-B, connection-level handshake with AACP negotiation, heartbeat frames, automatic reconnection with exponential backoff, workflow recovery via last-known message_id, full-duplex message exchange. |
| T-223 | AACP-Stdio Transport Binding | DIRECT SPEC | MEDIUM | T-210, T-213 | Specify the stdio binding: AASL-J over stdin/stdout (NDJSON format), process lifecycle management (spawn, handshake, exchange, shutdown), local development and CLI tool integration. Replaces MCP stdio transport. |

### Phase 2B — Security (Weeks 14-24)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-230 | AACP-Auth Security Module | FULL PIPELINE | CRITICAL | T-210 | Design the unified authentication and authorization module: OAuth 2.1 client/server, mTLS configuration, API key management, Ed25519 agent identity tokens, message-level signing over canonical hashes, replay detection (message_id + timestamp + seen-message cache), agent identity verification via public key registry or Agent Manifest signing, role-based and capability-based access control. All 7 existing AASL security layers promoted to protocol enforcement. Produces a Master Tech Spec. |
| T-231 | AACP Semantic Poisoning Defense Model | DIRECT SPEC | HIGH | T-230 | Extend the existing 13-threat-category model to cover AACP v2 transport-layer attacks: malformed handshake exploitation, transport-level replay, encoding downgrade attacks, bridge-mediated injection, Agent Manifest spoofing. Define detection mechanisms and admission gates for each. |

### Phase 2C — Tool Connectivity (Weeks 14-24)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-240 | AACP Tool Connectivity Protocol | FULL PIPELINE | CRITICAL | T-211, T-212 | Design the full tool lifecycle: tool_discovery (TL{} enumeration), tool_invocation (AASL-typed parameters with ontology validation and canonicalization), tool_result (automatic semantic bundle wrapping — every result is CLM + CNF + EVD + PRV), tool_change_notification. Define input/output schema validation against AASL types. This is the core replacement for MCP tools. Produces a Master Tech Spec. |
| T-241 | AACP Resource Access Protocol | DIRECT SPEC | MEDIUM | T-211 | Specify resource_list, resource_read, resource_subscribe, resource_update message flows. Define extended DS{} with access metadata (resource_id, type, format, size, access_level, URI, last_modified, content_hash). Provenance wrapping for resource reads. |
| T-242 | AACP Elicitation & Prompting Protocol | DIRECT SPEC | MEDIUM | T-211, T-212 | Specify prompt_list, prompt_get, clarification_request, clarification_response message flows. Define PMT{} parameter resolution, typed clarification schemas, multi-turn interaction model. Replaces MCP prompts + elicitation. |
| T-243 | AACP Streaming & Push Protocol | DIRECT SPEC | HIGH | T-211, T-220, T-222 | Specify stream_begin, stream_data, stream_end, push_subscribe, push_event message flows. Define incremental_sequence numbering, progress indicators, ordered reassembly, webhook registration and delivery. Integrate with HTTP SSE and WebSocket bindings. |
| T-244 | AACP Sampling Protocol | DIRECT SPEC | LOW | T-211 | Specify sampling_request and sampling_result for server-initiated LLM invocation. Define prompt, model preferences, constraints as AASL objects. Result wrapping with model provenance. |

### Phase 3A — Bridge Architecture (Weeks 20-30)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-250 | MCP-to-AACP Universal Bridge | FULL PIPELINE | CRITICAL | T-240 | Design the bridge that wraps any MCP server as an AACP endpoint: MCP tools/list → AACP tool_discovery translation, MCP tools/call → AACP tool_invocation translation, automatic semantic enrichment (CLM, CNF, PRV, EVD wrapping of MCP JSON results), bridge-generated provenance markers distinguishing native vs bridge provenance, zero per-server configuration requirement. Produces a Master Tech Spec. |
| T-251 | A2A-to-AACP Universal Bridge | FULL PIPELINE | HIGH | T-214 | Design the bridge that wraps any A2A agent as an AACP endpoint: Agent Card → Agent Manifest translation, A2A message → AACP message translation, A2A task artifact → AASL semantic bundle conversion, capability mapping. Produces a Master Tech Spec. |

### Phase 3B — Server Framework & Ecosystem (Weeks 24-34)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-260 | AACP Native Server Framework | FULL PIPELINE | CRITICAL | T-240, T-220, T-221 | Design the server framework for building native AACP tool servers. Decorator-based API (@aacp_tool), auto-discovery registration, input validation against AASL schemas, output wrapping in semantic bundles, provenance generation, transport binding selection. 50-line target for simple tool exposure. Python/TypeScript/Rust. Framework integration adapters for FastAPI, Express, Actix. Produces a Master Tech Spec. |
| T-261 | AACP Server Registry | DIRECT SPEC | HIGH | T-260, T-214 | Specify the public registry: server manifest format, tool schema indexing, capability search, provider trust scoring (based on verification history), programmatic agent_manifest_query against global registry, authentication requirements, usage documentation format. |
| T-262 | AACP SDK Architecture | DIRECT SPEC | HIGH | T-210, T-230, T-240 | Specify the 5-module SDK architecture (aacp.transport, aacp.session, aacp.security, aacp.messaging, aacp.semantics) for Python, TypeScript, and Rust. Define AACPClient class (connect, handshake, discover, invoke, stream), AACPServer class (register, handle, serve), type-safe builder patterns for all 42 message classes. |

### Phase 3C — LLM Integration (Weeks 20-30)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-270 | LLM Generation & Constrained Decoding for AASL-T | FULL PIPELINE | HIGH | T-212 | Design the system for LLM generation of well-formed AASL-T: few-shot prompt library, EBNF/PEG constrained decoding grammar, fine-tuning dataset specification (10K+ pairs), benchmark suite (accuracy, structural validity, semantic correctness). Target: >90% structural validity with few-shot, >95% with constrained decoding. Produces a Master Tech Spec. |

### Phase 4 — Developer Experience & Governance (Weeks 30-48)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-280 | AACP Developer Tooling Suite | DIRECT SPEC | MEDIUM | T-262 | Specify: aacp-cli (curl for AACP — connect, discover, tools, send, stream, manifest commands), AACP Inspector (web-based real-time message flow visualization with semantic chain rendering), bridge management CLI, VS Code extension extensions for AACP message types. |
| T-281 | AACP Conformance & Certification Framework | DIRECT SPEC | MEDIUM | T-210, T-211, T-230 | Specify: conformance test suite (1,000+ test vectors), certification tiers, interoperability testing methodology, bridge conformance requirements, transport binding conformance matrix. Extends the existing AASL conformance framework. |
| T-282 | AACP Governance & Open-Source Release Plan | Governance | MEDIUM | T-260 | Define: Apache 2.0 release scope, SEP (Specification Enhancement Proposal) process, contributor framework, maintainer governance, foundation submission criteria (post-Phase 3 decision point), partner recruitment strategy (5 early adopters). |

### Phase 4 — Integration & Validation (Weeks 34-48)

| ID | Task | Type | Priority | Dependencies | Description |
|----|------|------|----------|-------------|-------------|
| T-290 | AACP v2 Cross-Layer Integration with Atrahasis Stack | DIRECT SPEC | HIGH | T-210, T-240, T-230 | Specify how AACP v2 integrates with: C3 Tidal Noosphere (tidal scheduling messages over AACP transport), C5 PCVM (verification_request/result as AACP messages), C7 RIF (task decomposition over AACP), C8 DSF (settlement messages), C23 SCR (execution leases), C24 FHF (cross-habitat AACP routing), C36 EMA-I (external boundary as AACP ingress). |
| T-291 | AACP v2 Justification Test Specification | DIRECT SPEC | HIGH | All Phase 3 | Define the 7 justification tests as executable benchmarks: (1) LLM accuracy >90%, (2) compactness >2x, (3) semantic reuse demonstrated, (4) transport within 5% of A2A/MCP, (5) MCP bridge wraps 100+ servers, (6) native vs bridge provenance distinguishable, (7) one-day developer onboarding. Define pass/fail criteria, measurement methodology, and fallback to Alternative A if any test fails. |

---

## Recommended Execution Order

The user should direct Claude Code to execute tasks in this sequence. Tasks at the same level can be parallelized.

**Wave 1 — Foundation (execute first, sequential)**
1. T-200 (governance decision)
2. T-201 (type registry policy)
3. T-210 (five-layer protocol — this is the master architecture everything depends on)

**Wave 2 — Core Protocol (after T-210, can parallelize)**
4. T-211 (42 message classes)
5. T-212 (new AASL types)
6. T-213 (handshake/session)
7. T-215 (lineage/canonicalization)

**Wave 3 — Transport + Security (after Wave 2, can parallelize)**
8. T-220 (HTTP binding)
9. T-221 (gRPC binding)
10. T-222 (WebSocket binding)
11. T-223 (Stdio binding)
12. T-230 (auth module)
13. T-214 (Agent Manifest)

**Wave 4 — Tool Connectivity (after T-211, T-212, T-230)**
14. T-240 (tool connectivity — the core MCP replacement)
15. T-241 (resource access)
16. T-242 (elicitation/prompting)
17. T-243 (streaming/push)
18. T-244 (sampling)
19. T-231 (poisoning defense extension)

**Wave 5 — Bridges + Framework (after T-240)**
20. T-250 (MCP bridge)
21. T-251 (A2A bridge)
22. T-260 (server framework)
23. T-270 (LLM generation)

**Wave 6 — Ecosystem + Integration (after Wave 5)**
24. T-261 (server registry)
25. T-262 (SDK architecture)
26. T-280 (developer tooling)
27. T-281 (conformance framework)
28. T-290 (cross-layer integration)

**Wave 7 — Validation + Governance (final)**
29. T-291 (justification tests)
30. T-282 (governance/open-source release)

---

## Task Count Summary

| Category | FULL PIPELINE | DIRECT SPEC | Governance | Total |
|----------|--------------|-------------|------------|-------|
| Phase 1 — Core Protocol | 3 | 3 | 2 | 8 |
| Phase 2A — Transport | 0 | 4 | 0 | 4 |
| Phase 2B — Security | 1 | 1 | 0 | 2 |
| Phase 2C — Tool Connectivity | 1 | 4 | 0 | 5 |
| Phase 3A — Bridges | 2 | 0 | 0 | 2 |
| Phase 3B — Framework/Ecosystem | 1 | 2 | 0 | 3 |
| Phase 3C — LLM Integration | 1 | 0 | 0 | 1 |
| Phase 4 — Dev Experience | 0 | 2 | 1 | 3 |
| Phase 4 — Integration | 0 | 2 | 0 | 2 |
| **Total** | **9** | **18** | **3** | **30** |

9 tasks produce full Master Tech Specs through the complete AAS invention pipeline.
18 tasks produce direct specification extensions.
3 tasks are governance/policy decisions.
