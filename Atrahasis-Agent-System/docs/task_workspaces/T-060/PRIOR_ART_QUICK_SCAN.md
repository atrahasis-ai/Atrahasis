# T-060 Sentinel Graph — Prior Art Quick Scan (PRE-IDEATION)

## 1. Closest Existing Approaches

### A. SentinelAgent (Hu et al., arXiv 2505.24201, May 2025)
Graph-based anomaly detection for LLM multi-agent interactions. Models execution as typed directed dynamic graphs. Pluggable oversight agent detects prompt injection, tool misuse, collusion. **Gap:** Targets LLM prompt-level threats, not verification economics, tidal scheduling, or Sybil identity clustering. No co-occurrence affinity matrix or infrastructure fingerprinting.

### B. MIDAS (Bhatia et al., AAAI 2020 / TKDD 2022)
Microcluster-based anomaly detection in streaming edge graphs. Constant time/memory per edge, 162-644x faster than prior art. MIDAS-F resists state poisoning. **Gap:** No domain awareness of verification semantics, no behavioral fingerprinting, no cross-layer triggers. Promising algorithmic backbone but needs heavy adaptation.

### C. SybilRank / SybilGuard / SybilLimit / SybilSCAR Family
Graph-based Sybil detection via random walks (SybilRank), edge bounds (SybilLimit), Bayesian label propagation (SybilSCAR). **Gap:** All assume social-graph structure with honest seeds and sparse attack edges. AAS has verification co-occurrence, not social ties. C17 MCSD L2's B(a_i,a_j) with 5 modalities is already more domain-specific.

### D. GNN-Based Collusion Detection (Gomes et al., arXiv 2410.07091, Oct 2024)
R-GCNs and Graph Attention Networks for procurement/bidding collusion on heterogeneous graphs. **Gap:** Trained on economic data, not verification committees. No tidal epochs or MQI metrics.

### E. Behavioral Fingerprinting (IoT Device Profiling, 2018-2024)
Traffic timing, packet distributions, resource patterns for device identification. DEFT uses distributed SDN + k-means. >90% accuracy. **Gap:** Identifies device types, not collusion groups. C17's 5-modality approach already subsumes this literature.

### F. CooccurrenceAffinity (Mainali et al., 2024)
Novel alpha parameter for co-occurrence analysis with full null-distribution formulation. Corrects known flaws in Jaccard/Dice indices. **Gap:** Designed for ecological species co-occurrence. No streaming, no adversarial awareness, no epoch structure.

### G. Streaming Graph Frameworks (Neo4j+Flink, TinkerPop, Neptune)
Production infrastructure for graph storage + streaming ingestion. **Gap:** Infrastructure choices, not solutions. Provide primitives, not domain logic.

### H. MAESTRO / MAAIS Multilayer Security Frameworks (2024-2025)
Threat-modeling frameworks for agentic AI. Map threats across layers. **Gap:** Describe what to monitor, not how to detect. No algorithms.

## 2. Key Gaps — What Does NOT Exist

1. **Verification committee co-occurrence as a security signal** — no system treats committee assignment patterns as a first-class anomaly input.
2. **Unified graph combining behavioral, infrastructure, and economic signals** — existing systems address one signal type, not all four fused.
3. **Epoch-aware streaming detection tied to scheduling** — no detector understands tidal epochs, settlement ticks, or ETR triggers.
4. **Cross-layer security feedback loops** — no system where detection outputs directly modulate scheduling, verification, economics, knowledge, and governance.
5. **LSH-accelerated behavioral similarity at verification scale** — C17 designed it but no implementation exists for 1K-100K agents.
6. **MQI metric ingestion for graph construction** — no system ingests 10+ verification metrics and converts them to weighted graph edges.

## 3. Research Questions for the Ideation Council

1. SentinelAgent differentiation — acknowledge or extend? (They do LLM prompt security; we do distributed verification economics security.)
2. Co-occurrence statistics — chi-square, CooccurrenceAffinity alpha, or custom adversarial-aware statistic? False-positive implications under non-uniform committee selection?
3. MIDAS as foundation vs. custom design — adapt constant-time streaming or build epoch-native detector?
4. Graph unification — single unified graph (multi-edge types) or layered graph (separate affinity/behavioral/fingerprint with cross-links)?
5. Feedback loop stability — how to prevent detection→reassignment oscillation?
6. Relationship to C17 MCSD L2 and C12 AVAP — superset that subsumes both, or peer consuming their outputs?
7. Adversarial robustness of the graph itself — what anti-evasion techniques from day one?
