# C43 Pre-Mortem

Assume `C43` failed badly in production after broad MCP bridge rollout. The
most likely reasons are:

## 1. False native trust

Failure:
- bridged outputs were treated like native `C42` results
- downstream policy stopped distinguishing bridge posture from native posture

Root cause:
- posture disclosure too weak or optional

Mitigation:
- mandatory explicit bridge posture at manifest, invocation, result, and
  continuation surfaces

## 2. Semantic inflation

Failure:
- bridge generated confidence or provenance stronger than the source MCP server
  justified

Root cause:
- no hard source-observed vs bridge-inferred separation

Mitigation:
- explicit separation map and degraded posture when source metadata is thin

## 3. Snapshot drift

Failure:
- consumers invoked tools against stale translated inventories

Root cause:
- weak invalidation and expiry semantics

Mitigation:
- signed snapshot TTL, invalidation nonce, fail-closed stale invocation rules

## 4. Hidden per-server customization

Failure:
- universal bridge claim collapsed into bespoke adapters for popular servers

Root cause:
- conformance profile too vague about what counts as zero-config coverage

Mitigation:
- explicit generic translation profile and fail-closed boundary for
  non-conforming servers

## 5. Shadow framework growth

Failure:
- bridge accumulated too much state and started behaving like a quasi-native
  server framework

Root cause:
- bounded bridge state not bounded enough

Mitigation:
- explicit prohibition on native priming, runtime lease behavior, and hidden
  framework semantics inside the bridge
