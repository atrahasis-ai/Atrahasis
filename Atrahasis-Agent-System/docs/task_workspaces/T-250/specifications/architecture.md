# C43 Architecture Outline

## 1. Architectural role

`C43` sits between non-native `MCP` servers and native Alternative B consumers.
It does not replace `C42`. It wraps non-native tool surfaces into a bounded,
signed, policy-visible bridge contract.

## 2. Core architectural components

### 2.1 Bridge Inventory Snapshot Engine
- polls or receives source tool inventory updates
- derives one bridge-scoped signed inventory snapshot
- exposes invalidation and expiry semantics

### 2.2 Translation Policy Core
- maps MCP tool descriptors into translated tool identities
- binds invocation translation to one policy hash
- defines degraded or fail-closed behavior for unsupported source patterns

### 2.3 Semantic Separation Layer
- records source-observed fields separately from bridge-normalized structure
- records bridge-inferred accountability fields separately from both
- prevents bridge-side semantic inflation

### 2.4 Accountable Result Composer
- emits bridged `tool_result` bundles
- builds `CLM + CNF + EVD + PRV` wrappers under explicit bridge posture
- preserves source references and translation lineage

### 2.5 Bounded Bridge State Manager
- retains reusable snapshot and translation state
- optionally issues derated continuation handles
- enforces expiry, invalidation, and non-native ceilings

### 2.6 Manifest and Trust Disclosure Adapter
- publishes bridge origin and posture through `C41`-compatible manifest
  disclosure
- enforces `C40` bridge-limited trust boundaries

## 3. Key flows

### 3.1 Discovery
1. Bridge obtains source tool inventory.
2. Bridge translates inventory into canonical bridge-scoped tool entries.
3. Bridge signs and publishes one `BridgeInventorySnapshot`.
4. Consumers discover bridged tools through standard `C39` discovery flow.

### 3.2 Invocation
1. Consumer issues `tool_invocation` against a translated tool ref.
2. Bridge validates snapshot identity, translation policy hash, authority
   context, and bridge posture constraints.
3. Bridge translates the request into source MCP call shape.
4. Source server executes the call.

### 3.3 Result enrichment
1. Bridge captures source-observed result material.
2. Bridge derives normalized structure.
3. Bridge emits bounded inferred accountability fields.
4. Bridge returns bridged accountable result with explicit posture label.

### 3.4 Change and invalidation
1. Source inventory changes or snapshot expiry occurs.
2. Bridge invalidates affected snapshot state.
3. Bridge emits `tool_change_notification`.
4. Future invocations pinned to invalid state fail closed.

## 4. Hard boundaries

- `C39` owns the message classes.
- `C40` owns trust profile and bridge trust ceilings.
- `C41` owns manifest disclosure shape.
- `C42` remains native tool authority.
- `C23` remains runtime authority.
- `T-260` remains native server-framework authority.

## 5. Architectural success condition

The architecture succeeds if a native Atrahasis client can consume a bridged
MCP tool through a coherent `AACP` surface while still being able to answer:
- what the source system actually said,
- what the bridge normalized,
- what the bridge inferred,
- and why the result is still non-native.
