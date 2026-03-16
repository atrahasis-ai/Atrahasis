# T-240 Prior Art Report

## Scope

Evaluate prior art relevant to `C42` `Lease-Primed Execution Mesh (LPEM)`:
- native tool discovery and invocation,
- long-lived or warm protocol channels,
- partial and progressive result reporting,
- workload identity continuity,
- and invocation-to-execution handoff patterns.

This report uses primary sources only:
- MCP official specification,
- JSON-RPC 2.0 specification,
- gRPC official documentation,
- HTTP/2 RFC,
- LSP official specification,
- SPIFFE official overview,
- and the current Atrahasis canonical specs (`C39`, `C40`, `C41`, `C23`).

## Primary comparison set

### 1. MCP tools and streamable HTTP transport

Source:
- `https://modelcontextprotocol.io/specification/2025-06-18/server/tools`
- `https://modelcontextprotocol.io/specification/2025-06-18/basic/transports`

Contribution:
- explicit `tools/list`, `tools/call`, and `notifications/tools/list_changed`
- schema-described tool inputs and optional output schemas
- a practical baseline for tool discovery, invocation, and change signaling

Limitation:
- the official Streamable HTTP transport requires every client JSON-RPC message
  to be a new HTTP `POST`, even when the server can optionally stream messages
  back over SSE
- the tool layer does not define invocation-to-runtime continuity, lease handoff,
  or strong provenance/accountability semantics
- tool annotations are not trust-bearing by default

Relevance:
- direct baseline that `T-240` is replacing

### 2. JSON-RPC 2.0

Source:
- `https://www.jsonrpc.org/specification`

Contribution:
- stable request/response correlation
- notifications with no reply
- optional batch shape

Limitation:
- transport-neutral envelope only
- no semantic tool identity, no result accountability contract, no policy model,
  and no continuation or runtime handoff semantics

Relevance:
- useful base interaction pattern but not a sufficient native tool protocol

### 3. gRPC core concepts and keepalive

Source:
- `https://grpc.io/docs/what-is-grpc/core-concepts/`
- `https://grpc.io/docs/guides/keepalive/`

Contribution:
- typed service methods
- unary, client-streaming, server-streaming, and bidirectional streaming RPCs
- deadlines/timeouts
- long-lived channels and keepalive patterns over HTTP/2

Limitation:
- method-centric RPC, not tool-lifecycle semantics
- no built-in tool inventory, change-notification, or provenance-accountability
  model
- no native distinction between invocation and governed downstream execution

Relevance:
- strongest prior art for warm channels, low repeated setup cost, and streaming
  coordination

### 4. HTTP/2 multiplexing

Source:
- `https://www.rfc-editor.org/rfc/rfc9113`

Contribution:
- multiplexed independent streams on one connection
- flow control and prioritization
- header compression and optional server push

Limitation:
- transport capability only
- does not answer tool identity, authorization, provenance, or execution-policy
  handoff

Relevance:
- validates the transport-side feasibility of high-throughput, low-turn tool
  interactions without requiring one request per cold-start connection

### 5. Language Server Protocol (LSP)

Source:
- `https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/`

Contribution:
- long-lived client/server protocol over structured messages
- server-initiated progress
- partial result tokens and progressive result emission

Limitation:
- optimized for editor/server cooperation rather than governed tool execution
- does not define execution leases, trust floors, or explicit capability-grant
  semantics

Relevance:
- strong prior art for continuation-style work, partial result signaling, and
  token-based progress over one durable protocol relationship

### 6. SPIFFE

Source:
- `https://spiffe.io/docs/latest/spiffe-about/overview/`

Contribution:
- short-lived workload identities (`SVIDs`)
- mutual authentication across dynamic environments
- automatic rotation through workload-facing APIs

Limitation:
- identifies workloads, not tool executions
- does not define tool discovery, invocation continuity, or accountable result
  semantics

Relevance:
- important prior art for warm trust establishment and short-lived identity
  continuity that can feed lease-primed execution contexts

### 7. Existing Atrahasis substrate

Canonical repo sources:
- `C39` contributes the message-family authority for `tool_discovery`,
  `tool_invocation`, `tool_result`, and `tool_change_notification`
- `T-212` contributes `TL{}` as the semantic tool descriptor
- `C40` contributes capability grants and the no-ambient-authority rule
- `C41` contributes signed manifest disclosure of tool capability surfaces
- `C23` contributes lease-bound runtime execution

Limitation:
- these pieces exist separately but are not yet composed into one
  performance-first native tool protocol that can prime governed execution

Relevance:
- direct architectural lineage for `C42`

## What is not novel in C42

- cacheable discovery snapshots by themselves
- persistent authenticated channels by themselves
- bidirectional streaming by itself
- progress tokens or partial result notifications by themselves
- short-lived workload identity by itself
- lease-bound runtime execution by itself

## What is novel enough to justify C42

`C42` is justified only if it delivers an Atrahasis-specific composition that
mainstream tool protocols do not currently provide:

1. a native tool lifecycle grounded in `C39` and `TL{}`,
2. performance-oriented reuse of discovery, trust, and invocation context,
3. explicit continuation or execution-ready contexts that remain policy-visible,
4. deterministic accountability wrapping for results,
5. and a lawful handoff from protocol invocation into `C23` runtime leases
   without ambient authority.

That combination is materially different from:
- MCP's list/call/notification baseline,
- gRPC's high-performance method invocation,
- LSP's progressive long-lived collaboration,
- or SPIFFE's workload-identity substrate.

## Prior-art destruction attempts

### Claim: "This is just MCP with caching"
- Rebuttal: caching tool inventory does not create a governed execution-ready
  continuation context, nor does it connect invocation policy and provenance to
  downstream lease semantics.

### Claim: "This is just gRPC for tools"
- Rebuttal: gRPC gives efficient transport and streaming patterns, but it does
  not provide the semantic tool identity, accountability wrapping, or lease
  priming that `C42` aims to define.

### Claim: "This is just LSP progress plus SPIFFE identity"
- Rebuttal: progressive signaling plus short-lived workload identity still does
  not explain how tool invocation becomes policy-bound executable context with
  provenance continuity and explicit no-ambient-rights behavior.

## Prior-art conclusion

`C42` has a real novelty claim if it stays focused on one architectural move:
make trusted tool invocation the lawful beginning of a governed execution
fabric, rather than a one-off RPC call or a thin MCP replacement.

If it degenerates into:
- simple inventory caching,
- generic persistent channels,
- or vague continuation tokens without `C23` handoff discipline,
then the novelty drops materially.
