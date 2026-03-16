# Runtime State

This directory is the live mutable runtime surface for the Atrahasis Agent System.

- `state/` contains active workflow, provider, operator-session, telemetry, and related execution state.
- `logs/` contains runtime logs produced by the current execution stack.
- `archive/` contains retired runtime artifacts that were moved out of the active state buckets.

Do not treat the sibling `C:\Users\jever\Atrahasis\AAS\` folder as the active runtime state for this repo unless a future migration explicitly redefines that policy.
