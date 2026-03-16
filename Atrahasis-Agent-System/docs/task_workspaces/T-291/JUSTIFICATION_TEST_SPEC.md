# T-291 Direct Specification Draft

## Title

AACP v2 Justification Test Specification

## Task

Define the seven justification tests as executable benchmarks for the Alternative
C Forge pipeline, including pass/fail criteria, measurement methodology, and
fallback behavior when a criterion fails.

This task defines:

- the normalized seven-test program,
- the evidence and artifact model used to run the tests,
- full-program and lane-scoped decision semantics,
- the fallback posture when sovereignty claims are not justified.

This task does not redefine:

- the canonical conformance framework in `T-281`,
- the Forge architecture in `C47`,
- the constrained-generation benchmark authority in `C44`,
- the SDK and tooling surfaces in `T-262` and `T-280`,
- or the cross-layer integration contract in `T-290`.

## Governing Context

- The original `AACP-AASL` source packet defined justification tests in both the
  strategy document and the task list. The task-list version is the operative
  executable baseline for `T-291`.
- `C44` explicitly requires the later justification program to consume its
  benchmark outputs when judging whether the sovereign stack meaningfully
  outperforms a complement-only strategy.
- `C47` defines the current Forge dual-lane architecture and the quarantine and
  promotion rules that justification must evaluate, not bypass.
- `T-281` already defines the conformance corpus and certification evidence
  bundles. `T-291` must consume them rather than minting a second certification
  regime.
- `T-262` and `T-280` already define the executable SDK and tooling surfaces
  through which the justification harness is expected to run.
- `T-290` defines the runtime-evidence split and the native integration profile
  that justification runs must inspect for cross-layer correctness.

## 1. Historical Normalization Rule

The historical source packet contains two overlapping seven-test formulations.
This specification normalizes them into one executable set using these rules:

1. Preserve the task-list benchmark families because they were already phrased
   as executable measurements.
2. Preserve the strategy document's kill-criterion posture: failure is not
   advisory; it implies fallback.
3. Translate the old bridge-generality criterion into current-repo doctrine.

The key translation is:

- historical test: `MCP Bridge wraps 100+ servers with zero per-server configuration`
- current test: `C47` capability absorption demonstrates automated intake across
  `100+` representative external capabilities without reintroducing runtime
  bridge dependence

This keeps the strategic burden of proof intact while aligning it to the
zero-runtime-bridge architecture now canonical in the repo.

## 2. Purpose and Decision Boundary

`T-291` answers one question:

**Is the Alternative C Forge-centered sovereignty program justified relative to
the complement-only fallback posture?**

The answer is made at two scopes:

| Scope | Meaning |
|---|---|
| `FULL_PROGRAM` | whether the repo may continue claiming that the full sovereignty path is justified overall |
| `LANE_SCOPE` | whether a bounded lane or cohort may continue even if the full-program claim fails |

`FULL_PROGRAM` is strict: all seven tests must pass.

`LANE_SCOPE` is narrower: only the relevant subset of tests must pass for the
claimed lane, but any failure of provenance distinguishability or hard
quarantine rules is still a blocking failure.

## 3. Artifact Model

### 3.1 `JustificationRun`

```text
JustificationRun := {
  justification_run_id,
  scope,
  candidate_profile,
  baseline_profile,
  selected_tests[],
  evidence_pack_ref,
  result_set[],
  aggregate_result,
  fallback_profile,
  signed_at,
  signer_ref
}
```

### 3.2 `JustificationEvidencePack`

```text
JustificationEvidencePack := {
  evidence_pack_id,
  c44_benchmark_refs[],
  certification_bundle_refs[],
  vector_workspace_refs[],
  flow_capture_refs[],
  forge_quarantine_refs[],
  promotion_audit_refs[],
  axip_trace_refs[],
  onboarding_run_refs[],
  comparison_baseline_refs[]
}
```

The evidence pack aggregates canonical artifacts. It does not reinterpret them
into a second trust or certification system.

### 3.3 `TestResult`

```text
TestResult := {
  test_id,
  applicability_scope,
  metric_map,
  threshold_map,
  verdict,
  fallback_action,
  supporting_refs[],
  notes?
}
```

### 3.4 `ScopeDecision`

```text
ScopeDecision := {
  scope,
  verdict,
  retained_scope?,
  blocked_scope?,
  required_fallback,
  issued_at
}
```

## 4. Baselines and Comparison Profiles

Every justification run must compare a sovereignty candidate against at least
one explicit fallback baseline.

| Baseline ID | Meaning |
|---|---|
| `COMPLEMENT_ONLY` | semantic or operational posture that keeps the external capability stack as the primary dependency and treats sovereign layers as adjuncts |
| `LEASED_FIRST` | `C45` leased-cognition path retained as the primary execution substrate |
| `EXTERNAL_PROTOCOL_REFERENCE` | raw or minimally wrapped `A2A` / `MCP` transport or capability baseline used only for performance and ergonomics comparison |

The comparison baseline must be declared before the run starts. Post hoc
baseline switching is forbidden.

## 5. Execution Packs

The seven tests are executed through seven benchmark packs.

| Pack ID | Primary source |
|---|---|
| `JTP-01` Semantic-generation viability pack | `C44` `AGB-v1` outputs and frozen benchmark suite |
| `JTP-02` Compactness and reasoning-efficiency pack | source-packet benchmark workloads plus current canonical message/capture artifacts |
| `JTP-03` Semantic-reuse and cross-layer reuse pack | `AXIP-v1` traces, `task_result`, `attestation_submit`, memory and settlement evidence |
| `JTP-04` Transport-parity pack | native `AACP` bindings versus external protocol reference harnesses |
| `JTP-05` Capability-absorption breadth pack | `C47` locus-conversion corpus over `100+` representative external capabilities |
| `JTP-06` Provenance-distinguishability pack | registry, manifest, capture, and evidence artifacts spanning native, leased, compatibility, and Forge probation states |
| `JTP-07` One-day onboarding pack | end-to-end developer workflow over `T-260`, `T-262`, and `T-280` surfaces |

## 6. The Seven Tests

### 6.1 JT-01 Semantic-generation viability

**Question:** Can the sovereign semantic-emission path clear the baseline
viability floor?

**Evidence:** `C44` `AGB-v1` outputs.

**Required measurements:**

- structural validity,
- schema conformance,
- canonical equivalence,
- unknown-term invention rate.

**Pass rule:**

- `FS-OPEN` must meet or exceed the historical `>90%` floor and the current
  `C44_FEWSHOT_MIN_STRUCTURAL_VALIDITY` threshold,
- any mode claimed for guarded or production use must meet the corresponding
  `C44` thresholds for that mode.

**Hard fail condition:**

- any claimed emission mode fails its `C44` benchmark floor.

**Fallback action:**

- demote machine-authored `AASL-T` for the affected scope to assisted or
  debugging-only posture and remove semantic-generation credit from the full
  sovereignty claim.

### 6.2 JT-02 Compactness advantage

**Question:** Does the sovereign stack materially outperform the
complement-only baseline on compactness?

**Evidence:** representative task pack rendered through native and fallback
   artifact flows.

**Required measurements:**

- token-count ratio,
- wire-byte ratio,
- context-load ratio.

**Pass rule:**

- median compactness advantage must be `>= 2.0x`,
- lower quartile must remain `>= 1.5x`,
- and no flagship workload may regress below the fallback baseline.

**Hard fail condition:**

- median ratio `< 2.0x`.

**Fallback action:**

- remove compactness and savings claims from the sovereignty argument and treat
  the syntax or transport layer as unjustified for the failed scope.

### 6.3 JT-03 Semantic reuse demonstrated

**Question:** Does the reference runtime demonstrate measurable semantic reuse
with verified provenance rather than repeated rewrapping?

**Evidence:** `AXIP-v1` trace packs plus runtime, verification, memory, and
settlement artifacts.

**Required measurements:**

- canonical payload reuse across at least three downstream consumers,
- zero manual post hoc provenance insertion on the claimed native path,
- measurable reduction in duplicate parsing or wrapper generation work.

**Pass rule:**

- at least `95%` of benchmark workflows preserve one canonical payload or
  evidence chain across runtime, verification, and either memory or settlement,
- manual provenance-wrap rate on the native path is `0`.

**Hard fail condition:**

- equivalent tasks do not hit downstream consumers with verified provenance and
  reusable canonical identity.

**Fallback action:**

- freeze claims of semantic-accountability superiority for the affected scope
  until canonicalization and reuse boundaries are corrected.

### 6.4 JT-04 Transport quality and parity

**Question:** Does the sovereign transport stack reach production-quality parity
with raw external protocol references?

**Evidence:** same workload pack run over native `AACP` bindings and external
protocol reference harnesses on comparable hardware.

**Required measurements:**

- concurrent connection handling,
- p50 and p95 latency,
- throughput,
- error-rate delta.

**Pass rule:**

- the claimed native binding set sustains the required concurrency profile,
- p95 latency is within `5%` of the reference path,
- throughput is at least `95%` of the reference path,
- error rate is no worse than the reference path.

**Hard fail condition:**

- transport overhead materially exceeds the `5%` parity bound.

**Fallback action:**

- treat full transport sovereignty as unjustified for the failed surfaces and
  retain complement-only or leased-first transport posture there.

### 6.5 JT-05 Capability-absorption breadth

**Question:** Can the current Forge path absorb external ecosystem breadth
without reintroducing runtime bridge dependence?

**Evidence:** `C47` locus-conversion corpus over representative external
capabilities.

**Required measurements:**

- corpus size,
- automation rate,
- preflight success rate,
- quarantine-ready synthesis success rate,
- runtime-bridge reintroduction count.

**Pass rule:**

- the corpus contains at least `100` representative external capability
  specimens,
- every specimen uses the same automated intake path rather than bespoke
  runtime shims,
- at least `90%` reach build + manifest + quarantine-ready state,
- runtime bridge reintroduction count is `0`.

**Hard fail condition:**

- the intake path requires per-specimen runtime customization,
- or the automated conversion success rate falls below `90%`.

**Fallback action:**

- lane `LOCUS_CONVERSION` loses justification for broad ecosystem replacement
  claims and remains in complement-only or compatibility-bounded posture.

### 6.6 JT-06 Provenance distinguishability and integrity superiority

**Question:** Is native provenance measurably superior and distinguishable from
leased, compatibility, or probationary provenance?

**Evidence:** manifest snapshots, registry results, `FlowCaptureBundle`,
`CertificationEvidenceBundle`, `ForgeOperationRecord`, and runtime evidence.

**Required measurements:**

- false-native classification rate,
- explicit provenance labeling coverage,
- complete machine-verifiable provenance chain coverage on native paths.

**Pass rule:**

- false-native classification rate is exactly `0`,
- provenance labeling coverage is `100%` across benchmark artifacts,
- native path artifacts expose complete machine-verifiable provenance chains.

**Hard fail condition:**

- any leased, compatibility, bridge-historical, or Forge-probation artifact is
  misclassified as native,
- or provenance distinction cannot be made reliably from canonical metadata.

**Fallback action:**

- immediate fail-closed for the affected scope; no promotion or sovereignty
  superiority claim may continue until provenance separation is repaired.

### 6.7 JT-07 One-day developer onboarding

**Question:** Can a new external developer become productive with the native
stack in one working day?

**Evidence:** scripted developer workflow over `T-260`, `T-262`, and `T-280`
surfaces.

**Required workflow:**

1. install the tooling stack,
2. generate or author a simple native locus,
3. bind and publish a manifest,
4. run a local vector subset,
5. inspect the result in Inspector or equivalent tooling,
6. export a canonical capture or evidence artifact.

**Pass rule:**

- `80%` or more of the participant cohort completes the workflow within `8`
  hours elapsed time,
- no undocumented manual patching is required,
- and the simple native example remains within `1.25x` the lines-of-code of the
  historical MCP-style comparison sample.

**Hard fail condition:**

- the workflow exceeds one workday for the majority of the cohort,
- or success depends on undocumented expert intervention.

**Fallback action:**

- freeze ecosystem-expansion and onboarding claims for the affected scope until
  framework and tooling ergonomics improve.

## 7. Result Semantics

Each test returns one of:

- `PASS`
- `FAIL`
- `INCONCLUSIVE`

Each run returns one of:

- `JUSTIFIED`
- `JUSTIFIED_LIMITED_SCOPE`
- `NOT_JUSTIFIED_FALLBACK`

### 7.1 Aggregate rules

For `FULL_PROGRAM`:

- all seven tests must be `PASS` for `JUSTIFIED`,
- any `FAIL` yields `NOT_JUSTIFIED_FALLBACK`,
- any `INCONCLUSIVE` yields `JUSTIFIED_LIMITED_SCOPE` at most.

For `LANE_SCOPE`:

- only the applicable tests must run,
- `JT-06` is always mandatory,
- any `FAIL` in `JT-06` yields `NOT_JUSTIFIED_FALLBACK`,
- other failures may reduce the result to `JUSTIFIED_LIMITED_SCOPE` only when
  the claimed scope explicitly excludes the failed capability.

## 8. Fallback Profiles

The historical source packet required fallback to Alternative A if any test
fails. In the current repo, that fallback is normalized as one of these explicit
profiles:

| Fallback profile | Meaning |
|---|---|
| `COMPLEMENT_ONLY` | retain sovereign semantic components only where they already function as complements to external capability layers |
| `LEASED_FIRST` | retain `C45` leased cognition as the primary path for the failed execution scope |
| `NATIVE_LIMITED_SCOPE` | retain only the explicitly justified native subset and freeze expansion claims beyond it |

Fallback must be declared in the signed `JustificationRun`. A failed test may
not end in “continue anyway” as an implicit policy.

## 9. Execution Methodology

### 9.1 Reproducibility rules

- every run must pin registry snapshots and manifest snapshots,
- every baseline profile must be declared before execution,
- every comparison corpus must be frozen before scoring,
- all evidence references must remain replayable through canonical artifacts.

### 9.2 Tooling rules

The justification harness should run through the existing suite:

- `T-262` SDK surfaces execute vectors, captures, and certification bundles,
- `T-280` CLI and Inspector surfaces package and inspect evidence,
- `T-281` certification bundles and vectors remain authoritative for conformance
  inputs.

### 9.3 Scope-specific applicability

| Test | `FULL_PROGRAM` | `LOCUS_CONVERSION` | `MODEL_ADAPTATION` | `DX_SCOPE` |
|---|---|---|---|---|
| `JT-01` | required | optional unless model-generated semantics are in scope | required | optional |
| `JT-02` | required | required | required | optional |
| `JT-03` | required | required | required | optional |
| `JT-04` | required | required | optional | optional |
| `JT-05` | required | required | n/a | optional |
| `JT-06` | required | required | required | required |
| `JT-07` | required | required | required | required |

Model-adaptation justification is therefore still covered even though the
historical bridge/capability-breadth test was locus-centric.

## 10. Formal Requirements

| ID | Requirement | Priority |
|---|---|---|
| JTS-R01 | `T-291` MUST preserve a seven-test justification program rather than collapsing justification into one aggregate score | P0 |
| JTS-R02 | The executable baseline for the seven tests MUST follow the historical task-list formulation, normalized only where current Alternative C doctrine makes a bridge-era criterion obsolete | P0 |
| JTS-R03 | Every `JustificationRun` MUST declare its comparison baseline explicitly before execution begins | P0 |
| JTS-R04 | Every `JustificationRun` MUST bind to one immutable `JustificationEvidencePack` | P0 |
| JTS-R05 | `JT-01` MUST consume `C44` benchmark outputs rather than ad hoc prompt-quality impressions | P0 |
| JTS-R06 | `JT-04` MUST compare native `AACP` transport against an explicit external protocol reference harness using the same workload pack | P0 |
| JTS-R07 | `JT-05` MUST evaluate automated capability absorption under `C47` without permitting runtime bridge dependence as a passing strategy | P0 |
| JTS-R08 | `JT-06` MUST treat any false-native provenance classification as an immediate hard failure | P0 |
| JTS-R09 | `JT-07` MUST use a scripted reproducible onboarding workflow over the canonical framework, SDK, and tooling surfaces | P0 |
| JTS-R10 | `T-291` MUST consume `T-281` certification bundles and vector outputs as evidence rather than defining a second certification corpus | P0 |
| JTS-R11 | `FULL_PROGRAM` justification MUST fail if any of the seven tests fails | P0 |
| JTS-R12 | `LANE_SCOPE` justification MAY retain limited scope only when the failed capability is explicitly excluded and `JT-06` still passes | P1 |
| JTS-R13 | Every failed justification run MUST emit one explicit fallback profile; silent continuation is forbidden | P0 |
| JTS-R14 | Justification evidence MUST be replayable from canonical artifacts produced by the SDK, tooling, conformance, Forge, and AXIP surfaces | P1 |
| JTS-R15 | Historical source-packet bridge-centric criteria MAY be translated to `C47` capability absorption, but the burden of proof MUST remain at least as strict as the original criterion | P1 |

## 11. Parameters

| Parameter | Meaning | Initial guidance |
|---|---|---|
| `JTS_REQUIRED_TEST_COUNT` | total number of justification tests | `7` |
| `JTS_MIN_COMPACTNESS_RATIO` | minimum median compactness advantage | `2.0` |
| `JTS_MIN_COMPACTNESS_P25_RATIO` | minimum lower-quartile compactness advantage | `1.5` |
| `JTS_TRANSPORT_MAX_P95_DELTA` | max allowed p95 latency delta vs reference | `0.05` |
| `JTS_TRANSPORT_MIN_THROUGHPUT_RATIO` | minimum throughput ratio vs reference | `0.95` |
| `JTS_CAPABILITY_CORPUS_MIN` | minimum representative capability corpus size | `100` |
| `JTS_CAPABILITY_AUTOMATED_SUCCESS_MIN` | minimum automated capability-absorption success rate | `0.90` |
| `JTS_FALSE_NATIVE_CLASSIFICATION_ALLOWED` | allowed false-native classifications | `0` |
| `JTS_ONBOARDING_MAX_HOURS` | maximum onboarding time for the passing cohort | `8` |
| `JTS_ONBOARDING_PASS_COHORT_MIN` | minimum cohort completion ratio within one day | `0.80` |
| `JTS_SIMPLE_SERVER_LOC_RATIO_MAX` | maximum lines-of-code ratio versus the historical comparison sample | `1.25` |
| `JTS_DEFAULT_FALLBACK_PROFILE` | default fallback if a run fails and no narrower profile is justified | `COMPLEMENT_ONLY` |

## 12. Downstream Contracts

| Task | `T-291` provides |
|---|---|
| `T-300` | a concrete judgment surface for what must remain compatibility-only if the sovereignty case fails |
| `T-304` | the pass/fail basis for whether Forge compute cost is justified economically |
| `T-307` | the evidence gate for deciding whether large-scale sub-agent loci conversion is strategically justified |
| `T-308` | terminology and publication guidance on when “native” and “justified” claims may be stated repo-wide |

## 13. Conclusion

`T-291` turns the sovereignty argument into an executable burden of proof.

Its key move is not the seven-test list by itself. The key move is forcing every
claim of superiority, compactness, integrity, and developer viability to bind to
replayable evidence and to an explicit fallback posture if the claim fails.
