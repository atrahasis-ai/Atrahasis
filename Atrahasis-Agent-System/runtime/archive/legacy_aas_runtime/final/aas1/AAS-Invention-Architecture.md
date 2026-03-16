# AAS Invention Architecture

- Redesign target: `AAS0` at `C:\Users\jever\Atrahasis\Atrahasis-Agent-System`
- Reference AAS-RE CSSM: `AAS-State-v1.105`
- Resulting system: `AAS1`

## Baseline Preserved from AAS0

- Human-guided direction and approval gates remain mandatory.
- Stage-gate discipline remains, but the pipeline becomes invention-intelligence-first rather than document-first.
- Durable repo-canonical memory remains under `docs/`.
- Councils, adversarial review, and synthesis ownership remain.

## Orchestration Authority

`Invention Pipeline Manager` is the single execution controller for AAS1.

Responsibilities:

- own the full invention workflow pipeline
- activate the correct command flow for `AASBT`, `AASAQ`, `AASNI`, and `AASA`
- schedule subsystem execution order
- mediate all subsystem communication
- enforce HITL pauses, governance gates, and telemetry emission

The following modules are explicitly not controllers:

- Hypothesis Engine
- Exploration Control Engine
- Command Modifier Router
- Technology Opportunity Scanner
- Discovery Map

They are subsystems invoked by the `Invention Pipeline Manager`.

## AAS1 Architecture Stack

1. Invention Pipeline Manager
   - single orchestration authority
2. Command Modifier Router
   - parses `AASBT`, `AASAQ`, `AASNI`, and `AASA` and returns a normalized command request
3. GCML Memory Interface
   - loads and persists canonical repo memory and structured runtime artifacts
4. Discovery Intelligence Plane
   - maintains the Discovery Map, Technology Frontier Model, research clusters, and opportunity zones
5. Invention Reasoning Plane
   - generates hypotheses, contradictions, solution paths, novelty signals, feasibility judgments, and simulation plans
6. Governance and Human Guidance Plane
   - councils, Human Decision Interface, Exploration Control Engine, and stage-gate approvals
7. Artifact and Telemetry Plane
   - task workspaces, invention logs, reports, schemas, validators, and telemetry events

## Communication Rule

All subsystem interactions must pass through the `Invention Pipeline Manager`.

- subsystems do not call each other directly
- subsystems emit outputs into structured artifacts or in-memory result envelopes
- the `Invention Pipeline Manager` decides what module runs next

## Module Integration

- Command Modifier Router
  - normalizes command intent; does not run the pipeline
- Research Ingestion Engine
  - ingests repo materials, task artifacts, prior art, and new research inputs into a normalized evidence store
- Research Synthesis Engine
  - converts raw evidence into structured synthesis packets for downstream reasoning modules
- Research Quality Filter
  - scores evidence quality, duplication, citation depth, and uncertainty before evidence enters the Discovery Map
- Discovery Map
  - graph of domains, problems, analogies, contradictions, solutions, and inventions; updated only through the orchestration layer
- Technology Frontier Model
  - estimates frontier movement by domain, capability gap, and maturity trajectory
- Technology Opportunity Scanner
  - reads the Discovery Map, Technology Frontier Model, and research clusters to emit high-value opportunity zones; does not initiate exploration
- Hypothesis Engine
  - generates invention hypotheses prioritized by opportunity zones and explicit user goals; does not choose downstream actions
- Contradiction Engine
  - extracts unresolved tensions, blockers, and mutually incompatible assumptions from research and hypotheses
- Solution Path Generator
  - turns validated hypotheses plus contradictions into candidate architectures and staged execution paths
- Novelty Detection Engine
  - compares candidates against prior art, internal portfolio memory, and adjacent solution clusters
- Feasibility Analysis Engine
  - evaluates scientific, implementation, operational, and adoption feasibility
- Experiment Simulation Engine
  - runs lightweight design-of-experiment and architecture simulation plans before specification commitment
- Discovery Gap Detector
  - finds missing evidence, thinly researched zones, and unresolved unknowns
- Cross-Domain Analogy Engine
  - formalizes the current Domain Translator role into reusable analogy generation and scoring
- Idea Clustering Engine
  - groups related hypotheses, solution paths, and invention branches into portfolio-level themes
- Human Decision Interface
  - presents concise decision packets for concept selection, pivots, external research, and commitment decisions
- Exploration Control Engine
  - proposes exploration budgets, branch policies, and prioritization options to the orchestration layer; it does not control execution

## Command Modifier Integration

- `AASBT` enters through the Command Modifier Router, then the `Invention Pipeline Manager` activates subsystem impact analysis and emits implementation tasks plus redesign deltas.
- `AASAQ` enters through the Command Modifier Router, then the `Invention Pipeline Manager` activates architecture reading and synthesis flows without default invention generation.
- `AASNI` enters through the Command Modifier Router, then the `Invention Pipeline Manager` activates idea impact analysis, contradiction detection, opportunity matching, and integration planning.
- `AASA` enters through the Command Modifier Router, then the `Invention Pipeline Manager` activates repository-wide mapping, chunked subsystem analysis, weakness detection, and improvement recommendations.

## Repository Mapping

- Keep `docs/AGENT_STATE.md`, `docs/SESSION_BRIEF.md`, `docs/INVENTION_DASHBOARD.md`, `docs/DECISIONS.md`, and `docs/PATTERN_REGISTER.md` as the durable human-readable memory layer.
- Keep `docs/task_workspaces/` as the parent container for task-scoped work.
- Keep `docs/prior_art/` and `docs/specifications/` as canonical output surfaces.
- Add machine-readable invention-intelligence artifacts under task workspaces and invention folders instead of replacing the current docs.
- Add a real runtime package for invention orchestration rather than relying only on prompt prose and validators.

## Architectural Decision

- No required module is excluded.
- The major AAS1 shift is not more councils; it is a persistent invention-intelligence core governed by one orchestration spine.
