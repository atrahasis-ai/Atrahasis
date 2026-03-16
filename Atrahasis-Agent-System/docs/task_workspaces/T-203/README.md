# T-203 Parallelism Note

Purpose: annotate the Alternative B backlog with wave-by-wave parallel-capacity guidance so task delegation across multiple agents is safe and dependency-aware.

Main outcomes:
- Added explicit per-wave parallel-capacity notes to `docs/TODO.md`.
- Clarified launch-capacity versus total-task-count for waves with internal blockers.
- Tightened the early execution gate by making `T-210` depend on `T-201`.
- Preserved the hard-gate rule that downstream tasks must stop rather than invent missing upstream architecture.
