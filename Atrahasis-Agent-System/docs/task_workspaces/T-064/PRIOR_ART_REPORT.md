# T-064 Prior Art Report: Epistemic Membrane Architecture (EMA-I)
**Agent:** Adapa | **Date:** 2026-03-12

## Novelty Assessment Summary

### WELL-ESTABLISHED (no novelty if used alone)
- API gateway routing and access control (Kong, Apigee, AWS API Gateway)
- Role-based access control (RBAC/ABAC) — Auth0, Grafana, Kubernetes
- Audit logging of API interactions — Retraced, Audit.NET, Auditum
- SDK/API generation from typed specifications — OpenAPI Generator, Fern

### INCREMENTAL (novel combination of established ideas)
- Persona-specific API surfaces (Typed Interaction Receptors) — builds on BFF pattern + K8s Gateway API personas + MCP typed tools
- Governance action translation — extends Tally/Snapshot vote-to-execution to formal G-class claim mapping
- Interaction evidence feeding verification subsystems — connecting audit logs to PCVM verification layer

### GENUINELY NOVEL (3 areas)
1. **Epistemic Translation Engine with formal claim class mapping** — no prior art translates between human-native formats and a formal 9-class epistemic claim taxonomy. Closest: Google NL-to-graph-query, Kong semantic routing — both syntactic/query level, not epistemic.
2. **Persona Projections as epistemic state rendering** — existing systems (Grafana, K8s, Stripe Connect) provide role-based views of operational data. No system projects epistemic state (claims with verification status) through persona-specific semantic lenses.
3. **Membrane architecture as sovereign boundary** — theoretical grounding in boundary object theory (Mark/Lyytinen/Bergman JAIS) but no implementation precedent as formal software architecture for AI agent systems. MCP closest but tool-centric, not membrane-centric.

## Key Prior Art (Selected)

### Patents (7)
- US12,153,884: Epistemic embedding in NLP (covers embedding, not interface membrane)
- US12,189,782B2: NL-to-graph-query translation (covers NL→structured, not epistemic translation)
- US10,853,150B1: API knowledge graph generation (covers API semantics extraction)
- EP2019992A1: Immutable audit log generation (covers cryptographic evidence chains)

### Academic Papers (10)
- "Mind the Semantic Gap" (Frontiers AI 2025) — taxonomy of semantic gaps in HCI
- "From Disclosure to Evidence" (Accountability in Research 2025) — auditable AI provenance
- "Boundary Objects in Design" (Mark et al., JAIS) — strongest theoretical precedent for membrane concept
- "Information-Flow Perspective on Explainability" (KR 2025) — epistemic temporal logic for multi-agent info flow
- Formal methods for human-agent interaction (Brannstrom 2025)

### Existing Systems (10)
- Kong AI Gateway: closest commercial analog, but no epistemic typing
- Kubernetes Gateway API: explicit persona model (Infrastructure Provider/Cluster Operator/App Developer)
- MCP (Model Context Protocol): typed tool interfaces, closest to receptors, but tool-centric not membrane-centric
- Tally/Snapshot: governance vote→execution translation (single domain only)
- Grafana: role-based dashboards (RBAC filtering, not semantic projection)
- Stripe Connect: multi-persona marketplace (payment domain only)

### Open Source (7)
- OpenAPI Generator: SDK generation from specs
- Retraced/Auditum: audit log services
- DAOhaus: open-source DAO governance UI
