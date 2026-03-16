# Codex Web Search Policy
**Platform:** OpenAI Codex
**Purpose:** Define when and how AAS5 may use live external search

---

## Default Posture

Live web search is **off by default** in AAS5.

Reason:
- repo-canonical evidence remains primary
- live search introduces prompt-injection and evidence-quality risk
- many AAS5 tasks do not need current internet evidence
- repo-local Codex config sets `web_search = "disabled"` unless the operator
  opts in for a session or a specific run

---

## When Search Is Appropriate

Use live search only for bounded research tasks such as:
- prior art scans
- standards and specification checks
- official product or library documentation
- current landscape evidence
- source verification where the repo lacks the needed external evidence

Default roles:
- `prior_art_researcher`
- `landscape_analyst`
- `science_advisor`

---

## When Search Is Not Appropriate

Do not use live search to:
- override repo-canonical doctrine or workflow authority
- satisfy a HITL approval gate
- browse broadly without a scoped research question
- pull in private repo context or secrets
- replace careful synthesis with source dumping

---

## How To Enable It

### Interactive Session

Start Codex with search enabled:

```powershell
pwsh -File scripts/start_aas5_codex.ps1 -Search
```

### Non-Interactive Schema Run

```bash
python scripts/run_aas5_schema_exec.py \
  --search \
  --schema docs/schemas/<schema>.json \
  --output <artifact> \
  --prompt-file <prompt.txt>
```

---

## Output Discipline

When search is used:
- cite the source URL for each material external claim
- distinguish source evidence from inference
- prefer official or primary sources
- record the reason the source matters to the Atrahasis task
- state uncertainty when evidence is mixed or incomplete

---

## Approval Discipline

Stop and ask the operator before using live search if the task is approval-
sensitive, including:
- doctrinal pivots
- patent strategy
- public disclosure posture
- research that the current task instructions explicitly mark as approval-gated

If approval is not required, keep search narrow and purpose-built.
