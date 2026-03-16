# Codex Team Formation Policy
**Platform:** OpenAI Codex
**Purpose:** Make AAS delegation explicit, repeatable, and compatible with the
shared Atrahasis operating model
**Shared boundary:** `docs/platform_overlays/SHARED_OPERATING_MODEL.md`,
`docs/platform_overlays/PARALLEL_EXECUTION_PROTOCOL.md`

---

## Core Model

Codex runs AAS with one accountable parent session and zero or more bounded
child sessions.

Rules:
- the parent session is the Swarm Director
- the parent session owns task interpretation, HITL gates, and final output
- child sessions exist to perform narrow delegated work, not to become
  independent authorities
- when a task is marked real-swarm-required by policy, the runtime must form
  real child sessions or stop and report the blocker
- internal viewpoint simulation is allowed only for solo-eligible tasks and
  must not be labeled as swarm output

---

## Runtime Role Mapping

The AAS prompt names a reasoning swarm, while the runtime registry uses a
broader operational role catalog.

- `Lead Architect`
  Use as the parent session's baseline-planning viewpoint. If a separate child
  is required, map it to `architecture_designer`.
- `Visionary`
  Map to `visionary`.
- `Systems Thinker`
  Map to `systems_thinker`.
- `Critic`
  Map to `critic`.
- `Memory Reuse Analyst`
  Map to `memory_reuse_analyst`. This is an advisory-only role that surfaces reusable fragments, prior failure conditions, and hybrid opportunities from persisted redesign history.
- `Assessment Council`
  Use `assessment_council` for a composite review child. Do not default to
  three separate tribunal children unless the task explicitly needs that
  overhead.

Reference role catalog: `src/aas5/provider_runtime.py`

---

## Team Modes

### 1. Solo
Use no real children when:
- the task is small enough to stay coherent in one session
- the work is mostly linear
- the cost of coordination would exceed the value of fan-out
- the task is not a real-swarm-required `FULL PIPELINE / IDEATION` case

### 2. Core Swarm
Use the minimum serious AAS team for design, analysis, and governance work:
- parent: Swarm Director / Lead Architect viewpoint
- children as needed: `visionary`, `systems_thinker`, `critic`

### 3. Stage Team
Use stage-specific specialists for `FULL PIPELINE` work:
- add only the roles needed for the current stage
- keep fan-out narrow and evidence-focused

### 4. Execution Cell
Use code or tooling specialists for implementation-heavy tasks:
- `code_implementer`
- `schema_validator`
- `tooling_agent`
- `refactor_agent`
- `automation_agent`

### 5. Future Branch Swarm
Use this for architecture-heavy work where the parent must compare multiple
competing futures before converging. For ordinary `FULL PIPELINE / IDEATION`,
this is now the default swarm rather than an optional escalation:
- keep one accountable parent
- use four bounded lane managers under the parent: `Alpha`, `Beta`, `Gamma`, `Radical`
- each lane manager owns exactly three leaf branch agents: `visionary`, `systems_thinker`, `critic`
- add four real lane convergence reporters, one per lane
- add four real independent auditors: swarm compliance, runtime audit,
  authority coverage, adversarial integrity
- do not let every child recurse freely beyond that bounded lane-manager layer
- select only the roles that benefit from parallel futures
- require explicit parent convergence after the branch runs complete

Default typed futures:
- `visionary`: `conservative`, `aggressive`, `radical`
- `systems_thinker`: `minimal_change`, `modular`, `full_restructure`
- `critic`: `failure`, `abuse`, `governance_break`
- optional advisory companion: `memory_reuse_analyst`

Task-improvement lane mapping:
- `Alpha`: `conservative`, `minimal_change`, `failure`
- `Beta`: `aggressive`, `modular`, `abuse`
- `Gamma`: `radical`, `full_restructure`, `governance_break`
- `Radical`: `frame_replacement`, `authority_reset`, `foundational_invalidity`

When this swarm is used on a live task, these are bounded future-improvement
lanes, not a detached redesign exercise. The parent must use them
to discover whether the current task path should be rejected, adopted,
hybridized, or escalated to HITL.

This is a bounded hierarchy, not an open-ended swarm. The default depth is:
- one parent orchestrator
- one lane-manager layer
- one leaf branch-agent layer

Advisory memory reuse:
- spawn `memory_reuse_analyst` only when persisted redesign history exists and the current stage has real structural design pressure
- the role is read-only and advisory-only
- its output must be treated as considerations for the parent and other bounded children, not as a forced inheritance rule

### Radical Redesign Lane
Use the radical lane only when the parent needs at least one branch that can
reject current architectural assumptions rather than merely optimize them.

Rules:
- radical branches are still bounded children under the same accountable parent
- radical branches may challenge topology, authority boundaries, and core
  primitives
- radical branches may not bypass HITL, doctrine, or shared-state closeout
- when enabled, the parent must write `RADICAL_REDESIGN_REPORT.json` and choose
  one of `reject`, `hybridize`, or `promote`

Default radical-capable branches:
- `visionary:radical`
- `systems_thinker:full_restructure`
- `critic:governance_break`

---

## Recommended Team By Task Class

### Analysis

Default:
- parent baseline
- `systems_thinker`
- `critic`

Add `visionary` only when the operator wants a better alternative, not just a
straight answer.

### Governance

Default:
- parent baseline
- `systems_thinker`
- `critic`

Optional:
- `visionary` for stronger institutional design
- `operator_proxy` when the task is explicitly about approval surfaces or human
  control flow
- `chronicler` when the main output is a durable summary or policy closeout

### DIRECT SPEC

Default:
- parent baseline
- `systems_thinker`
- `critic`

Add when needed:
- `architecture_designer` for broad structural edits
- `specification_writer` for formal prose or requirement shaping
- `science_advisor` when soundness or empirical claims matter

### FULL PIPELINE

#### IDEATION

Default:
- parent baseline
- `FUTURE_BRANCH_SWARM` with four real lane managers:
  `Alpha Manager`, `Beta Manager`, `Gamma Manager`, `Radical Manager`
- each lane manager then owns three real leaf branch agents:
  `visionary`, `systems_thinker`, `critic`
- add four real lane convergence reporters:
  `Alpha Reporter`, `Beta Reporter`, `Gamma Reporter`, `Radical Reporter`
- add four real independent auditors:
  `Swarm Compliance Auditor`, `Runtime Audit Recorder`,
  `Authority Coverage Auditor`, `Adversarial Integrity Reviewer`

Add when needed:
- `domain_translator` for cross-domain synthesis or analogy pressure
- `memory_reuse_analyst` when persisted redesign history is materially relevant

Stop after ideation if a HITL gate applies. Do not advance concept promotion in
child sessions.

Real-swarm rule:
- for architecture-heavy subsystem or new-authority ideation, a real bounded
  child swarm is mandatory
- do not emit an "AAS Swarm Readout" from one parent session pretending the
  role viewpoints were separate agents
- if real child sessions are unavailable, stop and report `swarm_unavailable`
  instead of silently collapsing to solo ideation

Future Branch Swarm:
- this is the ordinary default for `FULL PIPELINE / IDEATION`, not only an optional escalation
- do not downgrade ordinary ideation to a smaller 3-role stage team unless the operator explicitly authorizes non-ABGR solo analysis
- do not collapse reporters or auditors into managers or the parent and still
  call the run compliant ordinary ideation

#### RESEARCH

Default:
- `prior_art_researcher`
- `landscape_analyst`
- `science_advisor`

Add when needed:
- `domain_translator` if framing or transfer analogies matter
- `research_synthesizer` if large evidence bundles must be compressed before the
  parent decides

#### FEASIBILITY

Default:
- `science_advisor`
- `adversarial_analyst`
- `critic`

Add when needed:
- `pre_mortem_analyst` for failure-mode forecasting
- `commercial_viability_assessor` for timing, market, or commercialization
  pressure

Controller gate:
- `FULL_PIPELINE / FEASIBILITY` requires a separate adversarial review record before the stage can close.
- Smaller task classes do not inherit this gate automatically; the workflow policy only turns it on when the risk profile justifies it.

#### DESIGN AND SPECIFICATION

Default:
- `architecture_designer`
- `specification_writer`

Add when needed:
- `systems_thinker` for cross-spec integration
- `critic` for final stress testing
- `code_implementer` or `schema_validator` if the design includes executable or
  schema-backed artifacts

Future Branch Swarm:
- preferred when the parent needs to compare competing design topologies before
  converging on one architecture

#### ASSESSMENT

Default:
- `assessment_council`

Optional:
- `critic` and `science_advisor` as independent supporting reviews when the
  assessment has unusual technical or empirical risk

### Code And Tooling

Default:
- parent baseline
- `code_implementer`
- `schema_validator`

Add when needed:
- `tooling_agent` for scripts, automation, or CLI surfaces
- `refactor_agent` for structural cleanup
- `automation_agent` for repeatable workflow wiring
- `fast_background` only for low-risk search, indexing, or bulk read-only scans

---

## Spawn Rules

### Real Swarm Required Cases

A real child swarm is required when any of these are true:
- the task is architecture-heavy `FULL PIPELINE / IDEATION`
- the operator uses the strict textual modifier `Full Pipeline Task:`
- the operator explicitly asks for agent findings, swarm findings, or multiple
  agent opinions before choosing a path
- the parent is evaluating whether a proposed subsystem is already absorbed by
  existing authority or needs a new canonical authority surface
- the parent is invoking `Future Branch Swarm` or bounded future-improvement
  ideation as an actual comparative swarm, not as a solo analysis

### When To Spawn

Spawn a real child only if at least one of these is true:
- the task can be parallelized cleanly
- a specialist perspective needs an independent evidence pass
- the delegated objective can be stated in one bounded paragraph
- the child result can be merged deterministically by the parent

### When Not To Spawn

Do not spawn a real child for:
- trivial lookups
- decisions that require direct user approval
- tasks that would create overlapping write surfaces without a clear safe zone
- work where the parent would need to rewrite the child's whole output anyway
- cases where policy already marks the work as real-swarm-required are not
  exempted by convenience; they must either spawn or stop

### Fan-Out Limits

Default maximums:
- `Solo`: 0 children
- `Core Swarm`: 2-3 children
- `Stage Team`: 3 children for ordinary stages, 4 only when the task surface is
  broad and parallel-safe
- `Execution Cell`: 2 writer-capable children max
- `Future Branch Swarm`: for ordinary AAS5 ideation, `24` non-parent
  participants max (`4` managers, `12` workers, `4` reporters, `4` auditors)
  with ideal simultaneous target `25` including the parent; batching is
  degraded rather than equivalent

Never run more than one writer-capable child against the same shared write
surface at the same time.

Do not let child sessions spawn deeper swarms by default. A future-branch swarm
is a parent-owned planning structure with one bounded manager layer plus one
bounded leaf-agent layer, not permission for open-ended recursive fan-out.

---

## Permission And Ownership Rules

Default child mode is read-only.

Children may write only if all of the following are true:
- the parent has assigned an explicit safe zone
- the write is compatible with claim-file rules
- the child does not cross a HITL or doctrine boundary
- the parent remains the final merger and closeout authority

Children must not:
- approve concept promotion
- mint `C-xxx` invention IDs
- update `docs/AGENT_STATE.md`, `docs/TODO.md`, `docs/DECISIONS.md`,
  `docs/INVENTION_DASHBOARD.md`, `docs/TRIBUNAL_LOG.md`, or
  `docs/platform_overlays/AGENT_REGISTRY.md` on their own
- perform sequential closeout during parallel execution

Synthesis-owned shared artifacts remain owned by the Synthesis Engineer per
`docs/INVENTION_CONTEXT.md`. Specialist children should route proposed changes
through contribution requests unless the parent is intentionally operating in
synthesis mode.

---

## Tracking Artifacts

Before spawning more than one child, or any child with write permission, the
parent should create a task-local team plan:
- `docs/task_workspaces/T-<ID>/TEAM_PLAN.yaml`

Use:
- `docs/platform_overlays/codex/templates/TEAM_PLAN_TEMPLATE.yaml`

Each child should return a compact result artifact or an equivalent structured
summary. Suggested template:
- `docs/platform_overlays/codex/templates/CHILD_RESULT_TEMPLATE.json`

When the team mode is `FUTURE_BRANCH_SWARM`, also write:
- `docs/task_workspaces/T-<ID>/FUTURE_BRANCH_REPORT.json`
- `docs/task_workspaces/T-<ID>/FUTURE_CONVERGENCE_REPORT.json`
- `docs/task_workspaces/T-<ID>/SWARM_TOPOLOGY_GRAPH.json`
- `docs/task_workspaces/T-<ID>/EXECUTION_PARALLELISM_RECORD.json`
- `docs/task_workspaces/T-<ID>/LANE_PLAN_<lane>.yaml`
- `docs/task_workspaces/T-<ID>/LANE_CONVERGENCE_REPORT_<lane>.json`
- `docs/task_workspaces/T-<ID>/SWARM_COMPLIANCE_AUDIT.json`
- `docs/task_workspaces/T-<ID>/RUNTIME_AUDIT_RECORD.json`
- `docs/task_workspaces/T-<ID>/AUTHORITY_COVERAGE_AUDIT.json`
- `docs/task_workspaces/T-<ID>/ADVERSARIAL_INTEGRITY_REVIEW.json`
- `docs/task_workspaces/T-<ID>/TASK_IMPROVEMENT_REPORT.json` when the
  improvement trigger policy is enabled
- `docs/task_workspaces/T-<ID>/RADICAL_REDESIGN_REPORT.json` when the radical
  trigger policy is enabled

When a real swarm is required, also write:
- `docs/task_workspaces/T-<ID>/SWARM_EXECUTION_RECORD.json`

Operator entry point:
- `python scripts/dispatch_aas_team.py <TASK_ID> --spawn-id <spawn_id> --execute`

Minimum fields to track:
- child role
- objective
- permission level
- assigned safe zone
- expected artifact
- status
- merge owner

---

## Merge Discipline

The parent must:
- wait for child completion before emitting the final merged answer
- reconcile disagreements explicitly rather than averaging them away
- preserve the strongest cited evidence from each child
- state exactly which roles were run as real children and which artifacts they
  produced
- if the task was real-swarm-required, treat internal role simulation as a
  contract failure rather than an acceptable fallback

For `FUTURE_BRANCH_SWARM`, the parent must also:
- compare the typed futures explicitly rather than collapsing them into one
  blended answer
- produce a convergence decision that names which future is chosen, rejected, or
  deferred
- when the improvement lane is active, explicitly decide whether the strongest
  discovered improvement should be `reject`ed, `adopt`ed, `hybridize`d, or
  `escalate_to_hitl`
- when the radical redesign lane is active, explicitly decide whether the
  radical path is rejected, hybridized into the main design, or promoted for
  HITL review
- stop for HITL if concept promotion or a major pivot depends on the
  convergence result

If child outputs conflict and the conflict affects a gate, the parent should
either:
- ask the user for direction, or
- spawn one additional bounded adjudication child such as `critic`,
  `science_advisor`, or `assessment_council`

---

## Practical Default

If there is no better reason to do otherwise, use this default:
- keep one parent controller
- spawn 2-3 children for the current stage
- make them read-only
- merge in the parent
- reserve shared-state writes and HITL interactions for the parent

For `FULL PIPELINE / IDEATION`, the default is stricter:
- parent baseline
- four real lane managers under the parent
- each lane manager owns real `visionary`, `systems_thinker`, and `critic`
  leaf agents for its lane
- four real lane convergence reporters under the parent
- four real independent auditors under the parent
- `SWARM_EXECUTION_RECORD.json` before the stage is considered complete
