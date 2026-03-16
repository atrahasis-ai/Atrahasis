# AAS Workflow Redesign

## Design Change

AAS0 is a stage-gate invention workflow with strong governance but weak internal invention intelligence. AAS1 keeps the human-guided gates and replaces the middle of the pipeline with explicit discovery, hypothesis, contradiction, and opportunity workflows controlled by one orchestration spine.

## Single Workflow Controller

`Invention Pipeline Manager` is the only module allowed to control execution order.

- it invokes the Command Modifier Router
- it invokes subsystem modules
- it decides when artifacts are persisted
- it pauses for human guidance
- it emits telemetry

Subsystems never invoke each other directly.

## Standard AAS1 Flow

1. Intake
   - `Invention Pipeline Manager` invokes Command Modifier Router
   - establishes task scope and HITL requirements
2. Context Load
   - `Invention Pipeline Manager` loads state, task workspace, portfolio memory, and relevant specs through the GCML memory interface
3. Discovery
   - `Invention Pipeline Manager` runs Research Ingestion, Research Quality Filter, Research Synthesis, Discovery Map, and Technology Frontier Model
4. Opportunity Framing
   - `Invention Pipeline Manager` runs Technology Opportunity Scanner and Discovery Gap Detector
5. Invention Reasoning
   - `Invention Pipeline Manager` runs Hypothesis Engine, Cross-Domain Analogy Engine, Idea Clustering Engine, and Contradiction Engine
6. Candidate Formation
   - `Invention Pipeline Manager` runs Solution Path Generator, Novelty Detection Engine, Feasibility Analysis Engine, and Experiment Simulation Engine
7. Governance
   - `Invention Pipeline Manager` builds decision packets for councils and the Human Decision Interface
8. Artifact Production
   - `Invention Pipeline Manager` emits updated task artifacts, invention artifacts, and implementation plans
9. Portfolio Learning
   - `Invention Pipeline Manager` writes patterns, decisions, and reusable opportunity knowledge back into memory

## Command Modifier Flows

### AASBT

- analyze the requested buildout task
- locate affected subsystems and artifacts
- determine whether current architecture supports implementation
- produce redesign deltas if required
- emit implementation task graph and artifact updates

### AASAQ

- read full architecture context
- synthesize the answer from the Discovery Map and current memory
- avoid new invention generation unless the question requires alternative designs

### AASNI

- map the new idea to existing hypotheses, contradictions, and opportunity zones
- detect subsystem redesign requirements
- produce an integration plan, not just commentary

### AASA

- recursively map the repository
- break work into subsystem analysis tasks
- generate chunked findings and improvement targets
- return strengths, weaknesses, and highest-leverage redesign areas

## Human Guidance Rules

- concept promotion remains human-approved
- pivots remain human-approved
- external research remains human-approved
- patent and disclosure decisions remain human-approved
- the Human Decision Interface must present concise evidence, contradictions, risks, and next actions

## Stage Model

- `INTAKE`
- `DISCOVERY`
- `HYPOTHESIS`
- `RESEARCH`
- `FEASIBILITY`
- `DESIGN`
- `SPECIFICATION`
- `ASSESSMENT`
- `PORTFOLIO_LEARNING`

This replaces the current ambiguous overlap between ideation, research, and design with a clearer invention-intelligence front half.

## Output Discipline

- every run produces a `COMMAND_REQUEST`
- every major reasoning pass produces structured machine-readable artifacts
- formal shared documents are updated only after synthesis and governance
- the Master Tech Spec remains the flagship deliverable, but it is now backed by a richer evidence graph
