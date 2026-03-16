# TASK_BRIEF: T-9011

## Title
Independent Model Inference Microservice Layer

## Classification
- Task class: `FULL_PIPELINE`
- Modifier: `AASNI`
- Mode: `exploratory candidate ideation`
- Canonical backlog task: `no`

## Operator Prompt
Candidate FULL PIPELINE idea for ideation-only evaluation:

Independent Model Inference Microservice Layer.

The original Atrahasis blueprint strictly separated the Agent Swarm (millions of lightweight software processes) from the Model Inference Layer (centralized GPU clusters hosting hundreds of specialized AI models exposed as microservices).

Reasoning for bringing it back:
Treating agents and the heavy LLMs they use as a single coupled unit wastes massive computational resources. By maintaining a strictly independent model inference layer, the system can scale its components separately based on actual need. Millions of lightweight agents can scale dynamically with task workloads, while the heavy GPU models only need to scale with actual inference demand. This prevents the agents from becoming bloated and preserves the system's economic and thermodynamic efficiency.

## Workspace Rule
This idea may not remain session-only. Use this workspace as the canonical audit surface for ideation, real child swarm evidence, and operator choice.

## Required Ideation Artifacts
- `COMMAND_REQUEST.yaml`
- `HUMAN_DECISION_RECORD.json`
- `WORKFLOW_RUN_RECORD.json`
- `AUTHORITY_COVERAGE_MATRIX.json`
- `TEAM_PLAN.yaml`
- `SWARM_EXECUTION_RECORD.json`
- `CHILD_RESULT_MERGE_PACKAGE.json`
- `children/visionary.json`
- `children/systems_thinker.json`
- `children/critic.json`

## Read-First Constraints
- Resolve named spec ids to their real titled paths before reading them.
- Read the contents of current claim YAML files before ideation so the swarm sees parallel work already underway.
- Stop after ideation and wait for operator choice before promotion.

## Dispatch Context
- Current canonical next dispatchable summary: `PARALLEL` - `T-303` + `T-306` + one of `T-305 / T-307`
