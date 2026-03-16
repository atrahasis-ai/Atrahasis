# T-240 Workspace Note

Purpose: define the `AACP Tool Connectivity Protocol` for Alternative B as the
canonical native replacement for `MCP`-style tool discovery, invocation, result
handling, and tool-catalog change signaling.

Execution state:
- Task is claimed by `Marduk`.
- Current stage is `ASSESSMENT` complete.
- User approval is recorded in `docs/task_workspaces/T-240/HITL_APPROVAL.md`.
- `IC-9` is promoted as `C42` - `Lease-Primed Execution Mesh (LPEM)`.
- Full pipeline artifacts are complete in the task workspace and `C42` safe zone.
- Shared-state closeout edits remain deferred to the handoff.

Primary authorities:
- `docs/TODO.md` task entry for `T-240`
- `docs/DECISIONS.md` (`ADR-041` and `ADR-042`)
- `docs/specifications/C39/MASTER_TECH_SPEC.md`
- `docs/specifications/C40/MASTER_TECH_SPEC.md`
- `docs/specifications/C41/MASTER_TECH_SPEC.md`
- `docs/task_workspaces/T-212/TYPE_EXTENSION_SPEC.md`
- `docs/specifications/C23/MASTER_TECH_SPEC.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replacement_Strategy.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_Council_Briefing.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_AAS_Tasks.md`

Workspace outputs:
- `PRE_IDEATION_KNOWN_SOLUTIONS.md`
- `PRE_IDEATION_DOMAIN_TRANSLATOR_BRIEF.md`
- `IDEATION_COUNCIL_OUTPUT.yaml`
- `IDEATION_COUNCIL_COMPARISON_IC2_VS_IC3.md`
- `IDEATION_COUNCIL_HYBRID_FOLLOWUP.yaml`
- `IDEATION_COUNCIL_PERFORMANCE_PRIORITIZED_FOLLOWUP.yaml`
- `HITL_APPROVAL.md`
- `CONCEPT_MAPPING.md`
- `PRIOR_ART_REPORT.md`
- `LANDSCAPE_REPORT.md`
- `SCIENCE_ASSESSMENT.md`
- `FEASIBILITY.md`
- `ASSESSMENT.md`
- `PROPOSED_TOOL_SUITE_MODULE_AND_TASK.md`
- `specifications/architecture.md`
- `specifications/pre_mortem.md`
- `specifications/simplification.md`

Task focus:
- Define the native tool lifecycle around `tool_discovery`, `tool_invocation`,
  `tool_result`, and `tool_change_notification`.
- Respect upstream boundaries already fixed by `C39`, `T-212`, `C40`, and `C41`
  rather than redesigning message classes, `TL{}` fields, or manifest structure.
- Produce concept options that can support downstream `T-250`, `T-260`,
  `T-262`, and `T-290` without assuming transport, streaming, or runtime details
  that belong to other tasks.
