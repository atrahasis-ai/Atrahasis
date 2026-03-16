# T-212 Direct Specification Draft

## Title
AASL Type Extension Specification for `TL{}`, `PMT{}`, and `SES{}`

## Task
Specify three new AASL object types for Alternative B:
- `TL{}` for tool descriptors,
- `PMT{}` for prompt templates,
- `SES{}` for session descriptors.

This task defines ontology placement, field schemas, canonicalization behavior, validation rules, and required parser/validator/compiler extensions. It does not define handshake frames, tool-result semantics, prompt exchange flows, or transport bindings.

## Governing Context
- Alternative B requires AASL-native replacements for MCP tool discovery, prompt-template exchange, and session/state surfaces.
- `T-201` already established the governance envelope: canonical registry admission, pinned snapshots, lifecycle-aware validator behavior, and no heuristic unknown-type acceptance.
- `C38` established that semantic meaning is authoritative at L5, while session mechanics remain L2 concerns and lineage remains an L4 concern.
- Existing AASL baseline documents already define namespace discipline, canonicalization, parser token growth, validator pass structure, and compiler ambiguity rules.

## 1. Normative Extension Package

### 1.1 Admission unit
`TL`, `PMT`, and `SES` SHALL be admitted together as one governed registry/module extension for Alternative B.

### 1.2 Ontology placement
- Namespace class: `system`
- Canonical namespace: `atr.protocol@1`
- Canonical module identifier: `module://atr.protocol.aacp/v1`
- Canonical module type: `protocol`
- Exported object-class terms: `TL`, `PMT`, `SES`
- Requested lifecycle state: `stable`
- Initial compatibility classification: `C2`

`C2` is required because this extension adds new admitted object classes and requires parser-token, validator-template, and compiler-mapping changes beyond editorial or purely optional documentation growth.

### 1.3 Authority boundary
- `TL`, `PMT`, and `SES` are L5 semantic object types.
- They MUST NOT absorb transport-binding fields, message-lineage fields, or security-signature material.
- `T-213`, `T-240`, `T-242`, and later tasks may reference these types, but SHALL NOT silently redefine their field meanings.

## 2. Common Rules

### 2.1 Common required semantics
All three types SHALL:
- resolve against an explicit pinned registry snapshot,
- carry a stable `id`,
- be authored only in admitted Atrahasis-controlled namespaces or imported through an explicitly trusted registry snapshot,
- reject heuristic reinterpretation when a consumer does not understand the type.

### 2.2 Canonical field names
Version 1 defines one canonical field spelling for each field. The following source-packet spellings are non-canonical and SHOULD be rewritten by tooling rather than admitted silently in strict or canonical modes:
- `provider_id` -> `provider`
- `client_id` -> `client`
- `server_id` -> `server`
- `params` -> `parameters`
- `created` -> `created_at`
- `last_active` -> `last_active_at`

### 2.3 Reference discipline
- Fields that identify other semantic objects SHOULD use AASL references or admitted stable identifiers, not free-text labels.
- If the parser/compiler cannot safely determine whether an external source artifact should map to `TL`, `PMT`, `SES`, or an older generic object family, it MUST emit ambiguity rather than guess.

### 2.4 Canonicalization overlay
The general AASL canonicalization rules remain in force. For these three types, the following additional rules apply:
- maps in `parameters` and `annotations` are order-insensitive and MUST canonicalize by lexicographic key order,
- sets in `permissions`, `supported_encodings`, and `supported_types` are order-insensitive and MUST canonicalize by lexicographic value order,
- inline `CST{}` payloads must be canonicalized before the containing object is hashed,
- non-canonical field aliases listed in Section 2.2 are not identity-preserving aliases for this release and are not part of the canonical surface.

## 3. `TL` - Tool Descriptor

### 3.1 Semantic role
`TL` represents an executable tool/function that an endpoint exposes for discovery and invocation.

`TL` is the protocol-facing structural realization of the broad AASL `Tool` conceptual class. It describes the tool itself, not a tool invocation, not a tool result, and not a permission grant.

### 3.2 Field schema

| Field | Req | Shape | Meaning |
|---|---|---|---|
| `id` | REQUIRED | stable identifier | Canonical tool identity |
| `name` | REQUIRED | string | Human-readable tool label |
| `description` | OPTIONAL | string | Human-readable summary |
| `provider` | REQUIRED | reference or stable identifier | Admitted provider object for this tool |
| `input_schema` | REQUIRED | `CST{}` or admitted schema/type reference | Valid invocation input surface |
| `output_schema` | REQUIRED | `CST{}` or admitted schema/type reference | Expected output surface before downstream wrapping |
| `permissions` | OPTIONAL | set of references or qualified identifiers | Declared capability/policy prerequisites |
| `annotations` | OPTIONAL | map | Non-authorizing hints such as read-only or cost indicators |
| `version` | REQUIRED | version string or version token | Tool schema/version identity |

### 3.3 Validation rules
- `provider` MUST resolve to an admitted endpoint, agent, runtime, or other profile-approved provider object.
- `input_schema` and `output_schema` MUST resolve against the active registry snapshot and MUST NOT rely on ambient local types.
- `permissions` entries MUST be explicit references or namespace-qualified terms. Free-text permission labels are invalid.
- `annotations` MUST NOT carry authorization decisions. They are hints, not authority.
- A `TL` object missing either schema field is invalid in all non-sandbox profiles.

### 3.4 Canonical example

```aasl
TL{
  id:tl.search.web.01
  name:"web_search"
  description:"Search a remote web index"
  provider:ag.tools.01
  input_schema:CST{id:cst.tl.search.input type:record}
  output_schema:CST{id:cst.tl.search.output type:record}
  permissions:[atr.auth/net.read]
  annotations:{atr.protocol/cost_hint:"metered",atr.protocol/read_only:true}
  version:"1.0.0"
}
```

### 3.5 Anti-examples
- `TL{... permissions:["internet"] ...}`: invalid because the permission surface is not namespace-qualified or referenced.
- `TL{... provider:"search team" ...}`: invalid in strict/canonical modes because provider identity is not a resolvable semantic object.

## 4. `PMT` - Prompt Template

### 4.1 Semantic role
`PMT` represents a reusable prompt template with typed parameters and an explicit declared output target.

`PMT` is a template definition object. It is not the rendered prompt instance, not a chat message, and not the model output produced from the template.

### 4.2 Field schema

| Field | Req | Shape | Meaning |
|---|---|---|---|
| `id` | REQUIRED | stable identifier | Canonical prompt-template identity |
| `name` | REQUIRED | string | Human-readable template label |
| `description` | OPTIONAL | string | Human-readable summary |
| `parameters` | REQUIRED | map from slot name to `CST{}` or admitted type/schema reference | Declared typed parameter surface |
| `template_text` | REQUIRED | string | Template body with explicit parameter slots |
| `output_type` | REQUIRED | admitted type/schema reference | Expected semantic output target |
| `annotations` | OPTIONAL | map | Rendering, audience, or safety hints that do not replace policy |
| `version` | REQUIRED | version string or version token | Template-version identity |

### 4.3 Validation rules
- When the active prompt-rendering profile uses explicit slot markers inside `template_text`, every referenced slot MUST correspond to a key in `parameters`.
- Every key in `parameters` MUST be unique within the object and MUST bind to an admitted constraint or type reference.
- `output_type` MUST resolve under the pinned registry snapshot.
- `template_text` MUST NOT depend on undeclared ambient variables or hidden defaults.
- `annotations` MUST NOT be used to smuggle execution policy or secret-bearing runtime credentials.

### 4.4 Canonical example

```aasl
PMT{
  id:pmt.summarize.01
  name:"summarize"
  description:"Summarize a target artifact with bounded length"
  parameters:{
    max_length:CST{id:cst.pmt.max_length type:integer}
    target:DS
  }
  template_text:"Summarize the target artifact with the configured maximum length."
  output_type:DS
  annotations:{atr.protocol/audience:"general"}
  version:"1.0.0"
}
```

### 4.5 Anti-examples
- `PMT{... template_text:"Use runtime default audience." parameters:{target:DS} ...}`: invalid because it depends on an undeclared hidden input.
- `PMT{... parameters:{target:"document"} ...}`: invalid in strict/canonical modes because the parameter schema is not an admitted type or constraint.

## 5. `SES` - Session Descriptor

### 5.1 Semantic role
`SES` represents a protocol session and the durable semantic facts about that session that matter to AASL-aware systems.

`SES` is not the message-lineage ledger and is not the full handshake transcript. It records the semantic session surface without collapsing L2 session state into L4 lineage or L3 security artifacts.

### 5.2 Field schema

| Field | Req | Shape | Meaning |
|---|---|---|---|
| `id` | REQUIRED | stable identifier | Canonical session identity |
| `client` | REQUIRED | reference or stable identifier | Initiating party |
| `server` | REQUIRED | reference or stable identifier | Serving party |
| `state` | REQUIRED | enum | Current session state |
| `mode` | REQUIRED | enum | `stateful` or `stateless` |
| `supported_encodings` | REQUIRED | set enum | Admitted encodings available to the session |
| `supported_types` | REQUIRED | set of type tokens or admitted term references | AASL types the session advertises as supported |
| `auth_method` | REQUIRED | qualified identifier or admitted reference | Authentication method used for this session surface |
| `created_at` | REQUIRED | timestamp literal or `TIM` reference | Session creation time |
| `last_active_at` | REQUIRED | timestamp literal or `TIM` reference | Most recent activity time |

The `mode` field is part of version 1 because Alternative B explicitly requires both `stateful` and `stateless` session operation. Leaving that distinction implicit would force downstream tasks to invent session semantics ad hoc.

### 5.3 Enumerations
`state` SHALL be one of:
- `negotiating`
- `active`
- `idle`
- `closing`
- `closed`
- `failed`

`mode` SHALL be one of:
- `stateful`
- `stateless`

`supported_encodings` entries SHALL be drawn from:
- `AASL-T`
- `AASL-J`
- `AASL-B`

### 5.4 Validation rules
- `client` and `server` MUST resolve to admitted identities.
- `supported_types` MUST contain only admitted object-type tokens or registered term references under the pinned snapshot.
- `last_active_at` MUST NOT precede `created_at`.
- `state` and `mode` MUST be explicit even when a runtime thinks they can be inferred.
- `SES` MUST NOT carry lineage fields such as `message_id`, `conversation_id`, or `workflow_id`; those belong to L4.
- `SES` MUST NOT carry transport-local socket handles, retry counters, or resume tokens; those remain downstream session-protocol concerns.

### 5.5 Canonical example

```aasl
SES{
  id:ses.tools.001
  client:ag.coordinator.01
  server:ag.tools.01
  state:active
  mode:stateful
  supported_encodings:[AASL-J,AASL-T]
  supported_types:[CLM,PMT,SES,TL]
  auth_method:atr.security/ed25519
  created_at:2026-03-12T12:00:00Z
  last_active_at:2026-03-12T12:05:00Z
}
```

### 5.6 Anti-examples
- `SES{... state:active supported_encodings:[json] ...}`: invalid because `json` is not an admitted AACP encoding token.
- `SES{... conversation_id:conv.1 ...}`: invalid because lineage fields are not session fields.

## 6. Parser, Validator, and AASC Changes

### 6.1 Parser changes
The parser token/grammar registry SHALL be extended to admit the object-type tokens:
- `TL`
- `PMT`
- `SES`

No new section types are required for this task.

### 6.2 Validator changes
Validator field-admissibility tables SHALL be extended so that:
- required/optional/prohibited fields for all three types are explicit,
- enumeration checks for `state`, `mode`, and `supported_encodings` are first-class rules,
- unknown-field handling for these canonical terms is profile-governed and never heuristic,
- registry-snapshot resolution is required before admission.

### 6.3 Compiler/AASC changes
The compiler SHALL add template mappings for:
- `TL` tool descriptors,
- `PMT` prompt templates,
- `SES` session descriptors.

Compiler behavior requirements:
- If source material clearly expresses a protocol tool with typed input/output, it MAY map to `TL`.
- If source material clearly expresses a reusable parameterized prompt artifact, it MAY map to `PMT`.
- If source material clearly expresses a protocol session surface, it MAY map to `SES`.
- If the source only weakly implies one of these types, the compiler MUST emit ambiguity rather than force the new type.
- Compiler output for these types MUST record the exact registry snapshot used.

## 7. Compatibility and Coexistence

### 7.1 Existing documents
Documents that do not use `TL`, `PMT`, or `SES` remain valid under earlier compatible snapshots.

### 7.2 Older workaround patterns
Older generic tool, resource, prompt, or state encodings MUST NOT be silently upgraded to these new types. Migration must be explicit and snapshot-bound.

### 7.3 Unsupported consumers
Consumers that do not support these types MUST reject or quarantine them according to profile. They MUST NOT reinterpret:
- `TL` as an arbitrary resource record,
- `PMT` as an untyped free-text string,
- `SES` as lineage or message state.

### 7.4 Downstream task boundaries
- `T-213` defines handshake, liveness, recovery, and stateless/stateful protocol mechanics.
- `T-240` defines tool discovery/invocation/result flows that consume `TL`.
- `T-242` defines prompt-listing and prompt-retrieval flows that consume `PMT`.
- This task only defines the semantic object surfaces those tasks rely on.

## Source Notes
- Alternative B source docs supplied the requirement to add the three types plus initial example field lists.
- `T-201` supplied the governance constraints and explicit ban on heuristic unknown-type reinterpretation.
- `C38` supplied the layer boundary: `SES` stays semantic and must not absorb lineage or transport authority.
- Existing AASL parser, validator, compiler, and registry documents supplied the baseline rules for namespace placement, token growth, field-admissibility tables, ambiguity handling, and snapshot binding.
