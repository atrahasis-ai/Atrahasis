# Synthesis Playbook (v1.0)
**Owner:** Synthesis Engineer (execution), Chronicler (documentation)

---

## Goal

Guarantee that:

- shared invention artifacts are edited **exactly once** per synthesis pass
- contributions are applied deterministically
- consistency checks are executed on the integrated result

---

## Golden Rules

1. Specialists never edit Synthesis-Owned shared artifacts.
2. Synthesis Engineer is the only role that edits shared artifacts.
3. Contributions are applied in a single controlled pass per invention.
4. Consistency checks must pass before the synthesis is considered complete.

---

## Standard Synthesis Workflow

1. **Collect inputs**
   - Identify contribution requests ready for synthesis.
   - Confirm each specialist has completed their invention log.

2. **Validate contribution requests**
   ```bash
   python scripts/validate_contribution_requests.py docs/contribution_requests
   ```

3. **Review for conflicts**
   - Check if multiple contributions target the same artifact section.
   - Resolve conflicts by consulting the relevant specialists or escalating to Director.

4. **Apply contributions**
   - Apply in deterministic order (sorted by `target_artifact`, then request `id`).
   - Keep edits minimal and mechanical (no new invention content).

5. **Run consistency checks**
   - Architecture matches specification descriptions
   - Claims are supported by the technical specification
   - Prototype validates the core claims
   - Prior art differentiators are reflected in claims
   - No contradictions between architecture, spec, and prototype

6. **Produce SYNTHESIS_RESULT**
   ```json
   {
     "type": "SYNTHESIS_RESULT",
     "invention_id": "C1",
     "contributions_applied": ["docs/contribution_requests/C1.yaml"],
     "shared_artifacts_modified": ["docs/specifications/C1/claims.md"],
     "conflicts_resolved": [],
     "consistency_checks": [
       {"check": "architecture matches spec", "result": "PASS"}
     ],
     "notes": "..."
   }
   ```

7. **Record state**
   - Synthesis result is reflected in:
     - `docs/AGENT_STATE.md`
     - `docs/INVENTION_DASHBOARD.md`

---

## Contribution Request Actions (supported)

### `add_claim`
Adds a patent-style claim to the claims document.

**data fields:**
- `claim_number`
- `claim_text`
- `dependent_on` (list of claim numbers, empty for independent claims)

### `update_claim`
Modifies an existing claim.

**data fields:**
- `claim_number`
- `claim_text`
- `rationale_for_change`

### `update_architecture`
Updates a section of the architecture document.

**data fields:**
- `section`
- `content`

### `add_prior_art_reference`
Adds a reference to the prior art report.

**data fields:**
- `reference_type` (patent | paper | product | open_source)
- `reference_id`
- `title`
- `relevance`
- `summary`

### `update_spec_section`
Updates a section of the technical specification.

**data fields:**
- `section`
- `content`

### `add_figure`
Adds a figure description to the figures directory.

**data fields:**
- `figure_number`
- `title`
- `description`

### `add_prototype_component`
Adds a component to the shared prototype.

**data fields:**
- `component_name`
- `file_path`
- `description`

### `update_landscape`
Updates the technology landscape analysis.

**data fields:**
- `section`
- `content`

### `add_embodiment`
Adds an embodiment description to the specification.

**data fields:**
- `embodiment_number`
- `title`
- `description`

### `update_abstract`
Updates the invention abstract.

**data fields:**
- `abstract_text`
