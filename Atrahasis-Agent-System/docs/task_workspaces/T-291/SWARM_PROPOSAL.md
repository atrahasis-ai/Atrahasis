# T-291 Swarm Proposal

- Task: `T-291`
- Title: `AACP v2 Justification Test Specification`
- Agent: `Ninkasi (Codex)`
- Status: `CLAIMED`
- Date: `2026-03-15`

## Governing Inputs

- `C44` benchmark outputs and semantic-generation admission thresholds
- `C47` Forge dual-lane topology, quarantine, and promotion rules
- `T-262` SDK conformance and certification-bundle surfaces
- `T-280` CLI, Inspector, Forge, and editor tooling surfaces
- `T-281` canonical vector corpus and certification evidence posture
- `T-290` `AXIP-v1` runtime-evidence and cross-layer message allocation rules
- historical source-packet justification tests from the `AACP-AASL` strategy and
  task documents

## State Note

The historical source packet contains two slightly different formulations of the
justification tests. The executable task-row definition is the correct baseline
for `T-291`, but one criterion must be normalized for the current repo:

- historical criterion: bridge wraps `100+` MCP servers with zero per-server
  configuration
- current repo criterion: `C47` capability-absorption breadth across `100+`
  representative external capabilities without runtime-bridge dependence

This proposal preserves the original strategic intent while aligning it to the
current Alternative C zero-runtime-bridge doctrine.

## Lead Architect

Define one executable seven-test harness that determines whether the Forge
pipeline is justified compared with the complement-only fallback posture.

The harness should produce:

- stable test IDs,
- explicit measurement packs,
- pass/fail thresholds,
- and unambiguous fallback actions when a criterion fails.

It must consume `C44`, `C47`, `T-281`, `T-262`, `T-280`, and `AXIP-v1` directly
rather than inventing a separate trust or evidence model.

## Visionary

Do not make this a strategy memo. Make it a kill-switch harness for the whole
sovereignty claim.

The seven tests should force the architecture to prove:

- it is actually better than complement-only semantics,
- it scales across transport and capability absorption,
- it preserves provenance distinctions that are impossible to fake cleanly,
- and developers can actually use it fast enough for an ecosystem to form.

If the system cannot pass those tests, the architecture should lose its right to
claim inevitability.

## Systems Thinker

The harness should define:

1. `JustificationRun`
   One signed execution of the seven-test program.

2. `JustificationEvidencePack`
   Aggregated evidence that references:
   - `C44` benchmark outputs,
   - `T-281` certification evidence,
   - `C47` quarantine and promotion audits,
   - `AXIP-v1` runtime-evidence traces,
   - `T-280` developer-workflow captures.

3. `TestResult`
   Per-test metric outputs, threshold comparison, and fallback action.

4. `ScopeDecision`
   Full-program or lane-scoped decision so the repo can distinguish
   “the whole strategy is justified” from “only this retained slice is
   justified.”

No new prerequisite task is required. This is a direct-spec judgment harness
over existing artifacts.

## Critic

Non-negotiable constraints:

- the justification harness must not become a second conformance framework,
- historical bridge-centric criteria must be translated honestly, not erased,
- provenance-distinguishability tests must treat false-native classification as
  an immediate hard failure,
- onboarding claims must be based on reproducible workflows, not anecdotal demo
  paths,
- a failed justification test must imply an actual fallback rule, not a vague
  “revisit later” sentence.

## Final Proposal

Write `T-291` as a direct specification for a normalized seven-test executable
benchmark program that decides whether Alternative C Forge expansion is
justified. The harness should preserve source-packet continuity, align to the
current zero-runtime-bridge doctrine, and produce explicit scope decisions plus
fallback actions from canonical evidence artifacts.
