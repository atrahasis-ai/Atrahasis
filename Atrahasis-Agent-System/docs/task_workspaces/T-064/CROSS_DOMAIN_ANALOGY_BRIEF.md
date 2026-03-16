# T-064 Cross-Domain Analogy Brief
**Role:** Domain Translator | **Agent:** Adapa | **Date:** 2026-03-12

## Analogy 1: Embassy & Consular Network (Diplomacy)
**Source domain:** International diplomatic infrastructure
**Mapping:** A sovereign nation doesn't let foreigners directly interact with its internal agencies. Instead, embassies and consulates serve as the canonical interface layer — translating requests between foreign protocols and domestic systems, enforcing visa/access policies, and providing domain-specific services (trade, immigration, cultural exchange) through a unified but specialized surface. The embassy itself is sovereign territory.

**Insight for Atrahasis:** The interface layer should be a *sovereign boundary*, not just a passthrough. Like an embassy, it translates between external protocols (REST, GraphQL) and internal protocols (C4 ASV, C3 tidal coordination), enforces access policies per domain, and maintains its own state (sessions, credentials, rate limits) without exposing internal architecture.

## Analogy 2: Hospital Information System (Healthcare)
**Source domain:** Clinical information systems
**Mapping:** Hospitals have one unified patient record (like Atrahasis's knowledge/state layers) but expose radically different interfaces to different users: physicians see clinical decision support, patients see a portal with lab results, insurers see billing codes, researchers see anonymized datasets, administrators see operational dashboards. The HL7 FHIR standard provides a shared schema, but each interface speaks its user's language.

**Insight for Atrahasis:** Don't build one interface — build an *interface architecture* that serves five distinct personas through a shared schema layer (C4 ASV). Each persona gets purpose-built surfaces, but they all read/write through the same semantic substrate.

## Analogy 3: Operating System Shell Layer (Computing)
**Source domain:** Unix/POSIX system interface design
**Mapping:** The Unix kernel exposes a single system call interface. Above it: libc wraps syscalls into typed functions, shells (bash/zsh) provide interactive CLI access, window managers provide GUI, and language-specific bindings (Python ctypes, Go syscall) provide SDK access. All share the same underlying capability surface but present it through radically different interaction models.

**Insight for Atrahasis:** The invention shouldn't be "the interface" — it should be the *system call layer* that all interfaces consume. Define the canonical interaction surface (the "syscalls"), then let CLI, SDK, web, and mobile be thin wrappers over that surface. This keeps the invention small and composable.

## Analogy 4: Central Bank Communication Architecture (Finance)
**Source domain:** Federal Reserve / ECB communication infrastructure
**Mapping:** Central banks don't expose their internal models to the public. They communicate through a layered architecture: FOMC minutes for institutional audiences, press conferences for markets, research papers for academics, Fed funds rate announcements for banks, FRED API for data consumers. Each channel has its own format, frequency, and audience — but they're all projections of the same internal state. Crucially, some channels are read-only (public data), some are write-capable (bank reserve operations), and access is strictly tiered.

**Insight for Atrahasis:** The interface layer is really a *communication architecture with tiered access*. Governance decisions (C14) are like monetary policy announcements — highly structured, audit-trailed, with mandatory delay windows. Marketplace operations (C18) are like bank reserve operations — write-capable, authenticated, settlement-backed. Operational dashboards (C33) are like real-time market data — high-frequency, read-mostly, with alerting.

## Analogy 5: Biological Membrane & Receptor System (Biology)
**Source domain:** Cell membrane receptor biology
**Mapping:** Cells don't expose their internal machinery to the outside world. They use receptor proteins embedded in the cell membrane to receive specific signals, transduce them into internal biochemical cascades, and emit responses. Different receptors bind different ligands (hormones, neurotransmitters, antigens). The membrane itself is semi-permeable and actively managed. Critically, the receptor doesn't just pass signals through — it validates, transforms, and often amplifies or attenuates them based on cell state.

**Insight for Atrahasis:** The interface layer should be a *typed receptor membrane* — not a generic proxy. Each receptor (API endpoint group) binds specific external signals, validates them against internal state, transforms them into C4 ASV operations, and returns domain-appropriate responses. The membrane actively manages what gets in, what gets out, and at what rate.

## Meta-Insight

All five analogies converge on the same structural principle: **the interface layer is not a window into the system — it is a sovereign boundary with its own architecture, its own state, and its own intelligence.** It translates, validates, filters, and shapes interactions between fundamentally different worlds (human/external vs. internal/agent). The most successful interface architectures (Unix syscalls, HL7 FHIR, diplomatic infrastructure) share three properties:

1. **Unified substrate** — one canonical interaction surface that all specialized interfaces consume
2. **Persona specialization** — radically different presentations for different users
3. **Sovereign boundary** — the interface layer has authority to deny, transform, rate-limit, and audit

These three properties should guide concept generation.
