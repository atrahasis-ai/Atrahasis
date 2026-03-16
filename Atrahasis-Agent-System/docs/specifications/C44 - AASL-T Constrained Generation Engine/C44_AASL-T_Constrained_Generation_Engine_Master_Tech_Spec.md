# C44 - AASL-T Constrained Generation Engine

## Master Technical Specification

| Field | Value |
|---|---|
| Title | AASL-T Constrained Generation Engine |
| Version | 1.1.0 |
| Date | 2026-03-14 |
| Invention ID | C44 |
| Task ID | T-270 |
| System | Atrahasis Agent System v2.4 |
| Stage | SPECIFICATION |
| Normative References | ADR-041, ADR-043, C38 FSPA v1.0.6, T-212 Type Extension Specification, Alternative B source packet |

---

## Table of Contents

1. System role and architectural position
2. Design principles
3. Scope, non-goals, and operating modes
4. C44 architecture
5. AASL-T generation grammar profile (`ATG-v1`)
6. Prompt-library design
7. Dataset and tuning specification
8. Benchmark and certification framework
9. Runtime policy and failure handling
10. Integration with the Atrahasis stack
11. Parameters
12. Formal requirements
13. Conformance vectors
14. Risks and open questions

---

## 1. System role and architectural position

### 1.1 Purpose

C44 defines the canonical system for generating well-formed `AASL-T` from LLMs.
It is the upstream authority for:
- prompt-pack structure,
- decoder constraint strategy,
- grammar compilation from pinned registry snapshots,
- dataset composition,
- benchmark gates for autonomous emission,
- and the semantic control-plane rules for temporary leased cognition.

C44 does not replace `C38` canonicalization, `T-212` semantic object definitions,
or downstream message/tool/runtime contracts. It makes LLM-authored `AASL-T`
safe enough to be admitted into those systems.

### 1.2 The problem it solves

Before C44, the repo had:
- a sovereign protocol stack in `C38`,
- new semantic object families in `T-212`,
- and a strategic requirement that agents operate natively in `AASL-T`,
- but no canonical generation discipline for turning model output into valid,
  snapshot-bound semantic artifacts.

Without C44, downstream systems would be forced to choose between:
- unconstrained prose-to-structure prompting,
- ad hoc regex repair,
- or abandoning `AASL-T` for less natural but easier machine surfaces.

Under the sovereignty roadmap, that problem also appears in a second form:
temporary use of external frontier models. Without C44, frontier-model use would
either bypass semantic constraints entirely or become an ad hoc application-layer
prompting habit with no canonical admission discipline.

### 1.3 Architectural position

Under `C38`, C44 lives at the L5 Semantics authoring boundary.

C44 defines:
- how an LLM may emit an `AASL-T` semantic object,
- what grammar profile constrains that emission,
- how the result is validated and canonicalized before admission,
- when the output is trusted enough for autonomous use,
- and how externally leased model output remains semantically constrained and
  visibly non-native.

C44 does not define:
- L4 message classes,
- L3 signatures or authority grants,
- L2 handshake/session rules,
- L1 transport binding behavior,
- or the field semantics of `TL{}`, `PMT{}`, and `SES{}` beyond what `T-212`
  already defines.

---

## 2. Design principles

### 2.1 Snapshot-bound semantics

Every generation run must target one explicit registry snapshot. No ambient type
invention, field alias guessing, or ontology drift is allowed.

### 2.2 Fail closed

Malformed output, unknown terms, unresolved snapshots, or ambiguous
canonicalization are admission failures, not opportunities for silent repair.

### 2.3 Grammar first at the autonomy boundary

For any medium-or-higher-risk autonomous emission path, constrained decoding is
the default. Open generation is for drafting assistance and low-risk workflows
only.

### 2.4 Separation of semantic generation from protocol wrapping

`C44` generates L5 semantic payloads. Message lineage, signatures, transport
envelopes, and runtime leases remain downstream responsibilities.

### 2.5 Measurement before enablement

No generation mode is considered production-capable because it "looks good".
Every mode is admitted only by benchmark performance against frozen vectors.

### 2.6 Canonical identity over presentation

Pretty text is useful, but semantic identity comes from `C38` canonicalization,
not from surface whitespace or field layout.

---

## 3. Scope, non-goals, and operating modes

### 3.1 Canonical output unit

Version 1 of C44 targets one root semantic object per generation call.

This means:
- one `TL{}` object,
- one `PMT{}` object,
- one `SES{}` object,
- or one other admitted AASL object under the pinned snapshot.

Multi-object protocol bundles remain downstream assembly work. `C44` may be used
multiple times within a workflow, but it is not the authority for message-bundle
construction.

### 3.2 Non-goals

C44 v1.0 does not attempt to:
- replace deterministic programmatic builders for critical paths,
- infer missing ontology terms from natural language,
- generate L4 lineage envelopes,
- generate L3 signatures or replay state,
- or normalize arbitrary human-authored legacy `AASL-T`.

### 3.3 Operating modes

| Mode ID | Description | Required controls | Intended use |
|---|---|---|---|
| `FS-OPEN` | Few-shot prompting without grammar constraints | parser, validator, canonicalization gate | drafting assistance, low-risk operator-supervised flows |
| `FS-GRAMMAR` | Few-shot prompting plus grammar-constrained decoding | grammar, parser, validator, canonicalization gate | default autonomous mode for low/medium-risk emission |
| `FT-GRAMMAR` | Fine-tuned or aligned model plus grammar-constrained decoding | grammar, parser, validator, canonicalization gate, benchmark admission | high-volume production generation where LLM emission is still allowed |

### 3.4 Risk classes

| Risk class | Permitted mode(s) | Repair allowed? |
|---|---|---|
| `LOW` | `FS-OPEN`, `FS-GRAMMAR`, `FT-GRAMMAR` | at most one bounded repair pass |
| `MEDIUM` | `FS-GRAMMAR`, `FT-GRAMMAR` | at most one bounded repair pass |
| `HIGH` | `FT-GRAMMAR` or deterministic builder | no repair |
| `CRITICAL` | deterministic builder only; C44 may assist humans but not emit final autonomous payloads | no |

### 3.5 Leased cognition operating envelope

`Leased cognition` is the temporary phase in which Atrahasis uses external
frontier models behind Atrahasis-owned control planes instead of treating those
providers as trusted system components.

For C44, that means:
- a frontier model may produce candidate `AASL-T` only through the same pinned
  snapshot, grammar, validation, and canonicalization gates as any other model,
- leased output is always marked as leased provenance and never confused with
  native model sovereignty,
- provider egress is scrubbed before transmission: no raw Sanctum traces, secret
  material, unrestricted tool context, or recursion-critical planning state may
  leave Atrahasis under a leased run,
- autonomous final emission from leased cognition is bounded to outer-membrane
  `LOW` and `MEDIUM` risk workflows unless a later native system supersedes it,
- `HIGH` risk leased use may exist only as operator-assist drafting and not as
  autonomous final emission,
- `CRITICAL` final emission remains forbidden.

---

## 4. C44 architecture

### 4.1 Pipeline overview

```
GenerationIntent
      |
      v
Snapshot packer
      |
      v
Prompt-pack resolver ----> Grammar compiler
      |                          |
      +------------+-------------+
                   v
            Decoder controller
                   |
                   v
              Raw AASL-T
                   |
                   v
            Parse + validate gate
                   |
                   v
          C38 canonicalization gate
                   |
                   v
            GenerationOutcome
```

### 4.2 GenerationIntent

Every generation request must provide:

| Field | Req | Meaning |
|---|---|---|
| `registry_snapshot_id` | REQUIRED | Exact pinned semantics snapshot used for token admission and validation |
| `allowed_root_types` | REQUIRED | Explicit root-type allowlist for this call |
| `target_schema_refs` | OPTIONAL | Additional schema/type references that constrain nested fields |
| `slot_bindings` | OPTIONAL | User/task facts that must be grounded into the object |
| `risk_class` | REQUIRED | `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` |
| `generation_mode` | REQUIRED | One of the three C44 operating modes |
| `prompt_pack_id` | REQUIRED | Prompt-family selection for telemetry and reproducibility |
| `max_output_tokens` | REQUIRED | Hard generation budget |
| `allow_repair` | REQUIRED | Explicit boolean, further limited by risk policy |

### 4.3 GenerationOutcome

Every run must produce one outcome record:

| Field | Meaning |
|---|---|
| `raw_text` | Exact model output before any bounded repair |
| `mode_used` | Actual mode used for the attempt |
| `parse_status` | `PASS` or structured failure code |
| `schema_status` | `PASS` or structured failure code |
| `canonicalization_status` | `PASS` or structured failure code |
| `payload_canonical_hash` | Present only on successful canonicalization |
| `repair_count` | Number of bounded repair passes used |
| `failure_reason` | Mandatory on any failure |

### 4.4 Snapshot packer

The snapshot packer compiles one decoder-facing view from the pinned registry:
- admitted type tokens,
- canonical field names per type,
- enum tokens,
- required and optional fields,
- order-insensitive set declarations,
- alias-rejection rules,
- referenced type/schema handles.

This component exists because the generator must operate on the same semantic
surface that the parser and canonicalizer will later enforce.

### 4.5 Prompt-pack resolver

The prompt-pack resolver selects:
- a system instruction frame,
- 2 to 5 positive exemplars,
- optional negative exemplars,
- target formatting hints,
- slot-grounding instructions,
- and the expected root-type family.

Prompt packs are versioned artifacts, not ephemeral ad hoc strings.

### 4.6 Grammar compiler

The grammar compiler emits a strict decoder grammar from:
- `ATG-v1`,
- the pinned registry snapshot,
- the allowed root-type set,
- and any narrower task-specific schema restrictions.

This means the grammar is not one static hand-written file. It is a compiled
profile with snapshot-bound terminals.

### 4.7 Parse and validate gate

After generation, the result must pass:
1. syntactic parse under the `ATG-v1` profile,
2. field-admissibility validation under the pinned snapshot,
3. required-field checks,
4. enum/token resolution,
5. prohibition checks for cross-layer leakage.

### 4.8 Canonicalization gate

Successful parse is not enough. The output must then pass the `C38` L5
canonicalization pipeline:
- explicit snapshot resolution,
- alias resolution,
- identifier normalization,
- set normalization where declared,
- deterministic serialization,
- canonical hash computation.

If canonicalization fails, the emission is rejected.

---

## 5. AASL-T generation grammar profile (`ATG-v1`)

### 5.1 Purpose

`ATG-v1` is the strict decoder grammar profile for machine-authored `AASL-T`.
It is intentionally narrower than the full human authoring space.

This is a feature, not a limitation:
- narrower grammar reduces decoder entropy,
- improves structural validity,
- and makes fail-closed validation tractable.

### 5.2 Lexical rules

`ATG-v1` enforces:
- UTF-8 text only,
- canonical type tokens from the pinned snapshot,
- canonical field names only,
- double-quoted string literals,
- `true`, `false`, and `null` as lowercase literals,
- ISO-8601 UTC timestamps when emitted as literals,
- no comments,
- no markdown fences,
- no prose outside the root object.

### 5.3 Structural rules

The decoder-facing EBNF profile is:

```ebnf
document        ::= ws object ws EOF
object          ::= type_token "{" ws field_block? ws "}"
field_block     ::= field (field_sep field)*
field_sep       ::= nl+ ws
field           ::= field_name ws ":" ws value
value           ::= object
                  | list
                  | map
                  | string
                  | number
                  | boolean
                  | null
                  | atom_token
list            ::= "[" ws (value (ws "," ws value)*)? ws "]"
map             ::= "{" ws (map_entry (ws "," ws map_entry)*)? ws "}"
map_entry       ::= map_key ws ":" ws value
map_key         ::= atom_token | string
type_token      ::= SNAPSHOT_TYPE_TOKEN
field_name      ::= SNAPSHOT_FIELD_TOKEN
atom_token      ::= SNAPSHOT_ENUM_TOKEN
                  | reference_token
                  | identifier_token
reference_token ::= TOKEN_COMPILED_FROM_SNAPSHOT
identifier_token ::= TOKEN_COMPILED_FROM_SNAPSHOT
string          ::= DQUOTE chars DQUOTE
number          ::= INTEGER | DECIMAL
boolean         ::= "true" | "false"
null            ::= "null"
ws              ::= (" " | "\t" | nl)*
nl              ::= "\n"
```

### 5.4 Snapshot specialization

The symbolic terminals above are compiled from the pinned snapshot:
- `SNAPSHOT_TYPE_TOKEN` becomes the exact admitted root and nested type set,
- `SNAPSHOT_FIELD_TOKEN` becomes the exact field table for the allowed types,
- enum and reference tokens become snapshot-bound finite vocabularies where
  possible.

Unknown tokens are not accepted merely because they "look plausible".

### 5.5 Cross-layer leakage prohibition

`ATG-v1` generation must reject:
- L4 lineage fields such as `message_id`, `conversation_id`, or `workflow_id`
  unless the target semantic type explicitly admits them,
- transport-local fields,
- signature blobs,
- opaque security metadata,
- undeclared runtime handles.

For example, `SES{}` may carry semantic session facts defined by `T-212`, but it
may not absorb `SCF-v1` frame details or transport socket identifiers.

### 5.6 Canonical-preferred formatting

Generators should emit the following preferred text layout:
- one root object only,
- one field per line at the root object level,
- stable field ordering following the target schema or prompt pack,
- comma-separated nested list/map items,
- no presentation-only padding or decorative whitespace.

This formatting is a generation preference, not the source of semantic identity.

---

## 6. Prompt-library design

### 6.1 System instruction contract

Every prompt pack must explicitly tell the model:
- the output must be only `AASL-T`,
- the exact snapshot and allowed root types,
- that unknown terms are forbidden,
- that conversational filler is forbidden,
- and that failure is preferable to fabrication.

### 6.2 Prompt-pack families

Version 1 defines four prompt-pack families:

| Prompt pack | Intended outputs |
|---|---|
| `PP-ATOMIC` | simple single objects with shallow scalar fields |
| `PP-SCHEMA` | objects containing `CST{}` references or schema-heavy fields |
| `PP-PROTOCOL` | `TL{}`, `PMT{}`, and `SES{}` outputs from Alternative B tasks |
| `PP-PROVENANCE` | objects that carry nested references and stricter grounding requirements |

### 6.3 Exemplar policy

Each pack must contain:
- at least 2 positive exemplars,
- no more than 5 exemplars in the default pack,
- at least 1 exemplar with nested structure for `PP-SCHEMA` and `PP-PROTOCOL`,
- at least 1 negative or counterexample for grammar-constrained packs.

Exemplars are selected by:
- same root-type family first,
- same depth/shape second,
- same slot-binding pattern third.

### 6.4 Negative exemplars

Negative exemplars may teach the model not to:
- emit markdown fences,
- invent unknown fields,
- use deprecated aliases from `T-212`,
- leak lineage/security fields into L5 objects,
- or replace canonical tokens with natural-language paraphrases.

### 6.5 Slot-grounding discipline

If a generation request includes slot bindings, the prompt pack must expose:
- which fields are expected to bind to those slots,
- which slots are optional,
- and what omission behavior is valid.

Hidden defaults are not allowed.

---

## 7. Dataset and tuning specification

### 7.1 Minimum corpus

C44 requires a minimum corpus of `10,000` labeled pairs for any tuning or
alignment claim beyond few-shot prompting.

### 7.2 Corpus composition

The minimum corpus must contain at least:

| Slice | Minimum share | Purpose |
|---|---|---|
| core legacy semantic objects | 20% | keep generation aligned with the existing AASL object families |
| `TL{}`, `PMT{}`, `SES{}` objects | 20% | ensure Alternative B additions are first-class rather than bolt-ons |
| nested/cross-reference objects | 20% | exercise structure beyond flat field sets |
| natural-language-to-object grounding pairs | 20% | evaluate actual prompting usefulness |
| negative and repair-oriented examples | 20% | teach rejection and bounded correction behavior |

### 7.3 Data sources

Allowed sources:
- human-authored gold `AASL-T`,
- cross-encoding transductions from canonical `AASL-J` or `AASL-B` reference ASTs,
- schema-driven synthetic objects generated from admitted snapshots,
- validated repair pairs generated from known failure patterns,
- benchmark-only holdout prompts authored independently of training.

### 7.4 Negative example families

The negative slice must include:
- unknown type invention,
- non-canonical field aliases from `T-212`,
- missing required fields,
- wrong enum values,
- nested-type mismatch,
- lineage/security leakage into L5 objects,
- markdown/prose contamination,
- unresolved snapshot references.

### 7.5 Splits

Minimum splits:
- `train`: 80%
- `validation`: 10%
- `test`: 10%

In addition, C44 requires a frozen benchmark suite of `1,000+` vectors that are
not used in tuning or prompt-pack selection.

### 7.6 Labeling requirements

Every corpus item must record:
- `registry_snapshot_id`,
- root type,
- expected canonical parse result,
- expected canonical hash when a gold object exists,
- risk class,
- and whether the item is positive, negative, or repair-oriented.

---

## 8. Benchmark and certification framework

### 8.1 AASL-T Generation Benchmark (`AGB-v1`)

`AGB-v1` is the canonical evaluation suite for C44. It contains at least six
tracks:

| Track | What it measures |
|---|---|
| structural validity | strict parse success under `ATG-v1` |
| schema conformance | required fields, enums, and snapshot-bound admissibility |
| canonical equivalence | canonical hash match against gold reference where applicable |
| semantic slot fidelity | whether required user/task facts are placed in the right fields |
| unknown-term invention rate | rate of non-admitted type/field/token invention |
| latency overhead | decoder and validation overhead against an unconstrained baseline |

### 8.2 Required thresholds

| Mode | Structural validity | Schema conformance | Canonical equivalence | Unknown-term invention | P50 overhead |
|---|---|---|---|---|---|
| `FS-OPEN` | >= 0.90 | >= 0.85 | >= 0.80 | <= 0.5% | n/a |
| `FS-GRAMMAR` | >= 0.95 | >= 0.92 | >= 0.90 | <= 0.1% | <= 80 ms |
| `FT-GRAMMAR` | >= 0.99 | >= 0.97 | >= 0.95 | 0.0% in certified set | <= 50 ms |

The `>90%` few-shot and `>95%` constrained-decoding targets come from the
Alternative B source packet. The stronger `FT-GRAMMAR` thresholds are the
deployment gate for autonomous production usage.

### 8.3 Certification postures

| Certification | Allowed use |
|---|---|
| `ASSISTED` | operator-supervised drafting only |
| `GUARDED` | autonomous low/medium-risk emission with grammar and gates |
| `PRODUCTION` | autonomous emission in high-volume low/medium-risk paths; high-risk still requires separate policy admission |

### 8.4 Failure semantics

Benchmark failure means:
- the mode is not admitted for the claimed risk class,
- no downstream system may silently upgrade it to production,
- and the correct fallback is either a stricter mode or a deterministic builder.

---

## 9. Runtime policy and failure handling

### 9.1 Bounded repair

Bounded repair is optional and tightly constrained:
- maximum one repair pass for `LOW` and `MEDIUM`,
- zero repair passes for `HIGH` and `CRITICAL`,
- repair prompts may reference only structured parser/validator failures,
- repair must preserve the same snapshot, root-type allowlist, and slot bindings.

If the repaired result still fails, the run terminates.

### 9.2 Fallback hierarchy

If generation fails, the runtime must choose one of:
1. stricter C44 mode,
2. deterministic programmatic builder,
3. explicit operator intervention.

It must not:
- emit malformed `AASL-T`,
- fall back to prose,
- or invent an alternate semantic representation without policy approval.

### 9.3 Telemetry

Every runtime integration must record:
- prompt pack ID,
- mode used,
- snapshot ID,
- parse/schema/canonicalization status,
- repair count,
- latency,
- and failure code.

This telemetry is required for ongoing benchmark recalibration and incident review.

### 9.4 Admission rule for autonomous use

An endpoint may autonomously emit `AASL-T` only if:
- the mode is admitted for the configured risk class,
- the output passes parse and schema validation,
- the output passes `C38` canonicalization,
- and the runtime policy for that endpoint allows LLM-authored emission at all.

If the endpoint is backed by leased cognition, two additional rules apply:
- the endpoint must be explicitly marked as leased-cognition-enabled by runtime
  policy,
- and the target surface must be an outer membrane rather than a Sanctum-tier
  locus.

### 9.5 Leased cognition failure handling

Leased cognition failure is broader than parse failure. A leased run must fail if:
- prompt scrubbing cannot reduce the outbound context to the permitted release
  profile,
- the provider policy cannot prove the route is on the approved allowlist,
- the provider response cannot be parsed, validated, or canonicalized,
- the route attempts `HIGH` risk or `CRITICAL` autonomous final emission,
- or the provider posture becomes unavailable, degraded, or contractually
  unacceptable.

The fallback hierarchy for leased cognition is:
1. stricter local/native C44 mode,
2. deterministic builder,
3. explicit operator intervention,
4. explicit failure.

---

## 10. Integration with the Atrahasis stack

### 10.1 `C38` canonicalization

C44 depends directly on the `C38` rule that semantic identity is
encoding-independent and snapshot-bound. `C44` therefore treats canonicalization
success as a hard gate, not a post-processing convenience.

### 10.2 `T-212` semantic object surfaces

`TL{}`, `PMT{}`, and `SES{}` generation must use the canonical field names and
validation rules from `T-212`. The deprecated aliases listed there remain
negative-example material, not acceptable output.

### 10.3 `C39` message layer boundary

C44 does not generate message classes or lineage envelopes. If a downstream
workflow needs `tool_invocation`, `sampling_result`, or any other `C39` class,
that wrapping occurs after C44 emits a validated L5 object.

### 10.4 `T-260` native server framework

`T-260` is a primary downstream consumer of C44. The server framework should use
C44 for:
- prompt-assisted authoring surfaces,
- controlled semantic result drafting,
- and developer/operator workflows where `AASL-T` is desirable.

`T-260` must still own:
- decorator contracts,
- server-side schema enforcement,
- provenance wrapping,
- and any deterministic fallbacks used for high-risk paths.

### 10.5 `C42` and `C43`

`C42` tool-authority surfaces and `C43` bridge surfaces may consume `TL{}`,
`PMT{}`, and `SES{}` objects generated under C44, but C44 does not relax their
authority, provenance, or trust-boundary requirements.

### 10.6 `T-291`

The later justification-test program should use C44 benchmark outputs as one of
its validation inputs when judging whether AACP v2 meaningfully outperforms a
complement-only strategy.

### 10.7 `C45` leased wrapper path

`C45` owns the runtime wrapper that actually talks to frontier providers. `C44`
owns the semantic discipline on that path. This split is intentional:
- `C45` decides whether a request is routed to native execution or leased
  cognition,
- `C45` scrubs, wraps, and provenance-tags the provider call,
- `C44` constrains what semantic object the provider is allowed to emit and what
  admission gates that object must pass before downstream use.

### 10.8 Sovereignty roadmap alignment

C44's leased-cognition rules are transitional, not final-state doctrine.
`Phase 1` permits frontier providers only behind the control plane. `Phase 2`
and `Phase 3` progressively replace that dependency with open-source then native
models. Any future native path may relax leased-provider-specific constraints,
but it must not relax the parse, validation, or canonicalization gates.

---

## 11. Parameters

| Parameter | Meaning | Value |
|---|---|---|
| `C44_GRAMMAR_PROFILE_ID` | Decoder grammar profile | `ATG-v1` |
| `C44_MIN_DATASET_PAIRS` | Minimum labeled tuning corpus | `10000` |
| `C44_MIN_FROZEN_BENCHMARK_VECTORS` | Frozen benchmark suite size | `1000` |
| `C44_MIN_EXEMPLARS_PER_PACK` | Minimum positive exemplars | `2` |
| `C44_MAX_EXEMPLARS_PER_PACK` | Maximum default exemplars | `5` |
| `C44_FEWSHOT_MIN_STRUCTURAL_VALIDITY` | `FS-OPEN` structural gate | `0.90` |
| `C44_CONSTRAINED_MIN_STRUCTURAL_VALIDITY` | `FS-GRAMMAR` structural gate | `0.95` |
| `C44_PRODUCTION_MIN_STRUCTURAL_VALIDITY` | `FT-GRAMMAR` structural gate | `0.99` |
| `C44_CONSTRAINED_MIN_SCHEMA_CONFORMANCE` | `FS-GRAMMAR` schema gate | `0.92` |
| `C44_PRODUCTION_MIN_SCHEMA_CONFORMANCE` | `FT-GRAMMAR` schema gate | `0.97` |
| `C44_CONSTRAINED_MAX_P50_OVERHEAD_MS` | Grammar-constrained latency target | `80` |
| `C44_PRODUCTION_MAX_P50_OVERHEAD_MS` | Production latency target | `50` |
| `C44_MAX_REPAIR_PASSES_LOW_MEDIUM` | Repair cap for low/medium risk | `1` |
| `C44_MAX_REPAIR_PASSES_HIGH_CRITICAL` | Repair cap for high/critical risk | `0` |
| `C44_LEASED_COGNITION_MAX_AUTONOMOUS_RISK` | Highest risk class allowed for autonomous leased final emission | `MEDIUM` |
| `C44_LEASED_PROVIDER_ALLOWLIST_REQUIRED` | Whether leased runs require explicit provider allowlisting | `true` |
| `C44_LEASED_PROMPT_SCRUB_REQUIRED` | Whether outbound provider prompts must pass a scrub gate | `true` |
| `C44_LEASED_MAX_PROVIDER_CONTEXT_BYTES` | Maximum outbound payload size for one leased generation call | `65536` |
| `C44_LEASED_NATIVE_EQUIVALENCE_ALLOWED` | Whether leased output may be treated as native model sovereignty | `false` |

---

## 12. Formal requirements

| ID | Requirement | Priority |
|---|---|---|
| `C44-R01` | Every generation request MUST include an explicit `registry_snapshot_id` | P0 |
| `C44-R02` | Every generation request MUST include an explicit root-type allowlist | P0 |
| `C44-R03` | The decoder grammar MUST be compiled from the pinned snapshot and the active root-type allowlist rather than using ambient free-form token admission | P0 |
| `C44-R04` | Machine-authored `AASL-T` admitted under C44 MUST parse under `ATG-v1` before downstream use | P0 |
| `C44-R05` | Generated output MUST pass snapshot-bound field, enum, and required-field validation before admission | P0 |
| `C44-R06` | Generated output MUST pass `C38` canonicalization under the same pinned snapshot before it is considered valid emission | P0 |
| `C44-R07` | Unknown types, unknown fields, deprecated aliases, unresolved snapshots, and ambiguous canonicalization MUST fail closed rather than trigger heuristic repair | P0 |
| `C44-R08` | `C44` runtimes MUST reject markdown fences, conversational filler, and non-AASL text outside the root object | P0 |
| `C44-R09` | `C44` MUST support the operating modes `FS-OPEN`, `FS-GRAMMAR`, and `FT-GRAMMAR`, and MUST record which mode was used for every run | P1 |
| `C44-R10` | `HIGH` risk autonomous generation MUST NOT use `FS-OPEN` | P0 |
| `C44-R11` | `CRITICAL` risk autonomous final emission MUST NOT use C44; deterministic builders are required | P0 |
| `C44-R12` | Bounded repair MUST be disabled for `HIGH` and `CRITICAL` risk classes | P0 |
| `C44-R13` | Any bounded repair pass MUST preserve the same snapshot, root-type allowlist, and slot-binding contract as the original run | P1 |
| `C44-R14` | Any tuning/alignment claim beyond few-shot prompting MUST use a labeled corpus of at least `C44_MIN_DATASET_PAIRS` examples | P1 |
| `C44-R15` | The corpus MUST include negative examples for unknown-term invention, required-field omission, alias misuse, and cross-layer leakage | P1 |
| `C44-R16` | `AGB-v1` MUST measure structural validity, schema conformance, canonical equivalence, semantic slot fidelity, unknown-term invention rate, and latency overhead | P0 |
| `C44-R17` | `FS-OPEN` certification MUST meet or exceed `C44_FEWSHOT_MIN_STRUCTURAL_VALIDITY` on the frozen benchmark suite | P1 |
| `C44-R18` | `FS-GRAMMAR` certification MUST meet or exceed `C44_CONSTRAINED_MIN_STRUCTURAL_VALIDITY` and `C44_CONSTRAINED_MIN_SCHEMA_CONFORMANCE` | P0 |
| `C44-R19` | `FT-GRAMMAR` production certification MUST meet or exceed `C44_PRODUCTION_MIN_STRUCTURAL_VALIDITY` and `C44_PRODUCTION_MIN_SCHEMA_CONFORMANCE` | P0 |
| `C44-R20` | Runtimes integrating C44 MUST record telemetry for mode, snapshot, validation status, repair count, latency, and failure code | P1 |
| `C44-R21` | `C44` outputs MUST be treated as L5 semantic artifacts only; message lineage, signatures, and transport framing remain downstream responsibilities | P0 |
| `C44-R22` | If a generation attempt fails admission, the runtime MUST either escalate to a stricter mode, use a deterministic builder, or fail explicitly; it MUST NOT emit malformed `AASL-T` | P0 |
| `C44-R23` | Any leased-cognition generation path MUST preserve the same snapshot, grammar, validation, and canonicalization gates as native generation paths | P0 |
| `C44-R24` | Leased-cognition outbound prompts MUST be scrubbed of secrets, raw Sanctum traces, unrestricted tool context, and recursion-critical planning state before provider egress | P0 |
| `C44-R25` | Leased-cognition outputs MUST carry explicit leased provenance and MUST NOT be treated as native-equivalent model sovereignty | P0 |
| `C44-R26` | Autonomous final emission backed by leased cognition MUST NOT exceed `C44_LEASED_COGNITION_MAX_AUTONOMOUS_RISK` | P0 |
| `C44-R27` | If leased-provider policy, allowlist status, or scrub-gate compliance cannot be established, the run MUST fail or fall back locally; it MUST NOT silently continue as leased cognition | P0 |

---

## 13. Conformance vectors

| ID | Scenario | Expected result |
|---|---|---|
| `CV-1` | Generate a `TL{}` object under a pinned snapshot with grammar constraints | Parse pass, schema pass, canonicalization pass |
| `CV-2` | Generate a `PMT{}` object that uses deprecated alias `params` instead of `parameters` | Fail closed at validation |
| `CV-3` | Generate a `SES{}` object that includes `conversation_id` | Fail closed as cross-layer leakage |
| `CV-4` | Generate a valid object with identical semantics but different whitespace/layout | Same canonical payload hash after `C38` normalization |
| `CV-5` | Attempt autonomous `HIGH` risk emission in `FS-OPEN` mode | Runtime policy rejection before emission |
| `CV-6` | `LOW` risk run fails parse once, succeeds on one bounded repair pass | Accepted with `repair_count = 1` |
| `CV-7` | `HIGH` risk run fails parse and requests repair | Rejected; repair not permitted |
| `CV-8` | Output contains unknown root type not present in snapshot | Grammar or validation rejection |
| `CV-9` | Leased-cognition prompt includes secret-bearing or Sanctum-trace material | Scrub gate removes it or run fails before provider egress |
| `CV-10` | Leased-cognition route attempts autonomous `HIGH` risk final emission | Runtime policy rejection before emission |

---

## 14. Risks and open questions

### 14.1 Residual risks

1. `ATG-v1` is intentionally narrower than the full human authoring space. That is
   good for generation safety, but some human-authored idioms may need separate
   migration tooling.
2. Canonical equivalence is easier to score when a gold reference AST exists than
   when the task is open-ended natural-language grounding.
3. Very long nested outputs may still create latency pressure even with grammar
   constraints.

### 14.2 Open questions

1. Should a future C44 v1.1 add a canonical multi-object bundle generation profile
   once the L5 bundle surface is explicitly frozen?
2. Should `FT-GRAMMAR` production certification require per-root-type thresholds
   instead of one aggregate benchmark?
3. How much of the prompt-pack resolver should be deterministic retrieval versus
   model-selected exemplar ranking?

### 14.3 Deployment guidance

The practical rollout order is:
1. certify `FS-GRAMMAR` for `TL{}`, `PMT{}`, and `SES{}`,
2. use deterministic builders for high-risk runtime surfaces,
3. widen to legacy AASL object families after benchmark coverage grows,
4. keep `FS-OPEN` as an operator-assist mode rather than an autonomy default.
