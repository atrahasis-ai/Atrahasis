# C39 - Lineage-Bearing Capability Message Lattice (LCML)

## Master Technical Specification

| Field | Value |
|---|---|
| Title | Lineage-Bearing Capability Message Lattice (LCML) |
| Version | 1.0.4 |
| Date | 2026-03-13 |
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
| `stream_end` | STREAM | notification/terminal | stream control bundle | parents prior `stream_*` message | T-243 |
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
| `resource_update_bundle` | subscribed resource change events carried via existing stream/status classes |
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
- Resource bundles MAY carry `DS{}` objects, but the metadata defined here is a resource-access overlay profile rather than a global redefinition of all `DS{}` semantics.
- Prompt bundles MAY reference `PMT` objects, but `PMT` field structure remains for `T-212`.
- Session-bound flows MAY reference `SES` identifiers where required, but `SES` object semantics remain for `T-212`.

### 8.3 Resource bundle refinements

| Bundle type | Carrier classes | Required content |
|---|---|---|
| `resource_catalog_bundle` | `resource_list` response | one or more resource-descriptor `DS{}` overlays, optional pagination or continuation cursor |
| `resource_content_bundle` | `resource_read` response | one resource descriptor, the returned content or reference, and an access provenance record bound to the returned hash/materialization |
| `resource_subscription_bundle` | `resource_subscribe` request/response | subscription intent or acknowledgment, selected `response_channel`, stable `subscription_id`, and any server-issued delivery constraints |
| `resource_update_bundle` | `stream_data` by default, `state_update` only for lifecycle/degraded status notice | `subscription_id`, resource descriptor reference/overlay, `update_kind`, `changed_at`, hash transition data, and optional changed content or tombstone/invalidation marker |

### 8.4 Prompt bundle refinements

| Bundle type | Carrier classes | Required content |
|---|---|---|
| `prompt_catalog_bundle` | `prompt_list` response | one or more prompt descriptors with canonical `prompt_id`, a `PMT` reference or inline `PMT`, parameter-surface summary, and optional cursor/filter echo |
| `prompt_template_bundle` | `prompt_get` request/response | one canonical `PMT` target, requested or accepted bindings keyed to `PMT.parameters`, and on responses one `resolution_state` plus any optional rendered projection that remains subordinate to the `PMT` identity |
| `clarification_bundle` | `clarification_request`, `clarification_response` | one stable `clarification_id`, one `blocked_message_id`, one `resolution_scope`, and either a typed `request_schema` or an `answered_inputs` map, plus optional `declined_inputs` when the responder refuses one or more requested fields |

- `prompt_catalog_bundle` MAY omit full `template_text` when access policy requires explicit `prompt_get`, but it MUST still expose enough `PMT` identity and parameter-surface detail for capability discovery.
- `prompt_template_bundle` is the authoritative prompt-retrieval surface. Even when a rendered projection is returned, the governing identity remains the `PMT` plus the accepted binding map.
- `clarification_bundle` is the canonical typed-input surface for multi-turn prompt or workflow completion. Generic status messages may report timeout or degradation, but they do not replace typed clarification payloads.

### 8.5 Stream bundle refinements

| Bundle type | Carrier classes | Required content |
|---|---|---|
| `stream_control_bundle` | `stream_begin`, `stream_end` | for `stream_begin`: `originating_message_id`, accepted `response_channel`, and any optional `subscription_id` or accepted callback descriptor; for `stream_end`: `final_sequence`, `terminal_state`, and any optional completion summary or final-result reference |
| `stream_chunk_bundle` | `stream_data` | `incremental_sequence`, one chunk payload or update body, optional `subscription_id`, and optional `progress_indicator` with stream-local progress metadata |

- `stream_control_bundle` is the authoritative lifecycle record for one logical `stream_id`. It MAY carry a `subscription_id` when the stream is rooted in a prior subscription flow, but it MUST still keep one `originating_message_id` that points back to the business message or acknowledgment that opened the stream.
- If `response_channel` is `push_callback`, `stream_control_bundle` on `stream_begin` MUST carry the accepted callback descriptor or one stable reference to it. The callback descriptor contains `callback_target`, `callback_auth_ref`, and `callback_expiry`.
- `stream_chunk_bundle` is logical reassembly material, not a transport fragment. One `stream_data` message represents one canonical chunk after any HTTP, WebSocket, or other carrier fragmentation has already been resolved.
- Push delivery does not introduce a new bundle or message class. A webhook consumer receives the same `stream_begin`, `stream_data`, and `stream_end` envelopes and bundle shapes that an SSE or WebSocket consumer would receive.

### 8.6 Sampling bundle refinements

| Bundle type | Carrier classes | Required content |
|---|---|---|
| `sampling_request_bundle` | `sampling_request` | one `prompt_surface`, one `model_preferences` bundle, one `sampling_constraints` bundle, and one `output_contract` declaration tied to the delegated invocation |
| `sampling_result_bundle` | `sampling_result` | one `execution_state`, one `model_provenance` bundle, and either one semantic output bundle or one refusal/failure record |

- `prompt_surface` is the canonical input surface for delegated generation. It MUST be expressed as either:
  - one inline semantic prompt bundle, or
  - one `PMT` reference or inline `PMT` plus the accepted binding set defined by `T-242`.
- `model_preferences` carries advisory execution hints such as preferred providers, preferred model IDs, reasoning-mode hints, latency class, or cost class. It does not guarantee that the responder can or will honor any specific model request.
- `sampling_constraints` carries bounded generation limits and policy constraints as typed AASL objects. It is the canonical location for token-budget hints, output-shape requirements, citation expectations, and tool-use posture.
- `output_contract` declares the expected result shape, such as one semantic object family, one bounded `BND{}` projection, or one schema-bound text/object result. It constrains what a valid `sampling_result` may return.
- `sampling_result_bundle` MUST disclose realized execution facts rather than restating the request:
  - `execution_state`
  - `model_provenance`
  - either `output_bundle` or `refusal_or_failure`
- `model_provenance` is the canonical execution record for delegated generation. It carries at minimum the executor/provider identity, the realized model identifier, the realized model version or digest, invocation time, completion reason, and the realized parameter set that actually governed generation.
- Sampling flows MUST NOT smuggle ambient tool authority. If delegated generation is expected to use tools, the request MUST carry an explicit external authority reference; otherwise the default tool-use posture is deny.
- If `response_channel` is `stream`, partial or progressive generation rides the existing `stream_*` family from `T-243`, but `sampling_result` remains the terminal semantic result artifact for the delegated invocation.

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
- Response contract: the responding endpoint returns a `resource_catalog_bundle` whose entries conform to the resource-descriptor `DS{}` overlay defined below.

#### `resource_read`
- Purpose: request and return resource content.
- Dual-phase rule: request and response share one class because both revolve around the same resource-content contract.
- Request contract: `target_id` MUST identify one canonical resource descriptor rather than an ephemeral transport path.
- Response contract: the response returns exactly one `resource_content_bundle` carrying the resolved descriptor, content or content reference, and access provenance bound to the returned `content_hash`.

#### `resource_subscribe`
- Purpose: request and acknowledge an ongoing resource subscription.
- Acknowledgment contract: the response MUST finalize one stable `subscription_id` and one ongoing delivery posture.
- Subsequent updates: content or descriptor change events use `stream_data` with `resource_update_bundle`; `state_update` remains reserved for subscription lifecycle or degraded-status notices when no payload-bearing update is being emitted.

#### Resource descriptor `DS{}` overlay

The resource family refines `DS{}` only enough to make resource discovery, read, and subscription interoperable at the message layer.

Every descriptor surfaced in `resource_catalog_bundle`, `resource_content_bundle`, or `resource_update_bundle` MUST expose these metadata fields:

| Field | Meaning |
|---|---|
| `resource_id` | canonical stable identifier for the resource |
| `resource_type` | semantic category of the resource |
| `resource_format` | returned format or media profile |
| `size` | current size or best-known size estimate |
| `access_level` | authority posture required to read or subscribe |
| `uri` | canonical fetch or reference URI when externally meaningful |
| `last_modified` | most recent authoritative change timestamp |
| `content_hash` | integrity anchor for the current materialized version |

The overlay is message-visible and resource-family-specific. It does not redefine unrelated `DS{}` usage elsewhere in the stack.

#### Resource read provenance contract

Every `resource_content_bundle` MUST include an access provenance record with at least:
- `provider_id`
- `accessed_at`
- `retrieval_mode`
- `content_hash`

This record states where the material came from, when it was accessed, and which version/hash was actually returned. The resource protocol itself does not fabricate a `CLM{}` or `CNF{}` wrapper for arbitrary content, but it MUST preserve any upstream claim/verification material already attached to the resource.

#### `resource_update` semantic flow (not a new message class)

LCML does not add a dedicated `resource_update` class. The canonical update flow is:
- subscription establishment via `resource_subscribe`
- stream establishment via `stream_begin` when ordered delivery is needed
- change delivery via `stream_data` carrying `resource_update_bundle`
- optional termination via `stream_end`

`state_update` MAY announce subscription health, authorization expiry, or producer-side degradation, but it MUST NOT replace `stream_data` for actual resource-content or descriptor-change payloads when a subscription is active.

Each `resource_update_bundle` MUST declare:
- `subscription_id`
- `update_kind` (`replace`, `append`, `patch`, `delete`, or `invalidate`)
- `changed_at`
- `content_hash` or a hash transition reference sufficient to identify the post-update version

If `update_kind` is `delete` or `invalidate`, the bundle MAY omit a content body but MUST still identify the affected resource and resulting invalidation state.

### 9.4 Prompt and clarification family

#### `prompt_list`
- Purpose: request or return prompt template inventory.
- Dual-phase rule: query and response share one class.
- Response contract: the responding endpoint returns a `prompt_catalog_bundle` carrying one or more prompt descriptors or inline `PMT` objects. Each entry MUST expose canonical prompt identity and the declared parameter surface. Full `template_text` MAY be elided from catalog responses when retrieval policy requires explicit `prompt_get`.

#### `prompt_get`
- Purpose: request or return a specific prompt template.
- Dual-phase rule: request and response share one class because both operate on one prompt-template contract.
- Request contract: `target_id` MUST identify one canonical `PMT`. The request payload MAY carry zero or more typed parameter bindings keyed only to canonical `PMT.parameters` names.
- Response contract: the response returns exactly one `prompt_template_bundle` carrying the resolved `PMT` reference or inline `PMT`, the accepted binding set, and one `resolution_state` (`template_only`, `partially_bound`, or `resolved`).
- Canonical rendering rule: if a rendered prompt projection is returned, the authoritative artifact remains the `PMT` identity plus the accepted binding map rather than the rendered text alone.

#### Prompt parameter resolution contract

Prompt parameter resolution is pinned-snapshot evaluation against the `PMT.parameters` surface defined by `T-212`.

- Every supplied binding MUST match one declared parameter name and satisfy the referenced `CST{}` or admitted type constraint.
- Producers MUST NOT invent undeclared defaults, silently drop unknown parameter keys, or coerce type-incompatible values into a successful resolution.
- If a consumer requests prompt retrieval without sufficient bindings, the producer MAY return `template_only` or `partially_bound` output, or MAY transition into the clarification flow defined below. In every case, unresolved slots MUST remain explicit.

#### `clarification_request`
- Purpose: request additional typed information needed to continue a workflow.
- Lineage rule: MUST parent the message whose progress is blocked.
- Request contract: the `clarification_bundle` MUST declare one `clarification_id`, one `blocked_message_id`, one `resolution_scope`, and one `request_schema` mapping required input keys to admitted type or `CST{}` references. When clarifying a `prompt_get`, requested keys SHOULD align to canonical `PMT.parameters` names.

#### `clarification_response`
- Purpose: answer a clarification request.
- Distinct-result justification: the reply resolves a blocked ambiguity rather than merely echoing catalog data.
- Response contract: the `clarification_bundle` MUST carry the same `clarification_id`, one `answered_inputs` map keyed exactly to the prior `request_schema`, and any explicit `declined_inputs` when the responder refuses one or more requested fields.

#### Multi-turn clarification model

LCML defines one canonical multi-turn prompting loop:

1. A `prompt_get` or other upstream message becomes blocked on missing or ambiguous typed input.
2. The producer emits `clarification_request` with the same `conversation_id` and `workflow_id`, plus one new `clarification_id`.
3. The consumer answers with `clarification_response`.
4. The producer either returns a resolved `prompt_get` response or emits a subsequent `clarification_request` if ambiguity remains.

Each subsequent `clarification_request` in the chain MUST parent the immediately preceding `clarification_response` while preserving the original `blocked_message_id` inside the bundle. `state_update` MAY report timeout, abandonment, or degraded prompt-service state, but it MUST NOT replace the typed clarification content itself.

### 9.5 Stream family

#### `stream_begin`
- Purpose: establish the logical stream context.
- Required fields: `stream_id`, `response_channel`.
- Bundle contract: MUST carry one `stream_control_bundle` containing `originating_message_id` and the accepted delivery posture for this `stream_id`.
- Start-of-stream rule: `stream_begin` is the first canonical business message in every stream chain. Carrier setup MAY occur earlier, but no valid `stream_data` is allowed before `stream_begin`.
- Delivery posture: `response_channel:inline` is not valid for a stream-family chain. `stream_begin` MUST therefore confirm either `response_channel:stream` or `response_channel:push_callback`.
- Carrier hints: when the granted delivery posture requires a separate carrier acquisition step, such as HTTP SSE resource retrieval under `T-220`, `stream_begin` MAY include a subordinate carrier hint or resource reference. That hint is advisory to carrier acquisition and MUST NOT replace the canonical `stream_id`.

#### `stream_data`
- Purpose: deliver an ordered partial result, update, or event chunk.
- Lineage rule: MUST parent the previous `stream_*` message in the same `stream_id` chain, or the `stream_begin` when sending the first chunk.
- Ordering contract: MUST carry one `stream_chunk_bundle` whose `incremental_sequence` starts at `1` and increases by exactly `1` for each new logical chunk in the same `stream_id`.
- Reassembly contract: receivers MAY buffer out-of-order carrier arrival, but logical reassembly is defined only by contiguous `incremental_sequence`. A receiver MUST NOT invent missing chunks, rewrite sequence numbers, or treat a forward gap as successful completion.
- Progress contract: `progress_indicator` is optional, but when present it MAY carry `completed_units`, `total_units`, `fraction_complete`, and `stage_label`. If more than one chunk reports the same numeric progress measure, that measure MUST be monotonic nondecreasing.
- Push delivery contract: webhook callbacks carry the same canonical `stream_data` envelopes. The callback carrier MUST NOT rename them into a push-only semantic event surface.

#### `stream_end`
- Purpose: terminate a stream cleanly.
- Lineage rule: MUST parent the final preceding `stream_*` message.
- Terminal contract: MUST carry one `stream_control_bundle` containing `final_sequence` plus one `terminal_state` from `completed`, `cancelled`, `failed`, `superseded`, or `expired`.
- Final-sequence rule: `final_sequence` equals the greatest `incremental_sequence` successfully emitted for the `stream_id`. A zero-chunk stream MAY close with `final_sequence: 0`.
- Completion rule: carrier shutdown, WebSocket close, SSE disconnect, or callback inactivity is not by itself a semantic completion signal. Clean business completion remains `stream_end`.

#### Push callback registration and delivery

Push is a delivery posture, not a new message class.

The canonical registration flow is:
1. An initiating business message or subscription root requests `response_channel:push_callback`.
2. That initiating payload supplies one callback descriptor with `callback_target`, `callback_auth_ref`, and `callback_expiry`.
3. The producer explicitly accepts or rejects the callback posture.
4. If accepted, the first callback payload is `stream_begin`, followed by zero or more `stream_data` messages and one terminal `stream_end`.

Rules:
- Producers MUST NOT silently downgrade `push_callback` to `inline` or ordinary stream delivery.
- Callback delivery remains carrier-local HTTP behavior layered on top of the canonical message classes already defined here.
- Callback retries preserve `message_id`, `stream_id`, and `incremental_sequence`; transport-local delivery counters are noncanonical.

#### HTTP SSE and WebSocket realization

The stream family consumes the carrier rules from `T-220` and `T-222` without changing them.

- For HTTP SSE, `POST /aacp/stream` and `GET /aacp/stream/{stream_id}` remain the carrier entry points defined by `C38`. After the SSE carrier is opened, `stream_begin` MUST be the first canonical event, each later SSE event carries exactly one complete `stream_*` envelope, and `stream_end` is the final canonical event before normal stream closure. The SSE event type SHOULD equal `message_class`.
- For WebSocket, stream traffic remains ordinary AACP business traffic after the accepted handshake. Independent `stream_id` chains MAY interleave on one socket, but ordering inside each lineage branch and each `stream_id` remains authoritative.
- `state_update` MAY announce carrier degradation, callback expiry, authorization expiry, or stream-health state, but it MUST NOT replace payload-bearing `stream_data` or terminal `stream_end` in an active stream flow.

### 9.6 Sampling family

#### `sampling_request`
- Purpose: request delegated model invocation.
- Lineage rule: MUST parent the upstream message whose workflow is requesting delegated generation, unless the sampling flow is a root workflow created specifically for delegated inference.
- Payload: one `sampling_request_bundle`.
- Request contract:
  - `prompt_surface` carries the semantic prompt input, either as an inline bundle or a `PMT`-bound prompt retrieval result.
  - `model_preferences` carries advisory model-selection and execution-profile hints.
  - `sampling_constraints` carries bounded execution controls such as output budget, schema/format requirements, citation expectations, and tool-use posture.
  - `output_contract` declares the expected result shape so the responder returns a semantic artifact compatible with the caller's downstream validation path.
- Delivery posture: `response_channel:inline` is the default. `response_channel:stream` is allowed for long-running or progressive generation, but it does not replace the terminal `sampling_result`.

#### `sampling_result`
- Purpose: return delegated model output.
- Distinct-result justification: the reply produces a new model-output artifact with distinct provenance and later verification implications.
- Lineage rule: MUST parent the initiating `sampling_request`.
- Response contract:
  - `execution_state` reports whether the delegated invocation completed, was refused, was truncated, failed, or was superseded.
  - `model_provenance` records what executor actually ran the request and under what realized parameterization.
  - `output_bundle_or_refusal` returns either a semantic result compatible with the declared `output_contract` or a typed refusal/failure record.
- Result posture:
  - A completed result MAY return one primary semantic object or one bounded `BND{}` of semantic artifacts.
  - A responder MAY include `CNF{}` only when it is exposing an explicit calibrated confidence signal; confidence MUST remain optional and MUST NOT be fabricated when the executor has no grounded confidence estimate.
  - If the responder cannot honor the requested preferences or constraints, it MUST disclose the realized execution facts in `model_provenance` and, when necessary, return `execution_state:refused` or `execution_state:failed` rather than silently coercing the request into an incompatible result.

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

#### Resource read response

```text
HEADER{
  message_class:resource_read
  message_family:RESOURCE
  interaction_mode:response
  parent_message_id:msg.241010
  target_id:ds.market_feed.01
  response_channel:inline
  provenance_mode:NATIVE
}

PAYLOAD{
  BND{bundle_type:resource_content_bundle}
}
```

#### Prompt get response

```text
HEADER{
  message_class:prompt_get
  message_family:PROMPT
  interaction_mode:response
  parent_message_id:msg.242010
  target_id:pmt.summarize.01
  response_channel:inline
  provenance_mode:NATIVE
}

PAYLOAD{
  BND{bundle_type:prompt_template_bundle}
}
```

#### Clarification request

```text
HEADER{
  message_class:clarification_request
  message_family:PROMPT
  interaction_mode:notification
  parent_message_id:msg.242010
  target_id:pmt.summarize.01
  response_channel:inline
}

PAYLOAD{
  BND{bundle_type:clarification_bundle clarification_id:clr.242.01}
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

PAYLOAD{
  BND{
    bundle_type:stream_control_bundle
    originating_message_id:msg.241220
    callback_target:https://client.example/aacp/callbacks/sub.700
    callback_auth_ref:cap.cb.700
    callback_expiry:2026-03-13T15:00:00Z
  }
}
```

#### Stream data with progress

```text
HEADER{
  message_class:stream_data
  message_family:STREAM
  interaction_mode:notification
  parent_message_id:msg.243701
  stream_id:str.700
  subscription_id:sub.700
  response_channel:push_callback
}

PAYLOAD{
  BND{
    bundle_type:stream_chunk_bundle
    incremental_sequence:1
    progress_indicator:{fraction_complete:0.50 stage_label:replay}
  }
}
```

#### Stream end after ordered delivery

```text
HEADER{
  message_class:stream_end
  message_family:STREAM
  interaction_mode:notification
  parent_message_id:msg.243702
  stream_id:str.700
  subscription_id:sub.700
  response_channel:push_callback
}

PAYLOAD{
  BND{
    bundle_type:stream_control_bundle
    final_sequence:1
    terminal_state:completed
  }
}
```

#### Sampling request

```text
HEADER{
  message_class:sampling_request
  message_family:SAMPLING
  interaction_mode:request
  message_id:msg.244100
  parent_message_id:msg.242310
  conversation_id:conv.900
  workflow_id:wf.900
  sender_id:ag.server.01
  receiver_id:ag.client.01
  target_id:sampling.default
  response_channel:inline
  provenance_mode:NATIVE
}

PAYLOAD{
  BND{
    bundle_type:sampling_request_bundle
    prompt_surface:{pmt_id:pmt.summarize.01 accepted_bindings:{target:ds.report.44 max_length:900}}
    model_preferences:{preferred_model_ids:[mdl.opus.latest] reasoning_mode_hint:deliberate latency_class:interactive}
    sampling_constraints:{max_output_tokens:900 schema_requirement:summary.v1 citation_requirement:required tool_use_policy:deny}
    output_contract:{result_family:BND result_profile:summary.v1}
  }
}
```

#### Sampling result

```text
HEADER{
  message_class:sampling_result
  message_family:SAMPLING
  interaction_mode:response
  message_id:msg.244101
  parent_message_id:msg.244100
  conversation_id:conv.900
  workflow_id:wf.900
  sender_id:ag.client.01
  receiver_id:ag.server.01
  target_id:sampling.default
  response_channel:inline
  provenance_mode:NATIVE
}

PAYLOAD{
  BND{
    bundle_type:sampling_result_bundle
    execution_state:completed
    model_provenance:{
      provider_id:prv.anthropic
      model_id:mdl.opus.latest
      model_version_or_digest:opus-4.6
      invoked_at:2026-03-13T03:05:00Z
      completion_reason:stop
      realized_parameters:{max_output_tokens:900 temperature_hint:0.2 top_p_hint:0.95}
    }
    output_bundle:{bundle_type:summary.v1}
  }
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

### 10.4 `T-241`
Defines the field-level resource access contract now incorporated here: `DS{}` access-metadata overlay, read provenance, and update carriage through existing stream/status classes without expanding the 42-class inventory.

### 10.5 `T-242`
Defines the prompt and clarification contract now incorporated here: prompt catalog/template bundle refinements, `PMT` parameter resolution, typed clarification schemas, and the canonical multi-turn clarification loop.

### 10.6 `T-240` and `T-244`
`T-240` defines the remaining business semantics for tool discovery, invocation, and accountable tool-result wrapping.

`T-244` now defines the field-level sampling contract incorporated here: delegated prompt carriage, advisory model preferences, bounded execution constraints, output-contract declaration, execution-state vocabulary, and model-provenance disclosure.

### 10.7 `T-243`
Defines the concrete stream and push operational behavior now incorporated here: ordered chunk numbering, progress semantics, explicit push-callback registration, and HTTP SSE / WebSocket realization without adding push-only classes.

### 10.8 `T-250` and `T-251`
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
| `AACP_RESOURCE_DESCRIPTOR_REQUIRED_FIELDS` | Mandatory resource-family `DS{}` overlay fields | `resource_id, resource_type, resource_format, size, access_level, uri, last_modified, content_hash` |
| `AACP_RESOURCE_UPDATE_KIND_SET` | Allowed semantic update modes | `replace, append, patch, delete, invalidate` |
| `AACP_RESOURCE_UPDATE_PRIMARY_CARRIER` | Canonical payload-bearing update class once subscribed | `stream_data` |
| `AACP_RESOURCE_STATUS_FALLBACK_CLASS` | Non-payload lifecycle/degraded-status notice class | `state_update` |
| `AACP_RESOURCE_READ_PROVENANCE_FIELDS` | Minimum provenance fields for `resource_content_bundle` | `provider_id, accessed_at, retrieval_mode, content_hash` |
| `AACP_PROMPT_RESOLUTION_STATE_SET` | Allowed `prompt_get` resolution states | `template_only, partially_bound, resolved` |
| `AACP_CLARIFICATION_SCOPE_SET` | Allowed typed clarification scopes | `prompt_parameter, workflow_input` |
| `AACP_CLARIFICATION_REQUEST_REQUIRED_FIELDS` | Minimum fields for a clarification request bundle | `clarification_id, blocked_message_id, resolution_scope, request_schema` |
| `AACP_CLARIFICATION_RESPONSE_REQUIRED_FIELDS` | Minimum fields for a clarification response bundle | `clarification_id, answered_inputs` |
| `AACP_PROMPT_RENDERING_AUTHORITY` | Canonical identity rule when a prompt is rendered | `PMT identity + accepted binding set remain authoritative` |
| `AACP_STREAM_BEGIN_REQUIRED_FIELDS` | Minimum begin-of-stream lifecycle fields | `originating_message_id, response_channel` |
| `AACP_STREAM_CHUNK_REQUIRED_FIELDS` | Minimum ordered chunk fields | `incremental_sequence` |
| `AACP_STREAM_END_REQUIRED_FIELDS` | Minimum terminal stream fields | `final_sequence, terminal_state` |
| `AACP_STREAM_TERMINAL_STATE_SET` | Allowed terminal outcomes for `stream_end` | `completed, cancelled, failed, superseded, expired` |
| `AACP_STREAM_SEQUENCE_ORIGIN` | Initial chunk sequence number for a new `stream_id` | `1` |
| `AACP_STREAM_PROGRESS_FIELDS` | Canonical optional progress keys for stream chunks | `completed_units, total_units, fraction_complete, stage_label` |
| `AACP_PUSH_CALLBACK_DESCRIPTOR_FIELDS` | Required callback-registration fields when `response_channel:push_callback` is requested | `callback_target, callback_auth_ref, callback_expiry` |
| `AACP_PUSH_DELIVERY_CARRIER` | Canonical callback-delivery posture | `HTTP POST carrying canonical AACP envelopes in the accepted encoding` |
| `AACP_SAMPLING_REQUEST_REQUIRED_FIELDS` | Minimum fields for a sampling request bundle | `prompt_surface, model_preferences, sampling_constraints, output_contract` |
| `AACP_SAMPLING_PROMPT_SURFACE_SET` | Allowed canonical prompt-input forms for delegated generation | `inline_prompt_bundle, pmt_reference` |
| `AACP_SAMPLING_PREFERENCE_FIELDS` | Canonical advisory preference fields | `preferred_model_ids, preferred_provider_ids, reasoning_mode_hint, latency_class, cost_class` |
| `AACP_SAMPLING_CONSTRAINT_FIELDS` | Canonical execution-constraint fields | `max_output_tokens, temperature_hint, top_p_hint, schema_requirement, citation_requirement, tool_use_policy` |
| `AACP_SAMPLING_RESULT_REQUIRED_FIELDS` | Minimum fields for a sampling result bundle | `execution_state, model_provenance, output_bundle_or_refusal` |
| `AACP_SAMPLING_RESULT_STATE_SET` | Allowed delegated-generation result states | `completed, refused, truncated, failed, superseded` |
| `AACP_SAMPLING_MODEL_PROVENANCE_FIELDS` | Minimum execution-fact fields disclosed by delegated generation | `provider_id, model_id, model_version_or_digest, invoked_at, completion_reason, realized_parameters` |
| `AACP_SAMPLING_DEFAULT_TOOL_POLICY` | Default tool posture for delegated generation absent explicit authority | `deny` |

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
| LCML-R19 | `resource_list` responses MUST carry a `resource_catalog_bundle` whose descriptors expose the full `AACP_RESOURCE_DESCRIPTOR_REQUIRED_FIELDS` set | P0 |
| LCML-R20 | `resource_read` responses MUST carry exactly one `resource_content_bundle` bound to the requested `target_id`, with returned content or content reference plus the full `AACP_RESOURCE_READ_PROVENANCE_FIELDS` set | P0 |
| LCML-R21 | `resource_subscribe` request/response pairs MUST converge on one stable `subscription_id` and one ongoing delivery posture, and MUST NOT silently degrade an active subscription to polling semantics | P1 |
| LCML-R22 | Payload-bearing resource change events for an active subscription MUST be emitted as `stream_data` carrying `resource_update_bundle`; `state_update` MAY only carry lifecycle or degraded-status notices for that subscription | P0 |
| LCML-R23 | Every `resource_update_bundle` MUST declare `subscription_id`, `update_kind`, `changed_at`, and enough hash/version material to identify the resulting resource state | P1 |
| LCML-R24 | The `resource_update_kind` vocabulary is bounded to the five values in `AACP_RESOURCE_UPDATE_KIND_SET` unless later governance extends it explicitly | P1 |
| LCML-R25 | The resource-family `DS{}` overlay defined here MUST remain a message-layer interoperability profile and MUST NOT silently redefine non-resource `DS{}` semantics elsewhere in Atrahasis | P0 |
| LCML-R26 | Resource-read and resource-update flows MUST preserve the canonical resource identifier in `target_id` or descriptor metadata rather than replacing it with transport-local filenames, URLs, or opaque bridge handles alone | P1 |
| LCML-R27 | `prompt_list` responses MUST carry a `prompt_catalog_bundle` whose entries expose canonical prompt identity and the declared parameter surface for each listed prompt | P0 |
| LCML-R28 | `prompt_get` requests MUST identify one canonical `PMT` in `target_id`, and supplied bindings MAY reference only declared `PMT.parameters` names | P0 |
| LCML-R29 | `prompt_get` responses MUST carry exactly one `prompt_template_bundle` with one `resolution_state` and the accepted binding set | P0 |
| LCML-R30 | Prompt parameter resolution MUST be validated against the pinned `PMT` parameter schemas from `T-212`, and MUST NOT silently invent defaults or coerce invalid bindings into success | P0 |
| LCML-R31 | If a rendered prompt projection is returned, `PMT` identity and the accepted binding set MUST remain explicit and authoritative | P1 |
| LCML-R32 | `clarification_request` MUST carry one `clarification_bundle` containing `clarification_id`, `blocked_message_id`, `resolution_scope`, and a typed `request_schema` | P0 |
| LCML-R33 | `clarification_response` MUST carry the same `clarification_id` and MUST key its answers only by inputs declared in the paired `request_schema` | P0 |
| LCML-R34 | Multi-turn clarification chains MUST preserve `conversation_id` and `workflow_id` lineage and MUST keep the original `blocked_message_id` visible until resolution or abort | P1 |
| LCML-R35 | Typed clarification MUST remain the canonical multi-turn input-completion surface; `state_update` MAY report timeout or degradation but MUST NOT replace clarification payloads | P1 |
| LCML-R36 | `stream_begin` MUST be the first canonical business message in a stream chain and MUST carry one `stream_control_bundle` containing `originating_message_id` and the accepted `response_channel` | P0 |
| LCML-R37 | If `response_channel` is `push_callback`, `stream_begin` MUST carry the full `AACP_PUSH_CALLBACK_DESCRIPTOR_FIELDS` set or one stable reference to an accepted callback descriptor; silent push acceptance without an explicit descriptor is invalid | P0 |
| LCML-R38 | `stream_data` MUST carry one `stream_chunk_bundle` whose `incremental_sequence` starts at `AACP_STREAM_SEQUENCE_ORIGIN` and increases by exactly `1` for each new chunk in the same `stream_id` | P0 |
| LCML-R39 | Receivers MAY buffer out-of-order carrier arrival, but logical reassembly MUST follow contiguous `incremental_sequence`; they MUST NOT invent missing chunks, rewrite sequence numbers, or declare completion across a forward gap | P0 |
| LCML-R40 | If `progress_indicator` is present in more than one `stream_data` chunk for the same `stream_id`, every reported numeric progress measure MUST be monotonic nondecreasing and MUST NOT imply terminal completion before `stream_end` | P1 |
| LCML-R41 | `stream_end` MUST carry one `stream_control_bundle` containing `final_sequence` and one `terminal_state` from `AACP_STREAM_TERMINAL_STATE_SET` | P0 |
| LCML-R42 | `final_sequence` MUST equal the greatest `incremental_sequence` successfully emitted for that `stream_id`; zero-chunk streams MAY close with `final_sequence: 0` | P1 |
| LCML-R43 | Push registration MUST be explicit: an initiating message that requests `response_channel:push_callback` MUST supply the `AACP_PUSH_CALLBACK_DESCRIPTOR_FIELDS` set, and the producer MUST explicitly accept or reject that delivery posture rather than silently downgrading it | P0 |
| LCML-R44 | Push delivery MUST use the existing `stream_begin`, `stream_data`, and `stream_end` classes unchanged; introducing `push_subscribe`, `push_event`, or any other push-only semantic substitute is invalid | P0 |
| LCML-R45 | Callback retries, SSE reconnect replay, or WebSocket retransmission MUST preserve canonical `message_id`, `stream_id`, and `incremental_sequence`; transport-local delivery counters or receipts MUST NOT replace message-layer idempotency identity | P1 |
| LCML-R46 | For HTTP SSE delivery, `stream_begin` MUST be the first canonical stream event after the carrier is opened, each later SSE event MUST carry exactly one complete `stream_*` envelope, and `stream_end` MUST be the final canonical stream event before normal stream closure | P1 |
| LCML-R47 | `state_update` MAY report stream health, callback expiry, or carrier degradation, but it MUST NOT replace payload-bearing `stream_data` or terminal `stream_end` in an active stream flow | P0 |
| LCML-R48 | Stream flows opened from an initiating business message MUST preserve the originating `conversation_id` and `workflow_id` across the entire `stream_id` chain and MUST keep `originating_message_id` visible until stream termination | P1 |
| LCML-R49 | `sampling_request` MUST carry exactly one `sampling_request_bundle` exposing the full `AACP_SAMPLING_REQUEST_REQUIRED_FIELDS` set | P0 |
| LCML-R50 | `prompt_surface` inside `sampling_request_bundle` MUST use one form from `AACP_SAMPLING_PROMPT_SURFACE_SET`; raw untyped prompt text alone is invalid as the canonical delegated-generation surface | P0 |
| LCML-R51 | `model_preferences` are advisory only; a responder MUST disclose the realized execution profile in `model_provenance` and MUST NOT imply that an unfulfilled preferred model was actually used | P0 |
| LCML-R52 | `sampling_constraints` MUST be represented as typed AASL constraint content and MUST preserve the bounded keys in `AACP_SAMPLING_CONSTRAINT_FIELDS`; absent explicit external authority, `tool_use_policy` defaults to `AACP_SAMPLING_DEFAULT_TOOL_POLICY` | P0 |
| LCML-R53 | `sampling_result` MUST carry exactly one `sampling_result_bundle` exposing the full `AACP_SAMPLING_RESULT_REQUIRED_FIELDS` set | P0 |
| LCML-R54 | `model_provenance` inside `sampling_result_bundle` MUST disclose the full `AACP_SAMPLING_MODEL_PROVENANCE_FIELDS` set | P0 |
| LCML-R55 | `execution_state` in `sampling_result_bundle` is bounded to `AACP_SAMPLING_RESULT_STATE_SET`; a responder MUST use `refused`, `truncated`, `failed`, or `superseded` rather than silently coercing an incompatible request into a nominally successful result | P1 |
| LCML-R56 | When `sampling_request` selects `response_channel:stream`, any progressive output MUST use the existing `stream_*` family from `T-243`, and `sampling_result` MUST remain the terminal semantic result artifact for that delegated invocation | P1 |

---

## 13. Risks and open questions

### 13.1 Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Legacy baseline normalization is disputed | MEDIUM | cite current repo lineage and record the normalization rule explicitly |
| Push-as-mode is misread as transport-specific behavior | MEDIUM | keep `response_channel` logical and require the same `stream_*` classes across SSE, WebSocket, and callback carriers |
| Downstream tasks re-inflate the inventory casually | HIGH | governance gate on growth beyond 42 |
| Bridge provenance labels are applied inconsistently | HIGH | T-250/T-251 must consume `provenance_mode` normatively |
| Resource providers leak incompatible ad hoc metadata into the `DS{}` overlay | MEDIUM | keep one bounded required-field set and treat extra provider fields as optional extensions rather than new mandatory semantics |
| Prompt providers return rendered text without preserving `PMT` identity or accepted bindings | HIGH | keep `prompt_template_bundle` authoritative and require rendered text to remain subordinate to the semantic template identity |
| Callback registration drifts into per-family ad hoc payloads | HIGH | keep one bounded callback descriptor field set and require explicit push acceptance or rejection |
| Producers signal completion through carrier close instead of `stream_end` | HIGH | make `stream_end` the only canonical completion signal and treat carrier close as transport state only |
| Delegated generation is misused as an implicit tool-execution path | HIGH | keep `tool_use_policy` explicit, default it to deny, and require external authority references for any tool-enabled sampling flow |

### 13.2 Open questions

1. Should any historical draft-era control-plane classes be formally reintroduced later, or should they remain archival lineage only?
2. Does `resource_update_bundle` eventually need a compression/delta profile beyond `replace`, `append`, `patch`, `delete`, and `invalidate`, or is that bounded set sufficient for Phase 1-4 interoperability?
3. Should later conformance tooling standardize explicit callback retry budgets and delivery receipts, or is message-level idempotency over `message_id`, `stream_id`, and `incremental_sequence` sufficient?
4. Do long-lived native streams eventually need a standardized backpressure advisory surface, or can backpressure remain carrier-local as long as canonical ordering and completion rules are preserved?
5. Should later governance standardize optional token-usage, reasoning-summary, or logprob disclosure inside `model_provenance`, or should the canonical sampling contract stay limited to execution identity and realized parameters?

---

## Conclusion

LCML gives Alternative B the bounded message inventory it was missing.

Its essential claim is simple:

Atrahasis can absorb the operational surfaces of A2A and MCP without losing message clarity only if the class inventory is expanded through explicit capability families, mandatory lineage, and strict class-economy rules rather than uncontrolled verb growth.

That is the contract this specification establishes.
