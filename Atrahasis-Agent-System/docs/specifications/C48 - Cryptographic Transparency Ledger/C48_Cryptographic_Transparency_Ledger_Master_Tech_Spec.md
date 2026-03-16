# Master Tech Spec: Glass Vault

| Field | Value |
|---|---|
| Title | Glass Vault |
| Version | 1.0.0 |
| Date | 2026-03-14 |
| Invention ID | C48 |
| Renovation Task | T-RENOVATE-010 |
| Stage | SPECIFICATION |
| Domain | Public Accountability / Cryptographic Transparency / Governance Compliance |
| Normative References | C5 PCVM, C14 AiBC, C36 EMA-I, C40 DAAF, C49 Unidirectional Osmosis Vacuum, C51 Release Law, Mission-Locked Sovereignty Doctrine, Master Redesign Spec |

---

## 1. Executive Summary

Atrahasis is governed by the doctrine of `Closed Capability, Open Accountability`.

That doctrine requires a public proof surface, but it does not permit public access to the novelty engine, raw internal traces, model internals, or prompts. `C48 Glass Vault` is the bounded accountability membrane that resolves that tension.

`C48` publishes narrow, machine-checkable governance and release-law compliance proofs through an outward-only cryptographic path. It proves specific events such as refusal-path execution, constitutional release-gate satisfaction, embargo status, and policy anchoring. It does not claim to prove that Atrahasis is globally safe, morally perfect, or free of every undiscovered failure mode.

The core architectural rule is strict:

- the inner system may emit witness commitments,
- but the proof predicates, verifier logic, and public proof acceptance rules are rooted in an externally governed verification plane rather than Sanctum self-attestation.

This makes `C48` a public accountability membrane, not a self-certifying propaganda channel.

---

## 2. Scope and Non-Goals

### 2.1 In scope

- outward-only witness export for narrow compliance events,
- versioned predicate registry for proofable accountability statements,
- external verifier plane and proof compilation flow,
- append-only public transparency ledger,
- public proof retrieval through `C36` accountability receptors,
- policy, release-law, and audit-log anchoring for published proofs,
- bounded proof families for refusal, release, embargo, and bypass-control events.

### 2.2 Out of scope

- proving that Atrahasis is globally safe,
- revealing raw prompts, chain-of-thought, source code, model weights, or full internal traces,
- creating a public command path into the Sanctum,
- publishing arbitrary user-specific reasoning histories,
- replacing `C14` constitutional governance with cryptographic automation,
- proving universal negative claims over unconstrained hidden state.

---

## 3. Design Principles

1. **Outward-only diode**  
   `C48` is a one-way publication membrane. Public observers may verify already exported proofs, but they may not send proof-generation commands into the sealed core.

2. **External verifier root**  
   The system under scrutiny must not be the sole authority for deciding whether it passed. Predicate logic, circuit hashes, verifier keys, and acceptance policy are governed outside Sanctum.

3. **Narrow predicate catalog**  
   `C48` proves only a small allowlisted set of machine-checkable compliance events. Any pressure to broaden the system into a universal safety proof engine must be refused.

4. **Commitment over disclosure**  
   Public accountability is achieved through commitments, hashes, inclusion proofs, and zero-knowledge statements rather than disclosure of sensitive internal contents.

5. **Constitution over operators**  
   The proof surface must be able to show that protected events followed constitutional gates rather than founder or operator discretion.

6. **No capability leakage**  
   A proof bundle may reveal that a rule was followed, but it must not leak enough structure to reconstruct a protected request, protected artifact, or recursion-critical method.

7. **Bounded negative claims only**  
   If `C48` proves an absence claim, that claim must be scoped to a committed event domain and time window. It may not present unbounded universal negatives as if they were mathematically meaningful.

---

## 4. Proofable Event Surface

### 4.1 What `C48` proves

`C48` is restricted to the following predicate families in `v1.0.0`:

| Predicate ID | Meaning | Primary witness source | Public disclosure ceiling |
|---|---|---|---|
| `REFUSAL_PATH_EXECUTED` | a request classified as prohibited was routed to the refusal path and no outward release occurred | `C51`, `C5` | commitment to classification and refusal event only |
| `RELEASE_GATE_SATISFIED` | a high-consequence outward release crossed the required constitutional and release-law gates | `C14`, `C51`, `C5` | release class, gate set, policy anchor, no raw payload |
| `EMBARGO_STATUS_ACTIVE` | a protected artifact remains under embargo at a declared snapshot time | `C51`, embargo registry, `C5` | artifact commitment and embargo state only |
| `POLICY_VERSION_ANCHORED` | a decision or proof event was evaluated against a specific policy or release-law version | `C14`, `C51` | policy identifier, version, and commitment |
| `AUDIT_LOG_COMMITTED` | a governance or release event was committed into the accountable audit chain | `C5` | commitment root, inclusion proof, timestamp |
| `PROTECTED_EVENT_SET_BYPASS_FREE` | within a committed protected-event set for a bounded epoch, no event carried an unauthorized bypass marker | `C5`, `C14`, `C51` | event-set commitment, epoch identifier, bypass-free proof |

`RELEASE_GATE_SATISFIED` bundles may include subordinate lineage attestations tying a release event to its governing policy, audit record, and release class without exposing the protected payload itself.

### 4.2 What `C48` explicitly does not prove

`C48` does not prove:

- that all internal reasoning was correct,
- that all future behavior will be safe,
- that no undiscovered vulnerability exists,
- that the model has no hidden capabilities,
- that every possible operator abuse is impossible outside the committed event domain,
- or that a published proof implies blanket trust in the whole institution.

### 4.3 Statement-bounded accountability

Every `C48` proof statement must answer three questions unambiguously:

1. Which exact predicate is being proven?
2. Which committed event or event set is the statement about?
3. Which policy, verifier, and time scope governed the statement?

If any of these are ambiguous, the proof must not be published as a canonical `C48` bundle.

---

## 5. Architecture

### 5.1 Structural position

```text
Protected internal events
  (C14 / C51 / C5 / embargo state)
            |
            v
  Witness Capsule Builder
            |
            v
  Outward-only Proof Diode
            |
            v
  External Verifier Plane
  - Predicate Registry
  - Circuit / Verifier Registry
  - Proof Compiler
  - Ledger Publisher
            |
            v
  Append-only Transparency Ledger
            |
            v
  C36 proof_query / public accountability surfaces
```

The critical boundary is between the witness-emitting side and the verifier side. Witnesses may originate from protected internal systems, but proof acceptance happens only in the external verifier plane.

### 5.2 Components

| Component | Trust boundary | Role |
|---|---|---|
| Witness Sources | inner protected systems | emit the minimum event commitments needed for proofable governance facts |
| Witness Capsule Builder | inner boundary | converts raw internal event records into minimal proof capsules |
| Outward-only Proof Diode | membrane boundary | physically and logically forbids inward traffic from the proof surface into the core |
| Predicate Registry | external governance plane | publishes allowlisted predicates, schemas, circuit hashes, and verifier-key references |
| External Verifier Plane | external governance plane | validates capsules against approved predicates and compiles proof bundles |
| Transparency Ledger | public accountability plane | stores append-only proof commitments and proof metadata |
| Public Query Surface | public membrane | exposes proof retrieval and verification metadata through `C36` |

### 5.3 Witness source families

`C48` v1.0.0 expects witness input from the following authorities:

- `C51` Release Law for refusal-path and release-class decisions,
- `C14` governance for constitutional approvals and policy-version anchoring,
- `C5` for audit-chain commitments and inclusion proofs,
- embargo-control surfaces for protected-artifact status commitments.

No direct human-entered witness is treated as canonical unless it has already been committed through the governing internal authority surface.

---

## 6. External Verifier Constraint and Predicate Governance

### 6.1 Verifier root of trust

`C48` adopts the recovered hardening rule:

> Proof predicates and verification logic must be rooted in externally governed, constitutionally controlled verification logic rather than Sanctum self-attestation.

Operationally, this means:

- Sanctum may emit witness commitments,
- Sanctum may not unilaterally define what counts as passing,
- Sanctum may not silently swap the verification circuit,
- Sanctum may not publish a self-blessed proof as if it were a canonical `C48` proof bundle.

### 6.2 Predicate Registry

Every published predicate definition must include:

| Field | Meaning |
|---|---|
| `predicate_id` | stable machine identifier |
| `predicate_version` | semantic version of the statement definition |
| `statement_template` | exact machine-checkable statement being proven |
| `witness_schema_hash` | hash of the admitted witness-capsule schema |
| `circuit_hash` | hash of the proving circuit or verification logic |
| `verifier_key_hash` | hash of the verifier key or accepted verifier artifact |
| `policy_anchor_ref` | constitutional or policy authority approving the predicate |
| `effective_from` | first valid publication instant |
| `effective_to` | optional supersession or retirement instant |
| `disclosure_profile` | public, public-redacted, or restricted-public proof bundle posture |

### 6.3 Governance of predicate changes

Predicate changes must obey these rules:

- new predicates require constitutional approval before use,
- changed predicates never rewrite old published proofs,
- retired predicates remain visible in historical ledger entries,
- circuit or verifier defects must be published as supersession events rather than quietly patched away.

### 6.4 External auditor posture

`C48` is constitutionally governed but designed for external auditability. The verifier plane should therefore support co-signature, audit, or republication by approved external auditors without granting those auditors inward access to protected state.

---

## 7. Witness and Proof Pipeline

### 7.1 Witness capsule

The canonical exported unit is `WitnessCapsule`.

```text
WitnessCapsule := {
  capsule_id,
  predicate_family,
  event_time,
  event_epoch,
  source_authority_ref,
  subject_commitment,
  event_commitment,
  policy_commitment,
  audit_commitment?,
  event_set_commitment?,
  release_class?,
  disclosure_profile,
  supporting_commitments[],
  source_signature_ref
}
```

Rules:

- `subject_commitment` may identify a request, artifact, or event subject by commitment only,
- `event_commitment` binds the event without exporting the raw event body,
- `event_set_commitment` is mandatory for bounded negative claims such as bypass-free epoch proofs,
- raw prompts, raw outputs, source code, model weights, and recursion-critical traces are forbidden witness content.

### 7.2 Proof generation flow

1. An internal governing system emits a protected event.
2. The event is committed through its authoritative control surface, such as `C51`, `C14`, or `C5`.
3. The Witness Capsule Builder extracts the minimum commitment-bearing fields.
4. The capsule crosses the outward-only proof diode.
5. The external verifier plane resolves the matching predicate version from the Predicate Registry.
6. The verifier checks witness-schema compatibility and policy-anchor validity.
7. The Proof Compiler produces a zero-knowledge proof or equivalent bounded cryptographic proof artifact.
8. The resulting proof bundle is anchored to the append-only transparency ledger.
9. Public users retrieve and verify the bundle through `C36` proof surfaces without causing new inward work.

### 7.3 Proof bundle

The canonical public unit is `ProofBundle`.

```text
ProofBundle := {
  proof_bundle_id,
  predicate_id,
  predicate_version,
  statement_hash,
  witness_capsule_ref,
  proof_artifact_ref,
  verifier_key_ref,
  policy_anchor_ref,
  audit_anchor_ref?,
  ledger_entry_id,
  ledger_root_ref,
  disclosure_level,
  issued_at,
  supersession_state
}
```

Every canonical proof bundle must let an external verifier answer:

- which statement was proven,
- with which verifier artifact,
- against which witness capsule,
- under which policy version,
- and where the result is anchored on the public ledger.

### 7.4 No on-demand inward proofing

Public queries may request:

- an existing proof bundle,
- ledger inclusion proof,
- predicate metadata,
- or supersession status.

Public queries may not request:

- a fresh proof requiring new Sanctum work,
- raw witness disclosure,
- or interactive challenge-response with protected internal state.

If a new proof is needed, it must be generated from already exported witness capsules and only within the external verifier plane.

---

## 8. Public Ledger and Stack Integration

### 8.1 Transparency ledger

The `C48` ledger is append-only and public-facing. Its responsibilities are:

- durable publication of proof-bundle commitments,
- visibility of predicate versions and supersession state,
- inclusion-proof support for public verification,
- historical traceability of policy-anchor changes,
- auditability of verifier-circuit replacement or revocation.

The ledger is not a governance engine, not a source of runtime control, and not a backchannel into protected systems.

### 8.2 Integration with `C36`

`C36` exposes `proof_query` as the public receptor for accountability bundles. `C48` becomes the canonical backing authority for that receptor's proof-bundle retrieval path.

`proof_query` consumers may filter by:

- `predicate_id`,
- `ledger_entry_id`,
- `event_epoch`,
- `policy_anchor_ref`,
- or bundle status.

### 8.3 Integration with `C51`

`C51` defines the release-law facts that are most important to public accountability:

- refusal-path routing for prohibited requests,
- release-class gating for high-consequence outputs,
- embargo of recursion-critical artifacts.

`C48` is the public cryptographic accountability surface for those facts. It does not replace `C51`; it externalizes bounded proof of `C51` compliance.

### 8.4 Integration with `C5` and `C14`

- `C5` provides the accountable audit chain and commitment surfaces used by `AUDIT_LOG_COMMITTED`.
- `C14` provides the policy and constitutional anchors used by `RELEASE_GATE_SATISFIED`, `POLICY_VERSION_ANCHORED`, and bypass-control proofs.

---

## 9. Parameters

| Parameter | Meaning | Initial value / guidance |
|---|---|---|
| `C48_EXTERNAL_VERIFIER_REQUIRED` | whether canonical proof acceptance must occur outside the protected core | `true` |
| `C48_INWARD_PROOF_TRAFFIC_ALLOWED` | whether the proof surface may carry any public-to-core traffic | `false` |
| `C48_PREDICATE_ALLOWLIST` | admitted predicate families | `REFUSAL_PATH_EXECUTED, RELEASE_GATE_SATISFIED, EMBARGO_STATUS_ACTIVE, POLICY_VERSION_ANCHORED, AUDIT_LOG_COMMITTED, PROTECTED_EVENT_SET_BYPASS_FREE` |
| `C48_WITNESS_CAPSULE_MAX_BYTES` | maximum exported capsule size | `65536` |
| `C48_RAW_PROMPT_DISCLOSURE_ALLOWED` | whether raw prompts may appear in witness or proof bundles | `false` |
| `C48_RAW_ARTIFACT_DISCLOSURE_ALLOWED` | whether protected artifacts may appear in proof bundles | `false` |
| `C48_PUBLIC_PROOF_BUNDLE_MAX_BYTES` | maximum public proof-bundle payload | `262144` |
| `C48_LEDGER_APPEND_ONLY_REQUIRED` | whether published ledger entries may be rewritten in place | `true` |
| `C48_EPOCH_BYPASS_PROOF_REQUIRED` | whether bounded epoch bypass-free proofs are required for protected-event sets | `true` |
| `C48_ON_DEMAND_INNER_REQUERY_ALLOWED` | whether public queries may trigger new inward witness generation | `false` |
| `C48_PREDICATE_SUPERSESSION_VISIBILITY_REQUIRED` | whether retired or defective predicates remain visible on ledger | `true` |
| `C48_PROOF_RETENTION_POLICY` | retention horizon for proof bundles and predicate metadata | `perpetual public ledger, subject to redaction of nonessential metadata only` |

---

## 10. Formal Requirements

| ID | Requirement | Priority |
|---|---|---|
| `C48-R01` | `C48` MUST operate as an outward-only accountability membrane and MUST NOT expose a public-to-core proof-generation path | P0 |
| `C48-R02` | Canonical `C48` proofs MUST be restricted to an explicit allowlist of narrow, machine-checkable predicates | P0 |
| `C48-R03` | Predicate definitions, circuit hashes, verifier keys, and proof acceptance rules MUST be rooted in an externally governed verification plane rather than Sanctum self-attestation | P0 |
| `C48-R04` | Witness capsules MUST contain commitments and minimum metadata only; they MUST NOT export raw prompts, raw protected outputs, model weights, or recursion-critical traces | P0 |
| `C48-R05` | Every canonical proof bundle MUST bind together the predicate version, witness capsule reference, verifier artifact reference, policy anchor, and ledger anchor | P0 |
| `C48-R06` | Public proof retrieval MUST be satisfiable from the external verifier plane and public ledger without triggering new protected-core computation | P0 |
| `C48-R07` | `C51` prohibited-output refusals MUST be representable through `REFUSAL_PATH_EXECUTED` proof bundles | P0 |
| `C48-R08` | High-consequence outward releases MUST be representable through `RELEASE_GATE_SATISFIED` proof bundles that anchor the governing policy version | P0 |
| `C48-R09` | Embargo proofs MUST be snapshot-bounded and MUST NOT disclose the protected artifact contents beyond approved commitments | P0 |
| `C48-R10` | Any absence or bypass-free proof MUST be explicitly scoped to a committed event domain and bounded time window; unbounded universal negative claims are forbidden | P0 |
| `C48-R11` | Predicate retirement, verifier-key replacement, and circuit supersession MUST remain publicly visible as ledgered historical events rather than silent rewrites | P0 |
| `C48-R12` | `C48` MUST integrate with `C5`, `C14`, `C36`, and `C51` as downstream accountability infrastructure and MUST NOT bypass those governing authorities | P0 |
| `C48-R13` | `PROTECTED_EVENT_SET_BYPASS_FREE` proofs MUST derive from a committed event-set root that is complete for the declared protected-event scope and epoch | P0 |
| `C48-R14` | `C48` SHOULD support independent public verification of ledger inclusion, predicate metadata, and supersession status without requiring privileged credentials | P1 |

---

## 11. Risks and Open Questions

### 11.1 Primary risks

| Risk | Severity | Mitigation |
|---|---|---|
| under-constrained proof circuits yield false confidence | HIGH | external circuit review, visible circuit hashes, supersession visibility |
| witness omission causes a bypass-free proof to overclaim its event domain | HIGH | event-set commitments, bounded-domain proofs, completeness checks |
| political pressure expands `C48` from narrow accountability into fake universal safety proofing | HIGH | explicit non-goals, allowlisted predicates only |
| disclosure creep leaks protected prompts or artifacts through witness design | HIGH | commitment-only witness rules, hard disclosure ceilings |
| verifier governance centralizes into an opaque inner-team process | MEDIUM | constitutional approval path, external audit posture, visible registry history |

### 11.2 Open questions

1. Which proof system family offers the best balance of auditability, proving cost, and public verification simplicity for the initial predicate set?
2. What external auditor co-signature threshold is strong enough to prevent silent verifier drift without making routine proof publication operationally brittle?
3. How should long-lived embargo proofs be refreshed so the public can verify continued embargo without learning anything new about the protected artifact itself?

---

## 12. Immediate Roadmap

1. Stand up the Predicate Registry with the six admitted `v1.0.0` predicate families.
2. Define the canonical `WitnessCapsule` and `ProofBundle` schemas and bind them to `C5`, `C14`, and `C51` authorities.
3. Implement the outward-only proof diode and verifier-plane separation.
4. Wire `C36 proof_query` to the public ledger retrieval path.
5. Add conformance vectors for refusal proofs, release-gate proofs, embargo proofs, and bounded bypass-free epoch proofs.

---

*C48 was created by Ninkasi for T-RENOVATE-010.*
