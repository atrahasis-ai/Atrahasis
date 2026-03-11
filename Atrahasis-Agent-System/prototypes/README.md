# Prototypes

One directory per invention: `<INVENTION_ID>/`

Each prototype directory should contain:
- `README.md` — what the prototype demonstrates, how to run it
- `requirements.txt` (or equivalent dependency file)
- Entry point script (e.g., `demo.py`, `main.py`)
- Test suite (e.g., `test_*.py`)

**Owner:** Prototype Engineer builds the prototype.
**Validation:** Prototype Validator runs it and reports results.

## Conventions
- Pin all dependencies
- Use virtual environments or containers
- Include at least one runnable demonstration script
- See `docs/INVENTION_CONTEXT.md` for full prototyping conventions
