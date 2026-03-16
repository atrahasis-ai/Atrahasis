# T-262 Direct Specification Draft

## Title

AACP SDK Architecture

## Task

Specify the canonical five-module SDK shape for Python, TypeScript, and Rust,
including `AACPClient` / `AACPServer` surfaces and typed message builders.

This task defines:

- the stable logical module decomposition for native `AACP` SDKs,
- shared object and API surfaces that must exist in every supported language,
- language-specific packaging and naming rules,
- generated-SDK overlay rules for downstream `C36` exports,
- conformance and certification helpers required by the `C38` framework.

This task does not redefine:

- `C38` transport, session, or canonicalization truth,
- `C40` security semantics,
- `C41` manifest truth,
- `C42` tool and continuation semantics,
- `C45` runtime internals,
- or `T-280` operator and developer tooling.

## Governing Context

- `C38` FSPA defines the five-layer protocol stack and the canonical
  message-identity chain.
- `T-213` and `T-215` define the session-control and canonicalization material
  that SDKs must surface rather than hide.
- `C40` requires `T-262` to expose security profiles, authority contexts,
  grants, signatures, and replay handling without inventing alternate L3
  behavior.
- `C41` explicitly reserves manifest fetch, parse, and negotiation surfaces for
  `T-262`.
- `C42` requires SDKs to treat snapshot caching, invalidation, continuation
  lifecycle, and runtime handoff as first-class concerns.
- `C45` requires language-native server ergonomics over FastAPI, Express, and
  Actix-style ecosystems.
- `T-261` defines the registry client and trust-vector response structures that
  `T-262` must consume.
- `C36` requires generated SDKs to preserve membrane metadata and session
  ordering.
- The `C38` conformance framework requires vector execution and
  certification-bundle builders to be first-class SDK surfaces.

## 1. Design Goal

`T-262` establishes one cross-language SDK architecture with the same five
logical modules in every supported language:

1. `aacp.protocol`
2. `aacp.security`
3. `aacp.discovery`
4. `aacp.runtime`
5. `aacp.conformance`

The implementation style may vary by language, but the nouns, dependency
direction, and authority boundaries must remain stable.

The central design decision is deliberate: `AACPClient` and `AACPServer` are
not separate top-level modules. They are the primary exported surfaces of
`aacp.runtime`, which keeps the module count fixed at five while preserving one
shared lifecycle layer for sessions, continuation state, transport adapters, and
framework bindings.

## 2. Design Principles

1. **Native-first default**
   The core SDK path assumes native `AACP` and native `C40` trust posture.
   Compatibility scaffolding may exist later, but it is not part of the default
   module boundary.

2. **Typed over ad hoc**
   Message construction, manifest parsing, negotiation, and certification should
   use typed builders and views rather than raw free-form maps.

3. **Shared nouns, ecosystem-native ergonomics**
   Python may be async-first, TypeScript may favor discriminated unions, and
   Rust may use builder traits and enums, but all three must expose the same
   architectural nouns.

4. **Generated overlays above core**
   `C36`-driven generated SDKs must sit on top of the five core modules rather
   than re-implementing protocol, trust, or canonicalization logic.

5. **Fail closed on trust ambiguity**
   Discovery, negotiation, manifest handling, and runtime admission must refuse
   unresolved trust or profile conflicts rather than silently degrading.

6. **Conformance is part of the SDK**
   Vector runners and certification-bundle builders are not optional side tools.
   They are required surfaces in the same architectural stack.

## 3. Canonical Five-Module Shape

| Module | Core responsibility | Mandatory top-level exports | Primary upstream authorities |
|---|---|---|---|
| `aacp.protocol` | message, codec, canonicalization, session tuple, binding-independent builders | `MessageBuilder`, `SessionTuple`, `CanonicalMessage`, `BindingCodec`, `HandshakeBuilder` | `C38`, `C39`, `T-213`, `T-215` |
| `aacp.security` | security profiles, authority contexts, capability grants, signatures, replay controls | `SecurityProfile`, `AuthorityContext`, `CapabilityGrant`, `SignatureEnvelope`, `ReplayPolicy` | `C40` |
| `aacp.discovery` | manifests, registry, capability negotiation, trust vectors, snapshot caches | `ManifestClient`, `ManifestView`, `RegistryClient`, `CapabilityNegotiator`, `TrustVector` | `C41`, `T-261`, `C42` |
| `aacp.runtime` | client/server execution surfaces, transport adapters, framework bindings, lifecycle handling | `AACPClient`, `AACPServer`, `ClientSession`, `ServerBinding`, `ContinuationHandle` | `C38`, `C42`, `C45` |
| `aacp.conformance` | vector execution, interoperability harnesses, certification bundle creation | `VectorRunner`, `InteropHarness`, `CertificationBundleBuilder`, `VectorReport` | `C38` conformance framework |

### 3.1 Dependency graph

The dependency graph is fixed:

- `aacp.protocol` depends on no higher SDK module.
- `aacp.security` may depend on `aacp.protocol`.
- `aacp.discovery` may depend on `aacp.protocol` and `aacp.security`.
- `aacp.runtime` may depend on `aacp.protocol`, `aacp.security`, and
  `aacp.discovery`.
- `aacp.conformance` may depend on all four lower modules.

Reverse dependencies are forbidden. A discovery helper must not import runtime
framework glue. A protocol builder must not import registry clients or
certification logic.

## 4. Module Specifications

### 4.1 `aacp.protocol`

`aacp.protocol` is the canonical typed-construction layer for messages and
session artifacts.

It must provide:

- message-envelope builders for the `C39` message classes,
- `SCF-v1` handshake and resume builders,
- canonicalization wrappers that consume the `T-215` message hash and envelope
  rules,
- binding codecs for `AASL-J`, `AASL-T`, and `AASL-B`,
- ordered batch builders that preserve session and lineage ordering,
- membrane metadata carriers required by `C36`.

Minimum exported surfaces:

| Surface | Purpose |
|---|---|
| `MessageBuilder<T>` | typed builder for one canonical message family |
| `HandshakeBuilder` | typed builder for `handshake_request`, `handshake_response`, resume, heartbeat, and close control frames |
| `CanonicalMessage` | immutable post-build message view carrying headers, payload reference, canonical hash, and lineage |
| `BindingCodec` | encode/decode canonical messages for one negotiated binding and encoding |
| `SessionTuple` | negotiated version, binding, encoding, and security profile tuple |

`aacp.protocol` owns message construction, not trust decisions. It may validate
shape, lineage completeness, and canonicalization preconditions, but it must not
admit or reject authority on its own.

### 4.2 `aacp.security`

`aacp.security` packages the `C40` DAAF surfaces that downstream code should
reuse rather than duplicate.

It must provide:

- `SecurityProfile` representations for the bounded DAAF profile set,
- `AuthorityContext` parsers, builders, and validators,
- `CapabilityGrant` parsing and verification helpers,
- `ABP-v1` and `SIG-v1` projection helpers,
- replay-cache keying, freshness-window validation, and downgrade-check hooks,
- manifest trust validation helpers needed before discovery or runtime
  admission.

Minimum exported surfaces:

| Surface | Purpose |
|---|---|
| `SecurityProfile` | typed representation of `SP-NATIVE-ATTESTED`, `SP-FEDERATED-SESSION`, `SP-WORKLOAD-MTLS`, `SP-BRIDGE-LIMITED` |
| `AuthorityContext` | authenticated subject context with role, provenance floor, and Sanctum admission class |
| `CapabilityGrant` | explicit bounded grant artifact |
| `SignatureEnvelope` | `SIG-v1` projection and verification helper |
| `ReplayPolicy` | replay-cache keying, freshness, and redelivery semantics |
| `ManifestTrustEvaluator` | fail-closed manifest, issuer-chain, and trust-posture checker |

`aacp.security` must not invent a second authorization model. It encodes `C40`
and leaves business policy to runtime consumers.

### 4.3 `aacp.discovery`

`aacp.discovery` handles endpoint discovery, negotiation, and native registry
consumption.

It must provide:

- manifest retrieval from `/.well-known/atrahasis.json` or governed successors,
- manifest parsing into typed `ManifestView` objects,
- registry search and subject-detail clients using `T-261` shapes,
- capability negotiation over manifest and caller policy,
- tool inventory snapshot caching and invalidation hooks for `C42`,
- trust-vector response objects and filtering helpers.

Minimum exported surfaces:

| Surface | Purpose |
|---|---|
| `ManifestClient` | fetch and refresh manifests |
| `ManifestView` | typed read model over admitted manifest content |
| `RegistryClient` | global registry search and subject detail access |
| `CapabilityNegotiator` | choose binding, encoding, security profile, and class support from caller policy plus manifest truth |
| `ToolSnapshotStore` | signed tool inventory snapshot cache with invalidation and expiry awareness |
| `TrustVector` | factorized trust summary from `T-261` |

`CapabilityNegotiator` is the SDK surface that satisfies the `C41`
"fetch/parse/negotiation" downstream contract. It may use caller preferences,
but it must fail closed when registry or manifest trust posture is unresolved.

### 4.4 `aacp.runtime`

`aacp.runtime` is the operational core of the SDK. It owns `AACPClient`,
`AACPServer`, transport adapters, framework integration, and lifecycle glue for
continuations and runtime handoffs.

It must provide:

- a client surface for discovery-aware session establishment and business
  exchanges,
- a server surface that binds handlers, manifests, security policy, and
  transport adapters,
- transport adapters for HTTP first and pluggable adapters for gRPC, WebSocket,
  and stdio,
- framework adapters for FastAPI, Express, and Actix-style ecosystems,
- snapshot-cache invalidation, continuation-context handling, and runtime
  handoff surfaces required by `C42`,
- strict preservation of membrane metadata and negotiated session ordering.

#### 4.4.1 `AACPClient`

`AACPClient` is the canonical active-peer surface.

It must expose:

- `discover(subject_ref | manifest_url)` to obtain manifest and registry state,
- `negotiate(policy)` to resolve the `SessionTuple`,
- `send(message)` and `request(builder)` for ordinary exchange,
- `stream(builder)` for ordered stream/push-compatible flows,
- `invoke_tool(builder)` with snapshot pinning and continuation handling,
- `resume(session_id, cursor)` for resume-aware sessions,
- `close()` for orderly shutdown.

The client must carry discovery and security collaborators explicitly rather than
silently re-fetching or re-authenticating under the hood.

#### 4.4.2 `AACPServer`

`AACPServer` is the canonical passive-peer surface and the direct SDK boundary
to `C45` framework ergonomics.

It must expose:

- manifest binding and publication hooks,
- security-profile floors and admission-policy hooks,
- handler registration for message families or routes,
- tool-inventory and continuation-policy binding,
- transport binding and framework adapter selection,
- conformance-introspection hooks needed by `aacp.conformance`.

`AACPServer` is not a generic web server abstraction. It is an `AACP` execution
surface that may attach to an existing framework.

#### 4.4.3 Runtime lifecycle helpers

`aacp.runtime` must also export shared lifecycle objects:

| Surface | Purpose |
|---|---|
| `ClientSession` | negotiated session state, heartbeat, resume cursor, and ordering rules |
| `ContinuationHandle` | typed wrapper over `C42` continuation contexts |
| `RuntimeHandoffHandle` | typed wrapper over runtime-handoff contracts that remains non-authorizing by itself |
| `TransportAdapter` | binding-specific send/receive abstraction |
| `ServerBinding` | framework-bound server execution adapter |

### 4.5 `aacp.conformance`

`aacp.conformance` packages the certification and test surfaces reserved by the
`C38` conformance framework.

It must provide:

- vector-corpus loaders,
- language-neutral vector execution against `AACPClient` and `AACPServer`,
- certification-bundle builders and serializers,
- interop-matrix reporting,
- negative-vector and quarantine-pack support.

Minimum exported surfaces:

| Surface | Purpose |
|---|---|
| `VectorRunner` | execute canonical vectors against one implementation target |
| `InteropHarness` | run multi-implementation interoperability matrices |
| `CertificationBundleBuilder` | build machine-readable certification evidence bundles |
| `VectorReport` | stable vector-result summary with per-vector outcomes |
| `CertificationBundle` | final signed evidence package |

This module is first-class because `T-281` explicitly requires SDKs to surface
vector execution and certification-bundle builders, not merely schema validators.

## 5. Shared Object Model

Every language binding must expose typed versions of the following shared
concepts.

| Object | Minimum semantics |
|---|---|
| `CanonicalMessage` | message class, lineage fields, payload reference, canonical hash, membrane metadata, session tuple reference |
| `NegotiatedSession` | selected binding, encoding, profile, heartbeat posture, resume policy |
| `ManifestView` | subject, trust posture, endpoints, security, messaging, semantics, supersession |
| `RegistrySubjectRecordView` | `T-261` subject summary, lifecycle, trust vector, manifest reference, tool match summaries |
| `ToolSnapshotHandle` | snapshot identity, inventory hash, expiry, invalidation nonce |
| `ContinuationHandle` | bounded continuation context with expiry and invalidation awareness |
| `RuntimeHandoffHandle` | runtime-handoff contract view without lease authority |
| `CertificationBundle` | vector results, manifest snapshot, binding scope, signing data, certification tier metadata |

No language binding may collapse these into untyped opaque blobs on the public
SDK surface.

## 6. Language Packaging Model

The logical module boundary is fixed, but package layout should match each
ecosystem's conventions.

### 6.1 Python

Python should ship as one canonical distribution with five stable subpackages:

- `aacp.protocol`
- `aacp.security`
- `aacp.discovery`
- `aacp.runtime`
- `aacp.conformance`

Rules:

- async-first for network and streaming APIs,
- builder surfaces may expose sync wrappers only where non-networked,
- type surfaces should use dataclasses or equivalent typed models,
- framework adapters should live under `aacp.runtime.fastapi` and similar
  subpackages.

### 6.2 TypeScript

TypeScript should ship as one package namespace with subpath exports:

- `@atrahasis/aacp/protocol`
- `@atrahasis/aacp/security`
- `@atrahasis/aacp/discovery`
- `@atrahasis/aacp/runtime`
- `@atrahasis/aacp/conformance`

Rules:

- discriminated unions for message and manifest shapes,
- promise-based async APIs,
- ESM-first packaging with stable type exports,
- Express adapters under `@atrahasis/aacp/runtime/express`.

### 6.3 Rust

Rust should ship as a workspace of crates plus an umbrella crate:

- `aacp-protocol`
- `aacp-security`
- `aacp-discovery`
- `aacp-runtime`
- `aacp-conformance`
- umbrella `aacp`

Rules:

- builder types and enums are preferred over stringly typed APIs,
- transport and framework support should be feature-gated,
- Actix integration should live behind the runtime crate's `actix` feature,
- no crate may hide canonical error conditions behind catch-all string errors.

## 7. Generated SDK Overlay Rules

`C36` `sdk_generate(language, version)` should produce generated capability
packages that depend on the five core modules rather than re-implementing them.

Generated overlays may add:

- subject-specific manifest constants,
- typed request and response stubs,
- receptor or capability descriptors,
- domain-shaped helper methods.

Generated overlays must not add:

- custom message hashing rules,
- custom trust or grant validation logic,
- alternate replay handling,
- alternate registry or manifest truth models.

The overlay rule is strict:

`generated package -> core five modules -> upstream canonical specs`

never:

`generated package -> private protocol/security fork`

## 8. Cross-Language API Naming Rules

The following public nouns must exist in every language, with only casing
adapted to local convention:

| Canonical noun | Python | TypeScript | Rust |
|---|---|---|---|
| `AACPClient` | `AACPClient` | `AACPClient` | `AACPClient` |
| `AACPServer` | `AACPServer` | `AACPServer` | `AACPServer` |
| `ManifestClient` | `ManifestClient` | `ManifestClient` | `ManifestClient` |
| `RegistryClient` | `RegistryClient` | `RegistryClient` | `RegistryClient` |
| `VectorRunner` | `VectorRunner` | `VectorRunner` | `VectorRunner` |
| `CertificationBundleBuilder` | `CertificationBundleBuilder` | `CertificationBundleBuilder` | `CertificationBundleBuilder` |

Method naming may follow local style:

- Python: `invoke_tool`, `fetch_manifest`, `run_vectors`
- TypeScript: `invokeTool`, `fetchManifest`, `runVectors`
- Rust: `invoke_tool`, `fetch_manifest`, `run_vectors`

but the architectural nouns must remain recognizable and stable.

## 9. API Sketches

### 9.1 Python sketch

```python
from aacp.discovery import ManifestClient, RegistryClient, CapabilityNegotiator
from aacp.runtime import AACPClient, AACPServer
from aacp.protocol import ToolInvocationBuilder

manifest_client = ManifestClient()
registry_client = RegistryClient()
client = AACPClient(
    manifest_client=manifest_client,
    registry_client=registry_client,
)

session = await client.negotiate("ag.example.01")
builder = ToolInvocationBuilder(snapshot_id="tis.004", tool_ref="tl.fs.read")
result = await client.invoke_tool(builder)
```

### 9.2 TypeScript sketch

```ts
import { AACPClient, AACPServer } from "@atrahasis/aacp/runtime";
import { ManifestClient, RegistryClient } from "@atrahasis/aacp/discovery";
import { ToolInvocationBuilder } from "@atrahasis/aacp/protocol";

const client = new AACPClient({
  manifestClient: new ManifestClient(),
  registryClient: new RegistryClient(),
});

const session = await client.negotiate({ subjectId: "ag.example.01" });
const builder = new ToolInvocationBuilder({
  snapshotId: "tis.004",
  toolRef: "tl.fs.read",
});
const result = await client.invokeTool(builder);
```

### 9.3 Rust sketch

```rust
use aacp_runtime::AACPClient;
use aacp_discovery::{ManifestClient, RegistryClient};
use aacp_protocol::ToolInvocationBuilder;

let client = AACPClient::builder()
    .manifest_client(ManifestClient::default())
    .registry_client(RegistryClient::default())
    .build()?;

let _session = client.negotiate("ag.example.01").await?;
let builder = ToolInvocationBuilder::new("tis.004", "tl.fs.read");
let result = client.invoke_tool(builder).await?;
```

These sketches are illustrative. The normative content is the module and object
boundary, not the exact constructor syntax.

## 10. Formal Requirements

| ID | Requirement | Priority |
|---|---|---|
| SDK-R01 | Every supported language binding MUST implement the same five logical modules defined by this task | P0 |
| SDK-R02 | `AACPClient` and `AACPServer` MUST be first-class exported runtime surfaces in every supported language | P0 |
| SDK-R03 | The SDK MUST expose typed message builders and canonical message views rather than requiring raw free-form payload assembly for normal use | P0 |
| SDK-R04 | The SDK MUST expose `C40` security profiles, authority contexts, capability grants, signature helpers, and replay handling through reusable typed surfaces | P0 |
| SDK-R05 | Manifest fetch, parse, and capability negotiation MUST be first-class discovery surfaces rather than hidden side effects of runtime connection code | P0 |
| SDK-R06 | Registry search and trust-vector response handling MUST consume the `T-261` model rather than inventing alternate discovery response shapes | P0 |
| SDK-R07 | Tool snapshot caching, invalidation, continuation contexts, and runtime handoff handles MUST be first-class runtime or discovery objects | P0 |
| SDK-R08 | Generated endpoint or receptor SDKs MUST depend on the core five modules and MUST NOT fork protocol or security logic | P0 |
| SDK-R09 | SDK public surfaces MUST preserve membrane metadata and negotiated session ordering required by `C36` | P0 |
| SDK-R10 | The runtime module MUST provide framework adapters aligned with `C45` for Python, TypeScript, and Rust server ecosystems | P1 |
| SDK-R11 | The conformance module MUST expose vector execution and certification-bundle builders as first-class public surfaces | P0 |
| SDK-R12 | The conformance module MUST be able to execute canonical vectors against both client and server targets without redefining vector identity | P1 |
| SDK-R13 | Discovery or runtime helpers MUST fail closed when manifest truth, registry truth, or security posture conflict materially | P0 |
| SDK-R14 | No core SDK module MAY treat bridge-limited posture as equivalent to native posture on the default path | P0 |
| SDK-R15 | The protocol module MUST remain independent of registry, runtime framework, and certification concerns | P1 |
| SDK-R16 | Rust crate features, Python extras, and TypeScript subpath exports MAY vary by ecosystem, but they MUST NOT alter the five logical module boundary | P1 |

## 11. Parameters

| Parameter | Meaning | Initial guidance |
|---|---|---|
| `SDK_CORE_MODULE_COUNT` | fixed count of logical SDK modules | `5` |
| `SDK_PRIMARY_LANGUAGES` | required first-wave language set | `python, typescript, rust` |
| `SDK_DEFAULT_HTTP_BINDING_REQUIRED` | whether first-wave runtime support must include `AACP-HTTP` | `true` |
| `SDK_GRPC_SUPPORT_OPTIONAL` | whether gRPC runtime support may ship after HTTP | `true` |
| `SDK_WS_SUPPORT_OPTIONAL` | whether WebSocket runtime support may ship after HTTP | `true` |
| `SDK_STDIO_SUPPORT_OPTIONAL` | whether stdio runtime support may ship after HTTP | `true` |
| `SDK_GENERATED_OVERLAY_ALLOWED` | whether generated overlays may be emitted above the core modules | `true` |
| `SDK_BRIDGE_HELPERS_IN_CORE_DEFAULT_PATH` | whether bridge helpers may appear on the default native import path | `false` |
| `SDK_CONFORMANCE_PUBLIC_REQUIRED` | whether vector and certification surfaces are public SDK exports | `true` |

## 12. Downstream Contracts

| Task | `T-262` provides |
|---|---|
| `T-280` | canonical CLI, inspector, and editor-tooling import surfaces across protocol, discovery, runtime, and conformance layers |
| `T-281` | stable vector-runner and certification-bundle API targets for automation |
| `T-290` | standardized client/server/discovery nouns for cross-layer integration examples |
| `T-305` | implementation-planning input for language rollout order, packaging, and generated-SDK strategy |

## 13. Conclusion

`T-262` defines the SDK as a sovereign implementation substrate, not a thin wire
wrapper.

The essential outcome is one stable five-module architecture:

- `aacp.protocol`
- `aacp.security`
- `aacp.discovery`
- `aacp.runtime`
- `aacp.conformance`

with `AACPClient` and `AACPServer` as first-class runtime surfaces, message
builders and trust helpers as reusable typed primitives, and conformance tooling
built into the SDK itself rather than bolted on afterward.
