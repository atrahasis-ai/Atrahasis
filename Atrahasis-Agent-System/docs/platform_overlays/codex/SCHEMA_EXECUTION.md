# Schema-Driven Codex Execution
**Platform:** OpenAI Codex
**Purpose:** Standardize machine-consumed AAS5 runs that require deterministic
JSON output plus event capture

---

## Why This Exists

Use schema-driven execution when the result is meant to feed:
- task workspace artifacts
- dispatch recommendations
- child-result records
- research packets
- assessment summaries
- other automation that should not parse free-form prose

The standard pattern is:
- constrain the final answer with `--output-schema`
- capture the full event stream with `--json`
- save both outputs on canonical repo surfaces

---

## Standard Wrapper

Preferred entry point:

```bash
python scripts/run_aas5_schema_exec.py \
  --schema docs/schemas/<schema>.json \
  --output docs/task_workspaces/T-<ID>/<ARTIFACT>.json \
  --prompt-file <prompt.txt>
```

This wrapper:
- runs `codex exec`
- applies `--output-schema`
- captures the Codex JSONL event stream
- writes stderr to a sidecar log
- keeps all artifacts on repo-canonical paths

---

## Interactive Use

Use interactive Codex when the operator needs to collaborate directly. Use the
schema wrapper when the output must be machine-consumable or replayable.

The interactive launcher is:

```powershell
pwsh -File scripts/start_aas5_codex.ps1
```

---

## Common Cases

### Dispatch Recommendations

```bash
python scripts/run_aas5_schema_exec.py \
  --schema docs/schemas/team_dispatch_recommendations.schema.json \
  --output docs/task_workspaces/T-9002/TEAM_DISPATCH_RECOMMENDATIONS.json \
  --prompt-file runtime/prompts/t9002_dispatch.txt
```

### Child Results

Prefer the built-in dispatcher path:
- `python scripts/dispatch_aas_team.py <TASK_ID> --spawn-id <spawn_id> --execute`

The dispatcher already uses the child-result schema and captures the child
session event stream.

### Research Packets With Live Search

```bash
python scripts/run_aas5_schema_exec.py \
  --search \
  --schema docs/schemas/prior_art_report.schema.json \
  --output docs/task_workspaces/T-9002/PRIOR_ART_REPORT.json \
  --prompt-file runtime/prompts/t9002_prior_art.txt
```

---

## Guardrails

- Use repo-relative schema and output paths whenever possible.
- Do not claim schema success unless the run completed successfully.
- Use live search only when the task actually needs external current evidence.
- Follow `docs/platform_overlays/codex/WEB_SEARCH.md` before enabling search.
