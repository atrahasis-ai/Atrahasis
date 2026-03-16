# Human-in-the-Loop Policy

## Core Rule

AAS1 is human-guided. It may analyze, synthesize, hypothesize, simulate, and recommend, but it must not finalize major invention decisions without operator review.

## Mandatory Review Gates

- concept or path selection
- pivots caused by contradiction or feasibility failure
- external research escalation
- resource-intensive implementation work
- public disclosure or patent-sensitive decisions
- abandonment or archival decisions

## Required Operator Artifacts

Every AAS1 run must produce:

- `HUMAN_DECISION_RECORD.json`
- `EXPLORATION_CONTROL_RECORD.json`
- `WORKFLOW_SUMMARY.md`

## Disallowed Behaviors

- no subsystem may self-authorize execution changes
- no automatic pivot may be applied without an operator decision
- no solution path may be treated as selected until a human confirms it
- no exploration budget recommendation may be treated as binding

## Control Ownership

`InventionPipelineManager` controls the workflow. `ExplorationControlEngine` recommends. `HumanDecisionInterface` packages the decision packet. The operator decides.
