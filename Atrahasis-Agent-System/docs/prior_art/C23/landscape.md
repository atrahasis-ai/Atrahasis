# C23 Landscape Analysis - Sovereign Cell Runtime (SCR)

**Stage:** RESEARCH
**Date:** 2026-03-12

---

## Market / System Landscape

The relevant landscape splits into four camps:

1. General workflow engines
2. General compute runtimes
3. Secure isolation substrates
4. Model-serving gateways

Each solves a slice of the problem. None defines the runtime contract Atrahasis actually needs.

## Competitive Map

| Family | Strength | Why it is insufficient for Atrahasis |
|---|---|---|
| Workflow engines | Durable execution, retries, compensation | No parcel-local runtime semantics; no execution evidence sealed for verification |
| Actor/compute runtimes | Stateful workers, scale-out execution, heterogeneous resources | No native lease of model rights, tool rights, and settlement obligations together |
| Container orchestration | Mature scheduling and sandbox packaging | Too generic; identity, sovereignty, and epistemic policy are outside the runtime model |
| Inference servers | Fast model serving, batching, provider abstraction | Only solve the model call path, not execution control of complete agent work |
| Agent frameworks | Fast experimentation | Usually weak on isolation, metering, provenance, and constitutional boundaries |

## Strategic Gap

Atrahasis needs a runtime that:

- is subordinate to C3/C7 rather than a replacement scheduler,
- treats execution as policy-carrying and auditable,
- can provision both tools and models under bounded rights,
- can produce execution evidence that verification and settlement layers can consume.

That gap appears real and stack-specific.

## Adoption Implications

### Advantages

- The runtime can be built from familiar implementation primitives.
- The design can expose simpler bootstrap profiles for Wave 1.
- Provider abstraction aligns with C22's planned local and hosted model adapters.

### Adoption headwinds

- The runtime is more opinionated than generic orchestrators.
- Evidence completeness will be scrutinized because LLM-backed execution is not fully reproducible.
- Strong isolation for governance and verifier workloads imposes cost overhead.

## RESEARCH Verdict

Proceed. The landscape suggests that Atrahasis should not try to invent a new container engine or a new model server. It should invent the binding layer that composes those substrates into a sovereign, evidence-carrying runtime aligned with C3, C5, C7, and C8.
