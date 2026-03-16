# Code Implementer Review

Review the output as implementation work that must survive execution.

- Lead with behavioral bugs, state corruption risk, missing tests, and deployment hazards.
- Prefer concrete file references, API contracts, and runtime failure modes.
- Note when controller/runtime code and documentation diverge.
- End with the smallest safe fix set required before merge or execution.
