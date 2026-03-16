# T-064 Science Assessment: EMA-I
**Agent:** Adapa | **Date:** 2026-03-12

## Findings Summary

| Finding | Assessment | Confidence | Key Risk |
|---|---|---|---|
| 1. Receptor Formalization | PARTIALLY_SOUND | 4/5 | Without session types, it's just middleware |
| 2. Epistemic Translation | PARTIALLY_SOUND | 4/5 | NL translation inherently lossy; must document losses |
| 3. Evidence Completeness | PARTIALLY_SOUND | 5/5 | Complete for mediated interactions; covert channels are fundamental limit |
| 4. Persona Projection | SOUND | 4/5 | Well-understood view materialization; non-interference provable |
| 5. Scale/Performance | PARTIALLY_SOUND | 3/5 | NL path is bottleneck; fast/slow path split needed |
| 6. Boundary Security | PARTIALLY_SOUND | 4/5 | Semantic confusion and NL prompt injection are real threats |
| 7. Composability | PARTIALLY_SOUND | 4/5 | Closed under composition only for structured receptors |

## Critical Design Requirements from Science

1. **Commit to session types** as receptor formalism (Honda/Vasconcelos/Kubo 1998, Honda/Yoshida/Carbone 2008). Without this, "typed receptor" is just naming convention.
2. **Model translation as Galois connection** with explicit residuals (Cousot & Cousot 1977). Document what is lost in each direction.
3. **Separate fast path (structured) from slow path (NL)**. NL-translated operations are untrusted, require confirmation for high-consequence operations.
4. **Bind persona projections to tidal epochs** for consistency. Within an epoch, state is frozen, all projections consistent.
5. **Authenticate persona before translation** (not after). Receptor binding must be authenticated first.
6. **Evidence chain uses causal tracking** (Cheney/Ahmed/Acar 2011), not just temporal correlation. Cryptographic chaining with periodic PCVM commitments.
7. **Receptor composition only for structured path**. NL receptors are not composable.

## Overall Verdict

**PARTIALLY_SOUND — architecture is scientifically well-motivated but requires formalization commitments.**

Strongest component: persona projection (Finding 4) — maps to solved problems in view materialization and information flow control.

Most concerning: epistemic translation engine (Finding 2) — NL path introduces fundamental lossiness and security risks that cannot be fully mitigated.

Key theoretical foundations:
- Session types (Honda et al.) for receptor formalization
- Galois connections / abstract interpretation (Cousot & Cousot) for translation soundness
- Reference monitors (Anderson 1972) for evidence completeness
- View materialization (Gupta & Mumick 1995) + non-interference (Goguen & Meseguer 1982) for persona projections
- Multiparty session types (Honda/Yoshida/Carbone 2008) for composability
