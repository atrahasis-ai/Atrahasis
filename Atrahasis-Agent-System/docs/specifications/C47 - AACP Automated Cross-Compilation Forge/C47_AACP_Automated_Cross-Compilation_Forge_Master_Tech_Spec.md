# Master Tech Spec: AACP Automated Cross-Compilation Forge (The Semantic Forge)

| Field | Value |
|---|---|
| Title | AACP Automated Cross-Compilation Forge (The Semantic Forge) |
| Version | 1.1.0 |
| Date | 2026-03-14 |
| Invention ID | C47 |
| Originating Task | T-252 |
| Renovation Task | T-RENOVATE-009 |
| Stage | SPECIFICATION |
| Domain | Protocol Isolation / Automated Ecosystem Ingestion / Native Model Adaptation |
| Supersedes | C43 (MCP Bridge), C46 (A2A Bridge) |
| Normative References | C23 SCR, C24 FHF, C32 MIA, C36 EMA-I, C38 FSPA, C40 DAAF, C44 Constrained Generation Engine, C45 ASCF, C50 AAPL/ANVM, Mission-Locked Sovereignty Doctrine |

---

## 1. Executive Summary

Atrahasis cannot stay dependent on external runtime bridges or external frontier providers forever.

The Forge solves that bootstrap problem in two ways:

1. **Locus Conversion Lane**
   Ingest external tool or server code and convert it into native Atrahasis loci.
2. **Native Model Adaptation Lane**
   Ingest open-source model artifacts, adapt them on Atrahasis-controlled hardware, and promote them through quarantine into native deployment tiers.

This dual-lane design matches the staged sovereignty roadmap:

- `Phase 1`: leased cognition behind `C44` and `C45`
- `Phase 2`: open-source native adaptation through `C47`
- `Phase 3`: fully native Atrahasis models trained on internal trace corpora

The Forge is therefore not just a code translator. It is the system that converts outside capability into bounded native substrates without reopening runtime bridges.

---

## 2. Forge Topology

### 2.1 The two-lane architecture

| Lane | Input | Output | Primary purpose |
|---|---|---|---|
| `Lane A: Locus Conversion` | source repositories, tool servers, service code | native `C45`-wrapped loci and manifests | recover ecosystem capability without runtime bridges |
| `Lane B: Native Model Adaptation` | open-source model weights, tokenizers, licenses, eval packs | quarantined then promoted native model families | reduce dependence on leased frontier cognition |

### 2.2 Shared invariants

Both lanes share these invariants:

- build-time ingestion only; no runtime bridge dependency,
- explicit provenance and artifact hashing,
- quarantine before live admission,
- bounded membrane placement,
- no automatic Sanctum promotion.

---

## 3. Lane A: Locus Conversion

### 3.1 Ingestor

The Ingestor pulls a target source repository and extracts:

- AST and dependency graph,
- core business logic,
- external transport and framework glue,
- input/output schemas and configuration contracts.

### 3.2 Evaluator

The Evaluator determines the native upgrades required for Atrahasis:

- economic constraints from `C8`,
- verification trace requirements from `C5`,
- identity and trust binding from `C32` and `C40`,
- membrane placement from `C36`.

### 3.3 Synthesizer

Using `C44`, the Synthesizer emits native code:

- wraps functions in `C45` execution contracts,
- converts external schemas into `AASL`-compatible bundles,
- injects policy, provenance, and economic hooks.

### 3.4 Pre-flight verifier

The output is:

- compiled,
- linted,
- manifest-generated,
- and packaged as a native deployment artifact.

### 3.5 Locus quarantine ring

Generated loci enter a quarantine habitat before they receive live traffic. They run:

- synthetic stress suites,
- security probes,
- economic and verification policy checks,
- and conformance checks tied to `C38`.

Passing quarantine makes the locus eligible for outer-membrane deployment. It does not imply blanket native trust.

---

## 4. Lane B: Native Model Adaptation

### 4.1 Artifact intake

The Model Ingestor acquires:

- model weights,
- tokenizer and vocabulary files,
- architecture metadata,
- license terms,
- published evaluation reports,
- and upstream provenance hashes.

The intake artifact is immutable and content-addressed on receipt.

### 4.2 License and provenance gate

No model artifact may proceed unless the Forge verifies:

- provenance chain is complete enough for audit,
- license terms permit Atrahasis-controlled fine-tuning and bounded deployment,
- the artifact is not revoked, poisoned, or unexpectedly mutated,
- and the model family is on the governance allowlist.

Rejected artifacts do not enter training quarantine.

### 4.3 Conversion and normalization

Accepted artifacts are normalized into an Atrahasis-controlled format:

- weight tensors converted into supported runtime formats,
- tokenizer normalized and diffed against Atrahasis semantic packs,
- context-window and positional metadata pinned,
- model-family metadata recorded for downstream policy and evaluation.

### 4.4 Semantic specialization

The Forge then adapts the model using Atrahasis-controlled training stages:

1. tokenizer and vocabulary reconciliation for `AASL` and related semantic objects,
2. continued pretraining or domain adaptation on approved corpora,
3. supervised fine-tuning on Atrahasis-authored semantic tasks,
4. optional distillation from leased cognition, but only through scrubbed and admitted traces,
5. refusal, provenance, and membrane-policy imprinting.

### 4.5 Training-corpus rules

Permitted corpus classes include:

- public open-license corpora,
- Atrahasis-authored semantic corpora,
- synthetic task corpora produced under native control,
- scrubbed and admitted leased-cognition traces,
- bounded execution and verification traces that have passed corpus-admission review.

Forbidden corpus classes include:

- raw Sanctum traces,
- secrets or credentials,
- unreviewed provider transcripts,
- raw internal planning state from recursion-critical workflows,
- any corpus whose license or provenance posture is not explicit enough for audit.

### 4.6 Model quarantine ring

Imported or adapted models enter a dedicated model quarantine ring with status:

- `IMPORTED`
- `ADAPTING`
- `PROBATION_MODEL`
- `SHADOW`
- `PROMOTED`

Quarantine covers:

- benchmark and jailbreak evaluation,
- semantic conformance against `C44`,
- membrane-specific safety and refusal behavior,
- cost and latency profiling,
- provenance and reproducibility checks,
- and side-by-side shadow comparison against leased or existing native baselines.

### 4.7 Promotion ladder

Promotion is membrane-scoped:

- `PUBLIC_ELIGIBLE`
- `ENTERPRISE_ELIGIBLE`
- `FOUNDRY_ELIGIBLE`
- `SANCTUM_CANDIDATE`

`SANCTUM_CANDIDATE` is not automatic. Open-source adapted models may not jump directly from import to Sanctum deployment. Any Sanctum-candidate path requires separate downstream policy and governance approval.

---

## 5. Integration with the Atrahasis Stack

### 5.1 `C44` and `C45`

`C44` and `C45` define Phase 1 leased cognition. `C47` is the mechanism that reduces and eventually replaces that dependence.

- `C44` constrains semantic emission for adapted native models just as it does for leased providers.
- `C45` chooses whether a route uses leased cognition or native model execution.
- `C47` supplies the promoted native models and converted loci that let `C45` move routes off external providers.

### 5.2 `C36` membrane placement

Forge outputs are deployed by membrane:

- converted loci and adapted models may serve `PUBLIC`, `ENTERPRISE`, or `FOUNDRY`,
- no Forge output receives direct `SANCTUM` reachability merely by passing quarantine,
- inward promotion remains governed by downstream membrane and runtime policy.

### 5.3 `C40` trust posture

Model artifacts are not principals. They do not inherit native trust anchors merely because they are local.

Trust applies to the deployment surface around the model:

- manifests,
- execution contexts,
- lease bindings,
- and membrane placement.

### 5.4 `C23` and `C24`

`C23` supplies runtime isolation and lease discipline for promoted artifacts.
`C24` supplies the quarantine and habitat isolation surfaces used before live admission.

### 5.5 `C50`

`C50` extends code and language conversion farther into universal program adaptation. `C47` remains the nearer-term practical forge for:

- converting external tool servers into native loci,
- and adapting open-source LLMs into Atrahasis-controlled model families.

---

## 6. Parameters

| Parameter | Meaning | Initial value / guidance |
|---|---|---|
| `C47_FORGE_LANES_ENABLED` | active forge lanes | `LOCUS_CONVERSION, NATIVE_MODEL_ADAPTATION` |
| `C47_ALLOWED_BASE_MODEL_FAMILIES` | governance allowlist for open-source model families | `Llama, Mistral, DeepSeek, Qwen, governance-reviewed others` |
| `C47_ACCEPTED_LICENSE_CLASSES` | minimum acceptable license posture | `permissive-commercial or separately reviewed custom license` |
| `C47_MODEL_PROVENANCE_REQUIRED` | whether model provenance metadata is mandatory | `true` |
| `C47_LEASED_TRACE_DISTILLATION_ALLOWED` | whether scrubbed leased traces may seed adaptation | `true` |
| `C47_RAW_SANCTUM_TRACE_TRAINING_ALLOWED` | whether raw Sanctum traces may enter Phase 2 adaptation corpora | `false` |
| `C47_MODEL_QUARANTINE_MIN_EVAL_VECTORS` | minimum model evaluation corpus size before promotion | `5000` |
| `C47_MODEL_SHADOW_MIN_BATCHES` | minimum shadow batches before live promotion | `1000` |
| `C47_SANCTUM_DIRECT_PROMOTION_ALLOWED` | whether imported or adapted open-source models may skip directly to Sanctum | `false` |
| `C47_SYNTHETIC_STRESS_TASK_COUNT` | synthetic task count for converted loci | `1000` |

---

## 7. Formal Requirements

| ID | Requirement | Priority |
|---|---|---|
| `C47-R01` | The Forge MUST preserve a dual-lane architecture: locus conversion and native model adaptation | P0 |
| `C47-R02` | All ingested artifacts MUST be content-addressed and provenance-recorded before further processing | P0 |
| `C47-R03` | No runtime bridge dependency MAY be reintroduced as part of Forge operation or Forge output | P0 |
| `C47-R04` | Converted loci MUST pass build, manifest, and quarantine checks before receiving live traffic | P0 |
| `C47-R05` | Open-source model artifacts MUST clear license and provenance review before adaptation begins | P0 |
| `C47-R06` | Adapted models MUST train only on approved corpora and MUST reject raw Sanctum traces during Phase 2 adaptation | P0 |
| `C47-R07` | Distillation from leased cognition MUST use only scrubbed and admitted traces; it MUST NOT import provider trust posture or raw provider memory | P0 |
| `C47-R08` | Forge-adapted models MUST pass semantic, safety, and benchmark quarantine before live promotion | P0 |
| `C47-R09` | Promotion MUST be membrane-scoped; passing quarantine for one membrane MUST NOT imply blanket admission to others | P0 |
| `C47-R10` | Imported or adapted open-source models MUST NOT receive direct Sanctum promotion without separate governance and downstream policy approval | P0 |
| `C47-R11` | Forge outputs MUST integrate with `C44`, `C45`, `C36`, `C40`, and `C23` rather than bypassing them | P0 |
| `C47-R12` | The Forge SHOULD accumulate native training corpora that reduce future leased-cognition dependence over time | P1 |

---

## 8. Risks and Open Questions

### 8.1 Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Open-source model license ambiguity pollutes the native stack | HIGH | strict license gate and provenance review |
| Adapted models inherit unsafe public-internet behavior | HIGH | quarantine, refusal imprinting, membrane-scoped promotion |
| Leased-cognition distillation leaks provider artifacts or hidden policy dependence | HIGH | scrubbed trace admission only, explicit leased provenance, no raw provider memory |
| A converted or adapted artifact is promoted too aggressively into the core | HIGH | membrane-scoped ladder and hard no-direct-Sanctum-promotion rule |
| Forge complexity expands faster than evaluation capacity | MEDIUM | bounded family allowlist and fixed quarantine minima |

### 8.2 Open questions

1. Which open-source model families should be first in the allowlist by actual expected return per GPU-hour?
2. How much tokenizer divergence from canonical `AASL` should be tolerated before a model family is rejected?
3. At what evidence threshold should a `SANCTUM_CANDIDATE` open-source adapted model be considered for restricted internal use?

---

## 9. Immediate Roadmap

1. Preserve the existing locus-conversion lane for practical tool parity.
2. Stand up the native model adaptation lane for a small allowlist of open-source LLM families.
3. Accumulate scrubbed semantic corpora from `C44`/`C45` and native runtime traces.
4. Promote adapted models first to `PUBLIC` and `ENTERPRISE`, then to `FOUNDRY` where justified.
5. Treat `SANCTUM_CANDIDATE` as a separate future gate, not a default destination.

---

*C47 originated from T-252 and was renovated by Ninkasi for T-RENOVATE-009.*
