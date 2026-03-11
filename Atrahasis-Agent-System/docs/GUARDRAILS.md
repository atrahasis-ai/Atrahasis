# Guardrails (v1.0)

## Why this exists
Guardrails prevent the most common multi-agent invention failure classes:

1) **Malformed outputs** (unparseable, ambiguous, incomplete)
2) **Scope violations** (unauthorized shared artifact edits, scope creep)
3) **IP hazards** (premature disclosure, unattributed prior art)

---

## Output Format Guardrails (all agents)

### 1) Parseable payload required
Every non-trivial agent must output exactly one structured payload:

- YAML (Ideation Council only)
- JSON (Specialists, Assessors, Synthesis, Researchers)

No extra prose outside the payload.

### 2) Required top-level `type`
All JSON outputs must include a top-level `type` field:
- `INVENTION_RESULT`
- `ASSESSMENT_COUNCIL_VERDICT`
- `PRIOR_ART_REPORT`
- `PROTOTYPE_VALIDATOR_REPORT`
- etc.

---

## Scope Guardrails (specialists)

### 1) Allowed-artifacts rule
Specialists may only change artifacts declared in the Specialist prompt:
- `ALLOWED ARTIFACTS TO MODIFY`
- `ALLOWED ARTIFACTS TO CREATE`

If additional artifacts are required, the specialist must issue a request to the Director.

### 2) Shared-artifacts rule (hard)
Specialists do not edit Synthesis-Owned shared artifacts at all.
They must submit contribution requests instead.

Violations automatically trigger `CONDITIONAL_ADVANCE` at minimum, often `REJECT`.

### 3) Read-before-write
Any artifact modified must be read fully first, and summarized in CHECKPOINT 1 of the invention log.

---

## Validation Guardrails

### Specialist-side (before INVENTION_RESULT)
Specialists must run any required validation and report evidence in their output.

### Synthesis-side
Synthesis Engineer must run:
- contribution request validation
- consistency checks (per INVENTION_CONTEXT)

### Assessment-side
Prototype Validator must execute the prototype and report raw outputs.

---

## IP Guardrails

### 1) No premature disclosure
Never publish, share externally, or post invention details to public repositories without explicit user approval (HITL gate: DISCLOSURE_RISK).

### 2) Prior art attribution
All prior art references must be properly cited. Do not copy patented content verbatim.

### 3) Claims integrity
Patent-style claims must be supported by the technical specification. No unsupported claims.

---

## Human-in-the-Loop Guardrail
Any action tagged `hitl_required: true` cannot proceed until the user explicitly approves.

See `docs/ATRAHASIS_SYSTEM_MASTER_PROMPT_v1.md` §10.
