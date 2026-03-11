# C4-A Landscape Analysis: AI-to-AI Communication via Semantic JSON Vocabulary

**Analyst:** Landscape Analyst
**Date:** 2026-03-09
**Subject:** Competitive landscape for C4-A -- extracting AASL's semantic model (provenance chains, claim classification, confidence tracking, typed tokens) into a JSON Schema vocabulary over standard transports (AACP)

---

## Executive Summary

The AI agent communication landscape has consolidated rapidly between 2024 and early 2026. Two dominant protocols -- MCP (Anthropic, tool-to-agent) and A2A (Google, agent-to-agent) -- have achieved industry convergence under the Linux Foundation's Agentic AI Foundation (AAIF). Both are JSON-based, transport-agnostic, and backed by every major AI provider. Neither provides native support for provenance chains, claim classification, confidence tracking, or typed semantic tokens -- the core differentiators C4-A proposes.

C4-A's strategic window is narrow but genuine: the semantic verification layer that sits above existing protocols. The risk is building a competing protocol; the opportunity is building a complementary vocabulary that plugs into the protocols that have already won.

---

## 1. AI Agent Communication Frameworks (2024-2026)

### 1.1 Google A2A (Agent-to-Agent Protocol)

- **Launched:** April 2025; donated to Linux Foundation June 2025
- **Format:** JSON-RPC over HTTP/SSE, with gRPC support added later
- **Core primitives:** Agent Cards (capability discovery), Tasks (lifecycle management), Messages (context exchange), Artifacts (output objects)
- **Adoption:** 100+ enterprise partners including Salesforce, SAP, ServiceNow, PayPal
- **Governance:** Linux Foundation Agentic AI Foundation (AAIF)
- **Provenance/confidence:** Agent Card signing via JWS (RFC 7515); audit logs with timestamps; trust scoring described at a high level but not deeply specified as structured semantic objects
- **Key gap for C4-A:** No typed claim objects, no first-class confidence distributions, no provenance chain primitives

Sources: [Google A2A Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/), [A2A Protocol Spec](https://a2a-protocol.org/latest/specification/), [Linux Foundation A2A Launch](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)

### 1.2 Anthropic MCP (Model Context Protocol)

- **Launched:** November 2024; donated to AAIF December 2025
- **Format:** JSON-RPC 2.0 over STDIO and HTTP transports
- **Core primitives:** Tools, Resources, Prompts (server-side); Roots, Sampling (client-side)
- **Adoption:** 97M+ monthly SDK downloads (Python + TypeScript); adopted by OpenAI, Google, Microsoft, Amazon, AWS
- **Governance:** AAIF (co-founded by OpenAI, Anthropic, Google, Microsoft, AWS, Block)
- **Schema:** Defined in TypeScript, published as JSON Schema
- **Provenance/confidence:** OAuth 2.0 Resource Server security model (v2025-06-18); no semantic provenance or confidence primitives
- **Key gap for C4-A:** MCP connects agents to tools, not agents to agents. No claim verification, no confidence tracking, no typed semantic tokens

Sources: [MCP Specification](https://modelcontextprotocol.io/specification/2025-11-25), [Anthropic MCP Announcement](https://www.anthropic.com/news/model-context-protocol), [MCP Spec Update](https://forgecode.dev/blog/mcp-spec-updates/)

### 1.3 OpenAI Structured Outputs / Function Calling

- **Format:** JSON Schema with `strict: true` mode
- **Mechanism:** Constrained decoding ensures model output conforms exactly to a provided JSON Schema
- **SDK support:** Pydantic (Python), Zod (JavaScript) for schema definition
- **Provenance/confidence:** None. Structured outputs guarantee format conformance, not semantic properties
- **Key gap for C4-A:** Pure format enforcement with no semantic vocabulary layer

Sources: [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs/), [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

### 1.4 Microsoft AutoGen / Agent Framework

- **Status:** AutoGen v0.4 reimagined; converging with Semantic Kernel into "Microsoft Agent Framework" targeting GA Q1 2026
- **Communication:** Asynchronous messages with event-driven and request/response patterns; cross-language (Python, .NET)
- **Standards adoption:** Native MCP, A2A, and OpenAPI integration
- **Observability:** OpenTelemetry support for message tracing
- **Provenance/confidence:** Metric tracking and message tracing via OpenTelemetry, but no semantic provenance primitives
- **Key gap for C4-A:** Framework-level agent orchestration, not a semantic vocabulary

Sources: [AutoGen v0.4](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/), [Agent Framework Migration](https://learn.microsoft.com/en-us/agent-framework/migration-guide/from-autogen/)

### 1.5 LangGraph / CrewAI

- **LangGraph:** Graph-based state machine; agents communicate indirectly via shared state. No native protocol support. Tightly coupled to LangChain ecosystem.
- **CrewAI:** Role-based agent collaboration; added A2A protocol support. Natural language inter-agent communication with task delegation.
- **Provenance/confidence:** Neither provides structured provenance or confidence primitives
- **Key gap for C4-A:** Orchestration frameworks, not communication standards

Sources: [CrewAI vs LangGraph comparison](https://zams.com/blog/crewai-vs-langgraph), [Framework Comparison 2026](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared)

### 1.6 IBM ACP (Agent Communication Protocol)

- **Launched:** March 2025 by IBM Research for BeeAI Platform
- **Status:** Merged into A2A under Linux Foundation, August 2025
- **Significance:** Demonstrates that competing agent protocols consolidate quickly toward dominant standards. ACP brought simplicity; A2A brought features and industry backing. The merged result is A2A.

Sources: [ACP Joins A2A](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/), [ACP Overview](https://www.ibm.com/think/topics/agent-communication-protocol)

---

## 2. Legacy Agent Communication Standards

### 2.1 FIPA ACL

- **Origin:** Foundation for Intelligent Physical Agents, 1996
- **Basis:** Speech act theory (Searle, Winograd/Flores)
- **Format:** S-expression-based messages with performatives (inform, request, query, propose)
- **What worked:** Formal semantics grounded in theory; interoperability goal was correct
- **Why it failed:** Overly formal; adoption waned as the web exploded; complexity of integration with legacy systems; agents gave way to service-oriented architectures (SOA/REST)

### 2.2 KQML (Knowledge Query and Manipulation Language)

- **Origin:** DARPA Knowledge Sharing Effort, 1990
- **Format:** S-expression performatives
- **What worked:** Pioneered the concept of typed inter-agent messaging
- **Why it failed:** Insufficient primitives for fine-grained interaction; dialect fragmentation (different KQML implementations could not interoperate, defeating the purpose); brittle error handling; no scalability for real-world deployment

### 2.3 Lessons for C4-A

| Failure Mode | FIPA/KQML | C4-A Risk |
|---|---|---|
| Over-specification before implementation | FIPA had extensive specs, low adoption | C4-A must ship working code alongside spec |
| Dialect fragmentation | KQML spawned incompatible variants | JSON Schema + vocabulary pinning mitigates this |
| Ignoring dominant paradigms | Both ignored the web/REST revolution | C4-A must build on top of A2A/MCP, not beside them |
| Excessive formalism | Speech-act semantics too academic | C4-A should be pragmatic: JSON vocabularies, not formal logics |
| No ecosystem incentive | No killer app drove adoption | C4-A needs a concrete use case (e.g., regulated AI audit trails) |

Sources: [Agent Communication Language (Wikipedia)](https://en.wikipedia.org/wiki/Agent_Communications_Language), [FIPA ACL Overview](https://smythos.com/developers/agent-development/fipa-agent-communication-language/)

---

## 3. Semantic Web / Linked Data Standards

### 3.1 JSON-LD

- **Status:** W3C Recommendation; dominant structured data format on the web
- **Adoption:** Used by 70% of websites with structured data (~11.5M domains); 45M+ web domains use Schema.org markup
- **Relevance to C4-A:** JSON-LD provides the `@context` mechanism for semantic vocabulary extension. C4-A's typed tokens (CLM, EVD, CNF, PRV, VRF) could be defined as a JSON-LD vocabulary, inheriting all existing tooling
- **Risk:** JSON-LD adds verbosity and complexity; most AI agent frameworks use plain JSON, not JSON-LD

### 3.2 W3C PROV (Provenance Ontology)

- **Status:** W3C Recommendation (PROV-O, PROV-DM, PROV-N)
- **Relevance to C4-A:** Directly addresses provenance chains with standardized concepts: Entity, Activity, Agent, wasGeneratedBy, wasDerivedFrom, wasAttributedTo
- **Assessment:** C4-A's provenance chain primitive (PRV) maps naturally onto PROV-O. Using PROV-O as the underlying ontology would provide immediate interoperability with existing provenance systems

### 3.3 W3C Verifiable Credentials 2.0

- **Status:** W3C Recommendation as of May 2025
- **Format:** JSON-LD with cryptographic proofs
- **Relevance to C4-A:** Directly applicable to C4-A's verification (VRF) and evidence (EVD) primitives. VCs provide cryptographically verifiable claims -- exactly what C4-A's claim classification needs
- **Active research:** Papers on equipping AI agents with DIDs and Verifiable Credentials for authentication and trust establishment across domains

### 3.4 W3C Activity Streams 2.0

- **Status:** W3C Recommendation
- **Relevance to C4-A:** Provides a JSON-LD vocabulary for describing actions and activities -- analogous to C4-A's action (ACT) and task (TSK) tokens

### 3.5 W3C AI Agent Protocol Community Group

- **Formed:** May 2025; first meeting June 2025
- **Focus:** Open protocols for agent discovery, identity, and collaboration on the web
- **Also:** "Semantic Agent Communication Community Group" proposed November 2025
- **Relevance to C4-A:** Directly overlapping scope. C4-A should monitor and potentially contribute to these groups

Sources: [W3C VC 2.0](https://www.w3.org/press-releases/2025/verifiable-credentials-2-0/), [W3C AI Agent Protocol CG](https://www.w3.org/community/agentprotocol/), [JSON-LD adoption](https://wpnewsify.com/blog/json-ld-at-scale-schemas-that-move-the-needle-in-2025/), [Schema.org stats](https://webdatacommons.org/structureddata/)

---

## 4. Emerging Standards and Transport

### 4.1 OpenAPI / AsyncAPI

- **OpenAPI:** RESTful API description standard; already used by A2A for Agent Card schemas
- **AsyncAPI:** OpenAPI equivalent for event-driven APIs; defines channels, messages, and schemas for pub/sub patterns
- **Relevance to C4-A:** Agent APIs using C4-A vocabulary could be described with OpenAPI/AsyncAPI, providing automatic documentation, client generation, and validation

### 4.2 CloudEvents

- **Status:** CNCF graduated project
- **Format:** Standard envelope for event metadata (source, type, id, time) with arbitrary data payload
- **Relevance to C4-A:** C4-A messages could be wrapped in CloudEvents envelopes for interoperability with cloud-native event systems (Kafka, Knative, etc.)

### 4.3 NATS / MQTT / Kafka as Transport

- **NATS:** Lightweight, cloud-native; supports pub/sub, request/reply, queue groups; JWT + NKey auth
- **MQTT:** IoT-focused; lightweight pub/sub; less suited to complex agent interactions
- **Kafka:** High-throughput event streaming; used with A2A+MCP in production deployments
- **IETF draft:** "An Overview of Messaging Systems and Their Applicability to Agentic AI" (draft-mpsb-agntcy-messaging-00) formally evaluates AMQP, MQTT, NATS, Kafka, and WebSockets for agent systems
- **Relevance to C4-A:** C4-A should be transport-agnostic. JSON vocabulary works over any of these transports.

Sources: [AsyncAPI + CloudEvents](https://www.asyncapi.com/blog/asyncapi-cloud-events), [IETF Agent Messaging Draft](https://www.ietf.org/archive/id/draft-mpsb-agntcy-messaging-00.html)

---

## 5. Industry Adoption and Standards Trajectory

### 5.1 What Format Do Most AI Agents Use Today?

**JSON dominates.** Every major framework (A2A, MCP, OpenAI function calling, AutoGen, CrewAI) uses JSON as the wire format. JSON-RPC is the specific variant used by both MCP and A2A. No production agent framework uses a custom syntax.

### 5.2 A2A vs MCP: Complementary, Not Competing

The market has settled this question. MCP and A2A are complementary:

| Dimension | MCP | A2A |
|---|---|---|
| **Purpose** | Agent-to-tool connectivity | Agent-to-agent collaboration |
| **Analogy** | USB for AI (plug in data/tools) | HTTP for AI (agents talk to agents) |
| **Direction** | Vertical (agent reaches down to resources) | Horizontal (agents collaborate as peers) |
| **Monthly SDK downloads** | 97M+ (Feb 2026) | Growing, 100+ enterprise partners |
| **Governance** | AAIF (Linux Foundation) | AAIF (Linux Foundation) |
| **Backing** | All major AI providers | All major AI providers |

### 5.3 The Consolidation Pattern

The agent protocol space is consolidating, not fragmenting:

- IBM's ACP merged into A2A (August 2025)
- Both MCP and A2A donated to AAIF (December 2025)
- NIST announced AI Agent Standards Initiative (February 2026)
- W3C formed AI Agent Protocol Community Group (May 2025)

This consolidation makes it extremely difficult for new competing protocols to gain adoption. It also creates a clear opportunity for complementary specifications that add capabilities the dominant protocols lack.

### 5.4 The Gap in the Market

No existing protocol provides:

| Capability | A2A | MCP | OpenAI | AutoGen | C4-A Proposal |
|---|---|---|---|---|---|
| First-class claim objects (CLM) | No | No | No | No | **Yes** |
| Typed confidence tracking (CNF) | Partial (trust scores) | No | No | No | **Yes** |
| Provenance chains (PRV) | Audit logs only | No | No | OpenTelemetry traces | **Yes** |
| Evidence linking (EVD) | No | No | No | No | **Yes** |
| Verification records (VRF) | JWS on Agent Cards | OAuth 2.0 | No | No | **Yes** |
| Claim classification taxonomy | No | No | No | No | **Yes** |
| Dual representation (source + canonical) | No | No | No | No | **Yes** |
| Semantic identity for objects | Agent Cards (agents only) | No | No | No | **Yes (all objects)** |

---

## 6. Competitive Positioning for C4-A

### 6.1 Strategic Options

| Strategy | Description | Risk | Reward |
|---|---|---|---|
| **A. Vocabulary extension** | Define C4-A types as a JSON Schema vocabulary / JSON-LD context that plugs into A2A and MCP messages | Low | High interoperability, low adoption friction |
| **B. Standalone protocol** | Build C4-A as an independent protocol competing with A2A/MCP | Very high | Only viable if backed by a major platform vendor |
| **C. W3C standards track** | Contribute C4-A primitives to W3C AI Agent Protocol CG | Medium | Legitimacy, but slow timeline |
| **D. Overlay specification** | Define C4-A as a "profile" or extension of A2A that adds semantic verification | Low-medium | Clear positioning, leverages A2A ecosystem |

**Recommended: Strategy A + D combined.** Define C4-A as a JSON Schema vocabulary that can be used as:
1. An extension to A2A Task/Message artifacts (overlay)
2. An extension to MCP Tool responses (vocabulary)
3. A standalone schema for semantic objects (persistence layer)

### 6.2 Concrete Positioning

```
                    ┌─────────────────────────────────┐
                    │     Application / Agent Logic     │
                    └────────────┬────────────────────┘
                                 │
                    ┌────────────▼────────────────────┐
                    │   C4-A Semantic Vocabulary        │
                    │   (CLM, EVD, CNF, PRV, VRF)      │
                    │   JSON Schema + JSON-LD context   │
                    └────────────┬────────────────────┘
                                 │
              ┌──────────────────┼──────────────────────┐
              │                  │                       │
     ┌────────▼───────┐  ┌──────▼───────┐   ┌──────────▼──────┐
     │  A2A Messages   │  │ MCP Tool     │   │ Standalone      │
     │  (agent-agent)  │  │ Responses    │   │ Persistence     │
     │  JSON-RPC/HTTP  │  │ JSON-RPC     │   │ JSON documents  │
     └─────────────────┘  └──────────────┘   └─────────────────┘
```

### 6.3 What C4-A Should Borrow From Existing Standards

| C4-A Primitive | Existing Standard to Align With | Rationale |
|---|---|---|
| PRV (Provenance) | W3C PROV-O ontology | Mature, widely implemented provenance model |
| VRF (Verification) | W3C Verifiable Credentials 2.0 | Cryptographic proof standard, just published |
| CLM (Claim) | VC Data Model claim structure | Claims are the core VC primitive |
| EVD (Evidence) | VC evidence property | Already defined in VC spec |
| CNF (Confidence) | No existing standard | **Genuine novel contribution** |
| AGT (Agent) | A2A Agent Card schema | Align identity model with dominant protocol |
| TSK (Task) | A2A Task schema | Align lifecycle with dominant protocol |
| ACT (Action) | W3C Activity Streams 2.0 | Existing vocabulary for actions |
| TIM (Timestamp) | RFC 3339 / ISO 8601 | Universal timestamp format |

### 6.4 What C4-A Should NOT Do

1. **Do not create a custom syntax.** JSON has won. Every production agent framework uses it. The AASL `AGT{id:ag.r1}` syntax has zero pre-training support in LLMs and zero tooling.
2. **Do not build a competing protocol.** A2A and MCP are under the Linux Foundation with backing from all major AI providers. ACP tried to compete and was absorbed in 5 months.
3. **Do not over-specify before implementation.** FIPA ACL and KQML died from over-specification. Ship a working vocabulary, then iterate.
4. **Do not require a custom parser.** Use standard JSON Schema validation. Every language has it.
5. **Do not assume centralized ontology governance.** Decentralized, namespace-based vocabulary extension (like JSON-LD contexts) scales better than centralized registries.

### 6.5 Defensibility Analysis

| C4-A Feature | Defensible? | Why |
|---|---|---|
| First-class confidence distributions | **Strong** | No existing standard addresses this. Novel contribution. |
| Claim classification taxonomy | **Strong** | No agent protocol classifies claim types semantically. |
| Provenance chains as structured objects | **Moderate** | PROV-O exists but is not integrated into any agent protocol. First mover in agent context. |
| Verification records | **Moderate** | VCs exist but are not yet standard in agent communication. Integration is the contribution. |
| Typed semantic tokens as JSON Schema | **Weak alone** | JSON Schema vocabularies are a known pattern. Value is in the specific vocabulary, not the mechanism. |
| Dual representation | **Moderate** | Useful for audit/regulatory contexts. Not addressed by competitors. |

---

## 7. Timeline and Market Context

| Date | Event | Impact on C4-A |
|---|---|---|
| Nov 2024 | Anthropic launches MCP | Tool connectivity standard established |
| Apr 2025 | Google launches A2A | Agent-to-agent standard established |
| May 2025 | W3C AI Agent Protocol CG formed | Standards body engaging with agent protocols |
| Jun 2025 | A2A donated to Linux Foundation | Neutral governance for agent-agent protocol |
| Aug 2025 | IBM ACP merges into A2A | Demonstrates consolidation velocity |
| Nov 2025 | W3C Semantic Agent Communication CG proposed | Validates need for semantic layer |
| Dec 2025 | MCP donated to AAIF; AAIF formed | Both dominant protocols under single foundation |
| Feb 2026 | NIST AI Agent Standards Initiative | Government-level standards engagement |
| Mar 2026 | **C4-A analysis (current)** | Window for semantic vocabulary contribution |

**Assessment:** C4-A is entering the market at a moment of protocol consolidation (A2A + MCP have won the transport/protocol layer) but semantic standardization is still open (W3C groups are forming, no vocabulary standard exists for agent claims/confidence/provenance). The window is approximately 12-18 months before the W3C groups or A2A extensions address this gap organically.

---

## 8. Key Recommendations

1. **Reframe C4-A as a vocabulary, not a protocol.** The protocol wars are over. A2A and MCP won. C4-A's value is the semantic types (CLM, EVD, CNF, PRV, VRF), not the transport.

2. **Publish as JSON Schema + JSON-LD context.** This gives maximum interoperability with zero custom tooling required.

3. **Align provenance and verification primitives with W3C standards** (PROV-O, Verifiable Credentials 2.0). Do not reinvent these.

4. **Focus on confidence tracking as the novel contribution.** No existing standard addresses structured confidence distributions for AI agent claims. This is C4-A's strongest differentiator.

5. **Build a reference implementation as an A2A extension.** Demonstrate C4-A vocabulary carried inside A2A Task artifacts. This provides immediate credibility and adoption path.

6. **Target regulated industries first.** Financial services, healthcare, and government AI deployments need auditable provenance and verified claims. This is where the vocabulary has immediate value.

7. **Engage with W3C AI Agent Protocol CG and Semantic Agent Communication CG.** Contribute C4-A concepts before these groups converge on their own vocabulary.

8. **Ship code before spec.** The AASL pattern of 24,000 lines of specification with no implementation is the highest-risk path. C4-A should ship a 200-line JSON Schema vocabulary with a working validator and 3 integration examples before writing extensive documentation.
