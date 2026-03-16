# Master Tech Spec: AACP Sovereign Compiler Framework (ASCF)

| Field | Value |
|---|---|
| Title | AACP Sovereign Compiler Framework (ASCF) |
| Version | 1.1.0 |
| Date | 2026-03-14 |
| Invention ID | C45 |
| Originating Task | T-260 |
| Renovation Task | T-RENOVATE-008 |
| Stage | SPECIFICATION |
| Domain | Agent Frameworks / Zero-Trust Execution / Provenance Compilation |
| Supersedes | Standard web-framework wrappers (FastAPI / Express / Actix baseline) |
| Normative References | C36 EMA-I, C40 DAAF, C42 LPEM, C44 Constrained Generation Engine, C23 SCR, C18 Funding |

---

## 1. Executive Summary

ASCF is the runtime wrapper that turns an ordinary service endpoint into a sovereign execution surface.

It supports two execution modes:

1. `NATIVE_SOVEREIGN`
   Work is executed with Atrahasis-native model and tool substrates.
2. `LEASED_COGNITION`
   Work is executed through a temporary frontier-model lease behind Atrahasis-owned control planes.

In leased mode, the external provider is never treated as a trusted system peer. The provider receives only a scrubbed prompt bundle, never raw Sanctum state, direct tool credentials, or authoritative memory ownership. The provider response re-enters Atrahasis only as a leased-provenance artifact and must still pass the `C44` and `C38` admission path before downstream use.

---

## 2. Core Architecture

### 2.1 Execution-mode split

| Mode | Primary substrate | Trust posture | Allowed membranes |
|---|---|---|---|
| `NATIVE_SOVEREIGN` | Atrahasis-controlled models and tools | native | `PUBLIC`, `ENTERPRISE`, `FOUNDRY`, and downstream native surfaces as policy allows |
| `LEASED_COGNITION` | external frontier provider behind ASCF wrapper | explicitly non-native | outer membranes only; never `SANCTUM` |

### 2.2 The `@aacp_sovereign` decorator

The primary entry point remains a language-native decorator or macro:

```python
from aacp.framework import aacp_sovereign

@app.post("/draft")
@aacp_sovereign(
    execution_mode="LEASED_COGNITION",
    provider_policy="frontier-safe-v1",
    lease_requirement="EXECUTION_PRIMED"
)
async def draft(request: AACPRequest, context: SovereignContext):
    return await context.execute(request)
```

The decorator does not merely route HTTP. It compiles the request into a sovereign execution plan, selects the permitted execution mode, binds authority, and enforces provenance and release posture.

### 2.3 Sovereign Context Injection

For every request, ASCF constructs a `SovereignContext`:

- **Identity lock** binds the inbound `C40` authority context to execution.
- **Membrane lock** binds the route to its permitted membrane class.
- **Lease enforcement** reads `C42` invocation priming and expiration.
- **Execution mode lock** prevents a route marked `NATIVE_SOVEREIGN` from silently falling back to leased cognition, and vice versa.

### 2.4 Leased Cognition Capsule

In leased mode, the framework creates a `LeasedCognitionCapsule`:

| Field | Meaning |
|---|---|
| `route_id` | Endpoint identity |
| `provider_policy_id` | Selected approved provider policy pack |
| `membrane_class` | Outer membrane for this call |
| `allowed_root_types` | `C44` root-type allowlist for provider output |
| `prompt_bundle_hash` | Hash of the scrubbed outbound prompt bundle |
| `scrub_profile_id` | Prompt-redaction profile applied before egress |
| `response_budget` | Max response size and latency budget |
| `provider_model_ref` | Provider/model identifier used for this lease |
| `leased_provenance_class` | Mandatory leased provenance label |

The capsule is an execution contract, not merely a network payload.

### 2.5 Provider Egress Scrubber

Before any outbound provider call, ASCF applies a mandatory egress scrubber.

The scrubber must remove or block:

- raw Sanctum traces,
- direct internal identifiers that expose sealed topology,
- secrets and credentials,
- unrestricted tool context,
- recursion-critical planning state,
- release-law forbidden material.

If scrubbing cannot produce a policy-compliant outbound bundle, the run fails.

### 2.6 Tool and memory containment

Leased cognition does not delegate tool authority or memory ownership to the provider.

Rules:

- providers never receive raw tool credentials,
- provider-suggested tool calls are converted into local `AASL` candidates and executed only by Atrahasis-controlled runtimes,
- long-lived memory remains local to Atrahasis,
- provider conversation state is treated as disposable transport state, not canonical memory.

### 2.7 Provenance graph compilation

ASCF still compiles a lease-bound provenance graph:

- inbound request authority and membrane classification,
- scrubbed outbound prompt hash,
- provider identity and policy pack,
- provider response hash,
- downstream validation and canonicalization result,
- local tool invocations and runtime effects.

The response may return before final sealing, but the provenance graph must be sealable asynchronously.

---

## 3. Integration with the Atrahasis Stack

### 3.1 `C40` security profiles

Inbound routing still enforces `C40` on the request path.

For outbound leased cognition:

- the provider call is never treated as native-equivalent,
- no leased route may claim `SP-NATIVE-ATTESTED`,
- provider-facing identity remains an explicitly bounded external posture.

### 3.2 `C44` semantic generation contract

If a provider is used for semantic emission:

- output must target a pinned snapshot,
- output must obey the active root-type allowlist,
- output must pass `C44` parse and schema validation,
- output must pass `C38` canonicalization,
- output must carry explicit leased provenance.

Malformed or ambiguous output is rejected rather than repaired heuristically across trust boundaries.

### 3.3 `C36` membrane placement

Leased cognition is an outer-membrane facility. It may be used only on routes that `C36` marks as `PUBLIC`, `ENTERPRISE`, or `FOUNDRY`.

It is forbidden for:

- `SANCTUM`-tier loci,
- raw novelty-engine access,
- direct recursion-critical planning,
- unscreened inward promotion to the core.

### 3.4 `C42` and `C23`

`C42` provides continuation and lease control. `C23` provides downstream runtime enforcement.

For leased cognition:

- the provider call itself is not the sovereign runtime,
- only Atrahasis-owned post-processing, tool use, and continuation handling may acquire local lease-bound rights,
- any downstream execution handoff remains local and auditable.

---

## 4. Latency and Performance Constraints

To preserve viability:

- prompt validation should remain zero-copy where supported,
- provider calls must respect explicit timeout and byte budgets,
- provenance sealing remains asynchronous,
- scrubbing and policy checks must run before provider egress,
- fallback to local deterministic behavior must not require human repair for every low-risk failure.

---

## 5. Parameters

| Parameter | Meaning | Initial value / guidance |
|---|---|---|
| `C45_DEFAULT_EXECUTION_MODE` | default route execution mode | `NATIVE_SOVEREIGN` |
| `C45_LEASED_PROVIDER_ALLOWLIST_REQUIRED` | whether leased routes require approved provider policy packs | `true` |
| `C45_LEASED_MEMBRANE_ALLOWLIST` | membranes eligible for leased cognition | `PUBLIC, ENTERPRISE, FOUNDRY` |
| `C45_LEASED_SANCTUM_ALLOWED` | whether leased cognition may target Sanctum-tier loci | `false` |
| `C45_LEASED_NO_TRAIN_REQUIRED` | whether provider contract/policy must prohibit training on leased prompts and outputs | `true` |
| `C45_LEASED_MAX_PROMPT_BYTES` | max outbound scrubbed prompt size | `65536` |
| `C45_LEASED_MAX_RESPONSE_BYTES` | max accepted provider response size | `131072` |
| `C45_LEASED_TOOL_CREDENTIAL_EGRESS_ALLOWED` | whether raw tool credentials may leave Atrahasis | `false` |
| `C45_LEASED_PROVIDER_MEMORY_ALLOWED` | whether provider-side persistent memory may be canonical | `false` |
| `C45_LEASED_RETURN_PROVENANCE_REQUIRED` | whether every leased response must carry explicit leased provenance metadata | `true` |
| `C45_ASYNC_PROVENANCE_SEALING` | whether final provenance sealing may occur after response dispatch | `true` |

---

## 6. Formal Requirements

| ID | Requirement | Priority |
|---|---|---|
| `C45-R01` | Every ASCF route MUST declare its execution mode explicitly or inherit `C45_DEFAULT_EXECUTION_MODE` from policy | P0 |
| `C45-R02` | `LEASED_COGNITION` routes MUST be limited to `C45_LEASED_MEMBRANE_ALLOWLIST` and MUST NOT target Sanctum-tier loci | P0 |
| `C45-R03` | Outbound leased provider calls MUST pass a scrub gate before egress | P0 |
| `C45-R04` | If scrubbed egress cannot satisfy release law or policy, the leased run MUST fail rather than partially disclose | P0 |
| `C45-R05` | Providers MUST NOT receive raw tool credentials, direct internal secrets, or canonical long-lived memory ownership | P0 |
| `C45-R06` | Provider responses used for semantic output MUST pass the `C44` and `C38` admission path before downstream use | P0 |
| `C45-R07` | Leased responses MUST carry explicit leased provenance and MUST NOT be mistaken for native model sovereignty | P0 |
| `C45-R08` | Leased cognition MUST NOT silently upgrade its trust posture to `SP-NATIVE-ATTESTED` or any native-equivalent status | P0 |
| `C45-R09` | Any downstream tool invocation suggested by a provider MUST be re-materialized and authorized locally under Atrahasis control | P0 |
| `C45-R10` | Provenance graphs for leased runs MUST include outbound prompt hash, provider identity, provider policy pack, response hash, and downstream admission verdict | P0 |
| `C45-R11` | Provider allowlist, no-train policy, and membrane eligibility MUST be checked before the outbound call is issued | P0 |
| `C45-R12` | If leased cognition is unavailable or policy-invalid, ASCF MUST fall back to native, deterministic, operator-mediated, or explicit failure paths; it MUST NOT bypass policy by making an ad hoc external call | P0 |

---

## 7. Required Supporting Subsystems

This architecture depends on:

- **T-263 Runtime Provenance Kernel** for asynchronous provenance graph sealing
- **provider policy packs** that encode allowlist, no-train, byte-budget, and scrub-profile rules
- **C44 semantic admission** for any leased provider used to emit `AASL` artifacts

These are support surfaces, not trust shortcuts.

---

*ASCF originated from T-260 and was renovated by Ninkasi for T-RENOVATE-008.*
