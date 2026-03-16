# T-061 Domain Analogy Brief

## Purpose

Find structural analogies for the missing agent runtime layer before ideation promotion.

## Analogy 1 - Operating System Process Supervisor

- Structural parallel: long-lived identity outside the process, short-lived execution units inside the kernel's scheduling and memory-protection model.
- Useful transfer: separate agent identity from execution cell identity; make leases and capabilities explicit rather than ambient.
- Limitation: a process supervisor does not understand claim verification, settlement, or epistemic provenance.

## Analogy 2 - Kubernetes Kubelet + Pod Sandbox

- Structural parallel: a node-local runtime receives scheduled work, materializes sandboxed workloads, mounts input state, and reports status upward.
- Useful transfer: keep scheduling and execution separate; use parcel-local hosts analogous to node-local executors.
- Limitation: generic workload runtimes do not encode proof obligations, claim classes, or budget-aware inference access.

## Analogy 3 - Telecom Baseband Scheduler

- Structural parallel: a central control plane allocates bounded radio resources to many flows while preserving deterministic time windows and backpressure.
- Useful transfer: inference capacity and tool slots should be leased like scarce spectrum, not treated as unlimited shared state.
- Limitation: telecom schedulers assume a narrow workload family and do not handle open-ended tool and reasoning execution.

## Analogy 4 - Theater Stage Manager

- Structural parallel: the script is fixed at the act level, but each scene needs specific actors, props, lighting rights, and time windows, all coordinated without letting performers improvise access to the whole building.
- Useful transfer: leaf intents should arrive with an execution packet that states exactly which tools, models, artifacts, and time budget are allowed.
- Limitation: theater has human improvisation and no machine-verifiable evidence path.

## Recommendation

The most useful synthesis is:

- node-local runtime from kubelet/pod models,
- explicit lease and capability boundaries from operating systems,
- scarce inference allocation from telecom scheduling,
- scene packetization from stage management.

This points toward an execution model where the core object is not "a container" or "a request" but a lease-bound sovereign cell with explicit rights, bounded duration, and a required evidence trail.
