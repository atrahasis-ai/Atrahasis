# T-301 Communication Dependency Inventory

Legend:
- `Critical`: explicit old-stack authority or implementation dependency
- `High`: substantive cross-layer dependency that will need rewrite
- `Medium`: real dependency, but narrower or downstream
- `Low`: reference-only or packaging-level wording; usually defer to T-308/T-309

| Artifact | Category | Dependency surface | Severity | Retrofit owner(s) | Patch-order note |
|---|---|---|---|---|---|
| `docs/specifications/C4/MASTER_TECH_SPEC.md` | Baseline spec | Defines ASV as JSON Schema vocabulary embedded in A2A/MCP; narrows scope away from sovereign AACP | Critical | T-300, T-307, T-308 | Supersession boundary source |
| `docs/specifications/C4/architecture.md` | Baseline spec | C4 architecture still framed around ASV over existing transport | Critical | T-300, T-307, T-308 | Keep in boundary tranche with C4 master spec |
| `docs/specifications/C4/technical_spec.md` | Baseline spec | Technical design delegates transport to A2A/MCP and treats ASV as portable vocabulary only | Critical | T-300, T-307, T-308 | Same boundary decision as above |
| `docs/specifications/UNIFIED_ARCHITECTURE.md` | Packaging / architecture overview | Layer 1 is ASV; top-level flow still says claims are wrapped in ASV and embedded in A2A/MCP | Critical | T-300, T-302, T-305, T-308, T-309 | One of the most visible old-stack narratives |
| `docs/specifications/C22/MASTER_TECH_SPEC.md` | Roadmap / implementation | Builds Wave 1 around ASV schema packages, MCP/A2A adapters, and protocol-selection gates | Critical | T-304, T-305, T-309 | Main roadmap rewrite target |
| `docs/specifications/C9/MASTER_TECH_SPEC.md` | Cross-layer integration | Section 6 is explicit ASV integration mapping and ASV token -> PCVM intake | Critical | T-300, T-302 | Core stack retrofit anchor |
| `docs/specifications/C36/MASTER_TECH_SPEC.md` | Interface / DX | Explicit MCP/A2A bindings and ASV-native receptor surfaces | High | T-302, T-306, T-307 | Main interface retrofit target |
| `docs/specifications/C7/MASTER_TECH_SPEC.md` | Cross-layer integration | RIF delegates claim management/provenance to C4 ASV and records intent outcomes as C4 claims | High | T-302 | Rewrite after T-290 |
| `docs/specifications/C8/MASTER_TECH_SPEC.md` | Cross-layer integration / economics | DSF economic messages are ASV schemas; communication efficiency stream sourced from C4 | High | T-302, T-304 | Impacts both contracts and cost model |
| `docs/specifications/C5/MASTER_TECH_SPEC.md` | Verification | PCVM consumes ASV CLM/EVD/PRV and emits ASV VRF | High | T-302, T-303 | Trust-boundary sensitive |
| `docs/specifications/C3/MASTER_TECH_SPEC.md` | Coordination | Historical note says canonical communication vocabulary is C4 ASV; monitors A2A competitive window | High | T-302, T-308 | Mix of substantive and terminology work |
| `docs/specifications/C6/MASTER_TECH_SPEC.md` | Memory / projection | C4 projection path, ASV-based summaries, reconstruction from ASV projections | Medium | T-303 | Trust/provenance retrofit, not first-wave rewrite |
| `docs/specifications/C6/PATCH_ADDENDUM_v1.1.md` | Memory addendum | Reconstruction helper explicitly rebuilds canonical state from ASV token chain | Medium | T-303 | Keep with C6 provenance rewrite |
| `docs/specifications/C23/MASTER_TECH_SPEC.md` | Runtime | Normative reference still points at C4 as communication authority | Medium | T-302, T-305 | Likely narrower than C5/C7/C8 |
| `docs/specifications/C35/MASTER_TECH_SPEC.md` | Security / anomaly | Contracts state all message types use C4 ASV vocabulary | Medium | T-303 | Native-vs-bridge semantics will matter |
| `docs/specifications/C34/MASTER_TECH_SPEC.md` | Recovery | Recovery scope explicitly excludes C4 because it is treated as stateless vocabulary | Medium | T-303, T-307 | Recovery boundary needs restatement under new stack |
| `docs/specifications/C14/MASTER_TECH_SPEC.md` | Governance | Governance vocabulary and competence categories still keyed to C4/ASV | Medium | T-300, T-308 | Boundary first, wording cleanup later |
| `docs/specifications/C17/MASTER_TECH_SPEC.md` | Governance / security | Still references C4 as agent communication vocabulary | Low | T-300, T-308 | Likely a reference sweep after boundary work |
| `docs/specifications/C18/MASTER_TECH_SPEC.md` | Funding / packaging | Pitch deck still names six-layer stack with ASV at Layer 1 | Low | T-304, T-309 | Mostly narrative refresh, not architectural rewrite |
| `docs/specifications/C12/MASTER_TECH_SPEC.md` | Security | Layer diagram still names C4 ASV | Low | T-308 | Reference-only unless later work adds more |
| `docs/task_workspaces/T-063/specifications/MASTER_TECH_SPEC.md` | Canonical spec in task workspace | Layer diagram still includes C4 ASV | Low | T-308 | Diagram/reference cleanup only |
| `docs/task_workspaces/T-067/specifications/MASTER_TECH_SPEC.md` | Canonical spec in task workspace | Problem statement still lists ASV as communication vocabulary layer | Low | T-302, T-308 | Mostly intro wording, but canonical spec artifact |

## Non-Targets / Already Rebased

| Artifact | Status | Note |
|---|---|---|
| `docs/TODO.md` | Already rebased | Now explicitly encodes Alternative B, ADR-042 authority, and T-202 dependency-safe waves |
| `docs/SESSION_BRIEF.md` | Already rebased | Describes C4 as historical baseline and Alternative B as active |
| `docs/AGENT_STATE.md` | Already rebased | Notes C4 as historical baseline and retrofit reference |
| `docs/DECISIONS.md` | Historical by design | ADR-041 and ADR-042 intentionally preserve old-stack lineage while activating Alternative B |
| `docs/specifications/C24/MASTER_TECH_SPEC.md` | No explicit old-stack dependency detected | Future T-290/T-302 work is additive integration, not old-stack cleanup |
| `docs/specifications/C33/MASTER_TECH_SPEC.md` | No substantive old-stack dependency detected | Current live text only references C4 at a high level |

## Supporting Inputs

| Artifact | Use |
|---|---|
| `docs/task_workspaces/T-089/COMPARISON_ANALYSIS.md` | Migration and bridge-policy context |
| `docs/task_workspaces/T-201/POLICY_DRAFT.md` | Confirms T-201 governance is complete and unblocks T-210 independently of this audit |
