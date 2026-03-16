# C38 Pre-Mortem

## Failure mode 1: Layers drift into each other
- Symptom: later tasks redefine auth in session docs or payload meaning in transport docs.
- Preventive control: every layer in the master spec has explicit forbidden behaviors.

## Failure mode 2: Canonical identity becomes encoding-specific
- Symptom: the same semantic payload has different authoritative hashes in different encodings.
- Preventive control: semantic canonicalization is authoritative; transport encodings are projections.

## Failure mode 3: Bridges become permanent authority
- Symptom: native AACP surfaces remain underspecified while bridge behavior quietly defines reality.
- Preventive control: bridges are marked compatibility-only with degraded provenance semantics.

## Failure mode 4: T-210 steals later tasks
- Symptom: downstream tasks become trivial restatements because the root spec already wrote their details.
- Preventive control: architecture-level scope only; field-level definition deferred deliberately.

## Failure mode 5: Atrahasis cross-layer consumers are treated as afterthoughts
- Symptom: C5/C6/C8/C23/C24/C36 retrofits become inconsistent because T-210 defined an abstract protocol with no stack bindings.
- Preventive control: integration contracts are included as first-class sections in the master spec.
