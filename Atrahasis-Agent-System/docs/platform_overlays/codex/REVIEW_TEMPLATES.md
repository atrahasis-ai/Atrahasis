# Review Templates
**Platform:** OpenAI Codex
**Purpose:** Provide stage- and role-aware review scaffolds for controller-managed review gates

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

## How To Use

### Automatic

```bash
python scripts/aas_controller.py start-review T-9002
```

The controller chooses a template from the current workflow stage.

### Explicit Role

```bash
python scripts/aas_controller.py start-review T-9002 --review-role critic
```

The controller records the selected template role and template path into the review gate record notes so the review surface stays auditable.

### Conditional Adversarial Review

```bash
python scripts/aas_controller.py start-adversarial-review T-9002
python scripts/aas_controller.py finalize-adversarial-review T-9002 REVIEW_APPROVED "Adversarial concerns addressed."
```

This is a separate gate from the ordinary review record. AAS5 only requires it when the workflow policy marks the current stage as high-risk enough to need explicit adversarial pressure.

---

## Why This Exists

These templates make review more consistent without moving review policy out of the repo.

They are intentionally simple:
- repo-local
- markdown-based
- human-readable
- easy to update alongside AAS5 policy

If stricter review control is needed later, the controller can evolve from markdown templates to structured review policies without changing the operator-facing command surface.
