# Anu Round-Five Merge Packet

## Decision

No new doctrine inventions.
I think we should do it like this:

- Keep the doctrine locked as already converged.
- Accept `AAT 4` as an implementation-hardening pass, not a new doctrine pass.
- Keep `C48`, but require its proofs to come from external human-governed audit
  and verification predicates, not Sanctum self-attestation.
- Keep the one-way osmosis model, but add a real quarantine stack before data
  promotion inward.
- Keep `AIC` internal-only and tie it to a hard thermodynamic cap backed by
  actual compute and energy budgets.
- Bootstrap `Sanctum` and a minimal operator-governance `Foundry` in parallel,
  then `Enterprise`, then `Public`.
- Treat the next work as spec hardening and execution, not more doctrine
  exploration.

## Repo-Grounded Note

- `RENOVATION_TASKS.md` already reflects most of these hardening moves.
- The main remaining documentation gap is in `MASTER_REDESIGN_SPEC.md`, where
  `C48` still needs an explicit statement that proof predicates are governed
  outside Sanctum's self-issued reasoning claims.
