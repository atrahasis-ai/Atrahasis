# T-RENOVATE-011 Membrane Audit

## Status

In progress on 2026-03-14 by `Ninkasi`.

This audit covers the actual repo surface behind the shorthand `C1 - C13` label:

- `C1` as a four-file legacy PTA packet,
- `C3` through `C9` as canonical cross-layer and subsystem specs,
- `C10` as a five-file hardening packet,
- `C11` through `C13` as defense-system specs,
- no `C2` directory currently present in `docs/specifications/`.

## Membrane rubric

| Membrane | Meaning in this audit |
|---|---|
| `SANCTUM` | recursion-critical or internal control-plane machinery; no direct external reachability |
| `FOUNDRY` | operator-mediated licensing, review, tribunal, or release-management surfaces |
| `ENTERPRISE` | bounded derivative service or contract-delivery surface |
| `PUBLIC` | public accountability, public documentation, or compatibility artifact safe for broad disclosure |

Primary membrane means where the component is allowed to execute or be directly exposed. A component may emit derivatives to outer membranes without changing its primary membrane.

## Surface anomalies

1. `C2` is missing. This audit treats that as an absent surface, not a placeholder to be invented ad hoc.
2. `C1` is still a legacy multi-file design packet rather than one normalized master spec.
3. `C10` is a hardening packet composed of multiple addenda that inherit membrane posture from the base systems they patch.
4. `C4` is still a legacy `A2A/MCP` compatibility vocabulary surface and therefore cannot be admitted to `SANCTUM` under the sovereign closed-core doctrine.

## Audit matrix

### C1 PTA legacy packet

| Surface | Primary membrane | Notes |
|---|---|---|
| `architecture.md :: Tidal Function Engine` | `SANCTUM` | internal scheduling core |
| `architecture.md :: Scheduling Resolver` | `SANCTUM` | internal assignment and convergence logic |
| `architecture.md :: Verifier Set Computer` | `SANCTUM` | verifier selection is core trust machinery |
| `architecture.md :: Settlement Calculator` | `SANCTUM` | retained only as internal precursor logic; `C8` remains the live settlement authority |
| `architecture.md :: Prediction Model Manager` | `SANCTUM` | internal optimization and surprise prediction |
| `architecture.md :: Surprise Signal Router` | `SANCTUM` | internal coordination traffic |
| `architecture.md :: Field Gradient Computer` | `SANCTUM` | internal topology and optimization |
| `architecture.md :: Tidal Version Manager` | `SANCTUM` | governance-protected internal version control |
| `architecture.md :: Capacity Snapshot Service` | `SANCTUM` | internal capacity view, not public telemetry |
| `architecture.md :: Integration Adapters` | `FOUNDRY` / `ENTERPRISE` / `PUBLIC` | outer-membrane-only compatibility edge if retained at all; never a Sanctum-native surface |
| `technical_spec.md :: Layer 1 Tidal Backbone` | `SANCTUM` | internal substrate protocol |
| `technical_spec_part2.md :: Layer 2 Predictive Delta Communication` | `SANCTUM` | internal parcel coordination |
| `technical_spec_part2.md :: Layer 3 Morphogenic Field` | `SANCTUM` | internal optimization only |
| `technical_spec_part2.md :: Economic Settlement Protocol` | `SANCTUM` | legacy internal precursor; do not interpret as a public market surface |

### C3 Tidal Noosphere

| Surface | Primary membrane | Notes |
|---|---|---|
| `Architecture Overview` | `SANCTUM` | core substrate ownership |
| `Operation-Class Algebra` | `SANCTUM` | internal execution semantics |
| `Tidal Scheduling` | `SANCTUM` | core parcel and locus coordination |
| `Verification Architecture` | `SANCTUM` | verification-routing substrate beneath `C5` |
| `Communication Architecture` | `SANCTUM` | inward-facing coordination only; no public ingress |
| `Governance and Safety` | `SANCTUM` | enforcement lives inside the core even when constitutional authority originates outside |
| `Economic Settlement hooks` | `SANCTUM` | feeds `C8`; not an external market surface |
| `Security Analysis` | `SANCTUM` | internal defense posture |
| `Scale Architecture` | `SANCTUM` | deployment of core coordination machinery |
| `Implementation Roadmap` | `FOUNDRY` | planning and operator rollout guidance, not runtime exposure |

### C4 ASV legacy compatibility surface

| Surface | Primary membrane | Notes |
|---|---|---|
| `ASV core vocabulary and schemas` | `PUBLIC` | public specification and compatibility artifact |
| `Standalone document format` | `PUBLIC` | documentation-safe semantic carrier |
| `A2A integration wrappers` | `ENTERPRISE` / `FOUNDRY` / `PUBLIC` | outer-membrane compatibility only |
| `MCP integration wrappers` | `ENTERPRISE` / `FOUNDRY` / `PUBLIC` | outer-membrane compatibility only |
| `Validator libraries and examples` | `PUBLIC` | developer-facing artifact |
| `Transport trust delegation assumptions` | `ENTERPRISE` / `FOUNDRY` | historical compatibility assumptions; not admitted to Sanctum |

### C5 PCVM

| Surface | Primary membrane | Notes |
|---|---|---|
| `Claim classification` | `SANCTUM` | core verification authority |
| `Tier 1 proof checking` | `SANCTUM` | core verification |
| `Tier 2 evidence evaluation` | `SANCTUM` | core verification |
| `Tier 3 attestation review and probing` | `SANCTUM` | core verification |
| `CACT pipeline` | `SANCTUM` | anti-forgery core |
| `Credibility engine` | `SANCTUM` | internal scoring and propagation |
| `Knowledge admission` | `SANCTUM` | gates what may enter `C6` |
| `Membrane Certificate Engine` | `SANCTUM` | internal certification authority; may emit outward proofs later |
| `Contestable Reliance Membrane` | `FOUNDRY` / `PUBLIC` derivative | challenge intake is outer-facing, but adjudication remains in the verification core |
| `Proof bundle and audit commitments` | `PUBLIC` derivative | public accountability exports must route through `C36` and `C48`, not direct core exposure |

### C6 EMA

| Surface | Primary membrane | Notes |
|---|---|---|
| `Epistemic Quantum model` | `SANCTUM` | core memory substrate |
| `Ingestion` | `SANCTUM` | admitted only through governed intake paths |
| `Circulation` | `SANCTUM` | internal knowledge flow |
| `Consolidation (Dreaming)` | `SANCTUM` | recursion-adjacent synthesis surface |
| `Catabolism` | `SANCTUM` | internal lifecycle control |
| `SHREC regulation` | `SANCTUM` | homeostatic controller |
| `Coherence graph` | `SANCTUM` | internal epistemic topology |
| `Projection engine` | `FOUNDRY` / `ENTERPRISE` / `PUBLIC` derivative | projections may be rendered outward, but the engine remains internal |
| `Retrieval` | `SANCTUM` | primary retrieval authority for the core; outer retrieval must be mediated elsewhere |

### C7 RIF

| Surface | Primary membrane | Notes |
|---|---|---|
| `Intent quantum and lifecycle` | `SANCTUM` | internal orchestration substrate |
| `Decomposition algebra` | `SANCTUM` | recursion-governing planning logic |
| `Domain-scoped state plane` | `SANCTUM` | internal coordination state |
| `Executive plane` | `SANCTUM` | internal execution control |
| `Agent registry and clock service` | `SANCTUM` | internal operating substrate |
| `Intent state registry` | `SANCTUM` | internal workflow truth |
| `Settlement router` | `SANCTUM` with `FOUNDRY` / `ENTERPRISE` consequences | internal accounting bridge into `C8` |
| `Failure detector` | `SANCTUM` | internal reliability layer |
| `Intent admission control` | `SANCTUM` | must remain inside the closed core even for outward-facing task requests |

### C8 DSF

| Surface | Primary membrane | Notes |
|---|---|---|
| `CRDT read path and EABS write path` | `SANCTUM` | internal settlement substrate |
| `Sponsor Budget / AIC` | `SANCTUM` | post-pivot interpretation is internal compute-allocation math |
| `Protocol Credits` | `SANCTUM` | internal anti-spam and contention control |
| `Capacity Slices` | `ENTERPRISE` / `FOUNDRY` | externalized delivery and licensing capacity may be reported here |
| `Settlement classes and streams` | `SANCTUM` | internal accounting authority |
| `Auction and clearing logic` | `SANCTUM` | internal allocator; not a public market venue |
| `Slashing and appeal routing` | `FOUNDRY` | operator and governance review consequences land here |
| `Treasury / public-goods language` | `FOUNDRY` residual | legacy terminology needs later cleanup; do not interpret as a public-token program |

### C9 Cross-Layer Reconciliation

| Surface | Primary membrane | Notes |
|---|---|---|
| `Authority hierarchy and invariants` | `SANCTUM` | canonical internal integration authority |
| `Temporal, class, and type mapping` | `SANCTUM` | internal cross-layer rules |
| `ASV integration mapping` | `PUBLIC` / `ENTERPRISE` / `FOUNDRY` compatibility | historical `C4` mapping should not be treated as Sanctum-native transport authority |
| `Settlement integration` | `SANCTUM` with `FOUNDRY` / `ENTERPRISE` consequences | internal authority over economic wiring |
| `Integration contract directory` | `SANCTUM` | canonical internal contract matrix |
| `Errata and conformance` | `FOUNDRY` / `PUBLIC` documentation | governance and implementation guidance, not runtime exposure |

### C10 hardening packet

| Surface | Primary membrane | Notes |
|---|---|---|
| `C3_HARDENING_EMERGENCY_ROLLBACK.md` | `SANCTUM` | patches internal rollback and governance-channel resilience |
| `C3_HARDENING_RECONFIG_STORM.md` | `SANCTUM` | internal reconfiguration defense |
| `C3_HARDENING_VRF_SMALLRING.md` | `SANCTUM` | internal committee and ring hardening |
| `C5_C6_HARDENING_DEFENSE_IN_DEPTH.md` | `SANCTUM` | internal verification and memory hardening |
| `C6_HARDENING_SHREC_COHERENCE.md` | `SANCTUM` | internal memory-regulation hardening |

### C11 CACT

| Surface | Primary membrane | Notes |
|---|---|---|
| `Commitment chain manager` | `SANCTUM` | internal anti-forgery substrate |
| `Proof checker` | `SANCTUM` | internal verification authority |
| `Evidence evaluator` | `SANCTUM` | internal verification |
| `Adversarial probing and environmental audit` | `SANCTUM` | internal defense execution |
| `Registered circuits and verifier artifacts` | `PUBLIC` derivative | auditability may be public, but use inside the defense remains internal |
| `Economic deterrent hooks` | `FOUNDRY` consequence | slashing and review consequences are externalized, not the defense engine itself |

### C12 AVAP

| Surface | Primary membrane | Notes |
|---|---|---|
| `Anonymous committees` | `SANCTUM` | internal verification defense |
| `Sealed opinion submission` | `SANCTUM` | internal committee protection |
| `Honeypot claims` | `SANCTUM` | internal anti-collusion trap surface |
| `Collusion deterrence payment` | `SANCTUM` with `FOUNDRY` / `ENTERPRISE` consequences | consequences may land on externalized economic actors, but the mechanism remains internal |
| `Conditional behavioral analysis` | `SANCTUM` | internal detection pipeline |
| `Enterprise liability audit` | `FOUNDRY` consequence | enterprise-facing sanction path is operator-governed, not public |

### C13 CRP+

| Surface | Primary membrane | Notes |
|---|---|---|
| `APRT robustness testing` | `SANCTUM` | internal anti-poisoning defense |
| `CODS dissent search` | `SANCTUM` | internal synthesis challenge surface |
| `Source purpose scoring` | `SANCTUM` | internal provenance defense |
| `VRF consolidation selection` | `SANCTUM` | internal K-class gating |
| `Graduated credibility ladder` | `SANCTUM` | internal knowledge-trust control |
| `Depth limits` | `SANCTUM` | internal anti-recursion / anti-poisoning bound |
| `Immune memory` | `SANCTUM` | internal institutional memory of rejected patterns |
| `Novelty pathway` | `SANCTUM` | protected route for paradigmatic discoveries |

## Residual findings

1. `C4` remains the strongest pre-pivot mismatch in the audited range. It is now clearly an outer-membrane compatibility artifact and should never be treated as a Sanctum-native authority surface.
2. `C8` still contains legacy token, treasury, and public-goods phrasing. The membrane assignment in this audit constrains runtime interpretation, but the language remains ripe for later doctrinal cleanup.
3. `C1` and `C10` should eventually be normalized into a clearer archival or supersession posture because their current multi-file packet format obscures membrane ownership.
4. `C5` and `C11` both describe publicly auditable proof material. Under the renovated doctrine, those outward artifacts should be understood as `C48`-style accountability derivatives rather than direct core exposure.

## Recommended normative treatment

- Make `C9` the canonical cross-layer location for this membrane audit summary.
- Treat all unclassified legacy compatibility materials in the audited range as outer-membrane-only until a later retrofit explicitly admits them to a narrower scope.
- Refuse any interpretation that turns `C4` or legacy `C1` integration adapters into direct `SANCTUM` communication authority.
