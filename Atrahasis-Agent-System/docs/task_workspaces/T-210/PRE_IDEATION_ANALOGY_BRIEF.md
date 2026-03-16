# T-210 Pre-Ideation Analogy Brief

## Purpose
Provide structural analogies for the root AACP v2 architecture before ideation.

## Analogy 1: TCP/IP versus application protocol layering

- Structural lesson: stable progress comes from narrow layer contracts, not from one huge universal protocol.
- Relevance to T-210: AACP v2 needs transport and session replaceability without semantic drift.
- Warning: over-layering can create ceremony if the contracts are vague.

## Analogy 2: Microkernel versus monolithic kernel

- Structural lesson: pushing responsibilities behind message-passing boundaries improves isolation and swapability, but only if the boundary is small and explicit.
- Relevance to T-210: the five layers should act like kernel boundaries with strict ownership, not like arbitrary chapter headings.
- Warning: too much chatter across the boundary turns a clean architecture into latency theater.

## Analogy 3: Tamper-evident shipping containers

- Structural lesson: the cargo and the transport vessel are distinct; integrity seals bind custody changes without changing the cargo itself.
- Relevance to T-210: the semantics layer owns meaning, while the security layer binds signatures to canonical meaning and the transport layer moves opaque frames.
- Warning: if the seal depends on the truck instead of the container, transfer across carriers breaks integrity.

## Analogy 4: Passport control at an international airport

- Structural lesson: session establishment, identity proof, authorization, routing, and content inspection are different checkpoints with different authorities.
- Relevance to T-210: handshake/session is not the same thing as security, and neither is the same thing as message semantics.
- Warning: letting one checkpoint silently reinterpret another checkpoint's decision creates governance confusion.

## Analogy 5: Printed music versus audio transmission

- Structural lesson: the score carries canonical structure, the performance carries temporal execution, and the wire carries encoded sound. They are related but not identical.
- Relevance to T-210: AASL semantics are the score, messaging is the score's packetization, session/security govern the performance context, and transport is the wire.
- Surprising implication: optimizing the wire format does not change what the composition means.

## Takeaway

The strongest analogy mix is:
- microkernel for boundary discipline,
- tamper-evident shipping for integrity binding,
- printed music for meaning-versus-transport separation.

That combination points away from a monolithic super-protocol and toward a five-layer stack with one critical rule: lower layers may preserve meaning, but they do not define it.
