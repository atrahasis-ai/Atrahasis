# T-210 Prior Art Report

## Scope
Assess the architectural patterns that already exist for multi-agent communication and determine where T-210 is genuinely additive.

## Compared baselines

### 1. C4 ASV
- Contribution: epistemic types, confidence, provenance, verification vocabulary.
- Limitation: explicitly a vocabulary, not a full sovereign protocol stack.
- Relevance: semantics-layer baseline and compatibility reference, not final Alternative B authority.

### 2. A2A / MCP
- Contribution: production-grade transport, discovery, and tool connectivity ecosystems.
- Limitation: semantic integrity chain breaks at the boundary; no Atrahasis-native end-to-end accountability.
- Relevance: target capabilities to absorb and bridge against.

### 3. Layered network protocol families (OSI / TCP-IP)
- Contribution: proof that separated layers and binding contracts allow substitution and evolution.
- Limitation: these families do not solve semantic accountability or canonical meaning.
- Relevance: architectural method, not domain solution.

### 4. Capability-based security and object-capability systems
- Contribution: clear authority boundaries, least privilege, revocable capabilities.
- Limitation: they do not define distributed semantic payload governance.
- Relevance: security-layer pattern for authorization and tool/resource rights.

### 5. Content-addressed and signed object systems
- Contribution: canonical hashes, tamper evidence, stable content identity, signature chains.
- Limitation: content address alone does not supply claim semantics, session lifecycle, or protocol structure.
- Relevance: essential for AACP's semantic-integrity story.

## What is not novel in T-210

- Using layers.
- Using transport bindings.
- Using cryptographic signatures.
- Using capability negotiation and version negotiation.

## What is novel enough to justify the task

The invention is not "five layers exist." The invention is the specific Atrahasis-native composition:

1. semantic canonicality originates in a governed AASL layer,
2. messaging references that canonical payload without redefining it,
3. security signs canonical meaning rather than transport bytes alone,
4. session negotiates layer capabilities and recovery behavior without owning payload semantics,
5. transport becomes replaceable plumbing instead of external architectural authority.

That composition closes the precise break that Alternative B is trying to eliminate: the loss of end-to-end semantic integrity at the old A2A/MCP boundary.

## Prior-art destruction attempt

### Claim: "This is just OSI plus JSON-LD"
- Rebuttal: OSI gives layering discipline, but not semantic integrity contracts, canonical-hash authority, or the Atrahasis cross-layer obligations to C3/C5/C6/C7/C8/C23/C24/C36/C37.

### Claim: "This is just C4 ASV scaled up"
- Rebuttal: C4 intentionally refused protocol ownership. T-210 must define session, security, transport, and binding contracts that C4 explicitly left to external protocols.

### Claim: "This is just A2A/MCP reimplementation"
- Rebuttal: T-210 absorbs those capabilities but changes the architectural center of gravity: bridges become compatibility tools, not the sovereign semantic backbone.

## Conclusion

T-210 is justified if it stays narrow:
- root architecture,
- hard layer boundaries,
- cross-layer invariants,
- upgrade contracts.

It is not justified if it turns into premature field-level specification for every later task.
