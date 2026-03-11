# Prototype Validator Guide (v1.0)

## Purpose
Convert assessments from "reasoning about designs" into "reasoning about executed evidence".

The Prototype Validator:
- runs the prototype's demonstration scripts and test harnesses
- captures raw command output
- reports results exactly (no interpretation beyond summarizing)

---

## Where the commands come from
The authoritative list of prototype validation commands lives in:
- `prototypes/<INVENTION_ID>/README.md` (per-prototype instructions)
- `docs/INVENTION_CONTEXT.md` under **Prototyping Conventions** (general standards)

If validation instructions are missing or unclear:
- Prototype Validator reports the gap
- Chronicler updates the relevant documentation once commands are confirmed

---

## Minimum required checks

For every prototype:
- Install dependencies (verify they resolve)
- Run the main demonstration script
- Run any included test suite
- Capture stdout, stderr, and exit codes

---

## Prototype Validator Output Format (JSON)

```json
{
  "type": "PROTOTYPE_VALIDATOR_REPORT",
  "invention_id": "C1",
  "commands": [
    {"cmd": "pip install -r requirements.txt", "exit_code": 0, "stdout": "...", "stderr": "..."},
    {"cmd": "python demo.py", "exit_code": 0, "stdout": "...", "stderr": "..."},
    {"cmd": "pytest -q", "exit_code": 0, "stdout": "...", "stderr": "..."}
  ],
  "overall": "PASS|FAIL",
  "core_claims_validated": [
    {"claim": "System achieves X", "validated": true, "evidence": "stdout shows..."}
  ],
  "notes": "short"
}
```

Rules:
- Always include exit codes.
- Include enough stdout/stderr to diagnose failures.
- Do not redact output unless it contains secrets (then redact only the secret).
- Map prototype results back to the invention's core claims when possible.
