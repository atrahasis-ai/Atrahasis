# C39 - Lineage-Bearing Capability Message Lattice (LCML)

## Master Technical Specification

| Field | Value |
|---|---|
| Title | Lineage-Bearing Capability Message Lattice (LCML) |
| Version | 1.0.0 |
| Date | 2026-03-12 |
| Invention ID | C39 |
| Task ID | T-211 |
| System | Atrahasis Agent System v2.4 |
| Stage | SPECIFICATION |
| Normative References | ADR-041, ADR-042, ADR-043, C38 FSPA, C3, legacy AASL/AACP message lineage |

---

## Table of Contents

1. System role and architectural position
2. Design principles
3. Normalized legacy baseline (23 classes)
4. LCML extension model
5. Nineteen new message classes
6. Resulting 42-class canonical inventory
7. Header extensions
8. Bundle contracts and payload obligations
9. Canonical class behavior by family
10. Downstream contract boundaries
11. Parameters
12. Formal requirements
13. Risks and open questions

---

## 1. System role and architectural position

### 1.1 Purpose

LCML defines the canonical L4 Messaging expansion for Alternative B. It is the upstream authority for how AACP v2 grows from the normalized 23-class current baseline to a 42-class inventory capable of supporting:
- agent discovery,
- tool connectivity,
- resource access,
- prompting and clarification,
- streaming and push-style delivery,
- delegated sampling.

### 1.2 The problem it solves

Before LCML, the repo had:
- a sovereign five-layer architecture in C38,
- a governance path for new AASL type families in ADR-043,
- an Alternative B packet that named the required operational surfaces,
- but no canonical message-layer design explaining how those surfaces become classes without inventory sprawl or cross-layer leakage.

Without LCML, downstream tasks would be forced to:
- guess which surfaces deserve dedicated classes,
- overcount transport-specific push/update variants,
- or hide meaning in payload conventions rather than explicit message classes.

### 1.3 Architectural position

Under C38, LCML lives entirely in L4 Messaging.

LCML defines:
- message classes,
- message-family grouping,
- lineage rules,
- header extensions,
- bundle-level payload obligations.

LCML does **not** define:
- L1 transport bindings,
- L2 handshake or session recovery frames,
- L3 security suites,
- L5 semantic object internals such as `TL{}`, `PMT{}`, `SES{}`, or Agent Manifest field structure.

---

## 2. Design principles

### 2.1 Explicit capability families

New operational surfaces are grouped into visible message families rather than hidden inside generic RPC verbs.

### 2.2 Class economy

A new message class is justified only when it creates materially distinct:
- lineage behavior,
- validation obligations,
- downstream trust/storage consequences,
- or notification semantics.

If request and response share the same core semantic contract, one dual-phase class is preferred.

### 2.3 Lineage completeness

Every new class inherits the mandatory four-field lineage from the Atrahasis lineage and C38:
- `message_id`
- `parent_message_id`
- `conversation_id`
- `workflow_id`

### 2.4 Delivery-mode separation

Push behavior is a message-layer delivery choice, not automatically a separate class family. This keeps L4 distinct from L1 binding specifics.

### 2.5 Semantic placeholder discipline

When a new class carries `TL`, `PMT`, `SES`, or Agent Manifest data, LCML defines the message obligation only. The semantic object internals remain downstream work.

### 2.6 Bridge honesty

Any class that can be emitted through bridges must expose provenance posture at the header layer so native and translated flows remain distinguishable.

---

## 3. Normalized legacy baseline (23 classes)

### 3.1 Why normalization is required

The older Atrahasis/AACP lineage contains more than one draft-era message inventory. LCML therefore establishes the **canonical pre-extension baseline** used by the current repo and Alternative B planning. Historical draft names outside this normalized baseline remain lineage artifacts, not the authoritative 23-class inventory for this task.

### 3.2 Canonical legacy families

#### Runtime lifecycle (11)

| Class |
|---|
| `task_submission` |
| `task_assignment` |
| `task_result` |
| `verification_request` |
| `verification_result` |
| `memory_lookup_request` |
| `memory_lookup_result` |
| `memory_admission_request` |
| `memory_admission_result` |
| `state_update` |
| `error_report` |

#### Coordination control (7)

| Class |
|---|
| `signal_publish` |
| `claim_submit` |
| `lease_request` |
| `lease_grant` |
| `lease_deny` |
| `attestation_submit` |
| `bundle_commit` |

#### Tidal extension (5)

| Class |
|---|
| `TIDAL_SCHEDULE_ANNOUNCE` |
| `SURPRISE_DELTA` |
| `TIDAL_VERSION_PROPOSE` |
| `ETR_VOTE` |
| `SETTLEMENT_PUBLISH` |

### 3.3 Historical note

Older Noosphere-era drafts contain additional operational names such as capsule, governance, and other control-path messages. LCML does not promote those draft-era names into the canonical 23-class baseline because the live Alternative B backlog and current repo state rely on the normalized inventory above.

---

## 4. LCML extension model

### 4.1 The lattice

Each new class is positioned by three attributes:

| Attribute | Meaning |
|---|---|
| `message_family` | discovery, tool, resource, prompt, stream, or sampling |
| `interaction_mode` | request, response, or notification |
| lineage rule | how `parent_message_id` and related continuation behavior must be applied |

### 4.2 Dual-phase rule

A class MAY be dual-phase when both request and response:
- operate over the same capability object family,
- share one validation profile,
- and do not create a new downstream trust/storage artifact class.

Examples:
- `agent_manifest_query`
- `tool_discovery`
- `resource_list`
- `resource_read`
- `resource_subscribe`
- `prompt_list`
- `prompt_get`

### 4.3 Distinct-result rule

A separate result class is REQUIRED when the reply:
- creates a materially distinct semantic artifact,
- has different provenance or storage consequences,
- or needs downstream verification/retention treatment different from the initiating request.

Examples:
- `tool_result`
- `sampling_result`
- `clarification_response`

### 4.4 Push compression rule

Push-style delivery is represented through `response_channel` and stream lineage rather than separate push-only classes. This is the primary rule that preserves the 19-class target.

---

## 5. Nineteen new message classes

| Class | Family | Mode | Primary payload contract | Parent rule | Downstream refinement |
|---|---|---|---|---|---|
| `agent_manifest_publish` | DISCOVERY | notification | manifest publication/update bundle | root or prior manifest publication | T-214 |
| `agent_manifest_query` | DISCOVERY | request/response | manifest query or manifest result bundle | response parents the query | T-214 |
| `agent_manifest_update` | DISCOVERY | notification | manifest delta or replacement bundle | prior publish/update | T-214 |
| `tool_discovery` | TOOL | request/response | tool inventory query/result bundle | response parents the query | T-240 |
| `tool_invocation` | TOOL | request | tool invocation bundle | parents upstream caller | T-240 |
| `tool_result` | TOOL | response | tool result bundle | parents `tool_invocation` | T-240 |
| `tool_change_notification` | TOOL | notification | tool inventory delta bundle | prior publish/update or subscription root | T-240 |
| `resource_list` | RESOURCE | request/response | resource catalog query/result bundle | response parents the query | T-241 |
| `resource_read` | RESOURCE | request/response | resource content request/result bundle | response parents the query | T-241 |
| `resource_subscribe` | RESOURCE | request/response | subscription request/ack bundle | ack parents the request | T-241, T-243 |
| `prompt_list` | PROMPT | request/response | prompt catalog query/result bundle | response parents the query | T-242 |
| `prompt_get` | PROMPT | request/response | prompt template request/result bundle | response parents the query | T-242 |
| `clarification_request` | PROMPT | notification/request | clarification bundle | parents blocked upstream message | T-242 |
| `clarification_response` | PROMPT | response | clarification answer bundle | parents `clarification_request` | T-242 |
| `stream_begin` | STREAM | notification/control | stream control bundle | parents request that opened stream | T-243 |
| `stream_data` | STREAM | notification | stream chunk bundle | parents prior `stream_*` message | T-243 |
| `stream_end` | STREAM | notification/terminal | stream completion bundle | parents prior `stream_*` message | T-243 |
| `sampling_request` | SAMPLING | request | delegated sampling bundle | parents upstream tool/prompt/workflow message | T-244 |
| `sampling_result` | SAMPLING | response | sampling result bundle | parents `sampling_request` | T-244 |

### 5.1 Deliberate non-classes

The following surfaces are intentionally **not** separate new classes in LCML:

- `push_subscribe`
- `push_event`
- `resource_update`
- `manifest_result`
- `prompt_result`

Reason:
- push is modeled through stream-family response channels,
- some query-like surfaces remain dual-phase classes,
- resource updates may ride `stream_data` or existing `state_update` depending on whether the producer is in a subscribed capability stream or a general runtime status path.

---

## 6. Resulting 42-class canonical inventory

### 6.1 Family counts

| Family | Count |
|---|---|
| Runtime lifecycle | 11 |
| Coordination control | 7 |
| Tidal extension | 5 |
| Discovery | 3 |
| Tool | 4 |
| Resource | 3 |
| Prompt | 4 |
| Stream | 3 |
| Sampling | 2 |
| **Total** | **42** |

### 6.2 Full inventory

#### Legacy 23

`task_submission`, `task_assignment`, `task_result`, `verification_request`, `verification_result`, `memory_lookup_request`, `memory_lookup_result`, `memory_admission_request`, `memory_admission_result`, `state_update`, `error_report`, `signal_publish`, `claim_submit`, `lease_request`, `lease_grant`, `lease_deny`, `attestation_submit`, `bundle_commit`, `TIDAL_SCHEDULE_ANNOUNCE`, `SURPRISE_DELTA`, `TIDAL_VERSION_PROPOSE`, `ETR_VOTE`, `SETTLEMENT_PUBLISH`

#### New 19

`agent_manifest_publish`, `agent_manifest_query`, `agent_manifest_update`, `tool_discovery`, `tool_invocation`, `tool_result`, `tool_change_notification`, `resource_list`, `resource_read`, `resource_subscribe`, `prompt_list`, `prompt_get`, `clarification_request`, `clarification_response`, `stream_begin`, `stream_data`, `stream_end`, `sampling_request`, `sampling_result`

---

## 7. Header extensions

### 7.1 New message-layer fields

| Field | Purpose | Required for |
|---|---|---|
| `message_family` | Class-family grouping for validation and routing | all 19 new classes |
| `interaction_mode` | request, response, or notification | all 19 new classes |
| `target_id` | primary capability target such as manifest, tool, resource, prompt, or sampling target | capability-targeted classes |
| `subscription_id` | stable identifier for ongoing subscriptions | `resource_subscribe`, `stream_*` when subscribed |
| `stream_id` | stable identifier for one stream instance | `stream_begin`, `stream_data`, `stream_end` |
| `response_channel` | inline, stream, or push callback mode | classes that may result in deferred delivery |
| `provenance_mode` | `NATIVE`, `BRIDGE_ENRICHED`, or `BRIDGE_DEGRADED` | classes that may traverse bridges |

### 7.2 Field intent

- `message_family` and `interaction_mode` are validation-visible and MUST NOT be inferred purely from `message_class`.
- `target_id` is a message-layer reference, not a substitute for semantic object definition.
- `response_channel` is a logical delivery posture. It does not encode a concrete transport binding.
- `provenance_mode` provides L4 visibility into whether guarantees are native or bridge-mediated.

---

## 8. Bundle contracts and payload obligations

### 8.1 Canonical bundle set introduced by LCML

| Bundle type | Primary use |
|---|---|
| `agent_manifest_bundle` | manifest publication and manifest query responses |
| `agent_manifest_query_bundle` | manifest query request |
| `tool_inventory_bundle` | tool discovery responses and tool change notifications |
| `tool_invocation_bundle` | tool invocation request |
| `tool_result_bundle` | tool invocation response |
| `resource_catalog_bundle` | resource listing responses |
| `resource_content_bundle` | resource reads |
| `resource_subscription_bundle` | subscription requests and acknowledgments |
| `prompt_catalog_bundle` | prompt listing responses |
| `prompt_template_bundle` | prompt retrieval |
| `clarification_bundle` | clarification requests and answers |
| `stream_control_bundle` | stream begin/end control messages |
| `stream_chunk_bundle` | stream data chunks |
| `sampling_request_bundle` | delegated LLM invocation requests |
| `sampling_result_bundle` | delegated LLM results |

### 8.2 Payload obligations by family

- Discovery bundles MUST carry manifest references or manifest payloads, but full manifest schema remains for `T-214`.
- Tool bundles MAY reference `TL`-family objects, but `TL` field structure remains for `T-212`.
- Prompt bundles MAY reference `PMT` objects, but `PMT` field structure remains for `T-212`.
- Session-bound flows MAY reference `SES` identifiers where required, but `SES` object semantics remain for `T-212`.

---

## 9. Canonical class behavior by family

### 9.1 Discovery family

#### `agent_manifest_publish`
- Purpose: publish a full manifest to a registry, endpoint, or subscriber.
- Lineage rule: MAY be root for a capability advertisement chain.
- Payload: one `agent_manifest_bundle`.

#### `agent_manifest_query`
- Purpose: request manifests or return matched manifests.
- Dual-phase rule: request and response share the same class; `interaction_mode` disambiguates.
- Response lineage: MUST parent the initiating query.

#### `agent_manifest_update`
- Purpose: notify that a published manifest has changed.
- Lineage rule: MUST parent the previous publish/update event that is being superseded or amended.

### 9.2 Tool family

#### `tool_discovery`
- Purpose: discover tool inventory.
- Dual-phase rule: request and response share one class.
- Response payload: one `tool_inventory_bundle`, potentially carrying `TL` references.

#### `tool_invocation`
- Purpose: invoke a tool with semantically typed arguments.
- Lineage rule: MUST parent the message that caused the tool call if invoked inside an existing workflow.

#### `tool_result`
- Purpose: return the result of a tool invocation.
- Distinct-result justification: the response produces a new result artifact with distinct provenance and downstream trust implications.
- Lineage rule: MUST parent the `tool_invocation`.

#### `tool_change_notification`
- Purpose: notify subscribers that tool inventory changed.
- Lineage rule: MUST parent the publish/update or subscription root that grounds the notification context.

### 9.3 Resource family

#### `resource_list`
- Purpose: list readable/subscribable resources.
- Dual-phase rule: query and response share one class.

#### `resource_read`
- Purpose: request and return resource content.
- Dual-phase rule: request and response share one class because both revolve around the same resource-content contract.

#### `resource_subscribe`
- Purpose: request and acknowledge an ongoing resource subscription.
- Subsequent updates: delivered via `stream_data` or `state_update` depending on whether the producer is inside a capability stream or a general runtime-status channel.

### 9.4 Prompt and clarification family

#### `prompt_list`
- Purpose: request or return prompt template inventory.

#### `prompt_get`
- Purpose: request or return a specific prompt template.

#### `clarification_request`
- Purpose: request additional typed information needed to continue a workflow.
- Lineage rule: MUST parent the message whose progress is blocked.

#### `clarification_response`
- Purpose: answer a clarification request.
- Distinct-result justification: the reply resolves a blocked ambiguity rather than merely echoing catalog data.

### 9.5 Stream family

#### `stream_begin`
- Purpose: establish the logical stream context.
- Required fields: `stream_id`, `response_channel`.

#### `stream_data`
- Purpose: deliver an ordered partial result, update, or event chunk.
- Lineage rule: MUST parent the previous `stream_*` message in the same `stream_id` chain, or the `stream_begin` when sending the first chunk.

#### `stream_end`
- Purpose: terminate a stream cleanly.
- Lineage rule: MUST parent the final preceding `stream_*` message.

### 9.6 Sampling family

#### `sampling_request`
- Purpose: request delegated model invocation.
- Payload: one `sampling_request_bundle`.

#### `sampling_result`
- Purpose: return delegated model output.
- Distinct-result justification: the reply produces a new model-output artifact with distinct provenance and later verification implications.

### 9.7 Canonical message skeleton examples

#### Tool invocation

```text
HEADER{
  protocol_version:2.0.0
  aasl_version:1.0.0
  ontology_version:1.1
  message_id:msg.211001
  conversation_id:conv.500
  workflow_id:wf.500
  parent_message_id:msg.210888
  sender_id:ag.coordinator.01
  receiver_id:ag.toolhost.01
  message_class:tool_invocation
  message_family:TOOL
  interaction_mode:request
  target_id:tl.web_search.01
  response_channel:inline
  provenance_mode:NATIVE
  payload_encoding:AASL-T
  timestamp:2026-03-12T13:30:00Z
  status:pending
}

PAYLOAD{
  BND{bundle_type:tool_invocation_bundle source_task_id:t.500}
}
```

#### Resource subscription

```text
HEADER{
  message_class:resource_subscribe
  message_family:RESOURCE
  interaction_mode:request
  target_id:ds.market_feed.01
  subscription_id:sub.700
  response_channel:stream
}
```

#### Stream begin in push mode

```text
HEADER{
  message_class:stream_begin
  message_family:STREAM
  interaction_mode:notification
  stream_id:str.700
  subscription_id:sub.700
  response_channel:push_callback
}
```

#### Sampling result

```text
HEADER{
  message_class:sampling_result
  message_family:SAMPLING
  interaction_mode:response
  parent_message_id:msg.211090
  provenance_mode:BRIDGE_ENRICHED
}
```

---

## 10. Downstream contract boundaries

### 10.1 `T-212`
Defines the semantic internals of `TL{}`, `PMT{}`, and `SES{}` referenced by LCML.

### 10.2 `T-214`
Defines the full Agent Manifest object model carried by the discovery-family classes.

### 10.3 `T-215`
Defines canonical hash computation and cross-encoding identity rules for the classes and bundles named here.

### 10.4 `T-240`, `T-241`, `T-242`, `T-244`
Define the business semantics and field-level protocol surfaces for tool, resource, prompt, clarification, and sampling flows.

### 10.5 `T-243`
Defines the concrete stream and push operational behavior for `stream_begin`, `stream_data`, and `stream_end` across bindings.

### 10.6 `T-250` and `T-251`
Consume `provenance_mode` and family structure to define native-versus-bridge translation honesty.

---

## 11. Parameters

| Parameter | Meaning | Initial value / guidance |
|---|---|---|
| `AACP_LEGACY_BASELINE_CLASS_COUNT` | Canonical pre-extension class count | `23` |
| `AACP_NEW_CLASS_COUNT` | Number of new classes added by LCML | `19` |
| `AACP_CANONICAL_CLASS_TOTAL` | Total class inventory after LCML | `42` |
| `AACP_MESSAGE_FAMILY_SET` | Canonical family labels for new classes | `DISCOVERY, TOOL, RESOURCE, PROMPT, STREAM, SAMPLING` |
| `AACP_RESPONSE_CHANNEL_SET` | Allowed logical delivery modes | `inline, stream, push_callback` |
| `AACP_PROVENANCE_MODE_SET` | Bridge/native posture labels | `NATIVE, BRIDGE_ENRICHED, BRIDGE_DEGRADED` |
| `AACP_MANDATORY_HEADER_EXTENSIONS` | New LCML header fields | `message_family, interaction_mode, target_id, subscription_id, stream_id, response_channel, provenance_mode` |

---

## 12. Formal requirements

| ID | Requirement | Priority |
|---|---|---|
| LCML-R01 | AACP v2 MUST normalize its pre-extension baseline to the 23-class inventory defined in this specification before adding new classes | P0 |
| LCML-R02 | LCML MUST add exactly 19 new classes and produce a canonical 42-class inventory | P0 |
| LCML-R03 | Every new class MUST declare a `message_family` and `interaction_mode` in the message header | P0 |
| LCML-R04 | Every new class MUST preserve the four mandatory lineage fields inherited from legacy AACP lineage and C38 | P0 |
| LCML-R05 | A new distinct result class MUST be introduced only when the response has materially different downstream semantic, provenance, or retention consequences | P0 |
| LCML-R06 | Query-like discovery, resource, and prompt interactions MAY use dual-phase classes when request and response share one semantic contract | P1 |
| LCML-R07 | Push-style delivery MUST be modeled through `response_channel` and stream-family behavior rather than extra push-only message classes | P0 |
| LCML-R08 | `tool_result` MUST remain distinct from `tool_invocation` | P0 |
| LCML-R09 | `sampling_result` MUST remain distinct from `sampling_request` | P0 |
| LCML-R10 | `clarification_response` MUST parent a prior `clarification_request` | P1 |
| LCML-R11 | `stream_data` and `stream_end` MUST carry or inherit a valid `stream_id` established by `stream_begin` | P0 |
| LCML-R12 | `resource_subscribe` MUST create a stable `subscription_id` for later stream or status updates | P1 |
| LCML-R13 | Classes that can traverse a bridge MUST expose `provenance_mode` explicitly | P0 |
| LCML-R14 | LCML MUST NOT define semantic field internals reserved for `T-212` or `T-214` | P0 |
| LCML-R15 | The bundle contracts named here MUST remain message-layer obligations and MUST NOT be treated as transport-binding definitions | P0 |
| LCML-R16 | Any future proposal to exceed 42 canonical classes MUST be handled as later governance work rather than silent downstream drift | P1 |
| LCML-R17 | `state_update` remains the generic operational-status class and MUST NOT be silently replaced by capability-family updates where no capability-specific contract exists | P1 |
| LCML-R18 | Downstream tasks MUST refine the classes and family rules defined here instead of replacing them by implication | P0 |

---

## 13. Risks and open questions

### 13.1 Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Legacy baseline normalization is disputed | MEDIUM | cite current repo lineage and record the normalization rule explicitly |
| Push-as-mode is misread as transport-specific behavior | MEDIUM | keep `response_channel` logical and defer binding details to T-243 |
| Downstream tasks re-inflate the inventory casually | HIGH | governance gate on growth beyond 42 |
| Bridge provenance labels are applied inconsistently | HIGH | T-250/T-251 must consume `provenance_mode` normatively |

### 13.2 Open questions

1. Should any historical draft-era control-plane classes be formally reintroduced later, or should they remain archival lineage only?
2. After `T-243`, will resource updates still fit cleanly inside `stream_data` and `state_update`, or will a later dedicated class prove necessary?
3. Does conformance tooling eventually require more explicit dual-phase response typing than `interaction_mode`, or is the current model sufficient?

---

## Conclusion

LCML gives Alternative B the bounded message inventory it was missing.

Its essential claim is simple:

Atrahasis can absorb the operational surfaces of A2A and MCP without losing message clarity only if the class inventory is expanded through explicit capability families, mandatory lineage, and strict class-economy rules rather than uncontrolled verb growth.

That is the contract this specification establishes.
