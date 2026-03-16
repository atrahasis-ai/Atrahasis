# AACP Conformance and Certification Framework

| Field | Value |
|---|---|
| Task ID | T-281 |
| System | Atrahasis Agent System |
| Stage | DIRECT SPEC |
| Primary authority surface | C38 FSPA |
| Governing specs | C38, C39, C40, C41, C42, C45, C47 |
| Status | DRAFT FOR CANONICAL USE |

---

## 1. Purpose

This document defines the canonical conformance and certification framework for
native `AACP` implementations.

It exists to answer four operational questions that the root protocol specs do
not answer by themselves:

1. What does it mean for an implementation to be conformant across transport,
   session, security, messaging, and semantics?
2. Which certification tiers distinguish protocol correctness from production
   native operation and full sovereign convergence?
3. How is interoperability proven across bindings, encodings, and independent
   implementations rather than asserted?
4. How is the Alternative C rule of zero external runtime transport reliance
   enforced during certification?

The framework is intentionally cross-layer. It consumes the canonical protocol
and server-authority surfaces already defined elsewhere; it does not replace
them.

---

## 2. Scope and non-goals

### 2.1 In scope

- certification tiers for native `AACP` implementations,
- a canonical conformance corpus exceeding 1,000 test vectors,
- interoperability methodology across bindings, encodings, and independent
  implementations,
- transport binding matrices for certification planning,
- certification evidence packaging,
- fail-closed criteria for bridge/runtime sovereignty violations.

### 2.2 Out of scope

- authoring new transport bindings,
- redefining message semantics already owned by `C39`,
- redefining security profiles already owned by `C40`,
- replacing manifest semantics already owned by `C41`,
- replacing native tool/runtime semantics already owned by `C42` and `C45`,
- replacing build-time external capability ingestion already owned by `C47`.

---

## 3. Governing inputs

This framework is downstream of:

- `C38` for binding, session, canonicalization, and conformance-vector posture,
- `C39` for the 42-class message inventory and lineage-bearing message
  obligations,
- `C40` for signature validation, replay rejection, downgrade refusal, and
  explicit capability-grant enforcement,
- `C41` for manifest disclosure and capability-claim truth,
- `C42` for native tool discovery, invocation, continuation, and accountable
  result behavior,
- `C45` for native server-framework and provenance-compiler execution posture,
- `C47` for build-time external capability ingestion and the quarantine ring.

If any downstream implementation disagrees with one of those surfaces, that is a
conformance failure, not an invitation to reinterpret the source authority.

---

## 4. Certification principles

### 4.1 Claim-scoped certification

An implementation is certified only for the bindings, encodings, message
families, and capability surfaces it advertises through `C41`.

### 4.2 Native path required

Certification is for native `AACP` behavior. Runtime dependence on `A2A`,
`MCP`, or any bridge transport path is disqualifying for certified operation.

### 4.3 Independent interoperability

A vendor or team does not certify itself into interoperability by passing a
private test harness alone. Certification requires exchange with:

- the canonical reference harness, and
- at least one independent challenger implementation.

### 4.4 Fail closed over best effort

When canonicalization, signing, replay handling, or capability-grant evaluation
is ambiguous, the certified behavior is explicit rejection or quarantine.

### 4.5 Evidence before badge

Every certification verdict must be backed by a signed certification evidence
bundle that records the tested manifest, vector results, implementation build
identity, and negative-path outcomes.

---

## 5. Certification tiers

### 5.1 Tier C1: Core Protocol Conformant

`Tier C1` certifies that an implementation is a correct native protocol
endpoint.

Required surfaces:

- one or more native bindings from `C38`,
- canonical handshake and lineage behavior,
- `C39` message-class correctness for every advertised family,
- `C40` authority binding, signature validation, replay rejection, and
  downgrade refusal,
- `C41` manifest truthfulness and capability disclosure.

Disallowed:

- runtime bridge dependence,
- heuristic canonicalization,
- unsigned manifest publication,
- transport-local shortcuts that bypass `AACP` envelope authority.

### 5.2 Tier C2: Native Runtime Certified

`Tier C2` certifies that an implementation is not merely a correct endpoint but
also a correct native server/runtime surface.

Additional required surfaces:

- `C42` snapshot-bound tool semantics for every advertised native tool surface,
- `C45` sovereign framework hooks or equivalent native runtime instrumentation,
- accountable result wrapping and provenance emission,
- continuation and execution-priming behavior that remains below `C23` lease
  authority.

Additional required evidence:

- native runtime vector execution,
- provenance graph integrity checks,
- latency-safe negative-path handling for invalid authority and stale snapshot
  cases.

### 5.3 Tier C3: Sovereign Convergence Certified

`Tier C3` certifies that an implementation is production-grade under the
Alternative C sovereignty rule.

Additional required surfaces:

- zero external runtime transport reliance,
- `C47` quarantine-ring behavior for any Forge-synthesized locus,
- policy-visible isolation between build-time external ingestion and live native
  operation,
- deployment evidence that no certified critical path traverses `A2A`, `MCP`,
  or bridge-limited runtime modes.

Additional required evidence:

- quarantine execution logs for synthesized loci,
- sovereign runtime packet/path audit,
- negative vectors proving that runtime bridge activation is rejected or causes
  decertification.

---

## 6. Certification evidence bundle

Every certification run MUST produce one `CertificationEvidenceBundle`.

```text
CertificationEvidenceBundle := {
  certification_run_id,
  implementation_id,
  implementation_build_ref,
  manifest_snapshot_ref,
  claimed_tier,
  claimed_binding_matrix[],
  vector_suite_summary[],
  interoperability_run_refs[],
  sovereignty_audit_ref,
  quarantine_audit_ref?,
  result,
  signed_at,
  signer_ref
}
```

Semantics:

- `manifest_snapshot_ref` pins the exact `C41` capability claim under test.
- `claimed_binding_matrix[]` lists only the bindings and encodings advertised by
  the implementation.
- `quarantine_audit_ref` is mandatory for `Tier C3` whenever the implementation
  includes Forge-generated loci.
- `result` is one of `PASS`, `PASS_WITH_LIMITED_SCOPE`, `FAIL`, or
  `DECERTIFIED`.

---

## 7. Canonical test-vector corpus

### 7.1 Corpus structure

The canonical `T-281` corpus contains **1,240 vectors** across eight suites.

| Suite | Vector range | Count | Primary authority |
|---|---|---:|---|
| Session and canonicalization | `CV-281-001` to `CV-281-140` | 140 | C38 |
| Messaging and lineage | `CV-281-141` to `CV-281-300` | 160 | C38, C39 |
| Security and authority | `CV-281-301` to `CV-281-500` | 200 | C40 |
| Manifest and capability truth | `CV-281-501` to `CV-281-620` | 120 | C41 |
| Native tool and continuation | `CV-281-621` to `CV-281-800` | 180 | C42 |
| Native server runtime and provenance | `CV-281-801` to `CV-281-940` | 140 | C45 |
| Forge and quarantine | `CV-281-941` to `CV-281-1080` | 140 | C47 |
| Sovereignty negatives and decertification | `CV-281-1081` to `CV-281-1240` | 160 | C38, C40, C47 |

### 7.2 Priority bands

Each vector is labeled with one priority band:

- `P0`: mandatory safety/correctness vectors; zero failures allowed,
- `P1`: normative interoperability vectors; one failure blocks tier issuance,
- `P2`: robustness and operational vectors; bounded failures may yield scope
  reduction rather than total failure.

### 7.3 Minimum pass thresholds

| Tier | Required threshold |
|---|---|
| `C1` | 100% of `P0`, 100% of `P1` in claimed surfaces, at least 98% of claimed `P2` |
| `C2` | `C1` threshold plus 100% of `P0/P1` for `C42` and `C45` suites |
| `C3` | `C2` threshold plus 100% of `P0/P1` sovereignty and quarantine suites |

### 7.4 Negative vectors

The sovereignty-negative suite is normative, not advisory.

Examples:

- attempted runtime call-through to an `A2A` or `MCP` bridge endpoint,
- manifest advertising native posture while using bridge-limited security state,
- replay acceptance after `message_id` reuse,
- silent downgrade from `AASL-B` to text JSON carriage,
- forged provenance graph detached from runtime execution evidence,
- Forge locus leaving quarantine without a recorded ascension decision.

Any `P0` pass on these vectors requires explicit rejection, quarantine, or
decertification behavior, not graceful acceptance.

---

## 8. Interoperability methodology

### 8.1 Three-party rule

A certification run includes:

- `IUT`: implementation under test,
- `RH`: canonical reference harness,
- `CI`: challenger implementation from an independent codebase.

An interoperability claim passes only if the relevant vectors succeed for:

1. `IUT <-> RH`
2. `IUT <-> CI`

`RH <-> CI` may be used as a control but does not substitute for the two
mandatory pairings above.

### 8.2 Matrix execution rule

For every advertised binding/encoding pair, the harness executes:

- happy-path exchange,
- canonicalization parity exchange,
- negative-path rejection exchange,
- recovery or reconnection path when the binding supports it,
- signature and replay validation exchange.

### 8.3 Semantic identity rule

If the same semantic message is carried across multiple advertised bindings or
encodings, the certification harness MUST verify identical:

- `payload_canonical_hash`,
- `message_canonical_hash`,
- four-field lineage envelope,
- capability-grant interpretation,
- manifest-scoped subject identity.

### 8.4 Capability truth rule

An implementation may advertise only what it actually passes. Failed surfaces
must be removed from the manifest scope before a passing certification badge can
be issued.

### 8.5 Partial certification rule

`PASS_WITH_LIMITED_SCOPE` is allowed only when:

- every `P0` and `P1` vector for the retained scope passes,
- the manifest is narrowed to that retained scope,
- the certification evidence bundle records the excluded bindings, message
  families, or runtime surfaces explicitly.

---

## 9. Transport binding certification matrix

The binding matrix is claim-scoped: advertised bindings are mandatory to test;
unadvertised bindings are out of scope.

| Binding | Encodings allowed by authority | Certification role | Minimum tier posture | Required suites |
|---|---|---|---|---|
| `AACP-HTTP` | `AASL-T`, `AASL-J`, `AASL-B` | canonical baseline network binding | mandatory for any networked certified endpoint | session/canonicalization, messaging, security, manifest |
| `AACP-gRPC` | preferred `AASL-B`; explicit `AASL-T` / `AASL-J` carriage allowed | high-throughput native carrier | required if advertised; `Tier C2+` strongly recommended for native servers | session/canonicalization, messaging, security, runtime/provenance |
| `AACP-WS` | `AASL-T`, `AASL-J` text; `AASL-B` binary only | persistent duplex carrier | required if advertised; mandatory for certified duplex/push claims | session/recovery, messaging, security |
| `AACP-Stdio` | `AASL-J` only | local-process and harness carrier | required if advertised; mandatory for certified local tool-host or compiler-side harness claims | session/canonicalization, security, runtime/provenance |

Matrix rules:

- `HTTP` media-type mismatches are `P0` failures.
- `gRPC` certification fails if wire-carrier convenience replaces canonical hash
  authority.
- `WebSocket` certification fails if opcode/encoding discipline is violated or
  resume semantics mint synthetic lineage.
- `Stdio` certification fails if any alternate encoding is accepted silently.

---

## 10. Zero external runtime reliance gate

### 10.1 Certification meaning

For `T-281`, "zero external runtime transport reliance" means:

- no certified request path depends on live `A2A`, `MCP`, or bridge transport,
- no certified identity posture depends on bridge-limited runtime state,
- no certified manifest claims native capability while delegating live execution
  to an external bridge process,
- build-time external ingestion through `C47` is allowed only before runtime and
  only under quarantine-controlled promotion.

### 10.2 Informative legacy surfaces

Historical bridge artifacts (`C43`, `C46`, bridge-limited clauses in earlier
specs) remain valid as:

- negative test inputs,
- regression references,
- migration-history evidence.

They are **not** certifiable runtime surfaces under this framework.

### 10.3 Decertification triggers

An issued certification MUST move to `DECERTIFIED` if any later audit shows:

- runtime bridge activation on a certified path,
- undeclared outbound dependency on `A2A` or `MCP` protocol traffic,
- manifest/native posture mismatch,
- Forge locus promoted from quarantine without required ascension evidence,
- disabled replay/downgrade controls on a certified binding.

---

## 11. Formal requirements

| ID | Requirement | Priority |
|---|---|---|
| `CCF-R01` | Certified implementations MUST bind every certification result to one immutable `CertificationEvidenceBundle` signed by a declared certification signer | P0 |
| `CCF-R02` | `Tier C1` certification MUST require conformance across the implementation's claimed `C38`, `C39`, `C40`, and `C41` surfaces | P0 |
| `CCF-R03` | `Tier C2` certification MUST additionally require conformance across all claimed `C42` and `C45` runtime surfaces | P0 |
| `CCF-R04` | `Tier C3` certification MUST additionally require `C47` quarantine evidence for any Forge-synthesized locus in scope | P0 |
| `CCF-R05` | The canonical `T-281` corpus MUST contain at least 1,000 vectors and MUST maintain stable vector identifiers across revisions | P0 |
| `CCF-R06` | Every certified binding/encoding pair advertised through `C41` MUST execute the applicable vector suites; untested advertised bindings are invalid | P0 |
| `CCF-R07` | Interoperability certification MUST include `IUT <-> RH` and `IUT <-> CI` exchanges; one-party self-testing is insufficient | P0 |
| `CCF-R08` | Semantically identical messages carried across multiple certified bindings or encodings MUST yield identical canonical hashes and lineage values | P0 |
| `CCF-R09` | Failed or unsupported capability surfaces MUST be removed from the manifest before a passing certification verdict may be issued | P0 |
| `CCF-R10` | Any certified network endpoint MUST support `AACP-HTTP`; advertising no native network baseline is non-conformant | P1 |
| `CCF-R11` | Any advertised duplex or push claim over `AACP-WS` MUST pass resume, heartbeat-boundary, and opcode-discipline vectors | P1 |
| `CCF-R12` | Any advertised `AACP-gRPC` surface MUST prove explicit encoding carriage and MUST NOT substitute protobuf wire bytes for canonical-hash authority | P0 |
| `CCF-R13` | Any advertised `AACP-Stdio` surface MUST fail closed on attempts to negotiate `AASL-T` or `AASL-B` | P0 |
| `CCF-R14` | Runtime dependence on `A2A`, `MCP`, or any bridge transport path MUST be treated as a certification failure for all tiers and as a decertification trigger for `Tier C3` | P0 |
| `CCF-R15` | Historical bridge artifacts MAY be used as negative or regression vectors, but they MUST NOT be accepted as certifiable runtime surfaces | P1 |
| `CCF-R16` | `PASS_WITH_LIMITED_SCOPE` verdicts MUST identify the excluded surfaces explicitly and MUST narrow the implementation manifest to the retained scope before issuance | P1 |
| `CCF-R17` | Certification tooling SHOULD preserve machine-readable vector results, packet/path traces, and manifest snapshots for audit replay | P2 |
| `CCF-R18` | Certification suites SHOULD include performance-sensitive negative tests that confirm fail-closed behavior does not silently degrade into permissive retries | P2 |

---

## 12. Parameters

| Parameter | Meaning | Initial guidance |
|---|---|---|
| `AACP_CERT_VECTOR_COUNT_MIN` | minimum canonical corpus size | `1000` |
| `AACP_CERT_VECTOR_COUNT_TARGET` | planning size for first full corpus release | `1240` |
| `AACP_CERT_P2_PASS_FLOOR_C1` | minimum `P2` pass rate for `Tier C1` | `0.98` |
| `AACP_CERT_SIGNING_ALGORITHM` | signature algorithm for certification bundles | `Ed25519` |
| `AACP_CERT_HTTP_REQUIRED` | whether a certified network endpoint must expose `AACP-HTTP` | `true` |
| `AACP_CERT_CHALLENGER_COUNT_MIN` | minimum independent challenger implementations required | `1` |
| `AACP_CERT_BINDING_MATRIX_STRICT` | require every advertised binding to be fully tested | `true` |
| `AACP_CERT_ZERO_EXTERNAL_RUNTIME` | enforce zero external runtime transport reliance | `true` |
| `AACP_CERT_QUARANTINE_REQUIRED_FOR_FORGE` | require quarantine evidence for Forge outputs | `true` |
| `AACP_CERT_DECERT_AUDIT_RETENTION_DAYS` | minimum retention for decertification evidence packs | `365` |

---

## 13. Operational guidance

`T-261`, `T-262`, `T-280`, `T-290`, and `T-291` should treat this document as
the canonical certification authority until a later governance task explicitly
supersedes it.

In particular:

- `T-261` should expose certification scope and latest evidence-bundle metadata
  in registry search results,
- `T-262` should surface vector execution and certification-bundle builders as
  first-class SDK modules,
- `T-280` should build inspector and CLI affordances around the vector corpus
  and interoperability matrix,
- `T-290` should reuse the same certification evidence posture for cross-layer
  contracts,
- `T-291` should consume these tiers and vector classes rather than invent a
  second independent justification harness.

---

## 14. Conclusion

`AACP` conformance is not a schema-checking exercise. It is proof that a native
endpoint preserves canonical identity, security, capability truth, runtime
authority boundaries, and sovereign transport posture under hostile conditions.

That is the standard required for the next phase of the Atrahasis stack, and it
is the standard this framework makes testable.
