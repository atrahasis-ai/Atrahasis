# T-062 Concept Selection Record

**Task:** T-062 — Recovery & State Assurance
**Date:** 2026-03-12
**HITL Decision:** APPROVED — combined concept (IC-1 + IC-2 + IC-3 scoped)

## Minted Invention
- **C34 — Black-Start Recovery Fabric with Adversarial State Reconstruction**

## Concept Composition
- **IC-1 (Part I):** Black-Start Boot Sequence — coordinated cross-layer recovery with strict boot order C8→C5→C3→C7→C6, per-epoch state digests, synchronization predicates, consistent-cut computation
- **IC-2 (Part II):** Recovery Witness Verification — post-recovery Merkle verification with authority-directed reconciliation via C9 hierarchy
- **IC-3 (Part III, subsystem of Part I):** Adversarial Reconstruction Fallback — declarative cross-layer reference registry, causal traversal for state reconstruction, bounded epoch window

## Council Scores (Combined)
- Novelty: 3.5
- Feasibility: 3.5
- Impact: 4.0
- Estimated spec: 4,000-5,500 lines

## Scoping Constraints (from Critic, accepted unanimously)
1. IC-3 is a SUBSYSTEM of IC-1, not co-equal
2. Hard coverage bounds — explicit declaration of what can/cannot be reconstructed
3. Bounded epoch window (≤10 epochs configurable)
4. Declarative reference registry, not general engine

## Monitoring Flags (carried from IDEATION)
- MF-1: Quantify cross-layer reference density during RESEARCH
- MF-2: Recovery coordinator placement (C7 vs C9) — resolve at DESIGN
- MF-3: C5 state snapshotting as blocking dependency
- MF-4: Benchmark continuous anti-entropy overhead
- MF-5: Novelty claims focus on architectural integration + adversarial resilience

## Dissent
- IC-3 was initially deferred by the council, then reintegrated after the user posed the question and the council reconvened. The adversarial resilience reframing (recovery-targeted attacks via digest corruption) was the deciding factor.
- No remaining dissent on the combined approach.
