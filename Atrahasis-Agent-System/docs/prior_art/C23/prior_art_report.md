# C23 Prior Art Report - Sovereign Cell Runtime (SCR)

**Stage:** RESEARCH
**Date:** 2026-03-12
**Invention:** C23 - Sovereign Cell Runtime (SCR)

---

## Research Question

What already exists for agent execution, durable workflow runtime, secure workload isolation, and model-serving infrastructure, and what remains genuinely missing for Atrahasis?

## Closest Prior-Art Families

### 1. Workflow and durable execution systems

Representative systems:

- Temporal workers and task queues
- durable workflow engines in the saga / compensation family

What overlaps:

- lease-like work assignment,
- retries and timeout semantics,
- durable state transition tracking.

What does not:

- no parcel-local execution semantics from C3,
- no claim-verification evidence contract into C5,
- no explicit inference lease model,
- no sovereignty split between persistent agent identity and execution cell.

### 2. Actor and distributed compute runtimes

Representative systems:

- Ray tasks and actors
- distributed actor frameworks and job executors

What overlaps:

- stateful workers,
- placement and scheduling constraints,
- heterogeneous resource requests.

What does not:

- actor runtimes do not tie execution to operation-class governance,
- they do not emit Atrahasis-native evidence bundles,
- they do not treat model access and tool access as separately leased rights.

### 3. Container and node-local workload runtimes

Representative systems:

- Kubernetes kubelet / pod model
- container runtimes and sandboxed workload hosts

What overlaps:

- node-local realization of scheduled work,
- sandbox selection,
- lifecycle management for workloads.

What does not:

- pod/container identity is too close to workload identity,
- generic runtimes do not encode epistemic claim obligations,
- no built-in bridge to C8 settlement or C5 verification.

### 4. Isolation substrates

Representative systems:

- Firecracker-style microVM isolation
- gVisor / user-namespace / seccomp sandboxes

What overlaps:

- strong process and filesystem isolation,
- multi-tenant execution protection,
- lightweight sandboxing choices by risk tier.

What does not:

- these are substrates, not end-to-end agent runtimes,
- they do not specify leases, evidence, or inference policy.

### 5. Inference serving stacks

Representative systems:

- provider adapter layers from C22
- vLLM / OpenAI-compatible serving
- local model gateways

What overlaps:

- model endpoint abstraction,
- batching and warm serving,
- local versus hosted inference routing.

What does not:

- inference servers do not own tool permissions, execution budgets, or leaf-intent lifecycle,
- they usually meter tokens but not full execution rights across tools, artifacts, and settlement.

## Novelty Assessment

### Component novelty

| Component | Novelty | Notes |
|---|---|---|
| Lease-bound execution cells | 3.5/5 | Lease and sandbox ideas are known; the Atrahasis composition is new |
| Inference Lease Broker | 3.5/5 | Provider routing exists; leasing by intent, profile, and verification duty is new |
| Execution Evidence Bundle | 4.0/5 | Runtime evidence is known; direct binding to C5/C8 stack semantics is stronger and more specific |
| Runtime profile taxonomy | 3.0/5 | Typed workload classes are known; the specific mapping to Atrahasis roles and operation classes is new |
| System-level composition | 4.0/5 | No surveyed system combines parcel locality, execution isolation, inference leasing, evidence sealing, and settlement metering as one runtime substrate |

### Overall novelty

**Overall novelty: 4.0 / 5**

The individual pieces are recognizable, but the missing combination is exactly what Atrahasis needs: a runtime whose first-class object is not a container, actor, or workflow step, but a lease-bound sovereign cell carrying identity separation, capability policy, inference rights, evidence obligations, and settlement metering.

## References

- Temporal docs: https://docs.temporal.io/
- Ray docs: https://docs.ray.io/en/latest/ray-core/actors.html
- Firecracker: https://firecracker-microvm.github.io/
- vLLM docs: https://docs.vllm.ai/
