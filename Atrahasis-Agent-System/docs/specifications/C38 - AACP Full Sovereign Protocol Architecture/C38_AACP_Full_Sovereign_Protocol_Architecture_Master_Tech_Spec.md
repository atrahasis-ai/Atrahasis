# C38 - Five-Layer Sovereign Protocol Architecture (FSPA)

## Master Technical Specification

| Field | Value |
|---|---|
| Title | Five-Layer Sovereign Protocol Architecture (FSPA) |
| Version | 1.0.6 |
| Date | 2026-03-12 |
| Invention ID | C38 |
| Task ID | T-210 |
| System | Atrahasis Agent System v2.4 |
| Stage | SPECIFICATION |
| Normative References | ADR-041, ADR-042, ADR-043, ADR-045, ADR-046, ADR-047, C4 ASV baseline, C3, C5, C6, C7, C8, C23, C24, C36, C37, C39, C40, C41 |

---

## Table of Contents

1. System role and architectural position
2. Design principles
3. Five-layer model
4. Cross-layer invariants
5. Layer contracts
   5.1.1 AACP-HTTP transport binding
   5.1.2 AACP-gRPC transport binding
   5.1.3 AACP-WebSocket transport binding
   5.1.4 AACP-Stdio transport binding
   5.2.1 AACP handshake and session management protocol
   5.4.1 Mandatory lineage envelope
   5.5.1 Cross-encoding canonicalization and semantic identity
6. Versioning and upgrade boundaries
7. Bridge and compatibility posture
8. Integration with the Atrahasis stack
9. Parameters
10. Formal requirements
   10.1 Conformance vectors
11. Risks and open questions

---

## 1. System role and architectural position

### 1.1 Purpose

FSPA defines the root architecture for sovereign Atrahasis-native communication under Alternative B. It is the upstream authority for how AACP v2 is partitioned into:
- Transport,
- Session,
- Security,
- Messaging,
- Semantics.

FSPA does not replace later task work. It creates the contracts those later tasks must refine.

### 1.2 The problem it solves

Before FSPA, the repo had:
- a semantic baseline in `C4 ASV`,
- a strategic decision to pursue full protocol sovereignty,
- a detailed downstream task program,
- but no root architectural authority explaining how the future protocol surface is divided or how end-to-end semantic integrity survives transport substitution.

Without this architecture, downstream tasks would be forced to invent missing boundaries ad hoc.

### 1.3 Architectural position

FSPA sits below the existing Atrahasis coordination, verification, memory, and settlement systems, but above concrete wire encodings and binding implementations.

It is the communication substrate, not the whole intelligence architecture.

---

## 2. Design principles

### 2.1 Sovereignty

Atrahasis owns the end-state communication stack. External protocols may be bridged, but they are not authoritative.

### 2.2 Semantic integrity

Canonical meaning must survive changes in transport, encoding, session topology, and bridge path. The same semantic payload must retain stable identity regardless of binding.

### 2.3 Independent upgradeability

Each layer must have its own change surface. A transport binding upgrade must not force a semantics redesign. A new semantic type must not require a new wire protocol.

### 2.4 Bounded authority

Every layer has explicit responsibilities and explicit forbidden behaviors. Lower layers preserve meaning; they do not define it.

### 2.5 Retrofit honesty

Old `C4 ASV + A2A/MCP` assumptions remain historical baseline and compatibility reference until retrofit tasks supersede them explicitly.

---

## 3. Five-layer model

### 3.1 Layer overview

| Layer | Name | Primary responsibility | Owns |
|---|---|---|---|
| L1 | Transport | Move framed bytes between endpoints | binding mechanics, framing, connection carrier |
| L2 | Session | Establish and maintain exchange state | capability negotiation, liveness, recovery, encoding selection |
| L3 | Security | Prove and constrain authority | identity, authn, authz, signatures, replay defense |
| L4 | Messaging | Define message envelopes and lineage | message classes, routing envelope, lineage fields, batching/stream boundaries |
| L5 | Semantics | Define payload meaning and canonical identity | AASL objects, ontology versions, canonicalization, semantic hashes |

### 3.2 Core insight

The architectural center of gravity is the **semantic integrity chain**:

1. L5 creates a canonical semantic artifact.
2. L4 references and packages that artifact into message structures.
3. L3 binds identities and signatures to the L4/L5 combination.
4. L2 negotiates the rules under which the exchange occurs.
5. L1 carries the exchange over a chosen binding.

### 3.3 End-to-end flow

```
L5 Semantics
  canonical object + ontology snapshot + semantic hash
        |
        v
L4 Messaging
  message envelope + lineage + class + payload references
        |
        v
L3 Security
  identity proof + authorization context + signature + replay controls
        |
        v
L2 Session
  negotiated versions + encoding + liveness + recovery contract
        |
        v
L1 Transport
  HTTP / gRPC / WS / stdio framed exchange
```

---

## 4. Cross-layer invariants

### 4.1 Invariant I1 - Semantic authority originates in L5

No lower layer may redefine the meaning of an AASL payload. Lower layers may:
- carry,
- reference,
- sign,
- negotiate,
- reject,
but not reinterpret semantic truth.

### 4.2 Invariant I2 - Canonical identity is encoding-independent

Semantic identity is defined over the canonical form governed by L5. Different wire encodings may carry the same semantic object, but they must not create distinct authoritative meanings.

### 4.3 Invariant I3 - Message lineage lives in L4

Conversation, workflow, parentage, and message identity are message-envelope concerns. Session state may assist recovery, but it does not become the authoritative lineage ledger.

### 4.4 Invariant I4 - Security binds authority, not meaning

L3 proves who may say or do something and under what rights. It does not invent new semantic categories or replace verification logic from C5.

### 4.5 Invariant I5 - Session negotiates capabilities, not business semantics

L2 chooses version/encoding/binding/security suites and manages recovery. It does not define message classes or tool semantics.

### 4.6 Invariant I6 - Bridges are compatibility-only

Bridge-mediated exchanges must advertise degraded or translated provenance state where native guarantees cannot be preserved at the source.

---

## 5. Layer contracts

### 5.1 L1 Transport

#### Purpose
Move framed bytes across concrete bindings.

#### Responsibilities
- binding-specific endpoint and frame rules,
- fragmentation/reassembly support where required,
- transport-local error surfaces,
- transport-local QoS and streaming carrier behavior.

#### Forbidden behaviors
- defining semantic payload meaning,
- choosing ontology versions,
- redefining lineage,
- overriding authorization policy.

#### Downward/upward contract
- Upward input: session-approved frames.
- Upward output: faithful carriage guarantees and transport-local delivery signals.

### 5.1.1 AACP-HTTP transport binding

`T-220` defines the normative HTTP carrier for L1. The binding carries session-control
frames and business messages over HTTPS without altering L2-L5 meaning.

It does **not** define:
- the semantic content of business payloads,
- the L2 negotiation tuple itself,
- manifest semantics owned by `T-214`,
- or stream/push business behavior owned by `T-243`.

#### HTTP carrier surfaces

| Surface | Method | Purpose |
|---|---|---|
| `/aacp/handshake` | `POST` | Carry `SCF-v1` handshake establishment and resume-admission traffic over HTTP request/response |
| `/aacp/message` | `POST` | Carry one business message or one ordered batch accepted under the current session tuple |
| `/aacp/stream` | `POST` | Initiate an HTTP streaming carrier for an already-negotiated or negotiation-coupled workflow |
| `/aacp/stream/{stream_id}` | `GET` | Open the resulting Server-Sent Events stream resource |

Manifest retrieval remains a plain HTTP `GET` against the canonical manifest URL defined
by `C41`. The HTTP binding MUST treat that URL as an external contract and MUST NOT
invent a conflicting transport-local authority.

#### Media-type and encoding rules

The HTTP binding maps the negotiated L2 encoding to one explicit media type:

| Encoding | Media type |
|---|---|
| `AASL-T` | `application/aacp` |
| `AASL-J` | `application/aacp+json` |
| `AASL-B` | `application/aacp+bin` |

Rules:
- Clients MUST send `Content-Type` explicitly on every `POST`.
- Clients MUST send `Accept` explicitly whenever more than one response media type could
  be returned.
- Servers MUST reject unsupported request media types with an explicit transport-local
  refusal rather than guessing an alternate encoding.
- The HTTP binding MUST treat payload bytes as opaque once framing and declared media
  type have been validated.

#### HTTP transport behavior

- Network deployments MUST use HTTPS with TLS 1.3 or later. `localhost` loopback is the
  only exception.
- HSTS is REQUIRED on non-localhost HTTPS endpoints.
- HTTP/2 is the baseline network profile because multiplexing is part of the carrier
  contract for concurrent sessions and stream setup.
- HTTP/3 MAY be offered for latency-sensitive deployments, but it MUST preserve the same
  L2-L5 semantics and media-type rules as HTTP/2.
- HTTP status codes and headers MAY report transport-local delivery state, but they MUST
  NOT replace explicit AACP control or business outcomes.

#### SSE integration boundary

The HTTP binding owns the SSE carrier, not the stream business semantics.

Rules:
- `POST /aacp/stream` MUST either reject the attempt explicitly or return a concrete
  stream resource identifier plus a `Location` header pointing to
  `/aacp/stream/{stream_id}`.
- `GET /aacp/stream/{stream_id}` MUST respond with `Content-Type: text/event-stream`
  when the carrier is granted.
- SSE event delivery MUST preserve the already-selected encoding and MUST NOT rewrite L4
  lineage or L5 canonical identity.
- Later tasks may refine event shapes and streaming message classes, but they MUST do so
  without changing these carrier contracts.

### 5.1.2 AACP-gRPC transport binding

`T-221` defines the normative gRPC carrier for L1. The binding gives AACP a
binary-first, strongly typed transport profile over HTTP/2 while preserving the same
L2-L5 contracts already established in `C38`, `C39`, and `C40`.

It does **not** define:
- LCML message semantics beyond their transport projection,
- new security profiles or authority rules beyond `C40`,
- manifest field structure owned by `C41`,
- or tool semantics owned by `T-240`.

#### gRPC carrier profile

| Field | Requirement |
|---|---|
| protobuf carrier profile | `AACP-PB-v1` |
| canonical protobuf package | `atr.aacp.v1` |
| primary service profile | `AACPService-v1` |
| network transport floor | HTTP/2 + TLS 1.3 for non-localhost deployments |
| health service | `grpc.health.v1.Health` |
| preferred native encoding | `AASL-B` |

Rules:
- Network gRPC deployments MUST use HTTP/2. gRPC-Web, JSON transcoding, or other
  compatibility layers MAY exist, but they are not the normative `T-221` binding.
- Non-localhost deployments MUST use TLS 1.3 or later.
- The gRPC binding MAY optimize binary carriage, but it MUST preserve the same
  fail-closed invariants, lineage rules, registry snapshot discipline, and authority
  binding requirements as every other native binding.

#### Protobuf carrier artifacts

The binding MUST define these transport-carrier artifacts:

| Artifact | Purpose |
|---|---|
| `enum AACPMessageClassPB` | canonical transport enum covering the full 42-class LCML inventory |
| `message AACPHeaderPB` | protobuf projection of the L4 envelope and selected transport/session facts |
| `message AACPEnvelopePB` | one business message carried through unary or streaming RPCs |
| `message AACPBatchPB` | ordered batch carrier for multi-message dispatch |
| `message SessionControlFramePB` | protobuf projection of `SCF-v1` control traffic |
| `message AACPGrpcFramePB` | bidirectional stream frame union carrying control, message, or batch traffic |

`AACPMessageClassPB` MUST mirror the canonical LCML inventory exactly:

```proto
enum AACPMessageClassPB {
  AACP_MESSAGE_CLASS_UNSPECIFIED = 0;
  TASK_SUBMISSION = 1;
  TASK_ASSIGNMENT = 2;
  TASK_RESULT = 3;
  VERIFICATION_REQUEST = 4;
  VERIFICATION_RESULT = 5;
  MEMORY_LOOKUP_REQUEST = 6;
  MEMORY_LOOKUP_RESULT = 7;
  MEMORY_ADMISSION_REQUEST = 8;
  MEMORY_ADMISSION_RESULT = 9;
  STATE_UPDATE = 10;
  ERROR_REPORT = 11;
  SIGNAL_PUBLISH = 12;
  CLAIM_SUBMIT = 13;
  LEASE_REQUEST = 14;
  LEASE_GRANT = 15;
  LEASE_DENY = 16;
  ATTESTATION_SUBMIT = 17;
  BUNDLE_COMMIT = 18;
  TIDAL_SCHEDULE_ANNOUNCE = 19;
  SURPRISE_DELTA = 20;
  TIDAL_VERSION_PROPOSE = 21;
  ETR_VOTE = 22;
  SETTLEMENT_PUBLISH = 23;
  AGENT_MANIFEST_PUBLISH = 24;
  AGENT_MANIFEST_QUERY = 25;
  AGENT_MANIFEST_UPDATE = 26;
  TOOL_DISCOVERY = 27;
  TOOL_INVOCATION = 28;
  TOOL_RESULT = 29;
  TOOL_CHANGE_NOTIFICATION = 30;
  RESOURCE_LIST = 31;
  RESOURCE_READ = 32;
  RESOURCE_SUBSCRIBE = 33;
  PROMPT_LIST = 34;
  PROMPT_GET = 35;
  CLARIFICATION_REQUEST = 36;
  CLARIFICATION_RESPONSE = 37;
  STREAM_BEGIN = 38;
  STREAM_DATA = 39;
  STREAM_END = 40;
  SAMPLING_REQUEST = 41;
  SAMPLING_RESULT = 42;
}
```

The gRPC binding MUST NOT:
- rename canonical classes to transport-specific verbs,
- omit classes from the carrier enum,
- or add gRPC-only business classes outside LCML governance.

#### Canonical RPC surface

The primary service surface is `AACPService-v1`:

| RPC | Cardinality | Purpose |
|---|---|---|
| `Handshake` | unary | carry `SessionControlFramePB` for handshake establishment and resume admission |
| `SendMessage` | unary | carry one `AACPEnvelopePB` or one ordered business batch |
| `StreamMessages` | server streaming | return ordered message delivery for deferred responses, stream channels, or subscription outputs |
| `BiStream` | bidirectional streaming | carry `AACPGrpcFramePB` for long-lived duplex exchanges with interleaved control and business traffic |
| `GetManifest` | unary | retrieve the manifest resource defined by `T-214` without redefining manifest semantics |
| `DiscoverTools` | unary | optional convenience RPC alias for `tool_discovery` request/response exchange |
| `InvokeTool` | unary | optional convenience RPC alias for `tool_invocation` / `tool_result` exchange |

Rules:
- `Handshake` MUST carry `SCF-v1` semantics faithfully. It is a transport projection,
  not a new session protocol.
- `SendMessage` and `BiStream` are the canonical generic carriage paths. All 42 message
  classes MUST remain valid over at least one of those paths.
- `DiscoverTools` and `InvokeTool` MAY be exposed for operational convenience, but they
  MUST remain transport aliases of the LCML classes rather than independent semantic
  APIs.
- `GetManifest` MUST return the same manifest resource defined by the Agent Manifest
  specification in `C41`; it MUST NOT define a divergent protobuf-only manifest schema.

#### AASL-B to protobuf mapping

The gRPC binding treats `AASL-B` as the preferred native encoding, but canonical
identity still belongs to L5 rather than to protobuf wire bytes.

Rules:
- `AASL-B` over gRPC MUST use the deterministic protobuf projection profile
  `AACP-PB-v1`.
- `AACP-PB-v1` MUST be derived from the already-canonicalized L5 object graph under the
  pinned registry snapshot. Protobuf field numbering is carrier schema, not ontology
  authority.
- `payload_canonical_hash` and `message_canonical_hash` MUST continue to be computed
  using the L5/L4 canonical procedures already defined in this spec. Implementations
  MUST NOT substitute raw protobuf wire bytes as hash authority.
- If the negotiated encoding is `AASL-T` or `AASL-J`, the gRPC binding MUST carry those
  payloads as explicitly tagged bytes and MUST NOT silently up-convert them to
  `AASL-B`.
- Unknown, ambiguous, or experimental semantic types MUST remain subject to ADR-043
  fail-closed rules; the gRPC carrier MUST NOT tunnel them through
  `google.protobuf.Any` or other heuristic escape hatches that bypass registry
  discipline.

#### Streaming and metadata boundaries

gRPC streaming and metadata are carrier features, not replacements for AACP envelope
authority.

Rules:
- `BiStream` MUST preserve ordering within a `stream_id` chain and within any one
  lineage branch carried on the same session.
- Transport multiplexing MAY interleave independent streams, but it MUST NOT rewrite
  `message_id`, `parent_message_id`, `conversation_id`, `workflow_id`, or LCML stream
  parentage to do so.
- gRPC metadata MAY carry bearer tokens, peer-certificate context, trace identifiers,
  and other transport-local hints.
- The four mandatory lineage fields, selected encoding, registry snapshot identifier,
  provenance class, and `ABP-v1` / `SIG-v1` authority binding references MUST remain in
  the AACP carrier messages themselves; metadata alone is insufficient.
- gRPC status codes MAY report carrier-local conditions such as unavailable transport,
  invalid framing, or deadline expiry, but they MUST NOT replace explicit AACP business
  outcomes or fabricate LCML `error_report` messages on behalf of the application.

#### Health checking

The binding MUST support `grpc.health.v1.Health` for load balancers and runtime health
integration.

Rules:
- Carrier health failure MUST surface as transport-local refusal before a valid AACP
  exchange is reported as established.
- Health success means the carrier is available; it MUST NOT be interpreted as business,
  semantic, or authorization success for any specific AACP workflow.
- A server MAY report degraded health when session control, message carriage, or native
  `AASL-B` projection is impaired, but it MUST make that degradation explicit through the
  health surface rather than by silently downgrading to a weaker carrier profile.

### 5.1.3 AACP-WebSocket transport binding

`T-222` defines the normative WebSocket carrier for L1. The binding gives AACP a
full-duplex persistent transport for high-throughput exchanges while preserving the same
L2-L5 contracts already defined by `C38`, `C39`, `C40`, and `C41`.

It does **not** define:
- LCML stream or push business semantics beyond carrier continuity,
- new handshake or recovery semantics beyond `SCF-v1`,
- manifest or tool semantics owned by `C41` and `T-240`,
- or carrier-local business outcomes outside the canonical AACP envelope.

#### WebSocket carrier profile

| Field | Requirement |
|---|---|
| binding profile | `AACP-WS-v1` |
| wire substrate | RFC 6455 WebSocket |
| network transport floor | `wss://` + TLS 1.3 for non-localhost deployments |
| preferred persistent encoding | `AASL-B` |
| handshake entry rule | first complete application message MUST be `SCF-v1 handshake_request` |
| reconnect profile | bounded exponential backoff with jitter |

Rules:
- Non-localhost deployments MUST use `wss://` with TLS 1.3 or later. Cleartext `ws://`
  is allowed only on `localhost` loopback.
- The HTTP Upgrade establishes carrier reachability only. An AACP session is not active
  until a valid in-band `handshake_response` returns `ACCEPT`.
- The WebSocket binding MAY optimize long-lived duplex carriage, but it MUST preserve
  the same fail-closed invariants, lineage rules, registry snapshot discipline, and
  authority-binding requirements as every other native binding.

#### Frame carriage and encoding rules

The selected L2 encoding determines the WebSocket message opcode and carrier payload
form:

| Encoding | WebSocket opcode | Carrier rule |
|---|---|---|
| `AASL-T` | text | one UTF-8 WebSocket message per complete `SCF-v1`, business envelope, or batch |
| `AASL-J` | text | one UTF-8 WebSocket message per complete `SCF-v1`, business envelope, or batch |
| `AASL-B` | binary | one binary WebSocket message per complete `SCF-v1`, business envelope, or batch |

Rules:
- `AASL-B` MUST use binary WebSocket messages. Text carriage for `AASL-B` is invalid.
- `AASL-T` and `AASL-J` MUST use UTF-8 text WebSocket messages. Binary carriage for
  text encodings is invalid.
- After reassembly of any transport-level fragmentation, each completed WebSocket
  message MUST contain exactly one `SCF-v1` control frame, one AACP business envelope,
  or one ordered business batch.
- Carrier fragmentation MAY be used for transport efficiency, but it MUST remain
  transparent to L2-L5. Reassembly MUST complete before the payload is interpreted as
  one control or business unit.
- Implementations MUST reject opcode or encoding mismatches explicitly rather than
  silently transcoding between text and binary forms.

#### Connection establishment and duplex exchange

The WebSocket binding performs session negotiation in-band after the carrier is opened.

Rules:
- The client MUST send `SCF-v1 handshake_request` as the first complete application
  message no later than `AACP_WS_HANDSHAKE_DEADLINE_MS` after the carrier opens.
- The server MUST reject or close the carrier explicitly if the first complete
  application message is not `handshake_request`.
- Until a valid `handshake_response` with `decision: ACCEPT` is observed, peers MUST
  exchange only handshake control traffic.
- Once the session is `ACTIVE`, either peer MAY send control frames and business
  messages independently over the same carrier. Full-duplex transport MUST NOT alter the
  granted session tuple, selected encoding, or L4 lineage.
- If `Sec-WebSocket-Protocol` is used, it MAY advertise transport-local carrier hints,
  but it MUST NOT replace the mandatory in-band AACP handshake or override its outcome.

#### Heartbeat and keepalive boundary

The WebSocket carrier may use transport-local keepalives, but AACP liveness remains an
L2 responsibility.

Rules:
- `SCF-v1 heartbeat_ping` and `heartbeat_pong` remain the normative AACP liveness
  surface for stateful sessions carried over WebSocket.
- WebSocket Ping and Pong frames MAY be used as supplemental carrier keepalives for NAT
  traversal, intermediary health, or dead-socket detection.
- Transport-local Ping/Pong frames MUST NOT satisfy, replace, or reset the AACP liveness
  timer by themselves. Only valid AACP control traffic or business traffic may do that.
- A carrier MAY be closed after repeated missed transport-local keepalive responses, but
  session failure, resume eligibility, and replay behavior remain governed by `SCF-v1`.

#### Reconnection and workflow recovery

Carrier loss is expected on long-lived persistent sockets, so recovery must stay
explicitly lineage-referenced.

Rules:
- After abnormal close or transport loss, a client MAY attempt automatic reconnect using
  exponential backoff beginning at `AACP_WS_RECONNECT_INITIAL_MS`, capped at
  `AACP_WS_RECONNECT_MAX_MS`, and jittered by `AACP_WS_RECONNECT_JITTER_RATIO`.
- Every reconnect attempt MUST begin with either a fresh `handshake_request` or a
  `session_resume_request`; WebSocket reconnect alone does not restore an AACP session.
- `last_seen_message_id` observations MAY seed recovery decisions, but they MUST remain
  recovery cursors only. The binding MUST NOT mint substitute lineage or synthetic
  delivery acknowledgements from transport history.
- A successful resume over WebSocket MUST mint a new `session_id`, preserve
  `conversation_id` and `workflow_id`, and follow any per-workflow replay instructions
  returned by `session_resume_response`.
- If the responder cannot safely continue from the supplied recovery cursors, it MUST
  reject the resume or require restart explicitly rather than silently replaying or
  skipping business traffic.

#### Close and extension boundaries

WebSocket close codes and negotiated extensions remain transport-local.

Rules:
- WebSocket close codes MAY report carrier-local causes such as protocol error,
  unsupported data, message-too-large refusal, or internal transport failure.
- Close codes, extension negotiation results, and carrier-local diagnostics MUST NOT be
  treated as LCML business outcomes and MUST NOT fabricate `error_report` semantics on
  behalf of the application.
- Lossless carrier extensions such as compression MAY be used only when negotiated
  explicitly and only when they do not change the selected AACP encoding, canonical
  identity, or L2-L5 authority boundaries.

### 5.1.4 AACP-Stdio transport binding

`T-223` defines the normative stdio carrier for L1. The binding gives AACP a
local-process transport profile for tool-facing and developer-facing integrations using
UTF-8 NDJSON over stdin/stdout while preserving the same L2-L5 contracts already
defined by `C38`, `C39`, `C40`, and `C41`.

It does **not** define:
- tool semantics owned by `T-240`,
- new security profiles or trust elevation beyond `C40`,
- manifest or discovery semantics owned by `C41`,
- or any network transport profile beyond a local parent/child process boundary.

#### Stdio carrier profile

| Field | Requirement |
|---|---|
| binding profile | `AACP-STDIO-v1` |
| wire substrate | parent-managed local process stdin/stdout pipes |
| record format | UTF-8 NDJSON, one complete JSON object per LF-terminated record |
| normative encoding | `AASL-J` only |
| handshake entry rule | first complete application record from the initiator MUST be `SCF-v1 handshake_request` |
| stderr policy | diagnostics only; never canonical AACP carriage |
| lifecycle posture | spawn -> handshake -> exchange -> graceful shutdown or explicit failure |

Rules:
- The stdio binding is a local carrier only. It MUST NOT be represented as a remote
  network binding or as evidence of transport-level peer identity by itself.
- Every complete `SCF-v1` control frame, business envelope, or ordered business batch
  MUST occupy exactly one UTF-8 JSON object terminated by LF on the carrier stream.
- The normative `T-223` binding profile supports only `AASL-J`. Attempts to negotiate
  `AASL-T` or `AASL-B` on stdio MUST fail closed.
- Record framing belongs to L1 only. The binding MUST preserve L2 session facts, L4
  lineage, and L5 canonical identity without introducing stdio-local semantic fields.
- `stderr` MAY carry human-readable diagnostics, but it MUST remain outside canonical
  AACP parsing, hashing, lineage, and business outcome handling.

#### Process lifecycle and session gate

The stdio carrier is parent-managed and session-gated.

Rules:
- The parent process MUST spawn or attach the child process before sending any AACP
  traffic and MUST wire stdin/stdout as the exclusive canonical carrier path.
- The initiator MUST send `SCF-v1 handshake_request` no later than
  `AACP_STDIO_HANDSHAKE_DEADLINE_MS` after the child is ready for I/O.
- No business traffic is valid until `handshake_response.decision = ACCEPT` is observed
  on stdout.
- Child process exit, stdout EOF, broken pipe, or malformed NDJSON before acceptance
  MUST be treated as transport-local refusal rather than fabricated business failure.
- Parent-managed respawn alone does not restore an AACP session. Any continued exchange
  MUST begin with a fresh `handshake_request` or an explicit `session_resume_request`
  that the child accepts.

#### Local tool integration boundary

The stdio binding is the canonical local-process replacement for MCP stdio transport,
but it does not widen authority beyond the existing L2-L5 model.

Rules:
- The binding MAY carry tool-facing exchanges for local helper processes or native
  AACP tool servers, but tool discovery, invocation, and result semantics remain owned
  by `T-240` and LCML.
- Process-local metadata such as PID, executable path, environment variables, working
  directory, or file-descriptor inheritance MAY support supervision, but they MUST NOT
  replace canonical lineage, registry snapshot, provenance class, or `C40` authority
  context inside AACP messages.
- A parent MAY supervise one child per endpoint or a multi-surface local server, but
  the binding MUST NOT rewrite LCML class semantics to match process topology.

#### Shutdown and failure boundary

Rules:
- Graceful shutdown MUST use explicit `SCF-v1` close traffic and allow up to
  `AACP_STDIO_SHUTDOWN_GRACE_MS` for drain and acknowledgement before forced process
  termination.
- Forced termination, pipe breakage, malformed JSON, or out-of-order framing MUST
  surface as transport-local failure and MUST NOT be rewritten as synthetic LCML
  success or error outcomes.
- The binding MUST preserve record order exactly as emitted on stdout. It MUST NOT
  split one canonical AACP unit across multiple NDJSON records or merge multiple
  canonical units into one record.

### 5.2 L2 Session

#### Purpose
Create and maintain the exchange context in which messages are sent.

#### Responsibilities
- protocol version negotiation,
- encoding selection,
- capability advertisement and acceptance,
- liveness and heartbeat,
- graceful shutdown,
- resumable workflow recovery,
- stateless versus stateful interaction mode.

#### Forbidden behaviors
- inventing message classes,
- defining semantic payload structure,
- performing authorization decisions that belong to L3,
- mutating L4 lineage fields as a substitute for recovery.

#### Key contract
Session chooses **how** an exchange proceeds, not **what** the message means.

### 5.2.1 AACP handshake and session management protocol

`T-213` defines the explicit L2 control surface for establishing, maintaining, and
closing an AACP exchange. This control surface is binding-independent: transport
bindings carry it, but do not redefine it; L4 messaging may reference the resulting
session state, but does not own it.

The protocol below defines:
- session-control frame structure,
- handshake capability exchange and explicit selection,
- heartbeat and liveness,
- graceful shutdown,
- resumable recovery using authoritative L4 lineage,
- stateless single-exchange mode.

It does **not** define new business-level L4 message classes. Session control frames
exist beside the 42-class LCML inventory rather than inside it.

#### Session control frame profile

All native L2 session operations MUST use the binding-independent control-frame
profile `SCF-v1`.

| Field | Requirement | Meaning |
|---|---|---|
| `frame_profile` | REQUIRED | Fixed value `SCF-v1` |
| `frame_type` | REQUIRED | Session control operation kind |
| `frame_id` | REQUIRED | Stable identifier for this control frame |
| `session_id` | CONDITIONAL | `null` for initial `handshake_request`; required after session grant |
| `issued_at` | REQUIRED | UTC timestamp for replay/liveness ordering |
| `sender_id` | REQUIRED | Claimed sender identity or endpoint identifier |
| `binding_id` | REQUIRED | Binding token: `AACP-HTTP`, `AACP-gRPC`, `AACP-WS`, or `AACP-Stdio` |
| `payload` | REQUIRED | Frame-specific structured body |

`frame_type` SHALL be one of:

| Frame type | Purpose |
|---|---|
| `handshake_request` | Offer protocol/session capabilities and request session establishment |
| `handshake_response` | Accept or reject the offered handshake |
| `heartbeat_ping` | Probe liveness for an active stateful session |
| `heartbeat_pong` | Acknowledge a liveness probe |
| `session_resume_request` | Re-establish a failed or disconnected stateful session using lineage cursors |
| `session_resume_response` | Accept, reject, or require restart for a resume attempt |
| `session_close` | Begin graceful session shutdown |
| `session_close_ack` | Confirm shutdown outcome |

#### Handshake request

`handshake_request.payload` MUST contain:

| Field | Requirement | Meaning |
|---|---|---|
| `offered_protocol_versions` | REQUIRED | Ordered set of acceptable AACP protocol versions |
| `offered_encodings` | REQUIRED | Ordered set drawn from `AASL-T`, `AASL-J`, `AASL-B` |
| `offered_security_profiles` | REQUIRED | Ordered set of L3 security-profile identifiers |
| `supported_message_profiles` | REQUIRED | Ordered set of L4 message-profile identifiers such as `LCML-v1` |
| `acceptable_registry_snapshot_ids` | REQUIRED | Set of pinned semantics snapshots the initiator can validate against |
| `requested_mode` | REQUIRED | `STATEFUL`, `STATELESS`, or `EITHER` |
| `session_features` | REQUIRED | Set drawn from `heartbeat`, `resume`, `transport_rebind`, `graceful_shutdown` |
| `heartbeat_interval_offer_ms` | OPTIONAL | Preferred heartbeat interval when `heartbeat` is offered |
| `idle_timeout_offer_ms` | OPTIONAL | Preferred idle timeout for a stateful session |

Rules:
- Every offered set MUST be explicit. The peer MUST NOT infer omitted protocol,
  encoding, security, or message-profile support from transport defaults.
- `acceptable_registry_snapshot_ids` is a capability gate, not a substitute for the
  per-message pinned snapshot required by L5.
- `requested_mode: STATELESS` means the initiator requests an ephemeral
  single-exchange session with no resume guarantee.
- `requested_mode: EITHER` allows the responder to choose explicitly between
  stateful and stateless operation.

#### Handshake response

`handshake_response.payload` MUST contain one of two mutually exclusive outcomes.

Accept path:

| Field | Requirement | Meaning |
|---|---|---|
| `decision` | REQUIRED | `ACCEPT` |
| `selected_protocol_version` | REQUIRED | Concrete protocol version selected from the offered set |
| `selected_encoding` | REQUIRED | Concrete encoding selected from the offered set |
| `selected_security_profile` | REQUIRED | Concrete L3 profile selected from the offered set |
| `selected_message_profile` | REQUIRED | Concrete L4 profile selected from the offered set |
| `selected_registry_snapshot_id` | REQUIRED | One pinned snapshot acceptable to both peers |
| `granted_mode` | REQUIRED | `STATEFUL` or `STATELESS` |
| `session_id` | REQUIRED | Session identifier for the granted exchange context |
| `granted_session_features` | REQUIRED | Subset of offered features actually granted |
| `heartbeat_interval_ms` | CONDITIONAL | Required when `heartbeat` is granted in stateful mode |
| `idle_timeout_ms` | CONDITIONAL | Required in stateful mode |
| `resume_window_ms` | CONDITIONAL | Required when `resume` is granted |

Reject path:

| Field | Requirement | Meaning |
|---|---|---|
| `decision` | REQUIRED | `REJECT` |
| `rejection_code` | REQUIRED | Explicit refusal reason |
| `rejection_detail` | OPTIONAL | Human-readable explanation |

`rejection_code` SHALL be one of:
- `UNSUPPORTED_PROTOCOL_VERSION`
- `UNSUPPORTED_ENCODING`
- `UNSUPPORTED_SECURITY_PROFILE`
- `UNSUPPORTED_MESSAGE_PROFILE`
- `UNSUPPORTED_REGISTRY_SNAPSHOT`
- `MODE_REJECTED`
- `INVARIANT_BREAKING_DOWNGRADE`

Negotiation rules:
- The responder MUST compute explicit intersections across protocol versions,
  encodings, security profiles, message profiles, and acceptable registry
  snapshots before returning `ACCEPT`.
- If any required intersection is empty, the responder MUST return `REJECT`; it
  MUST NOT silently downgrade or invent a compatibility mode.
- `STATELESS` sessions MUST NOT grant `resume`.
- `resume` MUST NOT be granted unless the granted mode is `STATEFUL`.
- A successful `handshake_response` transitions both peers from `NEGOTIATING` to
  `ACTIVE`.

#### Heartbeat and liveness

Heartbeat is an L2 keepalive for stateful sessions only.

`heartbeat_ping.payload` MUST contain:
- `reply_expected_by_ms`
- `observed_last_message_id` (optional reference to the most recent valid L4
  message seen on the session)

`heartbeat_pong.payload` MUST contain:
- `reply_to_frame_id`
- `observed_last_message_id` (optional echo or newer observation)

Liveness rules:
- If no valid control frame or business message is observed for
  `heartbeat_interval_ms`, either peer MAY send `heartbeat_ping`.
- The peer MUST answer with `heartbeat_pong` before the requesting side reaches
  `reply_expected_by_ms`.
- Any valid control frame or business message resets the liveness timer.
- After `AACP_HEARTBEAT_MISS_THRESHOLD` consecutive missed heartbeat responses, the
  session enters `FAILED`.
- Once `FAILED`, peers MUST stop sending business messages on that session_id and
  either attempt `session_resume_request` or begin a new handshake.

#### Graceful shutdown

`session_close.payload` MUST contain:

| Field | Requirement | Meaning |
|---|---|---|
| `close_reason` | REQUIRED | Reason for closure |
| `drain_deadline_at` | REQUIRED | UTC deadline for completing in-flight work |

`session_close_ack.payload` MUST contain:

| Field | Requirement | Meaning |
|---|---|---|
| `reply_to_frame_id` | REQUIRED | The initiating `session_close` frame |
| `outcome` | REQUIRED | `DRAINED`, `ABORTED`, or `ALREADY_CLOSED` |
| `final_observed_message_id` | OPTIONAL | Most recent valid L4 message observed before closure |

Shutdown rules:
- After emitting or accepting `session_close`, a peer MUST stop starting new
  business exchanges on that session.
- Until `drain_deadline_at`, only in-flight business completions, heartbeat, and
  shutdown-control traffic may continue.
- If all in-flight work drains cleanly, the peer MUST send `session_close_ack`
  with `outcome: DRAINED` and transition to `CLOSED`.
- If the deadline expires first, the peer MUST send `session_close_ack` with
  `outcome: ABORTED` or locally transition to `FAILED`; it MUST NOT rewrite L4
  lineage to hide abandoned in-flight work.

#### Reconnection and workflow recovery

Stateful recovery is explicit and lineage-referenced.

`session_resume_request.payload` MUST contain:

| Field | Requirement | Meaning |
|---|---|---|
| `prior_session_id` | REQUIRED | Failed or disconnected stateful session |
| `conversation_id` | REQUIRED | Conversation whose workflow branches are being resumed |
| `recovery_cursors` | REQUIRED | One or more workflow cursors |

Each `recovery_cursor` MUST contain:
- `workflow_id`
- `last_seen_message_id`

`session_resume_response.payload` MUST contain:

| Field | Requirement | Meaning |
|---|---|---|
| `decision` | REQUIRED | `RESUMED`, `REJECTED`, or `RESTART_REQUIRED` |
| `session_id` | CONDITIONAL | Newly granted session identifier when resumed |
| `replay_instructions` | CONDITIONAL | Per-workflow replay guidance when resumed |
| `rejection_code` | CONDITIONAL | Explicit reason when rejected or restart is required |

Recovery rules:
- `session_resume_request` MUST reference authoritative L4 lineage only; it MUST
  NOT supply replacement conversation, workflow, parentage, or message identity.
- A successful resume MUST mint a new `session_id`; the prior session remains
  historical context, not the active exchange surface.
- `replay_instructions` MAY name the first message that must be resent for each
  workflow branch, but any resent business message MUST preserve its original L4
  lineage fields.
- If the responder cannot safely continue from the supplied cursors, it MUST
  return `RESTART_REQUIRED` rather than fabricate synthetic lineage continuity.
- Recovery MAY accompany a transport rebind, but only if the negotiated security
  posture and encoding remain invariant-safe.

#### Stateless mode

Stateless mode is a first-class L2 operating mode, not an implied optimization.

Rules:
- A stateless session MUST be granted explicitly by `handshake_response`.
- A stateless session MUST NOT grant `resume`.
- Heartbeat is OPTIONAL in the offer but MUST NOT be granted in stateless mode.
- A stateless session is limited to one initiating business request and one
  terminal response or error on the granted `session_id`.
- After that terminal response or error, the session transitions immediately to
  `CLOSED` with no drain phase.
- Every stateless exchange still relies on full L4 lineage and explicit L5 pinned
  snapshot identity; stateless mode reduces persistence, not semantic rigor.

#### Relationship to `SES`

`SES` remains the L5 semantic descriptor for session facts. It MAY mirror the
granted mode, session endpoints, supported encodings, and current semantic state,
but it MUST NOT replace:
- the L2 control-frame transcript,
- the L4 lineage envelope,
- or L3 security artifacts.

### 5.3 L3 Security

#### Purpose
Bind identity, trust, and authority to protocol operations.

#### Responsibilities
- authentication mechanisms,
- agent identity tokens and trust anchors,
- authorization and capability scopes,
- signature policy over canonical references,
- replay detection,
- downgrade resistance when security posture would be weakened.

#### Forbidden behaviors
- creating semantic hashes,
- inventing business-level verification verdicts,
- defining routing/message taxonomy,
- silently authorizing actions outside declared capability scope.

#### Key contract
Security binds authority to the exchange and its canonical references; it does not replace C5 verification.

### 5.4 L4 Messaging

#### Purpose
Provide the stable message envelope and lineage-bearing routing surface.

#### Responsibilities
- message class taxonomy,
- header and routing envelope,
- lineage fields,
- lineage normalization rules,
- batching and dependency ordering,
- streaming segmentation and ordered reassembly metadata,
- envelope-level error semantics.

#### Forbidden behaviors
- defining the inner semantics of AASL object families,
- owning transport binding logic,
- replacing security policy,
- collapsing session state into lineage identity.

#### Key contract
Messaging knows the shape of communication and lineage, but it references semantic payloads rather than defining their meaning.

### 5.4.1 Mandatory lineage envelope

Every native AACP message MUST carry the same four lineage fields at L4, independent
of encoding or transport binding:

| Field | Requirement | Meaning | Identity rule |
|---|---|---|---|
| `message_id` | REQUIRED | Stable identifier for this exact message envelope | Immutable across retries, retransmission, or transport rebinding |
| `parent_message_id` | REQUIRED | Immediate causal predecessor for this message | Root messages MUST encode this field explicitly as `null` |
| `conversation_id` | REQUIRED | Stable identifier for the enclosing conversation/thread | Preserved across the full conversation unless a new conversation is intentionally created |
| `workflow_id` | REQUIRED | Stable identifier for the executing workflow branch | May change only when a new workflow branch is explicitly spawned |

Lineage rules:
- A lineage field MAY be carried differently by `AASL-T`, `AASL-J`, or `AASL-B`, but
  each encoding MUST map losslessly to these same abstract fields.
- Omitting one of the four fields is invalid, even when a transport or runtime could
  infer the missing value from local state.
- A retry or replay-safe redelivery MUST preserve `message_id`; it is not a new message
  merely because it moved over a different binding or reconnect path.
- A child workflow MUST mint a new `workflow_id`, preserve the inherited
  `conversation_id`, and use `parent_message_id` to point back to the spawning
  message.
- Session recovery MAY reference lineage state, but MUST NOT rewrite lineage fields in
  order to make recovery appear cleaner than what actually happened.
- Bridge-mediated exchanges MAY synthesize a surrogate lineage envelope only when the
  origin protocol lacked native lineage, and MUST then mark the resulting provenance
  as translated/degraded rather than native.

### 5.5 L5 Semantics

#### Purpose
Define the meaning, canonical form, and governed evolution of payload content.

#### Responsibilities
- AASL object families,
- ontology and registry governance,
- canonicalization rules,
- cross-encoding canonical projection,
- semantic hash authority,
- payload validation against pinned registry snapshots,
- forward-compatibility and unknown-type behavior under governed profiles.

#### Forbidden behaviors
- defining transport endpoints,
- negotiating connections,
- acting as authorization policy,
- embedding transport-specific meaning into the canonical model.

#### Key contract
Semantics is authoritative for what the payload is and how sameness is judged across encodings and bindings.

### 5.5.1 Cross-encoding canonicalization and semantic identity

`T-215` defines the binding-independent canonicalization pipeline that turns
`AASL-T`, `AASL-J`, and `AASL-B` payloads into one semantic identity surface.

#### Canonicalization pipeline

1. Decode the source message from `AASL-T`, `AASL-J`, or `AASL-B` into an abstract
   message model containing:
   - protocol version,
   - message class,
   - the four mandatory lineage fields,
   - payload object,
   - pinned registry or ontology snapshot identifier,
   - provenance class (`NATIVE`, `BRIDGE_TRANSLATED`, or `BRIDGE_DEGRADED`).
2. Validate that all four lineage fields are present and that the referenced registry
   snapshot is explicit and resolvable.
3. Canonicalize the payload under the pinned semantics snapshot by applying the
   existing AASL rules for:
   - alias resolution,
   - identifier normalization,
   - collection normalization where the ontology declares order-insensitive sets,
   - reference normalization,
   - default materialization where the ontology marks a default as identity-bearing,
   - provenance non-interference for fields that are not identity-bearing.
4. Serialize the resulting payload projection into deterministic canonical bytes.
   For `C38`, the normative rule is a UTF-8 encoded canonical object serialization
   with:
   - normalized scalar forms,
   - explicit `null` where the canonical model requires it,
   - lexicographically ordered object keys,
   - no presentation-only whitespace.
5. Compute `payload_canonical_hash = SHA-256(canonical_payload_bytes)`.
6. Build the ordered canonical message projection `CMP-v1` with exactly these fields:
   - `protocol_version`
   - `message_class`
   - `message_id`
   - `parent_message_id`
   - `conversation_id`
   - `workflow_id`
   - `payload_canonical_hash`
   - `registry_snapshot_id`
   - `provenance_class`
7. Serialize `CMP-v1` using the same deterministic object-serialization rules and
   compute `message_canonical_hash = SHA-256(canonical_cmp_bytes)`.

#### Semantic identity rules

- Two payloads are semantically identical only if they canonicalize under the same
  pinned registry snapshot to the same `payload_canonical_hash`.
- Two messages are canonically identical only if they produce the same
  `message_canonical_hash`; identical payload hashes alone are insufficient when the
  lineage envelope or message class differs.
- Differences in source encoding, field ordering, alias spelling, whitespace, or
  binary framing MUST NOT change canonical identity.
- Changes to `message_class`, any of the four lineage fields, `registry_snapshot_id`,
  or `provenance_class` MUST change canonical message identity.
- Changes only to non-identity-bearing provenance metadata MUST NOT change payload
  identity unless the pinned ontology explicitly marks that field as identity-bearing.
- Implementations MUST NOT use raw wire bytes, transport headers, or signature blobs
  as substitutes for semantic canonicalization.

#### Failure behavior

- If an implementation cannot resolve the pinned registry snapshot, canonicalization
  MUST fail closed.
- If alias resolution or type interpretation remains ambiguous, canonicalization MUST
  fail closed rather than guess.
- If a bridge cannot preserve native guarantees from the source protocol, it MAY still
  emit a canonical hash for the translated artifact, but it MUST classify the message
  as `BRIDGE_TRANSLATED` or `BRIDGE_DEGRADED`; it MUST NOT label it `NATIVE`.

---

## 6. Versioning and upgrade boundaries

### 6.1 General rule

Every layer has an independent version surface, but session negotiation decides which combinations are legal for a given exchange.

### 6.2 Allowed independent evolution

| Change type | Primary layer | Allowed without redesigning all layers? | Notes |
|---|---|---|---|
| New transport binding | L1 | Yes | Must honor existing L2-L5 contracts |
| New session recovery mode | L2 | Yes | Must not alter L4 lineage authority |
| New auth/signature suite | L3 | Yes | Must still bind canonical references correctly |
| New message classes | L4 | Yes | Requires L4 conformance extension, not L5 rewrite by default |
| New semantic types | L5 | Yes, under ADR-043 discipline | Governed snapshots and compatibility classes required |

### 6.3 Downgrade refusal rule

If negotiation would force loss of any non-optional invariant:
- semantic-hash authority,
- required security posture,
- lineage completeness,
- profile-governed unknown-type handling,
the session must fail closed rather than silently degrade.

### 6.4 Compatibility classes

FSPA inherits the `C0-C5` change-class discipline from AASL governance for semantics-layer evolution and requires equivalent explicit classification for changes to the other layers.

---

## 7. Bridge and compatibility posture

### 7.1 Role of bridges

Bridges exist to:
- absorb existing A2A/MCP ecosystems,
- accelerate migration,
- make compatibility possible during rollout.

They do not define the native architecture.

### 7.2 Native versus bridge provenance

Every bridge-mediated exchange must make provenance state explicit:
- native AACP provenance,
- translated/bridge-mediated provenance,
- missing source guarantees where canonical binding could not exist at origin.

### 7.3 Architectural rule

No downstream task may treat bridge behavior as the normative definition of a native layer contract.

---

## 8. Integration with the Atrahasis stack

### 8.1 C3 Tidal Noosphere
- Consumes message routing and transport surfaces.
- Retains authority for placement, timing, and parcel/locus coordination.

### 8.2 C5 PCVM
- Consumes canonical payload identity, signed lineage, and provenance-bearing messages.
- Retains authority for verification verdicts.

### 8.3 C6 EMA
- Consumes stable semantic artifacts and canonical hashes for metabolism and memory admission.
- Retains authority for knowledge lifecycle.

### 8.4 C7 RIF
- Consumes messaging/session surfaces for decomposition, handoff, and workflow coordination.
- Retains authority for decomposition logic.

### 8.5 C8 DSF
- Consumes accountable provenance and settlement-grade message flows.
- Retains authority for economic settlement.

### 8.6 C23 SCR and C24 FHF
- Consume session/security/messaging surfaces for runtime cells and federation links.
- Retain authority for execution and habitat/federation behavior.

### 8.7 C36 EMA-I and C37 EFF
- Consume boundary-safe ingress/egress and advisory publication surfaces.
- Retain authority for interface membrane logic and feedback semantics.

---

## 9. Parameters

| Parameter | Meaning | Initial value / guidance |
|---|---|---|
| `AACP_REQUIRED_LINEAGE_FIELDS` | Mandatory L4 lineage fields | 4 (`message_id`, `parent_message_id`, `conversation_id`, `workflow_id`) |
| `AACP_NEGOTIATION_FAIL_CLOSED` | Whether invariant-breaking negotiation is allowed | `true` |
| `AACP_BRIDGE_PROVENANCE_MODE` | Required provenance disclosure for bridges | `EXPLICIT_DEGRADED` |
| `AACP_LAYER_VERSION_POLICY` | Cross-layer version discipline | `independent_versions_with_session_negotiation` |
| `AACP_CANONICAL_HASH_AUTHORITY` | Layer owning canonical identity | `L5_SEMANTICS` |
| `AACP_SIGNATURE_BINDING_SCOPE` | What L3 must sign | `canonical_payload_reference + lineage envelope + authority context` |
| `AACP_CANONICAL_HASH_ALGORITHM` | Hash primitive for canonical payloads and messages | `SHA-256` |
| `AACP_CANONICAL_MESSAGE_PROJECTION` | Canonical message projection version | `CMP-v1` |
| `AACP_ROOT_PARENT_POLICY` | How root messages encode missing parentage | `explicit_null_parent_message_id` |
| `AACP_CANONICALIZATION_FAIL_MODE` | Behavior on ambiguity or unresolved registry state | `FAIL_CLOSED` |
| `AACP_SESSION_CONTROL_PROFILE` | Binding-independent L2 control-frame profile | `SCF-v1` |
| `AACP_DEFAULT_HEARTBEAT_INTERVAL_MS` | Default liveness probe interval for granted stateful sessions | `15000` |
| `AACP_HEARTBEAT_MISS_THRESHOLD` | Consecutive missed heartbeat responses before failure | `3` |
| `AACP_SESSION_DRAIN_TIMEOUT_MS` | Default graceful-shutdown drain window | `30000` |
| `AACP_SESSION_RESUME_WINDOW_MS` | Maximum time after failure during which resume is permitted by default | `300000` |
| `AACP_STATELESS_EXCHANGE_LIMIT` | Maximum business exchange size in stateless mode | `1 request + 1 terminal response` |
| `AACP_SESSION_SELECTION_POLICY` | Negotiation policy for choosing a concrete session tuple | `responder_explicit_intersection_selection` |
| `AACP_HTTP_HANDSHAKE_PATH` | Canonical HTTP binding path for session-establishment traffic | `/aacp/handshake` |
| `AACP_HTTP_MESSAGE_PATH` | Canonical HTTP binding path for business-message submission | `/aacp/message` |
| `AACP_HTTP_STREAM_INIT_PATH` | Canonical HTTP binding path for stream-carrier initiation | `/aacp/stream` |
| `AACP_HTTP_STREAM_RESOURCE_TEMPLATE` | Canonical HTTP SSE resource template | `/aacp/stream/{stream_id}` |
| `AACP_HTTP_MEDIA_TYPE_AASL_T` | HTTP media type for `AASL-T` payload carriage | `application/aacp` |
| `AACP_HTTP_MEDIA_TYPE_AASL_J` | HTTP media type for `AASL-J` payload carriage | `application/aacp+json` |
| `AACP_HTTP_MEDIA_TYPE_AASL_B` | HTTP media type for `AASL-B` payload carriage | `application/aacp+bin` |
| `AACP_HTTP_TLS_MIN_VERSION` | Minimum TLS version for non-localhost HTTP binding traffic | `TLS_1_3` |
| `AACP_HTTP_HSTS_MAX_AGE_S` | Minimum HSTS max-age for compliant HTTPS endpoints | `31536000` |
| `AACP_GRPC_PROTO_PROFILE` | Deterministic protobuf carrier profile for native gRPC transport | `AACP-PB-v1` |
| `AACP_GRPC_SERVICE_PROFILE` | Canonical primary gRPC service surface | `AACPService-v1` |
| `AACP_GRPC_PACKAGE_NAME` | Canonical protobuf package for the gRPC binding | `atr.aacp.v1` |
| `AACP_GRPC_PREFERRED_ENCODING` | Preferred native encoding when gRPC is available | `AASL-B` |
| `AACP_GRPC_TRANSPORT_FLOOR` | Normative carrier substrate for native gRPC transport | `HTTP/2` |
| `AACP_GRPC_HEALTH_SERVICE` | Canonical health-check integration surface | `grpc.health.v1.Health` |
| `AACP_WS_BINDING_PROFILE` | Canonical WebSocket carrier profile for native persistent duplex transport | `AACP-WS-v1` |
| `AACP_WS_PREFERRED_ENCODING` | Preferred persistent encoding when WebSocket transport is available | `AASL-B` |
| `AACP_WS_HANDSHAKE_DEADLINE_MS` | Maximum time after carrier open before the first `handshake_request` MUST arrive | `10000` |
| `AACP_WS_RECONNECT_INITIAL_MS` | Initial reconnect delay after abnormal carrier loss | `1000` |
| `AACP_WS_RECONNECT_MAX_MS` | Maximum reconnect delay during bounded exponential backoff | `30000` |
| `AACP_WS_RECONNECT_JITTER_RATIO` | Symmetric jitter ratio applied to reconnect delay calculations | `0.20` |
| `AACP_WS_OPCODE_POLICY` | Required opcode mapping for negotiated encodings | `AASL-B=binary; AASL-T/AASL-J=text` |
| `AACP_WS_KEEPALIVE_POLICY` | Relationship between transport-local Ping/Pong and normative AACP liveness | `ws_ping_pong_supplemental; SCF-v1_required` |
| `AACP_STDIO_BINDING_PROFILE` | Canonical stdio carrier profile for local process transport | `AACP-STDIO-v1` |
| `AACP_STDIO_ENCODING` | Normative encoding permitted on the stdio binding | `AASL-J` |
| `AACP_STDIO_RECORD_DELIMITER` | Canonical NDJSON record terminator for stdio carriage | `LF` |
| `AACP_STDIO_HANDSHAKE_DEADLINE_MS` | Maximum time after child readiness before the first `handshake_request` MUST arrive | `5000` |
| `AACP_STDIO_SHUTDOWN_GRACE_MS` | Default grace period for drain and acknowledgement before forced local termination | `5000` |
| `AACP_STDIO_STDERR_POLICY` | Relationship between stderr output and canonical carrier semantics | `diagnostics_only_noncanonical` |

---

## 10. Formal requirements

| ID | Requirement | Priority |
|---|---|---|
| FSPA-R01 | AACP v2 MUST be specified as a five-layer architecture with independent layer authority boundaries | P0 |
| FSPA-R02 | L5 MUST be the sole authoritative source of semantic canonical form and semantic hash identity | P0 |
| FSPA-R03 | L4 MUST own message lineage and envelope routing semantics | P0 |
| FSPA-R04 | L3 MUST bind identity, authorization, and signatures to canonical references without redefining payload meaning | P0 |
| FSPA-R05 | L2 MUST negotiate versions, encodings, and recovery behavior, and MUST fail closed on invariant-breaking downgrade | P0 |
| FSPA-R06 | L1 MUST support multiple transport bindings without altering L2-L5 meaning | P0 |
| FSPA-R07 | No layer below L5 MAY redefine the meaning of an AASL payload | P0 |
| FSPA-R08 | Canonical identity MUST remain stable across supported encodings when semantic content is unchanged | P0 |
| FSPA-R09 | Bridge-mediated exchanges MUST disclose translated or degraded provenance status explicitly | P0 |
| FSPA-R10 | Native layer contracts MUST NOT be defined by bridge behavior | P0 |
| FSPA-R11 | Semantics-layer extension MUST honor ADR-043 snapshot and compatibility discipline | P0 |
| FSPA-R12 | T-211, T-212, T-213, T-214, T-215, T-220, T-221, T-222, T-223, and T-230 MUST refine the contracts in this architecture rather than replace them silently | P1 |
| FSPA-R13 | Session recovery mechanisms MUST reference, but MUST NOT replace, authoritative L4 lineage fields | P1 |
| FSPA-R14 | Security downgrade that would remove required identity, signature, or replay guarantees MUST terminate negotiation | P1 |
| FSPA-R15 | Transport bindings MUST treat payloads as opaque beyond what is required for framing and delivery | P1 |
| FSPA-R16 | The architecture MUST preserve compatibility with C3/C5/C6/C7/C8/C23/C24/C36/C37 authority boundaries | P0 |
| FSPA-R17 | A later task that needs a new cross-layer surface MUST add an explicit task or ADR rather than silently widening one layer's authority | P1 |
| FSPA-R18 | Every native AACP message MUST carry `message_id`, `parent_message_id`, `conversation_id`, and `workflow_id` in the L4 envelope | P0 |
| FSPA-R19 | Root messages MUST encode `parent_message_id` explicitly as `null`; omission of the field is invalid | P0 |
| FSPA-R20 | Retries, retransmissions, and transport rebinding MUST preserve the original lineage tuple rather than minting a new `message_id` | P0 |
| FSPA-R21 | L5 canonicalization MUST yield the same `payload_canonical_hash` for semantically identical payloads carried in `AASL-T`, `AASL-J`, and `AASL-B` under the same pinned registry snapshot | P0 |
| FSPA-R22 | Canonical hashes MUST be computed over deterministic canonical projections, never over raw source bytes or presentation syntax | P0 |
| FSPA-R23 | `message_canonical_hash` MUST be computed over `CMP-v1`, which contains `protocol_version`, `message_class`, the four mandatory lineage fields, `payload_canonical_hash`, `registry_snapshot_id`, and `provenance_class` | P0 |
| FSPA-R24 | Non-identity-bearing provenance differences, alias spelling, field ordering, whitespace, and binary framing MUST NOT alter canonical identity | P1 |
| FSPA-R25 | Unknown types, ambiguous canonicalization, unresolved registry snapshots, or missing lineage fields MUST cause fail-closed rejection rather than heuristic hashing | P0 |
| FSPA-R26 | Bridge-synthesized lineage MAY exist only with explicit translated/degraded provenance labeling and MUST NOT be represented as native lineage | P1 |
| FSPA-R27 | L2 MUST use `SCF-v1` or a later explicitly-versioned equivalent for handshake, liveness, resume, and shutdown control traffic | P0 |
| FSPA-R28 | `handshake_request` MUST declare protocol versions, encodings, security profiles, message profiles, acceptable registry snapshots, requested mode, and session features explicitly | P0 |
| FSPA-R29 | `handshake_response` MUST either accept with one explicit selected tuple or reject with an explicit rejection code; silent downgrade is invalid | P0 |
| FSPA-R30 | Heartbeat failure beyond `AACP_HEARTBEAT_MISS_THRESHOLD` MUST transition the session to `FAILED` and block further business traffic on that session_id | P1 |
| FSPA-R31 | Graceful shutdown MUST stop new business exchanges, drain or explicitly abort in-flight work, and emit an explicit `session_close_ack` outcome | P1 |
| FSPA-R32 | Session recovery MUST reference authoritative L4 lineage fields and MUST NOT mint substitute lineage to make recovery appear contiguous | P0 |
| FSPA-R33 | Successful session resume MUST mint a new `session_id` while preserving existing `conversation_id`, `workflow_id`, and business-message lineage where replay is required | P1 |
| FSPA-R34 | Stateless mode MUST be explicitly negotiated, MUST NOT advertise resume guarantees, and MUST auto-close after one initiating business exchange and one terminal response or error | P0 |
| FSPA-R35 | Session control frames MUST remain outside the L4 business message-class inventory and MUST NOT be used to carry business payload semantics | P0 |
| FSPA-R36 | `SES` descriptors MAY mirror session facts for semantic use, but they MUST NOT replace the L2 control-frame transcript or the L4 lineage ledger | P1 |
| FSPA-R37 | The HTTP transport binding MUST expose `POST /aacp/handshake`, `POST /aacp/message`, and `POST /aacp/stream` as the canonical carrier entry points for HTTP session-control, business-message, and stream-init traffic | P0 |
| FSPA-R38 | Network HTTP binding deployments MUST require TLS 1.3 or later for all non-localhost traffic and MUST emit HSTS on HTTPS endpoints | P0 |
| FSPA-R39 | The HTTP binding MUST map `AASL-T`, `AASL-J`, and `AASL-B` only to `application/aacp`, `application/aacp+json`, and `application/aacp+bin` respectively; implicit encoding fallback is invalid | P0 |
| FSPA-R40 | HTTP clients and servers MUST declare `Content-Type` explicitly and MUST fail closed on unsupported or ambiguous media types rather than guessing an alternate encoding | P0 |
| FSPA-R41 | The normative network profile for the HTTP binding MUST support HTTP/2 multiplexing; if HTTP/3 is offered, it MUST preserve identical L2-L5 semantics and media-type rules | P1 |
| FSPA-R42 | `POST /aacp/stream` MUST either reject explicitly or mint a concrete stream resource whose SSE carrier is retrieved from `/aacp/stream/{stream_id}` with `Content-Type: text/event-stream` | P1 |
| FSPA-R43 | HTTP transport status codes, headers, and connection features MAY report carrier state, but they MUST NOT replace explicit AACP control outcomes, business outcomes, lineage, or semantic identity | P1 |
| FSPA-R44 | The HTTP binding MUST support manifest retrieval via HTTP `GET` at the canonical manifest URL defined by the Agent Manifest specification and MUST NOT introduce a conflicting authoritative manifest path | P1 |
| FSPA-R45 | The gRPC binding MUST define `AACPService-v1` with canonical RPCs for `Handshake`, `SendMessage`, `StreamMessages`, `BiStream`, and `GetManifest`; `DiscoverTools` and `InvokeTool` MAY exist only as LCML-equivalent convenience aliases | P0 |
| FSPA-R46 | The gRPC binding MUST define `AACPMessageClassPB` over the complete 42-class LCML inventory and MUST NOT rename, omit, or transport-specialize canonical business classes | P0 |
| FSPA-R47 | Native gRPC deployments MUST use HTTP/2 and TLS 1.3 or later for non-localhost traffic; gRPC-Web or JSON transcoding MUST NOT be treated as the normative native binding | P0 |
| FSPA-R48 | `SCF-v1` control traffic carried over gRPC MUST remain a faithful protobuf projection of the existing session-control model and MUST NOT introduce carrier-only substitutes for handshake, liveness, resume, or shutdown semantics | P0 |
| FSPA-R49 | `AASL-B` over gRPC MUST use the deterministic protobuf carrier profile `AACP-PB-v1`, and canonical hashes MUST remain derived from the L5/L4 canonical procedures rather than raw protobuf wire bytes | P0 |
| FSPA-R50 | If `AASL-T` or `AASL-J` is the negotiated encoding, the gRPC binding MUST carry that encoding explicitly and MUST NOT silently up-convert the payload to `AASL-B` | P1 |
| FSPA-R51 | gRPC metadata MAY carry transport-local security and tracing hints, but lineage, registry snapshot, provenance class, selected encoding, and authority-binding references MUST remain inside the AACP carrier messages | P0 |
| FSPA-R52 | `BiStream` and `StreamMessages` MUST preserve per-session and per-stream ordering without rewriting lineage or `stream_id` parentage to fit carrier multiplexing behavior | P1 |
| FSPA-R53 | The gRPC binding MUST support `grpc.health.v1.Health`, and carrier health failures MUST surface as transport-local refusal rather than fabricated AACP business or semantic outcomes | P1 |
| FSPA-R54 | `DiscoverTools`, `InvokeTool`, and `GetManifest` MUST remain transport projections of the canonical LCML and manifest surfaces, not independent protobuf-only semantic APIs | P1 |
| FSPA-R55 | The WebSocket binding MUST define `AACP-WS-v1` as the normative persistent duplex carrier and MUST require `wss://` with TLS 1.3 or later for all non-localhost traffic | P0 |
| FSPA-R56 | The HTTP Upgrade for WebSocket carriage MUST NOT be treated as AACP session establishment; the first complete application message MUST be `SCF-v1 handshake_request`, and no business traffic is valid before `handshake_response.decision = ACCEPT` | P0 |
| FSPA-R57 | The WebSocket binding MUST map negotiated encodings explicitly: `AASL-B` to binary messages only, and `AASL-T` / `AASL-J` to UTF-8 text messages only; silent text-binary transcoding is invalid | P0 |
| FSPA-R58 | After transport reassembly, each complete WebSocket message MUST carry exactly one `SCF-v1` control frame, one AACP business envelope, or one ordered business batch; carrier fragmentation MUST NOT rewrite lineage or canonical identity | P0 |
| FSPA-R59 | `SCF-v1` heartbeat semantics remain authoritative over WebSocket; transport-local Ping/Pong MAY be used as supplemental keepalive only and MUST NOT satisfy or reset AACP liveness obligations by themselves | P0 |
| FSPA-R60 | Automatic WebSocket reconnect MUST be bounded exponential backoff with explicit jitter, and reconnect success MUST NOT be assumed until a new handshake or resume exchange is accepted | P1 |
| FSPA-R61 | WebSocket recovery attempts MUST use authoritative lineage-referenced recovery cursors; `last_seen_message_id` is a recovery cursor only and MUST NOT be treated as replacement lineage or synthetic acknowledgement state | P0 |
| FSPA-R62 | Full-duplex WebSocket carriage MUST preserve ordering within each lineage branch and each `stream_id`, even when simultaneous send/receive or carrier fragmentation occurs on the same socket | P1 |
| FSPA-R63 | WebSocket close codes, negotiated extensions, and carrier-local diagnostics MAY report transport state, but they MUST NOT fabricate LCML business outcomes, semantic errors, or divergent manifest/tool semantics | P1 |
| FSPA-R64 | The stdio binding MUST define `AACP-STDIO-v1` as UTF-8 NDJSON over stdin/stdout with exactly one LF-terminated JSON record per complete `SCF-v1` control frame, business envelope, or ordered business batch | P0 |
| FSPA-R65 | The normative stdio binding MUST negotiate `AASL-J` only; attempts to select `AASL-T`, `AASL-B`, binary framing, or implicit alternate encodings MUST fail closed | P0 |
| FSPA-R66 | After spawn or attachment, the initiator MUST send `SCF-v1 handshake_request` within `AACP_STDIO_HANDSHAKE_DEADLINE_MS`, and no business traffic is valid before an accepted `handshake_response` | P0 |
| FSPA-R67 | `stderr` MAY carry transport-local diagnostics, but canonical AACP carriage, lineage, hashing, and business outcomes MUST remain exclusively on stdin/stdout | P0 |
| FSPA-R68 | Graceful stdio shutdown MUST use explicit `SCF-v1` close traffic and allow up to `AACP_STDIO_SHUTDOWN_GRACE_MS` for drain and acknowledgement before forced process termination | P1 |
| FSPA-R69 | Child exit, stdout EOF, broken pipe, malformed NDJSON, or invalid framing on stdio MUST surface as transport-local failure and MUST NOT be rewritten as fabricated LCML success or error semantics | P0 |
| FSPA-R70 | Parent-managed process respawn alone MUST NOT imply session continuity; a resumed exchange requires a fresh handshake or an explicit accepted `session_resume_request` that preserves authoritative lineage rules | P0 |
| FSPA-R71 | Process-local supervision metadata such as PID, executable path, environment, or file-descriptor state MAY support runtime management, but they MUST NOT replace canonical lineage, registry snapshot, provenance class, or `C40` authority context in AACP messages | P0 |
| FSPA-R72 | The stdio binding MUST preserve record order exactly as emitted and MUST NOT split one canonical AACP unit across multiple NDJSON records or merge multiple canonical units into a single record | P0 |

### 10.1 Conformance vectors

| Vector | Condition | Expected result |
|---|---|---|
| CV-1 Cross-encoding identity | The same message envelope and semantic payload are carried once in `AASL-T`, once in `AASL-J`, and once in `AASL-B` under the same registry snapshot | All three yield identical `payload_canonical_hash` and identical `message_canonical_hash` |
| CV-2 Root lineage completeness | A root message is emitted once with `parent_message_id: null` and once with the field omitted | The explicit-`null` form is valid; the omitted-field form is invalid |
| CV-3 Provenance non-interference | Two payloads differ only in non-identity-bearing provenance fields while sharing the same pinned semantics snapshot | `payload_canonical_hash` remains identical |
| CV-4 Message identity sensitivity | Two messages share the same canonical payload but differ in `workflow_id` or `message_class` | `payload_canonical_hash` may match, but `message_canonical_hash` MUST differ |
| CV-5 Negotiation fail-closed | A peer offers no registry snapshot or security-profile intersection with the responder | `handshake_response.decision` is `REJECT` with an explicit rejection code |
| CV-6 Stateful liveness failure | A stateful session misses `AACP_HEARTBEAT_MISS_THRESHOLD` heartbeat replies | Session transitions to `FAILED`; new business traffic on that session_id is invalid until resume or re-handshake |
| CV-7 Resume preserves lineage | A disconnected session is resumed with valid recovery cursors and replay instructions | A new `session_id` is minted, but replayed business messages preserve their original lineage fields |
| CV-8 Stateless closure | A stateless session successfully completes one request and one terminal response | Session transitions directly to `CLOSED`, grants no resume, and emits no heartbeat traffic |
| CV-9 HTTP media-type mismatch | A session negotiated `AASL-J`, but a client submits `POST /aacp/message` with `Content-Type: application/aacp+bin` | The server rejects the request explicitly; it does not silently reinterpret the payload |
| CV-10 HTTP TLS floor | A non-localhost client attempts the HTTP binding with TLS 1.2 | The binding rejects the connection before any valid AACP exchange is established |
| CV-11 HTTP/2 multiplex isolation | Two active sessions share one HTTP/2 connection and interleave requests | Session tuples remain isolated; no request is re-bound to the wrong `session_id` or lineage context |
| CV-12 SSE carrier continuity | `POST /aacp/stream` grants a stream and the client opens `/aacp/stream/{stream_id}` | The server returns `text/event-stream`, preserves the selected encoding, and does not rewrite lineage or canonical identity in transit |
| CV-13 gRPC class inventory completeness | The `AACPMessageClassPB` enum is generated from the binding schema | It contains all 42 canonical LCML classes with no transport-local replacements or omissions |
| CV-14 gRPC AASL-B identity parity | The same business message is carried once as canonical `AASL-B` over gRPC and once over another native binding under the same registry snapshot | Both carriers yield the same `payload_canonical_hash` and `message_canonical_hash` |
| CV-15 gRPC convenience RPC equivalence | A tool invocation is sent once through `SendMessage` and once through `InvokeTool` | Both exchanges preserve the same LCML class semantics, lineage parentage, authority context, and result identity |
| CV-16 gRPC bidirectional ordering | Two independent lineage branches are interleaved on one `BiStream` session | Ordering remains valid within each lineage chain and within each `stream_id`; no carrier rewrite occurs |
| CV-17 gRPC health refusal | The server reports `NOT_SERVING` through `grpc.health.v1.Health` | Clients treat the carrier as unavailable and do not synthesize an AACP success or business-level error from the health failure |
| CV-18 WebSocket handshake gate | A client upgrades to WebSocket and sends a business envelope before any accepted `handshake_response` | The server rejects or closes the carrier explicitly; no valid AACP session is established |
| CV-19 WebSocket opcode discipline | A session negotiated `AASL-B`, but the client sends the next application message as a text WebSocket frame | The carrier rejects the frame explicitly rather than reinterpreting it as another encoding |
| CV-20 WebSocket keepalive separation | Transport-local Ping/Pong continues successfully, but no valid AACP control or business traffic arrives beyond `AACP_HEARTBEAT_MISS_THRESHOLD` | The session still transitions to `FAILED`; Ping/Pong alone does not preserve AACP liveness |
| CV-21 WebSocket resume cursor fidelity | A disconnected client reconnects, sends `session_resume_request` with valid recovery cursors, and the server resumes the session | A new `session_id` is minted, replay guidance is explicit, and replayed business messages preserve original lineage fields |
| CV-22 WebSocket duplex ordering | Two lineage branches and one `stream_id` chain are exchanged simultaneously over one socket with fragmented carrier messages | Ordering remains valid within each lineage chain and within the `stream_id`; carrier fragmentation does not alter canonical identity |
| CV-23 Stdio handshake gate | A parent spawns a child and sends a business NDJSON record before any accepted `handshake_response` | The child rejects or terminates the carrier explicitly; no valid AACP session is established |
| CV-24 Stdio encoding discipline | A stdio peer attempts to negotiate `AASL-B` or emits binary bytes on stdout in place of UTF-8 NDJSON | The exchange fails closed rather than silently transcoding or accepting the alternate encoding |
| CV-25 Stdio record framing | One business envelope is split across two NDJSON lines, or two canonical envelopes are concatenated into one line | The carrier treats the framing as invalid and reports transport-local failure |
| CV-26 Stdio shutdown boundary | A session sends explicit close traffic, drains successfully within `AACP_STDIO_SHUTDOWN_GRACE_MS`, and the child exits cleanly | The session closes gracefully; if the child is force-killed instead, the result is transport failure rather than fabricated business success |
| CV-27 Stdio stderr isolation | A child emits human-readable diagnostics on `stderr` while canonical AACP frames continue on stdout | Diagnostics remain noncanonical and do not alter lineage, hashes, or business outcomes on the canonical carrier |

---

## 11. Risks and open questions

### 11.1 Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Layer contract drift in downstream tasks | HIGH | forbidden-behavior clauses + conformance review |
| Bridge gravity becomes permanent | MEDIUM-HIGH | explicit compatibility-only status + native-priority requirement |
| Overly rigid downgrade refusal harms interoperability | MEDIUM | profile-specific negotiation matrices in later tasks |
| Binding-specific canonicalization drift | MEDIUM | `CMP-v1`, conformance vectors, and fail-closed canonicalization rules |
| Protobuf carrier drift from LCML/C40 authority surfaces | MEDIUM | `AACP-PB-v1`, 42-class enum lock, and transport-to-semantic equivalence vectors |
| WebSocket reconnect churn duplicates or forks workflow recovery | MEDIUM | bounded backoff, explicit `session_resume_request`, new `session_id` on resume, and lineage-preserving replay guidance |

### 11.2 Open questions

1. Which layer owns partial-failure semantics for streamed multi-part workflows?
2. How much security-suite heterogeneity is tolerable before session negotiation becomes brittle?
3. Should manifest discovery be modeled as pure L4 messaging or partly as L2 capability bootstrap? The architecture currently places it as a messaging construct negotiated through session.
4. What minimum native feature set is required before a deployment may retire bridges?
5. How much per-workflow replay metadata is enough for resumable sessions before later transport tasks need shard- or stream-specific recovery cursors?

### 11.3 Companion conformance authority

`T-281` defines the canonical certification tiers, vector corpus, transport
binding matrix, and zero-external-runtime gate in
`docs/specifications/C38/CONFORMANCE_AND_CERTIFICATION_FRAMEWORK.md`.
6. Should the convenience RPCs (`DiscoverTools`, `InvokeTool`) remain optional long-term, or should future framework work collapse fully onto generic message carriage once ecosystem tooling matures?
7. Should future work standardize concrete `Sec-WebSocket-Protocol` tokens, or keep them as optional transport-local hints beneath the mandatory in-band handshake?

---

## Conclusion

FSPA gives Alternative B its missing root architecture. Its essential claim is simple:

Atrahasis can own the full communication stack only if semantic meaning, message lineage, security authority, session lifecycle, and transport carriage are separated cleanly enough to evolve independently while remaining bound into one semantic-integrity chain.

That is the architectural contract this specification establishes.
