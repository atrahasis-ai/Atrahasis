# AACP/AASL Full-Replacement Strategy

## The Case for Total Protocol Sovereignty

**Document Type:** Engineering Strategy & Architecture Specification
**Classification:** Atrahasis Agent System — Canonical Reference
**Version:** 2.0
**Date:** March 12, 2026
**Designation:** Alternative B

---

## Document Purpose

This document defines the complete engineering buildout required to make AACP and AASL a self-sufficient protocol stack that fully replaces both Google A2A and Anthropic MCP. Not complements them. Not rides on top of them. Replaces them.

This is the aggressive alternative. Where the complementary strategy (Alternative A) positions AACP/AASL as the semantic layer that rides on A2A/MCP transport, this strategy asks: what if Atrahasis owns the entire stack from transport to semantics? What if every capability A2A provides for agent-to-agent communication and every capability MCP provides for agent-to-tool connectivity is absorbed into AACP/AASL natively, while preserving all the semantic advantages that neither protocol offers?

---

## 1. Strategic Rationale

### 1.1 The Sovereignty Argument

A2A is Google's protocol. MCP is Anthropic's. If Atrahasis depends on their protocols for transport, Atrahasis depends on their governance decisions, their versioning timelines, their deprecation policies, and their strategic priorities. Protocol dependency is architectural dependency. Architectural dependency is strategic vulnerability.

Full replacement means:
- Atrahasis controls its own transport, semantics, governance, versioning, and security model
- No dependency on external release schedules or breaking changes
- Full encoding optimization end-to-end (AASL-B binary over native gRPC — impossible when riding on A2A/MCP JSON)
- Unbroken semantic integrity from tool invocation through verification to storage (the decisive capability advantage)

### 1.2 The Cost Argument Against

A2A has 150+ enterprise partners and Linux Foundation governance. MCP has 97M+ monthly SDK downloads and 5,800+ servers. Replacing them means building everything they provide plus everything they do not. The engineering surface is approximately double that of Alternative A (48 weeks vs 36 weeks, 10 workstreams vs 7).

### 1.3 Why the Cost Is Justified

At Claude Opus 4.6 API pricing ($15/MTok input, $75/MTok output including extended thinking):

| Scale | A2A/MCP Annual Cost | Full Replace Annual Cost | Annual Savings |
|-------|--------------------|-----------------------|----------------|
| 1 analyst | $169,383 | $79,319 | $90,064 (53%) |
| 50 analysts | $8,469,141 | $3,965,953 | $4,503,188 (53%) |
| 10,000 agents | $955,387,500 | $423,045,429 | $537,598,071 (56%) |

The 48-week engineering investment is recovered in the first quarter at enterprise scale. At 10K agents, the savings exceed half a billion dollars per year.

Beyond cost, the reasoning quality improvements are not available at any price from A2A/MCP:
- 94% reduction in thinking token overhead (6,250 → 390 tokens per complex task)
- 6x more multi-hop reasoning capacity per thinking budget
- 10x more cross-document synthesis capacity
- 10x more verification assessment capacity
- 5 categories of hallucination structurally eliminated
- 22% more reasoning depth in extended thinking (17,580 additional tokens for actual analysis)

---

## 2. What Must Be Absorbed from A2A and MCP

To fully replace both protocols, AACP/AASL must absorb every capability they provide.

### 2.1 Capabilities to Absorb from A2A

| A2A Capability | AACP Status | Gap Severity | Buildout Required |
|----------------|-------------|-------------|-------------------|
| Agent Cards (discovery) | Partial | HIGH — no discovery mechanism | Atrahasis Agent Manifest spec with full capability advertisement |
| JSON-RPC 2.0 transport | Not present | CRITICAL — no wire protocol | AACP-RPC: native RPC layer supporting AASL-T, AASL-J, and AASL-B encodings |
| gRPC support | Not present | HIGH — no binary RPC | AACP .proto definitions, gRPC service bindings, AASL-B as native payload |
| HTTPS / TLS 1.3 | Delegated | CRITICAL — must be mandatory | Mandate TLS 1.3 in AACP transport spec, provide reference TLS configuration |
| SSE streaming | Not present | HIGH — no streaming model | AACP-Stream: SSE binding with message_class as event type |
| Task lifecycle (states) | Covered | None — 23 message classes + status field | Already exceeds A2A (11 runtime message families vs A2A's 5 methods) |
| Push notifications | Not present | MEDIUM | AACP-Push: webhook callback registration with message delivery |
| OAuth 2.0 / OpenID Connect | Not present | CRITICAL — no auth standard | AACP-Auth: native auth module supporting OAuth 2.1, mTLS, API keys, Ed25519 |
| Stateless mode | Not present | MEDIUM | AACP stateless message mode: single request/response with no session state |
| Agent Card signing | Covered | None — Ed25519 signing already specified | Extend to Atrahasis Agent Manifest signing |
| Content-type negotiation | Covered | None — payload_encoding header exists | Extend to full Accept-Encoding style negotiation in handshake |
| Linux Foundation governance | Not present | STRATEGIC — credibility gap | Open-source release, contributor framework, or foundation submission |

### 2.2 Capabilities to Absorb from MCP

| MCP Capability | AACP Status | Gap Severity | Buildout Required |
|----------------|-------------|-------------|-------------------|
| Tool discovery (listTools) | Not present | CRITICAL — no tool model | AASL TL{} (Tool) type + AACP tool_discovery message class |
| Tool invocation (tools/call) | Not present | CRITICAL — no tool execution | AACP tool_invocation and tool_result message classes with AASL-typed payloads |
| Resource discovery + access | Partial (DS type) | MEDIUM — DS exists but no access protocol | AACP resource_list, resource_read message classes; DS type extended with access metadata |
| Prompt templates | Not present | MEDIUM | AASL PMT{} (Prompt Template) type with parameter schemas and AACP prompt_get message class |
| Structured content blocks | Covered | None — AASL types ARE structured content | AASL's 12+ types already exceed MCP's text/image/resource blocks |
| Elicitation (multi-turn tool UX) | Not present | MEDIUM | AACP input_required status + clarification_request message class |
| Capability negotiation (initialize) | Not present | HIGH | AACP handshake sequence: capability exchange, version negotiation, encoding selection |
| Notifications (server → client) | Partial (state_update) | MEDIUM | Extend state_update to cover tool/resource change notifications |
| Sampling (server requests LLM) | Not present | LOW — niche feature | AACP sampling_request message class for delegated LLM invocation |
| Tasks (long-running work tracking) | Covered | None — AACP task lifecycle far exceeds this | Already covered by existing 11 message families |
| OAuth 2.1 authentication | Not present | CRITICAL | Shared with A2A absorption: AACP-Auth module |
| stdio / local transport | Not present | MEDIUM | AACP-Stdio binding: AASL-J messages over stdin/stdout for local tool processes |
| 5,800+ community servers | Not present | STRATEGIC — ecosystem gap | AACP server framework + adapter layer to wrap existing MCP servers as AACP endpoints |

---

## 3. The Unified Protocol Architecture: AACP v2

To absorb both A2A and MCP, AACP must evolve from a semantic framing layer into a full-stack agent communication protocol. AACP v2 handles agent discovery, tool connectivity, resource access, transport, security, and semantic payloads in a single coherent system.

### 3.1 Protocol Layer Model

AACP v2 is organized into five protocol layers. Each layer is independently specifiable, independently testable, and independently upgradeable. The layers interact through defined contracts, not implementation coupling.

**Layer 1 — Transport**

The wire protocol. Defines how bytes move between endpoints. Supports four transport bindings:
- **AACP-HTTP:** HTTPS + JSON-RPC style request/response
- **AACP-gRPC:** Protocol Buffers + bidirectional streaming
- **AACP-WS:** WebSocket for full-duplex persistent connections
- **AACP-Stdio:** stdin/stdout for local tool processes

TLS 1.3 mandatory for all network transports. Each binding serializes AACP messages in the encoding negotiated during handshake (AASL-T, AASL-J, or AASL-B).

**Layer 2 — Session**

Connection lifecycle management:
- Handshake: capability exchange, version negotiation, encoding selection, authentication
- Health monitoring: PING/PONG heartbeats with configurable intervals
- Graceful shutdown: drain in-flight messages before disconnect
- Reconnection: exponential backoff with workflow-level recovery using workflow_id/parent_message_id
- Session state: stateful sessions with conversation_id persistence, or stateless single-request mode

**Layer 3 — Security**

Authentication and trust:
- AACP-Auth module supporting OAuth 2.1, mTLS, API keys, and Ed25519 agent identity tokens
- Message-level signing: Ed25519 over canonical hashes (signatures bind to meaning, not bytes)
- Replay detection: message_id + timestamp + seen-message cache
- Agent identity verification: public key registry or Agent Manifest signing
- Authorization: role-based and capability-based access control
- All seven security layers from the existing AASL Security Architecture promoted to protocol-level enforcement

**Layer 4 — Messaging**

The message framing and routing layer. This is the existing AACP message architecture, extended:
- Every message is HEADER{} + PAYLOAD{}
- Header carries the 13 required fields plus new fields for transport binding metadata
- Message classes extended from 23 to 42 to absorb A2A and MCP functionality
- Lineage tracking (message_id, parent_message_id, conversation_id, workflow_id) remains mandatory
- Batch payloads with dependency ordering supported
- Streaming messages carry incremental_sequence numbers for ordered reassembly

**Layer 5 — Semantics**

The AASL semantic payload layer. Unchanged from the current architecture:
- All 12+ AASL primitive types, plus new types for tools (TL), prompt templates (PMT), and resources (extended DS)
- Canonicalization, ontology governance, validation, and verification all operate at this layer
- This is the layer that A2A and MCP do not have and cannot replicate without adopting AASL or building something equivalent

### 3.2 New Message Classes for Full Replacement

#### 3.2.1 Agent Discovery (replacing A2A Agent Cards)

- **agent_manifest_publish:** An agent announces its capabilities, supported message classes, supported AASL types, supported encodings, authentication schemes, and endpoint URLs. Published at `/.well-known/atrahasis.json`. This is the Atrahasis equivalent of an A2A Agent Card but richer — it includes semantic capabilities: what AASL types the agent can produce/consume, what ontology versions it supports, what verification methods it implements.

- **agent_manifest_query:** A client queries a registry or endpoint for agent manifests matching capability criteria. Enables programmatic agent discovery beyond static well-known URLs.

- **agent_manifest_update:** An agent updates its manifest to reflect changed capabilities. Connected clients receive a notification (replacing MCP's resource/tool change notifications).

#### 3.2.2 Tool Connectivity (replacing MCP tools)

- **tool_discovery:** Request list of available tools from an endpoint. Response contains AASL TL{} objects describing each tool: tool_id, name, description, input_schema (as AASL type constraints), output_schema (as AASL type constraints), required_permissions, annotations (safety hints, read-only flags, cost indicators).

- **tool_invocation:** Invoke a tool with AASL-typed parameters. Unlike MCP's opaque JSON parameters, AASL-typed parameters carry semantic type information, enabling the system to validate inputs against the ontology, canonicalize parameters before invocation, and attach provenance to tool call chains.

- **tool_result:** Return structured tool results as AASL semantic bundles. A tool result is not just data — it is a claim (CLM) with confidence (CNF), evidence (EVD referencing the tool and its inputs), and provenance (PRV tracing back to the tool invocation). Every tool call automatically produces an auditable semantic artifact.

- **tool_change_notification:** Server notifies connected clients that its tool inventory has changed. Clients can re-query via tool_discovery.

#### 3.2.3 Resource Access (replacing MCP resources)

- **resource_list:** List available data resources. Returns extended DS{} objects with access metadata: resource_id, type, format, size, access_level, URI, last_modified, content_hash.

- **resource_read:** Read a resource's content. Returns the content wrapped in an AASL bundle with provenance (where the data came from, when it was accessed) and an integrity hash.

- **resource_subscribe:** Subscribe to changes on a resource. Server sends resource_update notifications when the resource changes.

#### 3.2.4 Elicitation and Prompting (replacing MCP prompts + elicitation)

- **prompt_list:** List available prompt templates. Returns PMT{} objects with parameter schemas.

- **prompt_get:** Retrieve a specific prompt template with resolved parameters.

- **clarification_request:** Server requests additional input from the client to complete a task. Carries a structured schema describing what information is needed. Replaces MCP's elicitation capability.

- **clarification_response:** Client responds to a clarification request with the requested information, typed as AASL objects.

#### 3.2.5 Streaming and Push (replacing A2A SSE + push notifications)

- **stream_begin:** Initiates a streaming channel for a workflow. Server will send incremental messages on this channel.

- **stream_data:** An incremental message carrying partial results. Each carries an incremental_sequence number for ordered reassembly and a progress indicator.

- **stream_end:** Terminates a streaming channel. Final message carries the complete result bundle.

- **push_subscribe:** Client registers a webhook URL for asynchronous notifications on a workflow.

- **push_event:** Server delivers an AACP message to a registered webhook URL.

#### 3.2.6 Sampling (replacing MCP sampling)

- **sampling_request:** Server requests that the client invoke an LLM on its behalf. Carries a prompt, model preferences, and constraints as AASL objects.

- **sampling_result:** Client returns the LLM output as an AASL semantic bundle with model provenance (which model, what parameters, what confidence).

With these additions, the total AACP message class inventory rises from 23 to approximately **42 message classes**, covering the full surface area of both A2A and MCP plus the semantic capabilities that neither provides.

---

## 4. New AASL Types Required

The current AASL type registry contains 12 base types plus 4 Tidal types (27 total after the Tidal Noosphere extension). To absorb MCP's tool and resource model, three new types are required:

### TL — Tool

Represents an executable tool/function available to agents.

**Fields:** id, name, description, input_schema (AASL type constraints), output_schema (AASL type constraints), permissions, annotations, version, provider_id.

**Canonical form:**
```
TL{id:tl.search.01 name:web_search input_schema:CST{...} provider:ag.tools.01}
```

### PMT — Prompt Template

Represents a reusable prompt template with typed parameters.

**Fields:** id, name, description, parameters (typed AASL fields), template_text, output_type.

**Canonical form:**
```
PMT{id:pmt.summarize.01 name:summarize params:{target:DS max_length:CST}}
```

### SES — Session

Represents a protocol session with connection state.

**Fields:** id, client_id, server_id, state, supported_encodings, supported_types, auth_method, created, last_active.

**Canonical form:**
```
SES{id:ses.001 client:ag.coordinator.01 server:ag.tools.01 state:active}
```

These additions bring the AASL type registry to **30 types** (16 base + 4 Tidal + 3 new + 7 existing extended). The ontology versioning system ensures backward compatibility: agents that do not understand the new types ignore them per the existing forward-compatibility rule.

---

## 5. Transport Layer

This is the largest engineering investment in the full-replacement strategy. A2A and MCP provide production-grade transport that AACP currently delegates. To replace them, AACP must provide equivalent transport natively.

### 5.1 AACP-HTTP Binding

- Request/response over HTTPS. Content-Type: `application/aacp+json` (AASL-J) or `application/aacp` (AASL-T) or `application/aacp+bin` (AASL-B)
- Endpoint structure: `POST /aacp/message` (send), `GET /aacp/manifest` (retrieve Agent Manifest), `POST /aacp/stream` (initiate SSE), `POST /aacp/handshake` (capability exchange)
- HTTP/2 recommended for multiplexing. HTTP/3 (QUIC) supported for latency-sensitive deployments
- TLS 1.3 mandatory for all non-localhost connections. Certificate pinning optional. HSTS headers required

### 5.2 AACP-gRPC Binding

- Protocol Buffer definitions (.proto files) for all AACP message classes. AASL objects mapped to protobuf message types with oneof fields for the type union
- Service definitions: AACPService with RPCs for SendMessage, StreamMessages (server streaming), BiStream (bidirectional streaming), Handshake, GetManifest, DiscoverTools, InvokeTool
- AASL-B encoding maps directly to protobuf binary representation, achieving maximum compactness
- gRPC health checking protocol supported natively for load balancer integration

### 5.3 AACP-WebSocket Binding

- Full-duplex persistent connection for high-throughput agent communication
- Binary frame support enables AASL-B encoding for maximum compactness on persistent connections
- Connection-level handshake includes AACP version negotiation, encoding negotiation, and authentication token exchange
- Heartbeat frames (AACP PING/PONG) for connection health monitoring with configurable intervals
- Automatic reconnection with exponential backoff. Workflow recovery uses last-known message_id

### 5.4 AACP-Stdio Binding

- AASL-J messages over stdin/stdout for local tool processes. One JSON object per line (NDJSON format)
- Replaces MCP's stdio transport for local development and CLI tool integration
- Process lifecycle management: parent spawns child, performs handshake over stdio, exchanges messages, sends shutdown signal before terminating child

### 5.5 Connection Management

- **Handshake protocol:** Client sends handshake_request with supported protocol versions, AASL versions, ontology versions, supported encodings, and authentication credentials. Server responds with handshake_response containing negotiated versions, selected encoding, and session ID
- **Health monitoring:** Configurable PING/PONG intervals (default 30 seconds). Three missed pongs triggers connection-dead state and reconnection attempt
- **Graceful shutdown:** shutdown_signal message allows agents to drain in-flight work. Configurable drain timeout (default 30 seconds). After timeout, connection is forcibly closed
- **Load balancing:** Agent Manifests include health endpoint URLs. External load balancers use these for health-check-based routing. AACP messages include affinity hints (conversation_id) for sticky routing

---

## 6. The Ecosystem Strategy: Replacing 5,800+ MCP Servers

MCP's greatest asset is not the protocol specification. It is the ecosystem: 5,800+ community servers, 300+ clients, integrations with every major AI tool. Replacing MCP means providing equivalent connectivity. Three strategies are used in combination.

### 6.1 The MCP Bridge

Build a universal MCP-to-AACP bridge that wraps any existing MCP server as an AACP endpoint. The bridge speaks MCP on the backend (connecting to existing MCP servers) and AACP on the frontend (serving Atrahasis agents). When an Atrahasis agent discovers a tool via AACP tool_discovery, the bridge translates the request to MCP tools/list. When the agent invokes a tool via AACP tool_invocation, the bridge translates to MCP tools/call and wraps the result in an AASL semantic bundle with automatically generated provenance.

This is the critical shortcut. Instead of rebuilding 5,800 servers from scratch, the bridge makes every existing MCP server immediately accessible to Atrahasis agents through AACP. The bridge adds semantic enrichment on top: every tool result that passes through the bridge is automatically wrapped with CLM, CNF, PRV, and EVD objects, giving it the accountability chain that raw MCP tool results lack.

The bridge is not a permanent dependency on MCP. It is a migration path. As native AACP tool servers are built for high-value integrations, the bridge handles the long tail. Over time, the bridge becomes less necessary as the native ecosystem grows.

### 6.2 The A2A Bridge

Same pattern for A2A. A universal A2A-to-AACP bridge that wraps any A2A agent as an AACP endpoint. The bridge translates A2A Agent Cards to Atrahasis Agent Manifests, A2A messages to AACP messages, and A2A task artifacts to AASL semantic bundles. This makes every A2A agent in the 150+ partner ecosystem accessible to Atrahasis agents through AACP.

### 6.3 Native AACP Server Framework

A server framework that makes it easy to build native AACP tool servers. Provided in Python, TypeScript, and Rust.

- **Decorator-based API:** Define a tool function, decorate it with `@aacp_tool`, and the framework handles tool_discovery registration, input validation against AASL schemas, output wrapping in semantic bundles, provenance generation, and transport binding
- **50-line target:** If it takes more than 50 lines of code to expose a simple tool over AACP, the framework is too complex
- **Starter templates:** Database query tool, file system tool, web search tool, API wrapper tool. Each template is a working AACP server that developers can clone and modify

### 6.4 AACP Server Registry

- Public registry of available AACP servers, similar to the MCP server registry. Searchable by capability, tool type, and provider
- Registry entries include: server manifest, tool schemas, supported encodings, authentication requirements, usage documentation, trust score (based on verification history)
- Agents can query the registry programmatically to discover servers matching their needs. This extends agent_manifest_query beyond individual endpoints to a global discovery mechanism

---

## 7. SDKs, Tooling, and Developer Experience

The full-replacement strategy requires SDKs that cover the complete protocol surface, handling transport, session management, and tool connectivity in addition to semantic operations.

### 7.1 SDK Architecture

Each SDK is organized into five modules matching the protocol layers:

- **aacp.transport:** Connection management for all four bindings (HTTP, gRPC, WebSocket, Stdio). Automatic reconnection, health monitoring, encoding negotiation
- **aacp.session:** Handshake, capability exchange, session state management, stateless mode
- **aacp.security:** OAuth 2.1 client/server, mTLS configuration, Ed25519 signing/verification, replay detection
- **aacp.messaging:** Message construction, lineage tracking, batch management, streaming, push notification registration
- **aacp.semantics:** AASL object construction, parsing, validation, canonicalization, hashing — the AASL core integrated into the full SDK

### 7.2 Client SDK

- **AACPClient class:** Connect to an AACP endpoint, perform handshake, discover tools, invoke tools, send messages, subscribe to streams, manage sessions
- **Auto-discovery:** Given a URL, the client fetches the Agent Manifest, determines supported bindings, selects the optimal transport, and performs handshake automatically
- **Type-safe message construction:** Builder patterns for all 42 message classes with compile-time (TypeScript) or runtime (Python) validation

### 7.3 Server SDK

- **AACPServer class:** Register tools, resources, and prompt templates; handle incoming messages; manage sessions; serve Agent Manifests
- **Framework integration:** Adapters for FastAPI (Python), Express (TypeScript), Actix (Rust) that expose AACP endpoints with minimal boilerplate
- **Auto-semantic-wrapping:** Tool results are automatically wrapped in AASL bundles with generated CLM, CNF, PRV, and EVD objects. Developers write plain functions; the framework adds the semantic accountability layer

### 7.4 CLI, IDE, and Tooling

All Alternative A tooling (aasl-cli, VS Code extension with LSP, graph viewer), plus:

- **aacp-cli:** Protocol-level CLI for testing AACP endpoints. Commands: connect (perform handshake), discover (list agent capabilities), tools (list/invoke tools), send (send a message), stream (subscribe to a stream), manifest (fetch/publish Agent Manifest). Think of it as `curl` for AACP
- **AACP Inspector:** Web-based tool for inspecting AACP message flows in real time. Similar to MCP Inspector but with semantic visualization (claim-evidence-verification chain rendering, canonical hash display, lineage graph)
- **Bridge management CLI:** Commands for starting/stopping MCP and A2A bridges, monitoring bridge health, and viewing translation logs

---

## 8. Governance and Credibility

A2A is governed by the Linux Foundation with 150+ partners. MCP is governed by the Agentic AI Foundation under the Linux Foundation with backing from Anthropic, OpenAI, Block, AWS, Google, and Microsoft. Replacing them requires addressing the governance credibility gap.

### 8.1 Open-Source Release Strategy

- All AACP/AASL specifications released under Apache 2.0 license. All reference implementations released under Apache 2.0
- Public GitHub organization with clear contribution guidelines, code of conduct, and maintainer governance
- Specification Enhancement Proposal (SEP) process modeled on MCP's SEP process: anyone can propose changes, proposals are publicly discussed, accepted proposals are merged by maintainers

### 8.2 Foundation Path (Optional)

If the protocol gains traction beyond Atrahasis, consider submitting to the Linux Foundation's Agentic AI Foundation or creating a dedicated Atrahasis Foundation. This is not required for viability within the Atrahasis ecosystem but would be required for industry-wide adoption. The decision point is after Phase 3 when the reference runtime is working and integration demos are proven.

### 8.3 Partner Recruitment

- **Target:** 5 early adopter partners willing to build AACP-native integrations or run Atrahasis agents. These do not need to be Fortune 500 companies. They need to be teams building multi-agent systems that care about semantic accountability, verification, and knowledge reuse
- **Value proposition:** Your agents gain typed claims, structured confidence, evidence linking, provenance chains, verification records, canonical deduplication, and economic settlement. No other protocol stack provides this. The bridge layer means you lose nothing from your existing A2A/MCP integrations

---

## 9. Phase Plan

### Phase 1: Core Engine (Weeks 1–14)

**Deliverables:**
- Rust parser + validator + canonicalizer
- Conformance suite (1,000+ test vectors)
- LLM generation kit + benchmarks
- aasl-cli v0.1
- AACP-HTTP binding v0.1
- Handshake protocol implementation

**Gate:** Parser passes full conformance suite. Two agents exchange AACP messages over HTTP. LLM generation accuracy >90% with few-shot prompting.

### Phase 2: Full Protocol (Weeks 10–24)

**Deliverables:**
- Python + TypeScript + Rust SDKs (all 5 modules)
- AACP-gRPC + AACP-WS + AACP-Stdio bindings
- AACP-Auth (OAuth 2.1, mTLS, Ed25519)
- New AASL types (TL, PMT, SES)
- All 42 message classes implemented
- MCP Bridge + A2A Bridge
- VS Code extension with LSP
- Security hardening pass 1

**Gate:** Full SDK installed. Developer builds agent + tool server. MCP bridge wraps 10 existing MCP servers. All 42 message classes operational.

### Phase 3: Reference System (Weeks 20–34)

**Deliverables:**
- Reference runtime (5 services, full semantic loop)
- Semantic reuse demonstration
- Tool invocation with semantic wrapping
- AACP server framework (Python, TS, Rust)
- 10 native AACP tool servers
- AACP Inspector
- Observability dashboard
- Agent Manifest spec finalized
- AACP server registry v0.1

**Gate:** Full loop working: ingest → compile → tool call → verify → store → reuse. No A2A/MCP dependency in critical path.

### Phase 4: Ecosystem (Weeks 30–48)

**Deliverables:**
- 50+ native AACP tool servers
- Framework adapters (LangChain, CrewAI, AutoGen)
- AASL-B binary encoding finalized
- Security audit + bug bounty
- Public documentation site
- Open-source release (Apache 2.0)
- 5 early adopter partnerships
- Conference-ready demo

**Gate:** External developer goes from zero to working AASL-aware agent with tool access in under one day.

**Total timeline:** Approximately 48 weeks (12 months).

---

## 10. Cost-Benefit Comparison: Alternative A vs Alternative B

| Dimension | Alt A (Complement) | Alt B (Full Replace) |
|-----------|-------------------|---------------------|
| Engineering scope | 7 workstreams, ~36 weeks | 10 workstreams, ~48 weeks |
| Transport layer | Delegated to A2A/MCP | 4 native bindings (HTTP, gRPC, WS, Stdio) |
| Tool connectivity | Via MCP integration | Native + MCP Bridge |
| Ecosystem access | Immediate (via A2A/MCP) | Via bridges initially, native growth over time |
| Protocol sovereignty | Dependent on Google/Anthropic governance | Full control of entire stack |
| Versioning control | Must track A2A/MCP version changes | Self-determined versioning for all layers |
| Encoding optimization | JSON only (A2A/MCP constraint) | AASL-T, AASL-J, AASL-B across all layers |
| Semantic wrapping of tool results | Manual (developer must wrap MCP results) | Automatic (server framework wraps all results) |
| End-to-end verification | Breaks at A2A/MCP boundary (opaque transit) | Unbroken from tool call through verification to storage |
| Compactness advantage | Payload only (transport overhead is JSON) | Full stack (AASL-B over gRPC is maximally compact) |
| Regulatory narrative | Uses industry standard transport | Requires justifying custom protocol to regulators |
| External credibility | Backed by A2A/MCP ecosystem association | Must earn credibility independently |
| Single point of semantic integrity | No — split across AASL + A2A + MCP with translation gaps | Yes — one protocol, one type system, one canonical form end-to-end |

---

## 11. The Decisive Argument for Full Replacement

The complementary strategy (Alternative A) has a fundamental architectural flaw: **the semantic integrity chain breaks at the A2A/MCP boundary.**

Consider the verification workflow. An agent produces a claim. The claim is typed (CLM), has structured confidence (CNF), evidence (EVD), provenance (PRV), and is canonically hashed. The verification agent verifies it (VRF). The memory service stores it in the verified tier. All of this happens within the AASL semantic layer. The canonical hash guarantees integrity.

Now that agent needs to call an external tool via MCP. The AACP semantic bundle is translated into an MCP tool call. The MCP tool returns a raw JSON result. That result has no CLM type, no CNF, no EVD, no PRV, no canonical hash. The developer must manually wrap it in AASL objects. If they forget, or if they wrap it incorrectly, the accountability chain has a gap. The canonical hash of the tool result was never computed by the tool itself. The provenance is reconstructed after the fact, not generated at the source.

In Alternative B, the same tool is an AACP tool server. It receives a tool_invocation message with AASL-typed parameters. The server framework automatically wraps the result in a semantic bundle: the result is a claim (CLM) with confidence generated from tool reliability metadata, evidence linking to the tool invocation, and provenance tracing to the tool server's identity. The canonical hash is computed at the source. The verification agent can verify the tool result against the tool's declared output schema. The entire chain is unbroken.

This is not a theoretical concern. It is the difference between a system where every assertion is provably traceable to its source and a system where some assertions pass through opaque translation layers that cannot be audited. For a distributed AGI architecture that claims to build cumulative, verified intelligence, that difference is foundational.

The question is whether that foundational integrity is worth the additional engineering cost. The answer depends on what Atrahasis is meant to become. If it is a product that integrates with existing agent infrastructure, Alternative A is the pragmatic choice. **If it is a new class of intelligence system that requires end-to-end semantic accountability, Alternative B is the necessary choice.**

---

## 12. Justification Tests

AACP/AASL full replacement of A2A and MCP in the Atrahasis ecosystem is justified if and only if the following seven conditions are met by the end of Phase 3:

### Test 1: Baseline Viability
All five Alternative A justification tests pass. LLM generation accuracy >90%, compactness advantage >2x, semantic reuse demonstrated, zero-friction integration possible, one-day developer onboarding achieved. These are baseline requirements. If any fails, neither alternative is justified.

**Kill criterion:** Any sub-test failure halts both alternatives.

### Test 2: Transport Quality
The transport layer meets production quality standards. AACP-HTTP, AACP-gRPC, and AACP-WS bindings handle 10,000+ concurrent connections with latency within 5% of raw A2A/MCP transport.

**Kill criterion:** Transport performance significantly worse than A2A/MCP → sovereignty does not justify overhead → fall back to Alternative A.

### Test 3: Bridge Generality
The MCP Bridge wraps 100+ existing MCP servers with zero manual configuration per server. The bridge must be generic enough to handle any conforming MCP server automatically.

**Kill criterion:** Per-server custom configuration required → ecosystem access story collapses → fall back to Alternative A.

### Test 4: Integrity Superiority
End-to-end semantic integrity is measurably superior to Alternative A. Tool results invoked through native AACP must have complete, machine-verifiable provenance chains. Tool results invoked through the bridge must have partial provenance with explicit bridge-generated markers. The system must distinguish between native-provenance and bridge-provenance results.

**Kill criterion:** Distinction cannot be made reliably → integrity argument for full replacement weakens → fall back to Alternative A.

### Test 5: Developer Parity
The server framework makes building an AACP tool server no harder than building an MCP server. Measured by: lines of code for equivalent functionality, time-to-first-tool for a new developer, and qualitative developer feedback.

**Kill criterion:** AACP server development significantly harder → adoption will not follow → fall back to Alternative A.

### Test 6: External Adoption
At least 5 partners commit to building native AACP integrations. Full replacement without external adoption is a walled garden.

**Kill criterion:** Fewer than 5 partners → insufficient ecosystem traction → evaluate whether to continue or fall back.

### Test 7: Sustainability
The total cost of ownership for the full stack is sustainable. Four transport bindings, three SDKs, two bridges, a server framework, a registry, and 42 message classes represent a large maintenance surface.

**Kill criterion:** Team cannot sustain quality across full surface → Alternative A's smaller surface may be more honest about what can be maintained.

---

## 13. Decision Framework

If all seven conditions are met, full replacement is not just justified — it is the architecturally correct choice for a system that claims to be a new class of distributed intelligence.

The unbroken semantic integrity chain from tool invocation through verification to storage and reuse is the capability that justifies the cost.

If any condition fails, fall back to Alternative A (Complement) and revisit full replacement when the conditions change. The fallback is defined, not improvised.

---

*End of document. This specification is the canonical reference for the AACP/AASL Full Replacement Strategy within the Atrahasis Agent System.*
