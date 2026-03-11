# Invention Context

Institutional knowledge for the Atrahasis Agent System.

---

## Synthesis-Owned Shared Artifact Registry

The following artifacts are owned by the Synthesis Engineer. **No other role may edit them directly.** Submit contribution requests instead.

| Artifact | Description |
|---|---|
| `docs/specifications/<ID>/claims.md` | Patent-style claims for each invention |
| `docs/specifications/<ID>/architecture.md` | Shared system architecture document |
| `docs/prior_art/<ID>/prior_art_report.md` | Consolidated prior art report |
| `docs/prior_art/<ID>/landscape.md` | Technology landscape analysis |

---

## Prototyping Conventions

- **Language preference:** Python for rapid prototyping; Rust/Go for performance-critical components
- **Structure:** Each prototype lives in `prototypes/<INVENTION_ID>/` with its own README, requirements, and entry point
- **Testing:** Every prototype must include at least one runnable demonstration script
- **Dependencies:** Pin all dependencies; use virtual environments or containers

---

## Specification Format Standards

### Patent-Style Claims
- Independent claims: broad, covering the core innovation
- Dependent claims: narrowing with specific embodiments
- Method claims, system claims, and apparatus claims as appropriate

### Technical Specification
- Abstract (200 words max)
- Field of the invention
- Background / problem statement
- Summary of the invention
- Detailed description of embodiments
- Figures and diagrams (described textually with references)
- Claims

---

## Prior Art Search Methodology

1. Define search queries from the invention's key innovation and technical approach
2. Search patent databases (USPTO, EPO, WIPO conceptually)
3. Search academic literature
4. Search commercial products and services
5. Search open-source repositories
6. Document closest prior art and explicit differentiators

---

## Consistency Checks (run during Synthesis)

- Architecture matches specification descriptions
- Claims are supported by the technical specification
- Prototype validates the core claims
- Prior art differentiators are reflected in claims
- No contradictions between architecture, spec, and prototype

---

*Updated by Chronicler when new conventions or patterns are established.*
