# T-250 Workspace Note

Purpose: define the `MCP-to-AACP Universal Bridge` for Alternative B as the
canonical migration bridge from `MCP` servers into `AACP` endpoints with
automatic semantic enrichment and explicit native-versus-bridge provenance
markers.

Execution state:
- Task is claimed by `Nergal`.
- Current stage is `ASSESSMENT` complete in task-local state.
- User approval is recorded in `docs/task_workspaces/T-250/HITL_APPROVAL.md`.
- `IC-4` is promoted as `C43` - `Custody-Bounded Semantic Bridge (CBSB)`.
- Full pipeline artifacts are complete in the task workspace and `C43` safe zone.
- Shared-state closeout edits remain deferred to the handoff.

Primary authorities:
- `docs/TODO.md` task entry for `T-250`
- `docs/DECISIONS.md` (`ADR-041` through `ADR-048`)
- `docs/specifications/C39/MASTER_TECH_SPEC.md`
- `docs/specifications/C40/MASTER_TECH_SPEC.md`
- `docs/specifications/C41/MASTER_TECH_SPEC.md`
- `docs/specifications/C42/MASTER_TECH_SPEC.md`
- `docs/task_workspaces/T-301/COMM_DEPENDENCY_AUDIT.md`
- `C:\\Users\\jever\\Atrahasis\\AACP-AASL\\AACP_AASL_Full_Replacement_Strategy.md`
- `C:\\Users\\jever\\Atrahasis\\AACP-AASL\\AACP_AASL_Full_Replace_Council_Briefing.md`
- `C:\\Users\\jever\\Atrahasis\\AACP-AASL\\AACP_AASL_Full_Replace_AAS_Tasks.md`

Workspace outputs created in this stage:
- `PRE_IDEATION_KNOWN_SOLUTIONS.md`
- `PRE_IDEATION_DOMAIN_TRANSLATOR_BRIEF.md`
- `IDEATION_COUNCIL_OUTPUT.yaml`
- `IDEATION_COUNCIL_COMPARISON_IC2_VS_IC3.md`
- `IDEATION_COUNCIL_HYBRID_FOLLOWUP.yaml`
- `HITL_APPROVAL.md`
- `CONCEPT_MAPPING.md`
- `PRIOR_ART_REPORT.md`
- `LANDSCAPE_REPORT.md`
- `SCIENCE_ASSESSMENT.md`
- `FEASIBILITY.md`
- `ASSESSMENT.md`
- `specifications/architecture.md`
- `specifications/pre_mortem.md`
- `specifications/simplification.md`

Task focus:
- Design a generic bridge that can wrap conforming `MCP` servers without
  per-server bespoke translation logic.
- Preserve the Alternative B authority boundary: the bridge is migration
  scaffolding, not the intended end-state architecture.
- Keep bridged tool inventory, invocation, result, and continuation posture
  visibly distinct from native `C42` behavior.
- Make semantic enrichment explicit and auditable instead of implying that raw
  `MCP` results are native `AACP/AASL` outputs.

Next gate:
- Shared-state closeout only. Do not edit shared-state files until user
  requests it.
