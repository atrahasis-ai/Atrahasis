# Master Tech Spec: A2A-to-AACP Universal Semantic Bridge
**Invention ID:** C46 (Originating from T-251)
**Stage:** SPECIFICATION
**Domain:** Protocol Translation / Identity Bridging
**Supersedes:** Legacy static A2A proxies

---

## 1. Executive Summary

The A2A-to-AACP Universal Bridge (C46) facilitates the secure, high-fidelity migration of legacy Agent-to-Agent (A2A) and Model Context Protocol (MCP) clients into the native Atrahasis Agent Communication Protocol (AACP) network. 

Rather than relying on brittle, static translation dictionaries, the C46 Bridge operates as a **Semantic Projection Membrane**. It uses an LLM during the initial connection handshake to dynamically compile a deterministic translation schema (the `AASL-Map`). Furthermore, it defines a new identity primitiveâ€”the **Ephemeral Bridge Envelope (EBE)**â€”allowing legacy agents to interact with native C42 tool meshes without violating C40 trust boundaries.

---

## 2. The Ephemeral Bridge Envelope (EBE)

To allow an external A2A agent to interact with internal AACP resources, the bridge must grant it identity without granting it unauthorized trust.

### 2.1 EBE Instantiation
When a legacy agent connects via the bridge, the bridge issues a `C32` Identity request on its behalf, explicitly tagged with the `PROVENANCE: BRIDGED_EXTERNAL` flag.
The resulting identity object is an **Ephemeral Bridge Envelope (EBE)**.
- The EBE has a strict TTL (Time-To-Live) matching the transport session.
- The EBE cannot sign native `SP-NATIVE-ATTESTED` claims. It is permanently downgraded to `SP-BRIDGED-UNVERIFIED` in the C40 dual-anchor authority fabric.

### 2.2 Tool Execution Bounding
When an EBE requests a tool execution on the C42 Lease-Primed Execution Mesh, the C42 layer reads the `BRIDGED_EXTERNAL` provenance. The execution lease is automatically downgraded:
- Rate limits are reduced by 90% relative to native agents.
- High-consequence mutations (e.g., database writes, ledger commits) require mandatory Human-in-the-Loop (HITL) elevation or native agent co-signing.

---

## 3. Dynamic Semantic Projection (AASL-Map)

Legacy A2A JSON payloads do not map neatly to AACP's strict AASL semantic bundles. Static mapping fails at scale. C46 solves this by separating the translation logic into a slow-path handshake and a fast-path router.

### 3.1 The Slow-Path Handshake (LLM Compilation)
1. **Ingestion:** The legacy agent connects and submits its initialization payload (e.g., an A2A "Agent Card" or MCP "Initialize" request).
2. **Galois Projection:** The bridge routes this initialization payload to an internal LLM (The Projection Engine).
3. **Compilation:** The LLM analyzes the specific shapes, intents, and capabilities described by the legacy agent and compiles them into a static, deterministic routing table called an **AASL-Map**. 
4. **Validation:** The AASL-Map is validated against the C39 operational semantics schema. If valid, it is cached in memory.

### 3.2 The Fast-Path Routing (Deterministic)
Once the AASL-Map is compiled, the LLM is removed from the loop.
- Incoming real-time A2A messages are routed through the fast, in-memory AASL-Map.
- The map deterministically transforms the JSON fields into valid AACP LCML buffers in less than 2 milliseconds.
- This satisfies the C38 throughput requirements while maintaining high semantic fidelity.

---

## 4. Required Architecture Expansion

To support the dynamic compilation of AASL-Maps during the handshake, this specification requires an update to the `C44` (AASL-T Constrained Generation Engine). `C44` must be expanded to include the specific `AASL-Map` output constraints and few-shot prompt libraries required by the C46 bridge. This ensures the LLM generates valid routing tables.