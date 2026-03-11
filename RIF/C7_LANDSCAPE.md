# C7 Landscape Analysis — Recursive Intent Fabric (RIF)

**Date:** 2026-03-10
**Analyst:** Landscape Analyst

## Competitor Summary

| Name | Max Scale | Architecture | Key Gap vs RIF |
|------|-----------|-------------|---------------|
| Microsoft Agent Framework | ~tens of agents | Event-driven layered | No recursive decomposition, no intent lifecycle, no sovereignty |
| OpenAI Agents SDK | ~5-20 agents | Flat handoff | Stateless, no hierarchy, no formal algebra |
| LangGraph | ~dozens | Graph state machine | Flat graph, no recursion, no sovereignty |
| CrewAI | ~5-15 | Role-driven sequential | Linear cost scaling, no formal algebra |
| AgentOrchestra (TEA) | Single-session | Hierarchical planner | Closest analog but single-session, no sovereignty, no VSM |
| Google DeepMind | Research-scale (hundreds) | Analytical framework | Descriptive not prescriptive; no runtime |
| Google A2A | Protocol-level | Agent discovery + handoff | Protocol only, not orchestration architecture |
| Anthropic MCP | 10K+ servers | Tool connection | Tool interface, not agent orchestration |
| Ray/RayAI | 1.8M+ tasks/sec | Distributed actor/task | Infrastructure layer, no intent semantics |
| Temporal.io | Enterprise-scale | Durable workflow | No intent semantics, no recursive decomposition |
| Kubernetes Federation | 100K+ microservices | Hierarchical cluster | Container orchestration, wrong abstraction |

## Novelty Positioning

RIF occupies an **empty high-scale tier** in the landscape:
- **Low-scale tier (2-20 agents):** CrewAI, MetaGPT, OpenAI Agents SDK — flat/shallow hierarchies
- **Mid-scale tier (tens to low-hundreds):** LangGraph, Microsoft Agent Framework, AgentOrchestra — graph-based/hierarchical
- **Infrastructure tier:** Ray, Temporal, Kubernetes — distributed execution without agent-aware semantics
- **Protocol tier:** MCP, A2A — connectivity without organizational architecture
- **High-scale tier (1K-10K+):** EMPTY — this is where RIF sits

No existing system combines:
1. Intent quanta as first-class lifecycle objects
2. Three-level recursive decomposition with formal algebra
3. VSM-inspired System 3/System 4 distinction
4. Enumerated sovereignty non-interference guarantees
5. Two-plane architecture (infrastructure + executive)

## Market Window

**Estimated window: 12-18 months**

| Threat | Time to Match | Reasoning |
|--------|--------------|-----------|
| Google DeepMind | 12-18 months | Closest research trajectory (scaling laws + delegation framework); primary threat |
| Microsoft | 18-30 months | Engineering resources but needs architectural rethink |
| OpenAI | 18-24 months | Rapid iteration but philosophically opposed (stateless) |
| LangGraph | 24-36 months | Could extend graph to recursive nesting; focus is DX not scale |
| Ray/Anyscale | 12-18 months | Moving toward agent orchestration but organizational architecture not their focus |

## Risk Factors

**HIGH:**
- Google convergence risk — their scaling laws research is converging on similar conclusions
- Adoption complexity — VSM + formal algebra requires conceptual overhead

**MEDIUM:**
- Standard displacement — Agentic AI Foundation may evolve standards to include hierarchical decomposition
- Infrastructure competition — Ray's opinionated orchestration views may create friction
- Scale validation gap — no system has demonstrated 1K-10K coherent agent orchestration

**LOW:**
- Current framework competition — optimizing for small scale, not planetary
- Academic scooping — different scale targets, no VSM/sovereignty/algebra

## Recommended Positioning

Frame RIF as an **orchestration architecture layer** above existing frameworks:
- MCP/A2A for connectivity
- Ray/Temporal for durable execution
- Existing agent frameworks for individual agent implementation
- RIF as "orchestration of orchestrators"

This avoids direct competition and leverages the ecosystem.
