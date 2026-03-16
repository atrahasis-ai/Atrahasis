# TASK_BRIEF: T-9012

## Title
Independent Model Inference Microservice Layer

## Classification
- Task class: `FULL_PIPELINE`
- Modifier: `AASNI`
- Mode: `exploratory candidate ideation`
- Canonical backlog task: `no`

## Operator Prompt
Treat the following as a candidate new FULL PIPELINE task, but do not add it to docs/TODO.md, do not claim a canonical task, and do not edit shared state yet. Your job is to decide whether this idea: 1. should be added back in as a real new subsystem, 2. is already covered well enough by the current architecture and should be rejected, 3. should inspire a different new subsystem or redesign direction instead. Run AAS4 in IDEATION mode only. Requirements: First evaluate the idea against the current authoritative architecture, especially the current roles of C45, C42, C47, C36, C18, C22, C39, and T-300. One valid outcome is reject as already subsumed. One valid outcome is keep the objective but redesign it into a different module. One valid outcome is add it as a real new subsystem and identify likely downstream redesign tasks. Present me 3-4 concrete options. For each option, include short name, one-sentence summary, main upside, main risk, whether it integrates cleanly or requires redesign of existing modules. Then give me your recommended option. Stop after IDEATION and wait for my choice. Do not continue into research or specification. Idea: An Independent Model Inference Microservice Layer. The original Atrahasis blueprint strictly separated the Agent Swarm (millions of lightweight software processes) from the Model Inference Layer (centralized GPU clusters hosting hundreds of specialized AI models exposed as microservices). Reasoning for bringing it back: Treating agents and the heavy LLMs they use as a single coupled unit wastes massive computational resources. By maintaining a strictly independent model inference layer, the system can scale its components separately based on actual need. Millions of lightweight agents can scale dynamically with task workloads, while the heavy GPU models only need to scale with actual inference demand. This prevents the agents from becoming bloated and preserves the system’s economic and thermodynamic efficiency.

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

## Named Authority Surfaces
- `C45`
- `C42`
- `C47`
- `C36`
- `C18`
- `C22`
- `C39`
- `T-300`
