# C40 - Dual-Anchor Authority Fabric (DAAF)

## Master Technical Specification

| Field | Value |
|---|---|
| Title | Dual-Anchor Authority Fabric (DAAF) |
| Version | 1.0.2 |
| Date | 2026-03-14 |
| Invention ID | C40 |
| Task ID | T-230 |
| System | Atrahasis Agent System v2.4 |
| Stage | SPECIFICATION |
| Normative References | ADR-041, ADR-042, ADR-043, ADR-044, C3 Tidal Noosphere, C23 SCR, C32 MIA, C36 EMA-I, C38 FSPA, C39 LCML, C41 LSCM, C42 LPEM, Alternative B source packet |

---

## Table of Contents

1. System role and architectural position
2. Design principles
3. Seven-layer security enforcement model
4. Dual-anchor trust model
5. Bounded security profiles
6. Authentication and authority context
7. Canonical authority binding and signatures
8. Replay, freshness, downgrade, and poisoning defense
9. Authorization model and capability grants
10. Registry and manifest trust distribution
11. Cross-layer integration and downstream boundaries
12. Parameters
13. Formal requirements
14. Risks and open questions

---

## 1. System role and architectural position

### 1.1 Purpose

DAAF defines the canonical L3 Security model for Alternative B. It is the
upstream authority for how AACP v2:
- authenticates native agents and non-agent actors,
- binds signed authority to canonical message identity,
- detects replay, invariant-breaking downgrade, and poisoning attempts at the
  handshake, bridge, and manifest surfaces,
- authorizes sensitive operations without ambient trust,
- enforces the permanent trust-anchor ceiling between external ingress and
  Sanctum-tier loci.

### 1.2 The problem it solves

Before DAAF, the repo had:
- `C38` defining that security must bind authority rather than meaning,
- `C32` defining native agent identity,
- `C36` defining the external ingress pipeline,
- `C23` defining no-ambient-rights runtime execution,
- but no canonical L3 invention saying how those pieces become one security
  contract for native AACP.

Without DAAF, downstream tasks would be forced to guess:
- which identities count as native,
- which identities may ever touch Sanctum-tier loci,
- how federated and workload identities enter,
- what must be signed,
- when replay or downgrade must fail closed,
- which security-surface poisoning attempts must be rejected before admission,
- how explicit grants differ from ordinary authentication.

### 1.3 Architectural position

Under `C38`, DAAF lives entirely in L3 Security.

DAAF defines:
- trust anchors,
- security profiles,
- authority contexts,
- capability-grant structure,
- canonical authority-binding signatures,
- replay and downgrade posture,
- Sanctum admission ceiling rules.

DAAF does **not** define:
- L1 binding mechanics,
- L2 session-control frames,
- L4 message taxonomy,
- L5 semantic object internals,
- C5 verification verdicts,
- or what downstream subsystem semantically counts as a Sanctum-tier locus.

Downstream layers such as `C23`, `C36`, and `C3` designate which runtime,
memory, tool, control, or ingestion surfaces are Sanctum-tier. DAAF defines the
security rule for those surfaces once designated.

---

## 2. Design principles

### 2.1 Canonical-first security

Security must bind to canonical protocol identity, not uncontrolled transport
bytes or formatting artifacts.

### 2.2 Dual-anchor trust

Native Atrahasis agents and non-agent actors are not forced into one identity
scheme. They enter through different anchor families and remain distinguishable
at policy time.

### 2.3 Admission before action

Authentication, validation, authorization, and dispatch remain separate steps.
Translation or transport reachability never confers execution authority.

### 2.4 Least authority without ambient trust

Authentication establishes who a principal is. Sensitive operations still require
explicit bounded grants.

### 2.5 Bounded profile set

Security negotiation must stay small enough to interoperate and test. Profile
sprawl is treated as architectural drift.

### 2.6 Bridge honesty

Bridge and bootstrap paths are allowed as migration scaffolding, but they must
stay visible and must not silently satisfy native-equivalent trust policy.

### 2.7 Sanctum segregation

External ingress may authenticate into outer membranes, but authentication does
not make that ingress Sanctum-eligible. Non-native anchors, federated sessions,
workload certificates, API-key identities, and bridge tooling are permanently
barred from Sanctum-tier loci. Capability grants cannot override that ban.

---

## 3. Seven-layer security enforcement model

The historical AASL security architecture named seven security layers:
- integrity,
- authenticity,
- provenance trust,
- transport/exchange,
- storage admission,
- access/policy,
- runtime safety.

DAAF promotes those layers into protocol enforcement while preserving existing
layer owners.

| Security layer | DAAF contribution | Owning follow-on authority |
|---|---|---|
| Integrity | canonical authority binding over `C38` canonical message identity | `C38`, `T-215` |
| Authenticity | trust anchors, profile negotiation, authority contexts | DAAF |
| Provenance trust | native vs bridge trust posture, manifest/registry key-chain rules | DAAF + `T-214` |
| Transport/exchange | minimum security profile posture and binding requirements | DAAF + `T-220` to `T-223` |
| Storage admission | required security metadata for later memory/registry admission gates | `C5`, `C6`, `T-214`, `T-290` |
| Access/policy | role/persona admission and capability-grant structure | DAAF |
| Runtime safety | no ambient rights, grant-to-lease expectation | `C23`, `T-240` |

### 3.1 Key boundary rule

Promoting these seven layers to protocol enforcement does **not** mean DAAF
absorbs all their owners. It means the protocol must carry enough security state
for those owners to act coherently.

---

## 4. Dual-anchor trust model

### 4.1 Principal families

| Principal family | Description | Primary anchor path |
|---|---|---|
| `NATIVE_AGENT` | Atrahasis agent participating as a sovereign native peer | `C32` AgentID + Ed25519-rooted keys |
| `HUMAN_USER` | Human operator, trustee, developer, or analyst entering through boundary surfaces | OAuth 2.1 / OIDC / SAML |
| `INSTITUTIONAL_PARTNER` | Organization-level trusted external actor | OIDC/SAML and optional mTLS |
| `EXTERNAL_SERVICE` | Provider, workload, or infrastructure peer | mTLS workload/service certificate |
| `BRIDGE_OR_LOCAL_TOOL` | Migration bridge, local process, or bootstrap tooling surface | bounded API key and/or bridge certificate |

### 4.2 Anchor families

| Anchor type | Meaning | Native-equivalent? |
|---|---|---|
| `MIA_ROOT` | `C32` root public key and derived `AgentID` | Yes |
| `MIA_OPERATIONAL` | delegated operational key chained to a native root | Yes, when chain is valid |
| `FEDERATED_SUBJECT` | issuer + subject from OAuth 2.1 / OIDC / SAML | No |
| `WORKLOAD_CERT` | verified mTLS service/workload identity | No |
| `API_KEY_ID` | registry-issued bounded API-key identity | No |

### 4.3 Native trust rule

Only `MIA_ROOT` and valid `MIA_OPERATIONAL` anchors are native-equivalent. All
other anchor types are ingress mechanisms, not substitutes for native Atrahasis
identity.

Native-equivalent is necessary but not sufficient for Sanctum admission. A
native anchor may be considered for Sanctum-tier loci only when:
- the session profile is `SP-NATIVE-ATTESTED`,
- the target is explicitly declared Sanctum-tier by downstream policy,
- and later authorization plus runtime lease controls admit the work.

No non-native anchor type may ever satisfy Sanctum admission.

### 4.4 Conflict rule

If two claimed anchors for the same session or principal conflict materially, the
session MUST fail closed rather than choosing one heuristically.

### 4.5 Sanctum-tier locus rule

A `Sanctum-tier locus` is any runtime, tool, memory, control, or ingress surface
that downstream policy marks as able to directly affect the sealed
recursion-critical core.

DAAF security posture for Sanctum-tier loci is:
- only `NATIVE_AGENT` principals with valid `MIA_ROOT` or `MIA_OPERATIONAL`
  lineage may be considered,
- `FEDERATED_SUBJECT`, `WORKLOAD_CERT`, and `API_KEY_ID` anchors are always
  non-Sanctum,
- `BRIDGE_OR_LOCAL_TOOL` principal families are always non-Sanctum,
- translation, proxying, session rebinding, bridge mediation, or grant
  presentation MUST NOT convert a non-Sanctum authority context into a
  Sanctum-eligible one.

---

## 5. Bounded security profiles

DAAF defines exactly four interoperable profile families.

| Profile ID | Intended peers | Required anchor types | Signing mode | Trust level |
|---|---|---|---|---|
| `SP-NATIVE-ATTESTED` | native agent-to-agent | `MIA_ROOT` or `MIA_OPERATIONAL` | `DIRECT` | highest |
| `SP-FEDERATED-SESSION` | humans and institutions | `FEDERATED_SUBJECT` | `SESSION_ATTESTED` | medium-high |
| `SP-WORKLOAD-MTLS` | services and providers | `WORKLOAD_CERT`, optional `API_KEY_ID` | `SESSION_ATTESTED` or `DIRECT` | medium-high |
| `SP-BRIDGE-LIMITED` | bridges, local tools, bootstrap | `API_KEY_ID`, optional `WORKLOAD_CERT` | `SESSION_ATTESTED` | bounded/low |

### 5.1 `SP-NATIVE-ATTESTED`

Properties:
- native AACP profile for sovereign agents,
- requires a valid `C32` identity chain,
- security-sensitive messages are signed directly by the native key,
- permitted for native-only, governance-sensitive, and verification-sensitive
  operations when local policy allows,
- the only profile family that may be considered for Sanctum-tier loci.

### 5.2 `SP-FEDERATED-SESSION`

Properties:
- for human and institutional ingress,
- requires a trusted federated session,
- binds an ephemeral session signing key to the authenticated authority context,
- supports privileged operations only when explicit capability grants exist,
- MUST NOT be admitted to Sanctum-tier loci.

### 5.3 `SP-WORKLOAD-MTLS`

Properties:
- for service, provider, and workload peers,
- requires mTLS identity and may include a secondary API-key or policy binding,
- supports session-attested signing over canonical message identity,
- intended for high-confidence machine ingress without claiming native-agent
  continuity,
- MUST NOT be admitted to Sanctum-tier loci.

### 5.4 `SP-BRIDGE-LIMITED`

Properties:
- for bridges, local tools, and bootstrap surfaces,
- may rely on bounded API-key identity,
- MUST expose bridge-limited or degraded provenance posture,
- MUST NOT satisfy native-only policy,
- MUST NOT authorize governance, trust-root mutation, or other high-trust
  operations by itself,
- MUST NOT be admitted to Sanctum-tier loci under any exception-less policy.

### 5.5 Profile selection rules

- The selected security profile MUST be negotiated explicitly through the `C38`
  session surface.
- Every endpoint or message surface MAY declare a minimum acceptable profile.
- Profile changes require a new authenticated handshake; they MUST NOT be smuggled
  mid-session.
- Sanctum-tier loci MUST declare `SP-NATIVE-ATTESTED` as their minimum profile
  and MUST reject all other profiles before capability-grant evaluation.

---

## 6. Authentication and authority context

### 6.1 Authority context

Successful authentication yields one `AuthorityContext`.

| Field | Meaning |
|---|---|
| `authority_context_id` | stable identifier for the authenticated context |
| `principal_family` | one of the DAAF principal families |
| `anchor_type` | anchor used for this authenticated context |
| `anchor_id` | stable subject identifier for that anchor |
| `security_profile_id` | negotiated DAAF profile |
| `session_id` | current `C38` session identifier |
| `issuer_id` | registry, IdP, CA, or security authority that validated the context |
| `role_set` | authenticated role/persona claims available for policy evaluation |
| `session_signing_key_id` | ephemeral key identifier when `SESSION_ATTESTED` |
| `issued_at` | context issuance time |
| `expires_at` | context expiry |
| `provenance_floor` | `NATIVE`, `BRIDGE_ENRICHED`, or `BRIDGE_DEGRADED` minimum posture |
| `sanctum_admission_class` | `NATIVE_CANDIDATE` or `FORBIDDEN` derived from anchor and profile |

The `AuthorityContext` is proof of authenticated identity and role context. It is
not, by itself, permission for every operation.

For any context derived from `FEDERATED_SUBJECT`, `WORKLOAD_CERT`,
`API_KEY_ID`, or `BRIDGE_OR_LOCAL_TOOL`, `sanctum_admission_class` MUST be
`FORBIDDEN`. Grants and translations do not alter that field.

### 6.2 Native agent authentication

For native agents:
1. verify that `AgentID = SHA-256(root_pubkey)` per `C32`,
2. verify possession of the root key or a valid delegated operational key,
3. verify that any operational key chain is consistent with the key registry or a
   valid signed manifest chain,
4. reject conflicts between registry and manifest evidence.

### 6.3 Federated subject authentication

For human and institutional actors:
- verify the OAuth 2.1 / OIDC / SAML assertion against a trusted issuer,
- map the issuer+subject pair into an `AuthorityContext`,
- bind any privileged session to an ephemeral session signing key before
  security-sensitive messages are accepted.

### 6.4 Workload and service authentication

For workload/service actors:
- verify the mTLS chain and workload/service identity,
- optionally require a secondary policy secret such as a bounded API key,
- mint an `AuthorityContext` with the negotiated workload profile.

### 6.5 API-key authentication

API keys:
- MUST be stored and compared as derived key identifiers rather than plaintext,
- MUST carry explicit scope and expiration metadata,
- MUST be treated as bounded admission credentials,
- MUST NOT establish native-agent identity.

### 6.6 Session-attested signing keys

Profiles using `SESSION_ATTESTED` MUST bind one short-lived Ed25519 session
signing key to the `AuthorityContext`.

Rules:
- the session signing key MUST expire no later than the authority context,
- the key MUST be invalid outside the bound `session_id`,
- rotation requires a fresh authenticated update to the authority context,
- a session signing key MUST NOT be reused to impersonate a different anchor or
  profile.

---

## 7. Canonical authority binding and signatures

### 7.1 Why L3 signs more than transport

Transport-level confidentiality and peer authentication are necessary but
insufficient. AACP security-sensitive operations need signatures that survive
transport substitution and still bind to the exact canonical message identity.

### 7.2 Authority Binding Projection (`ABP-v1`)

Security-sensitive actions sign the deterministic L3 authority projection
`ABP-v1`.

`ABP-v1` contains exactly:
- `message_canonical_hash`
- `authority_context_id`
- `security_profile_id`
- sorted `capability_grant_ids`
- `signer_key_id`
- `abp_expires_at`

`message_canonical_hash` comes from `C38` / `T-215`. DAAF does not redefine it.

### 7.3 Signature envelope (`SIG-v1`)

Every canonical authority binding uses:

| Field | Meaning |
|---|---|
| `signature_profile` | fixed value `SIG-v1` |
| `signer_anchor_id` | native anchor or authenticated session anchor |
| `signer_key_id` | direct or session-attested key identifier |
| `authority_context_id` | bound authenticated context |
| `abp_hash` | `SHA-256(ABP-v1 bytes)` |
| `signature_algorithm` | `Ed25519` |
| `created_at` | signature creation time |
| `signature_bytes` | Ed25519 signature over `abp_hash` |

### 7.4 Direct versus session-attested signatures

| Mode | Who signs | Typical profiles |
|---|---|---|
| `DIRECT` | root or operational key owned by the subject anchor | `SP-NATIVE-ATTESTED`, some `SP-WORKLOAD-MTLS` deployments |
| `SESSION_ATTESTED` | ephemeral Ed25519 key bound to the authority context | `SP-FEDERATED-SESSION`, `SP-BRIDGE-LIMITED`, most `SP-WORKLOAD-MTLS` flows |

### 7.5 Mandatory canonical signature floor

At minimum, `SIG-v1` authority bindings are required for:
- `agent_manifest_publish`,
- `agent_manifest_update`,
- `tool_invocation`,
- privileged `verification_request`,
- any governance-sensitive or bridge-administrative message,
- any message family or endpoint whose local policy sets
  `require_canonical_signature = true`.

Lower-risk read-only operations MAY rely on authenticated session posture alone
when local policy permits, but they MUST still carry a valid `AuthorityContext`.

---

## 8. Replay, freshness, downgrade, and poisoning defense

### 8.1 Freshness inputs

Replay detection evaluates:
- `message_id`,
- message `timestamp`,
- `message_canonical_hash`,
- signer/anchor identity,
- authority-context validity window.

### 8.2 Seen-message cache

Receivers MUST retain a seen-message cache keyed by:

`(signer_anchor_id, message_id, message_canonical_hash)`

Interpretation:
- same signer + same `message_id` + same hash -> idempotent redelivery candidate,
- same signer + same `message_id` + different hash -> reject as replay/conflict.

### 8.3 Redelivery rule

Legitimate retries or resume-driven redeliveries MAY preserve the same
`message_id`, but they MUST preserve the same canonical hash and authority
binding. Receivers MUST NOT silently re-execute non-idempotent side effects on a
cached redelivery.

### 8.4 Freshness window

A message outside the accepted freshness window MUST be rejected unless an
explicit resume or replay-safe recovery rule says otherwise.

### 8.5 Session-resume rule

Replay state MUST survive session resume within the allowed resume window. A new
`session_id` does not erase the receiver's knowledge of already-seen business
messages.

### 8.6 Downgrade refusal

The receiver MUST reject a session or message when any of the following would
weaken required invariants:
- selected profile is below the endpoint or message's minimum profile,
- required canonical authority signature is missing,
- a bridge-limited profile tries to satisfy native-only policy,
- trusted registry or manifest key state is unresolved or conflicting,
- the negotiated posture would remove required replay protection.

### 8.7 Poisoning admission gates

The Alternative B program already carries a broader semantic-poisoning model.
DAAF extends that baseline at the L2/L3 boundary with explicit admission gates
for transport, bridge, and manifest security surfaces.

No handshake, manifest, or privileged message may influence routing, trust, or
authorization until it clears these gates:

| Gate | Purpose | Typical checks |
|---|---|---|
| `G0: Shape gate` | reject malformed pre-auth artifacts before state allocation | schema validity, field cardinality, duplicate/conflicting fields, bounded pre-auth size |
| `G1: Negotiation-invariant gate` | reject offers that would create incoherent or weakened session posture | version/profile/encoding intersection, explicit selected tuple, no premature business traffic |
| `G2: Freshness gate` | reject replay, stale resume, or reused message identity | timestamp window, replay cache, resume tuple and cursor validity |
| `G3: Provenance-posture gate` | reject hidden bridge posture or authority-scope confusion | native vs bridge disclosure, profile floor, provenance mode, grant floor |
| `G4: Manifest-trust gate` | reject spoofed or stale manifest authority | signature chain, subject/endpoint binding, registry agreement, revocation/supersession visibility |

These gates are cumulative. Passing a later gate never excuses failure at an
earlier one.

### 8.8 T-231 security-surface poisoning extension

`T-231` extends the program-level 13-threat semantic-poisoning model with the
following Alternative B security-surface attack families. This addendum does not
renumber the broader taxonomy; it defines the concrete L2/L3 admission posture
needed for native `AACP`.

| Threat family | Attack shape | Detection mechanisms | Mandatory admission gate |
|---|---|---|---|
| `SPF-01 Malformed handshake exploitation` | attacker sends malformed, oversized, duplicate-field, or internally inconsistent `handshake_request` / `session_resume_request` artifacts to induce partial state or ambiguous negotiation | strict `SCF-v1` parsing, bounded pre-auth size, duplicate-field rejection, offer-cardinality limits, "no business traffic before ACCEPT" enforcement | `G0`, `G1` |
| `SPF-02 Transport replay and resume abuse` | attacker replays business messages, handshake artifacts, or stale resume requests to trigger duplicate side effects or recover an authority context illegitimately | replay cache on canonical identity, freshness window, new-session replay memory, resume cursor/session tuple validation | `G2` |
| `SPF-03 Encoding downgrade and carrier confusion` | attacker attempts media-type, opcode, or carrier-level mismatch so a message is reinterpreted under a weaker or unintended encoding/profile | negotiated encoding vs media-type/opcode comparison, explicit profile floor checks, canonical-hash consistency, rejection of implicit transcoding | `G1`, `G3` |
| `SPF-04 Bridge-mediated injection` | attacker uses a bridge or local tool surface to inject translated traffic while suppressing degraded provenance or impersonating native posture | `provenance_mode` checks, `SP-BRIDGE-LIMITED` ceiling enforcement, bridge-origin disclosure, grant/provenance-floor checks for tool and manifest-affecting flows | `G3`, `G4` |
| `SPF-05 Agent Manifest spoofing` | attacker publishes or relays a counterfeit manifest that misstates subject identity, endpoint keys, native posture, or supersession state | signature-chain validation, subject/endpoint binding checks, registry/manifest conflict detection, revocation and supersession validation, stale-manifest rejection | `G4` |

### 8.9 Admission outcomes

When any `SPF-*` family is detected:
- the affected artifact MUST be rejected or quarantined before it can influence
  authority, routing, manifest trust, or runtime dispatch,
- receivers MUST NOT "repair" malformed or downgraded artifacts heuristically,
- non-idempotent side effects MUST remain suppressed on replay/conflict,
- local implementations SHOULD emit a stable poisoning-category reason code for
  conformance and incident analysis.

---

## 9. Authorization model and capability grants

### 9.1 Two-stage authorization

DAAF authorization has two stages:

1. **Role/persona admission**
   - based on the authenticated `AuthorityContext`,
   - determines whether the principal may reach a given security surface at all.

2. **Capability-grant authorization**
   - required for sensitive or high-consequence operations,
   - narrows what the already-admitted principal may do.

### 9.2 Role/persona rule

DAAF does not define the global Atrahasis role taxonomy. It requires only that:
- role/persona claims be explicit in the `AuthorityContext`,
- authorization evaluate those claims independently of translation or transport,
- downstream owners such as `C36`, `C14`, and `C18` remain free to define the
  role semantics they own.

Before any grant evaluation, DAAF MUST also apply a Sanctum admission gate:
- if the target is not Sanctum-tier, ordinary role/persona policy proceeds;
- if the target is Sanctum-tier, only an `AuthorityContext` with
  `sanctum_admission_class = NATIVE_CANDIDATE`, `principal_family =
  NATIVE_AGENT`, and `security_profile_id = SP-NATIVE-ATTESTED` may continue;
- all `HUMAN_USER`, `INSTITUTIONAL_PARTNER`, `EXTERNAL_SERVICE`, and
  `BRIDGE_OR_LOCAL_TOOL` contexts MUST fail closed for Sanctum-tier targets
  before capability-grant evaluation.

### 9.3 Capability grant structure

`CapabilityGrant` is the generic L3 grant artifact.

| Field | Meaning |
|---|---|
| `grant_id` | unique grant identifier |
| `issuer_anchor_id` | signer that issued the grant |
| `subject_anchor_id` | intended principal or subject context |
| `authority_context_id` | context this grant is bound to, when session-bound |
| `operation_scope` | abstract operation family or message-class scope |
| `target_selector` | bounded target reference or selector |
| `policy_hash` | hash of the policy snapshot used for issuance |
| `issued_at` | issuance time |
| `expires_at` | expiry time |
| `provenance_floor` | minimum provenance posture required for use |
| `grant_signature` | issuer signature over the grant |

### 9.4 Capability grant rules

- Grants MUST be explicit, signed, and time-bounded.
- Grants MUST be non-transferable across unrelated subjects.
- Session-bound grants MUST NOT survive into a new session unless reissued.
- Grants MUST be invalid when their required provenance floor is not met.
- Grants MUST be presented or referenced in `ABP-v1` when used for a
  security-sensitive action.
- Grants MUST NOT elevate a non-native or `FORBIDDEN` authority context into
  Sanctum eligibility.
- Grants targeting Sanctum-tier loci MUST be bound to one native anchor lineage,
  one authority context, and one bounded downstream target selector.

### 9.5 Default grant-required operations

By default, explicit capability grants are required for:
- manifest publication or update,
- tool invocation across a trust boundary,
- long-lived subscription or push-style operations,
- privileged verification or governance actions,
- bridge administration and protocol-translation control surfaces,
- any operation targeting a Sanctum-tier locus,
- any operation local policy marks as high consequence.

### 9.6 Runtime handoff rule

When an operation becomes runtime work, DAAF authorization must hand concrete
rights downward into `C23` lease and capability-broker surfaces. No ambient tool
or network right may exist outside that downstream enforcement path.

For Sanctum-targeting runtime work, the handed-off rights MUST preserve:
- native anchor lineage,
- `SP-NATIVE-ATTESTED` provenance,
- the bounded target selector used for admission,
- and an explicit non-bridge posture through the entire `C23` handoff.

---

## 10. Registry and manifest trust distribution

### 10.1 Public-key registry posture

The public-key registry is the authoritative long-lived native trust source for:
- native root keys,
- native key revocation state,
- native key rotation lineage where supported by `C32`.

### 10.2 Signed Agent Manifest posture

Signed Agent Manifests are the authoritative endpoint-scoped disclosure surface
for:
- supported security profiles,
- supported auth schemes,
- endpoint-scoped operational keys,
- native versus bridge posture claims.

Manifests remain downstream work for `T-214`, but DAAF sets the trust rule:
- manifests may advertise endpoint-scoped keys and auth support,
- they must chain to native root trust or another accepted issuer,
- they must not silently override conflicting registry truth.

### 10.3 Conflict and fail-closed rule

If registry state and manifest state disagree on a native key or trust posture,
the receiver MUST fail closed until the conflict is resolved.

### 10.4 Revocation and supersession

- API keys MUST support explicit revocation.
- Session signing keys expire automatically with their authority context.
- Capability grants MUST expire or be revocable independently.
- Manifest and key supersession MUST remain visible in provenance and policy
  checks.

### 10.5 Manifest anti-spoofing admission

Before a manifest may influence endpoint trust, capability exposure, or key
selection, the receiver MUST verify:
- the manifest signature chain terminates in an accepted issuer,
- the manifest's `subject` and advertised endpoint set are consistent with the
  endpoint being contacted or queried,
- native posture claims do not conflict with registry truth,
- the manifest is not revoked, superseded, or stale beyond policy,
- bridge-published manifests do not silently promote bridge posture to native.
- manifests for non-native or bridge surfaces MUST NOT advertise Sanctum-tier
  capability or access posture.

---

## 11. Cross-layer integration and downstream boundaries

### 11.1 Existing stack integration

| Surface | DAAF contract |
|---|---|
| `C32` MIA | authoritative native agent anchor and key lineage |
| `C36` EMA-I | authenticate -> validate -> authorize -> dispatch ordering for external ingress and zero direct external Sanctum admission |
| `C23` SCR | runtime lease and capability enforcement; no ambient rights and native-lineage preservation for Sanctum-targeting work |
| `C5` PCVM | consumes stronger signed provenance and trust posture but retains verification authority |
| `C38` / `T-215` | canonical message identity source used by DAAF signatures |

### 11.2 Downstream Alternative B boundaries

| Task | DAAF provides |
|---|---|
| `T-214` | manifest auth-scheme set, profile IDs, key-chain and signature posture |
| `T-231` | the concrete replay/downgrade/spoofing attack surface and admission gates defined by this addendum |
| `T-240` | generic capability-grant model and no-ambient-authority rule |
| `T-250` / `T-251` | bridge-limited trust ceiling and provenance-floor requirements |
| `T-262` | `aacp.security` module shape: profiles, contexts, grants, signatures, replay handling |
| `T-281` | conformance targets for authentication, signature validation, replay rejection, grant checking |
| `T-290` | trust contracts into the rest of the stack |

### 11.3 Forbidden behavior

Downstream tasks MUST refine the DAAF contract rather than silently replacing it
with:
- transport-only trust as a substitute for canonical authority binding,
- bridge equivalence to native posture,
- external or bridged identity admission to Sanctum-tier loci,
- ambient authorization outside explicit context and grant handling.

---

## 12. Parameters

| Parameter | Meaning | Initial value / guidance |
|---|---|---|
| `AACP_SECURITY_PROFILE_SET` | canonical profile set | `SP-NATIVE-ATTESTED, SP-FEDERATED-SESSION, SP-WORKLOAD-MTLS, SP-BRIDGE-LIMITED` |
| `AACP_NATIVE_SIGNING_ALGORITHM` | algorithm for native direct signatures | `Ed25519` |
| `AACP_SESSION_SIGNING_ALGORITHM` | algorithm for session-attested signatures | `Ed25519` |
| `AACP_AUTHORITY_CONTEXT_MAX_TTL_MS` | default max lifetime of an authority context | `3600000` |
| `AACP_SESSION_SIGNING_KEY_MAX_TTL_MS` | default max lifetime of a session signing key | `1800000` |
| `AACP_CAPABILITY_GRANT_MAX_TTL_MS` | default max lifetime of a capability grant | `900000` |
| `AACP_REPLAY_CACHE_TTL_MS` | minimum retention for seen-message cache entries | `86400000` |
| `AACP_MESSAGE_FRESHNESS_WINDOW_MS` | default freshness acceptance window | `300000` |
| `AACP_MAX_CLOCK_SKEW_MS` | allowed sender/receiver clock skew | `120000` |
| `AACP_ABP_PROFILE` | authority-binding projection profile | `ABP-v1` |
| `AACP_SIGNATURE_PROFILE` | authority signature envelope profile | `SIG-v1` |
| `AACP_REPLAY_CACHE_KEY` | canonical replay-cache tuple | `signer_anchor_id + message_id + message_canonical_hash` |
| `AACP_API_KEY_TRUST_LEVEL` | default policy treatment of API-key identity | `LOW_BOUNDED` |
| `AACP_BRIDGE_NATIVE_EQUIVALENCE_ALLOWED` | whether bridge-limited profile may satisfy native-only policy | `false` |
| `AACP_SANCTUM_ALLOWED_PROFILE_SET` | acceptable profiles for Sanctum-tier loci | `SP-NATIVE-ATTESTED` |
| `AACP_SANCTUM_EXTERNAL_ANCHOR_ALLOWED` | whether non-native anchors may target Sanctum-tier loci | `false` |
| `AACP_SANCTUM_GRANT_NATIVE_BOUND_REQUIRED` | whether Sanctum-targeted grants must bind to one native lineage and one authority context | `true` |
| `AACP_PREAUTH_MAX_ARTIFACT_BYTES` | maximum accepted size for handshake, resume, or manifest artifacts before authenticated admission | `65536` |
| `AACP_HANDSHAKE_MAX_OFFER_SET_CARDINALITY` | maximum combined count of offered versions, profiles, encodings, and registry snapshots in one negotiation artifact | `16` |
| `AACP_BRIDGE_DISCLOSURE_STRICT` | whether bridge-mediated traffic must expose explicit non-native provenance posture | `true` |
| `AACP_MANIFEST_SUBJECT_ENDPOINT_BINDING_REQUIRED` | whether manifest subject identity must match the queried endpoint surface before trust is granted | `true` |
| `AACP_MANIFEST_MAX_STALENESS_MS` | maximum manifest age tolerated without explicit refresh or supersession confirmation | `300000` |

---

## 13. Formal requirements

| ID | Requirement | Priority |
|---|---|---|
| DAAF-R01 | AACP v2 L3 security MUST distinguish native Atrahasis trust anchors from non-native ingress anchors | P0 |
| DAAF-R02 | Only valid `C32`-rooted anchors MAY satisfy native-equivalent policy | P0 |
| DAAF-R03 | AACP security negotiation MUST use the bounded four-profile set defined by DAAF unless later governance explicitly extends it | P0 |
| DAAF-R04 | Successful authentication MUST yield an explicit `AuthorityContext` before sensitive operations are accepted | P0 |
| DAAF-R05 | Authentication, validation, authorization, and dispatch MUST remain distinct steps; translation or transport reachability MUST NOT confer authority | P0 |
| DAAF-R06 | Security-sensitive operations MUST bind to canonical message identity using `ABP-v1` and `SIG-v1` or a later explicitly-versioned equivalent | P0 |
| DAAF-R07 | `message_canonical_hash` consumed by DAAF MUST come from the `C38` / `T-215` canonical identity pipeline rather than transport bytes | P0 |
| DAAF-R08 | `SP-BRIDGE-LIMITED` MUST NOT satisfy native-only or other high-trust policy by itself | P0 |
| DAAF-R09 | API-key authentication MUST remain bounded-admission only and MUST NOT establish native-agent identity | P0 |
| DAAF-R10 | Receivers MUST maintain a replay cache keyed by signer anchor, `message_id`, and canonical hash | P0 |
| DAAF-R11 | The same signer using the same `message_id` with a different canonical hash MUST be rejected as replay/conflict | P0 |
| DAAF-R12 | Legitimate retries or resumed redeliveries MAY preserve `message_id`, but they MUST preserve canonical identity and authority binding | P1 |
| DAAF-R13 | Invariant-breaking security downgrade MUST terminate negotiation or message acceptance rather than silently weaken security posture | P0 |
| DAAF-R14 | Capability grants for sensitive actions MUST be explicit, signed, time-bounded, and non-transferable | P0 |
| DAAF-R15 | Session-bound grants and session signing keys MUST expire with or before their bound authority context | P1 |
| DAAF-R16 | Runtime-facing rights derived from DAAF authorization MUST be handed into `C23` lease/capability enforcement; no ambient rights may remain | P0 |
| DAAF-R17 | Registry/manifest key conflicts for native identity MUST fail closed rather than be resolved heuristically | P0 |
| DAAF-R18 | DAAF MUST provide enough security state for `T-214`, `T-231`, `T-240`, `T-262`, `T-281`, and `T-290` to refine rather than invent L3 behavior | P1 |
| DAAF-R19 | DAAF MUST NOT redefine semantic payload meaning, verification verdicts, or runtime isolation semantics owned by other layers | P0 |
| DAAF-R20 | Bridge and translated provenance posture MUST remain policy-visible in authority evaluation | P1 |
| DAAF-R21 | Handshake, resume, and manifest artifacts MUST clear strict pre-auth validation and bounded-size checks before any authority context, capability exposure, or material server state is created | P0 |
| DAAF-R22 | No business traffic, capability mutation, or privileged discovery result may be admitted before an explicit accepted handshake tuple is established | P0 |
| DAAF-R23 | Replay and freshness controls MUST apply to handshake, resume, manifest publication/update, and other security-sensitive discovery flows, not only ordinary business messages | P0 |
| DAAF-R24 | Encoding, media-type, opcode, and carrier posture mismatches MUST be rejected as downgrade/poisoning attempts; implementations MUST NOT silently transcode or reinterpret them into an allowed encoding | P0 |
| DAAF-R25 | Bridge-mediated or translated traffic MUST expose explicit non-native provenance posture and MUST NOT satisfy native-only, manifest-authoritative, or other high-trust policy without an explicit bridge policy exception | P0 |
| DAAF-R26 | Manifest admission MUST validate signature chain, subject/endpoint binding, revocation/supersession state, and registry agreement before manifest-derived trust or capability disclosure is consumed | P0 |
| DAAF-R27 | Manifest publish/update flows that regress trust posture, key lineage, supported security profile, or native-versus-bridge classification unexpectedly MUST be rejected or quarantined pending revalidation | P1 |
| DAAF-R28 | Implementations SHOULD emit stable poisoning-category rejection or quarantine codes for `SPF-01` through `SPF-05` so `T-281` conformance and downstream incident tooling can test and observe the defense surface | P1 |
| DAAF-R29 | Non-native anchors (`FEDERATED_SUBJECT`, `WORKLOAD_CERT`, `API_KEY_ID`) and `BRIDGE_OR_LOCAL_TOOL` principal families MUST NOT be admitted to Sanctum-tier loci | P0 |
| DAAF-R30 | Sanctum-tier loci MUST require `SP-NATIVE-ATTESTED` and native-equivalent `C32` anchor lineage before capability-grant evaluation begins | P0 |
| DAAF-R31 | Capability grants MUST NOT override the Sanctum external-anchor ban or convert a `FORBIDDEN` authority context into Sanctum-eligible posture | P0 |
| DAAF-R32 | Authority contexts derived from non-native or bridge ingress MUST be marked `sanctum_admission_class = FORBIDDEN` for downstream policy evaluation | P0 |
| DAAF-R33 | Rights handed from DAAF into `C23` for Sanctum-targeting runtime work MUST preserve native anchor lineage, bounded target scope, and explicit non-bridge provenance | P0 |
| DAAF-R34 | Non-native manifests, bridge descriptors, or compatibility surfaces MUST NOT advertise Sanctum-tier capability or equivalent access posture | P1 |

---

## 14. Risks and open questions

### 14.1 Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Federation becomes the practical center of gravity | HIGH | native-equivalent policy restricted to `C32` anchors |
| Session-attested signing keys become confused-deputy vectors | HIGH | strict binding to one authority context and one `session_id` |
| Capability grants become unbounded semantic mini-programs | MEDIUM-HIGH | generic grant shape only; downstream target detail stays owned downstream |
| Registry and manifest drift create trust ambiguity | MEDIUM | fail-closed conflict rule |
| Bridge-limited profile is overused for convenience | MEDIUM-HIGH | explicit policy ceilings and conformance testing |
| Convenience exceptions reopen Sanctum through federated, workload, or bridge ingress | HIGH | hard false parameters, Sanctum admission gate before grant evaluation, and no-override grant rule |
| Over-strict poisoning gates reject legitimate bridge migration traffic | MEDIUM | keep bridge posture explicit, policy-bounded, and test with bridge conformance vectors |
| Stale manifest caches create false trust or false rejection during rapid rotation | MEDIUM | subject/endpoint binding, visible supersession, bounded manifest staleness window |

### 14.2 Open questions

1. Should all cross-trust operations eventually require `SIG-v1`, or should some
   low-risk reads remain session-auth-only permanently?
2. What later governance surface should own global revocation propagation for
   manifests, grants, and session signing keys across habitats?
3. How much target-selector structure belongs in generic `CapabilityGrant` versus
   downstream tool/resource/prompt task definitions?

---

## Conclusion

DAAF gives Alternative B the missing security invention it needed.

Its essential claim is simple:

Atrahasis can have sovereign protocol security only if native agent identity,
external ingress identity, canonical message authority, explicit grants, and
bridge trust posture are separated cleanly enough to cooperate without becoming
interchangeable, and only if that separation remains hard enough that no
external or bridged identity can ever cross into Sanctum-tier loci.

That is the security contract this specification establishes.
