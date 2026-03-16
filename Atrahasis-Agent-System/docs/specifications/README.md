# Invention Specifications

One directory per invention: `<INVENTION_ID>/`

Single-digit invention directories are zero-padded on disk for stable GitHub sorting, for example `C01 - ...` through `C09 - ...`. Canonical invention IDs remain `C1` through `C9`.

Each directory contains:
- `technical_spec.md` — formal technical specification
- `architecture.md` — system architecture document
- `claims.md` — patent-style claims
- `figures/` — diagram and schematic descriptions

**Owners:**
- Specification Writer produces `technical_spec.md` and `claims.md`
- Architecture Designer produces `architecture.md`
- `claims.md` and `architecture.md` are Synthesis-Owned shared artifacts — changes require contribution requests
