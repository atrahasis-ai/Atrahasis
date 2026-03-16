# T-211 Workspace Note

Purpose: define the Alternative B message-layer expansion from the normalized 23-class AACP baseline to a canonical 42-class inventory under C38.

Primary source documents:
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replacement_Strategy.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_Council_Briefing.md`
- `C:\Users\jever\Atrahasis\AACP-AASL\AACP_AASL_Full_Replace_AAS_Tasks.md`
- `docs/specifications/C38/MASTER_TECH_SPEC.md`

Upstream authorities:
- ADR-041, ADR-042, ADR-043
- C38 Five-Layer Sovereign Protocol Architecture (FSPA)

Boundary conditions:
- This task is L4 Messaging work under C38 and MUST NOT silently redesign L1 transport, L2 session, L3 security, or L5 semantics.
- `TL{}`, `PMT{}`, and `SES{}` are referenced as semantic payload contracts but their internal field definitions remain downstream work for `T-212`.
- Agent Manifest payload semantics remain downstream work for `T-214`.
- Streaming/push delivery details remain downstream work for `T-243`, but this task defines the message-class inventory they refine.

Expected outputs:
- full AAS pipeline artifacts for `T-211`
- canonical message-family model and 19 new message classes
- normalized 23-class legacy baseline plus resulting 42-class canonical inventory
- header extensions, payload contract bundles, lineage rules, and messaging-layer requirements for downstream tasks
