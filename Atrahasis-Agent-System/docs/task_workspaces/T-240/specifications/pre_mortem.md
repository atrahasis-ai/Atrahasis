# C42 Pre-Mortem

## Failure mode 1 - Primed contexts become shadow leases

Cause:
- clients or servers start treating continuation or execution-ready contexts as
  if they already authorize runtime work.

Mitigation:
- require explicit `C23` lease issuance for actual execution,
- make runtime handoff data necessary but never sufficient,
- fail closed when the downstream lease step is skipped.

## Failure mode 2 - Stale snapshots drive invalid execution

Cause:
- clients reuse signed inventory state after revocation, tool upgrade, or policy
  change.

Mitigation:
- hard expiry on snapshots,
- explicit invalidation via `tool_change_notification`,
- primed contexts bound to snapshot identity and invalidation state.

## Failure mode 3 - Warm channels leak authority

Cause:
- a long-lived session keeps trust state warm after grants expire or authority
  context changes.

Mitigation:
- bind cached or warm state to authority context and expiry,
- invalidate on grant/session/profile mismatch,
- prohibit warm-channel reuse from becoming ambient rights.

## Failure mode 4 - Bridge executions look native

Cause:
- bridge-derived continuations or execution-ready contexts are not visibly
  degraded compared with native tool execution.

Mitigation:
- require explicit bridge posture markers,
- allow lower provenance floors and capability ceilings for bridge paths,
- preserve policy-visible native-versus-bridge distinction end to end.

## Failure mode 5 - Simple tool calls become too expensive

Cause:
- the protocol forces every tool through continuation-aware, execution-primed
  machinery even when a bounded call-and-result path is enough.

Mitigation:
- keep `IMMEDIATE_ONLY` as the default path,
- make richer priming explicit and opt-in,
- ensure server frameworks can expose simple tools without mandatory advanced
  flow control.
