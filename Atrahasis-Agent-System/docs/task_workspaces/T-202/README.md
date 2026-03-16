# T-202 Ordering Note

Purpose: reorder the Alternative B backlog in `docs/TODO.md` by execution-safe wave order and tighten dependency links where category grouping could cause speculative downstream design.

Main outcomes:
- Replaced topic-bucket ordering with wave-based execution order.
- Added explicit dependency-safety rules to prevent downstream tasks from inventing architecture when prerequisites are incomplete.
- Tightened several dependencies to reflect practical sequencing:
  - `T-214` now depends on `T-230`
  - `T-231` now depends on `T-214` and `T-240`
  - `T-262` now depends on `T-260`
  - `T-281` now depends on `T-250` and `T-260`
  - Retrofit tasks now depend on `T-301` and `T-300` where boundary/audit context is required
