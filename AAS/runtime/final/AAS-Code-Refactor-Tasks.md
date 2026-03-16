# AAS Code Refactor Tasks

- Extract reusable `aas_re` modules for `coordination_kernel`, `pressure_testing`, `adversarial_review`, and shared runtime support.
- Reduce `aas_paee_cycle_runner.py` to a thin entrypoint that delegates execution to the Coordination Kernel.
- Update bootstrap generation so fresh AAS-RE initialization includes the expanded stack, telemetry channels, and adversarial team registry entries.
- Wire the PAEE pipeline to enforce `swarm -> proposals -> council -> pressure -> adversarial -> selection -> CSSM`.
- Encode convergence with `capability_plateau`, `swarm_consensus`, and `aep_stagnation`, bounded by `maximum_cycles = 20`.
- Add regression checks for bounded convergence, freeze generation, and telemetry emission across pressure and adversarial stages.
