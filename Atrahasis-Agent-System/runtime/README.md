# Runtime State

This directory is the live mutable runtime surface for the Atrahasis Agent System.

- `state/` contains active workflow, provider, operator-session, telemetry, and related execution state.
- `logs/` contains runtime logs produced by the current execution stack.
- `archive/` contains retired runtime artifacts that were moved out of the active state buckets.

The old controller-owned App Server runtime was retired from AAS5. The live runtime surface should no longer contain:
- `runtime/app_server_home`
- `runtime/app_server_home_test`
- `runtime/app_server_ws_smoke.mjs`

If those surfaces reappear, treat them as drift.

Do not treat the sibling `C:\Users\jever\Atrahasis\AAS\` folder as the active runtime state for this repo unless a future migration explicitly redefines that policy.
