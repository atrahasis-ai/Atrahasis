# C38 Architecture Notes

## Core architecture statement

AACP v2 is a sovereign five-layer communication stack:

1. **Transport** moves framed bytes.
2. **Session** negotiates and maintains connection state.
3. **Security** proves and constrains authority.
4. **Messaging** frames lineage-bearing messages.
5. **Semantics** defines governed payload meaning.

## Narrow-waist rule

The narrow waist of the architecture is the boundary between Messaging and Semantics:
- Messaging must be able to route, batch, stream, and resume payloads without redefining payload meaning.
- Semantics must be able to evolve under governed registry/version rules without depending on one transport or session form.

## Semantic integrity chain

1. Semantics canonicalizes payload meaning.
2. Messaging packages that canonical payload into a lineage-bearing envelope.
3. Security signs and authorizes the envelope's canonical references.
4. Session negotiates how the exchange will proceed and recover.
5. Transport carries frames unchanged.

## Result

Every later Alternative B task either:
- refines one layer,
- adds constructs inside one layer,
- or formalizes a cross-layer contract already named here.
