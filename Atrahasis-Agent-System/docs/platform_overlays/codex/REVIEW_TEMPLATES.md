# Review Templates
**Platform:** OpenAI Codex
**Purpose:** Preserve stage- and role-aware review scaffolds for AAS5 review work

---

## What Exists

Repo-local review templates live under:

```text
docs/platform_overlays/codex/review_templates/
```

Current templates:
- `assessment_council.md`
- `adversarial_analyst.md`
- `critic.md`
- `systems_thinker.md`
- `prior_art_researcher.md`
- `specification_writer.md`
- `code_implementer.md`

---

## Default Mapping

If the operator does not choose a review role explicitly, the controller resolves one from the current workflow stage:

- `IDEATION` -> `systems_thinker`
- `RESEARCH` -> `prior_art_researcher`
- `FEASIBILITY` -> `critic`
- `DESIGN` -> `systems_thinker`
- `SPECIFICATION` -> `specification_writer`
- `ASSESSMENT` -> `assessment_council`

Fallback role:
- `critic`

---

## Current Posture

The old controller-owned review-start commands were retired with the App Server runtime.

These templates are still kept in-repo because they remain useful for:
- direct provider-session reviews
- manual review drafting
- future controller review flows if AAS5 reintroduces a provider-neutral review launcher

Finalization commands still exist for controller records, but review startup is no longer performed by the controller CLI or operator UI.

---

## Why This Exists

These templates make review more consistent without moving review policy out of the repo.

They are intentionally simple:
- repo-local
- markdown-based
- human-readable
- easy to update alongside AAS5 policy

If stricter review control is needed later, the controller can evolve from markdown templates to structured review policies without changing the operator-facing command surface.
