# T-064 Pre-Ideation: Prior Art Quick Scan
**Agent:** Adapa | **Date:** 2026-03-12

## Problem Statement

No spec defines how humans or external systems interact with Atrahasis. The system has 14+ completed architectural specs but zero interface surface. Every consumer-facing interaction is assumed but never specified.

## What Exists Inside Atrahasis

| Spec | What It Provides | What It Assumes (Undefined) |
|------|------------------|-----------------------------|
| C4 ASV | JSON Schema vocabulary, JSON-LD context, A2A/MCP embedding | No REST/gRPC/WebSocket API, no human-readable rendering, no query language |
| C14 AiBC | Governance taxonomy, voting thresholds, tribunal structure | Trustee portal, AiDP voting UI, tribunal evidence interface, emergency dashboard |
| C16 Outreach | Nominating agreement templates, engagement tiers | Nominating body portal, candidate submission, agreement tracking |
| C18 Funding | Task marketplace roadmap, VaaS pricing, enterprise licensing | Provider portal, task submission UI, VaaS API, enterprise SDK |
| C22 Planning | Tech stack (Rust/Python/TypeScript), wave schedule | Developer CLI, contract test dashboard, integration monitoring UI |
| C23 SCR | Execution Evidence Bundles, cell lifecycle FSM | Runtime telemetry UI, cell status query API, broker dashboards |
| C33 OINC | Incident capsules, authority envelopes, playbooks | Incident viewer, postmortem UI, escalation routing, evidence export API |
| C24 FHF | Habitat boundaries, gateway model | Habitat status dashboard, federation monitoring |
| C34 BSRF | Recovery predicates, boot sequence | Recovery status UI, predicate satisfaction dashboard |
| C35 Sentinel | STA/LTA anomaly detection, PCM correlation | Anomaly visualization, alert management interface |

## Five Distinct Interface Domains

1. **Governance** — Trustees, tribunal, AiDP voting, constitutional amendments, emergency authority (C14, C16)
2. **Marketplace** — External providers, task submission/verification, VaaS, enterprise integration (C18, C15)
3. **Operations** — Incident management, recovery status, anomaly monitoring, habitat health (C33, C34, C35, C24)
4. **Developer** — CLI tooling, contract test runners, schema validators, SDK generation (C22, C4)
5. **Agent Management** — Identity lifecycle, cell status, credibility queries, onboarding (C32, C23, C31)

## Known Prior Art (Quick Scan)

- **Kubernetes Dashboard / kubectl / client-go**: Multi-surface interface (Web + CLI + SDK) for distributed system management
- **Stripe API / Stripe.js**: Unified API gateway with typed SDKs in multiple languages, embedded UI components
- **Grafana / Prometheus**: Operational dashboards with query language, alerting, and plugin extensibility
- **GitHub API / gh CLI / Octokit**: REST + GraphQL + CLI + SDK pattern for platform interaction
- **Ethereum JSON-RPC / web3.js / MetaMask**: Decentralized system with standardized RPC, typed SDK, and user-facing wallet UI
- **MCP (Model Context Protocol)**: Tool-use protocol that C4 already integrates with; potential transport for interface layer
- **A2A (Agent-to-Agent)**: Google's agent communication protocol; C4 already embeds ASV as A2A parts

## Key Design Tensions

1. **Unification vs. specialization**: One API gateway vs. domain-specific interfaces
2. **Internal-first vs. external-first**: Serve agents first (C4/MCP native) vs. humans first (REST/GraphQL native)
3. **Thick client vs. thin client**: Rich web apps with local state vs. server-rendered with minimal client
4. **Schema-driven vs. endpoint-driven**: Generate interfaces from C4 JSON Schema vs. hand-craft per domain
5. **Atrahasis-native vs. standards-compliant**: Custom protocols vs. OpenAPI/GraphQL/gRPC conformance
