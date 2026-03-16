# C34 Prior Art Report — Sentinel Graph (Seismographic Sentinel with PCM-Augmented Tier 2)

**Invention ID:** C34
**Invention Name:** Sentinel Graph (Seismographic Sentinel with PCM-Augmented Tier 2)
**Domain:** Graph-based security and anomaly detection for distributed multi-agent systems
**Stage:** RESEARCH
**Search Date:** 2026-03-11
**Search Scope:** Patents, academic papers, commercial products, open-source projects, standards
**Researcher:** Prior Art Researcher

---

## Executive Summary

Extensive prior art exists for individual components of C34, but no single system combines all six key innovations into a unified architecture. The STA/LTA technique is well-established in seismology but has not been applied to multi-agent verification security. Graph-based anomaly detection and Sybil defense are active research areas with substantial prior art. The Permitted Correlation Model (PCM) concept -- computing expected inter-agent correlation from structural covariates and detecting only residual anomalies -- represents C34's most novel contribution with no direct precedent found. The combination of seismographic per-agent triggering, structural-covariate-adjusted regional correlation, and epidemiological backward tracing into a single three-tier pipeline is novel. SentinelAgent (May 2025) is the closest overall system but differs fundamentally in method (LLM-based semantic reasoning vs. statistical signal processing) and lacks PCM, STA/LTA, or epidemiological tracing.

---

## Prior Art Findings

### Academic Papers

#### PA-01: SentinelAgent: Graph-based Anomaly Detection in Multi-Agent Systems

- **Source:** He, Wu, Zhai, Sun -- arXiv 2505.24201 (May 2025)
- **URL:** https://arxiv.org/abs/2505.24201
- **Relevance:** HIGH

**Summary:** Three-tier graph-based anomaly detection framework for LLM-based multi-agent systems. Tier 1: global output anomaly detection. Tier 2: single-point failure localization. Tier 3: multi-point failure attribution. Uses dynamic execution graphs with node/edge/path-level analysis via LLM-as-judge semantic reasoning plus IBM Granite Guardian and LlamaFirewall.

**Overlap with C34:** Three-tier hierarchical structure, graph-based modeling of agent interactions, multi-agent attack detection including collusion, backward attribution from detected anomaly to source agent(s).

**Key Differentiators for C34:**
- C34 uses statistical signal processing (STA/LTA) not LLM semantic reasoning
- C34's PCM has no equivalent -- SentinelAgent lacks structural covariate adjustment
- C34's Tier 1 is per-agent O(1) statistical detection; SentinelAgent's is global output verification
- C34's multi-channel quorum (4-channel, 3-of-4) has no parallel in SentinelAgent
- C34 targets verification-system Sybil/collusion; SentinelAgent targets prompt injection and tool misuse
- C34 uses epidemiological overdispersion; SentinelAgent uses attack-path pattern matching
- SentinelAgent requires LLM inference per detection cycle; C34 is purely statistical at Tier 1

---

#### PA-02: MIDAS: Microcluster-Based Detector of Anomalies in Edge Streams

- **Source:** Bhatia, Hooi, Yoon, Shin, Faloutsos -- AAAI 2020
- **URL:** https://arxiv.org/abs/1911.04464
- **Relevance:** HIGH

**Summary:** Streaming graph anomaly detection using count-min sketches (CMS) and chi-squared tests to detect microclusters of suspiciously correlated edges arriving simultaneously. O(1) per edge, constant memory. Processes edges 162-644x faster than prior art. MIDAS-R adds temporal/spatial relations; MIDAS-F adds anti-poisoning via conditional merge.

**Overlap with C34:** C34 explicitly references MIDAS-style streaming edge detection as augmenting PCM at Tier 2. Shared: streaming O(1) edge processing, chi-squared statistical tests, detection of coordinated edge formation.

**Key Differentiators for C34:**
- MIDAS detects raw edge bursts; C34 PCM first subtracts expected correlation from structural covariates, then applies MIDAS-style detection only to residuals
- MIDAS has no concept of permitted vs. unexplained correlation
- MIDAS operates on a single edge stream; C34 uses 4-channel quorum over verification/behavioral/infrastructure/economic dimensions
- MIDAS lacks hierarchical tier structure -- it is a single-pass algorithm
- C34 integrates MIDAS as one component within a larger PCM-augmented pipeline

---

#### PA-03: HAVEN: Hierarchical Autonomous Vehicle Enhanced Network

- **Source:** arXiv 2511.12648 (Nov 2025)
- **URL:** https://arxiv.org/abs/2511.12648
- **Relevance:** HIGH

**Summary:** Three-tier hierarchical anomaly detection for autonomous vehicle networks. Tier 1: lightweight ensemble ML at edge (Random Forest + SVM + LSTM) with sub-10ms latency. Tier 2: Byzantine-robust federated learning with trimmed mean aggregation across regional clusters. Tier 3: selective blockchain logging for tamper-proof threat intelligence. Achieves 94% accuracy scaling to 1000 vehicles.

**Overlap with C34:** Three-tier hierarchy with local detection, regional correlation, and global coordination. Per-entity Tier 1 detection with dual thresholds (anomaly score > 0.7 AND confidence > 0.8). Regional clustering of entities. Byzantine fault tolerance at Tier 2.

**Key Differentiators for C34:**
- HAVEN uses supervised ML ensemble; C34 uses unsupervised STA/LTA statistical ratios
- HAVEN's regional tier uses federated learning model aggregation; C34 uses PCM residual correlation on spectrally-clustered neighborhoods
- HAVEN has no concept of permitted correlation or structural covariate adjustment
- HAVEN's Tier 3 is forward-looking threat intelligence; C34's Tier 3 is backward epidemiological tracing
- HAVEN targets sensor data (LiDAR, camera); C34 targets verification metrics (latency, acceptance rate, committee frequency)
- C34's 4-channel quorum has no parallel in HAVEN

---

#### PA-07: SybilGuard / SybilLimit / SybilRank -- Graph-Based Sybil Defense

- **Source:** Yu et al. (2006, 2008); Cao et al. (2012)
- **URL:** https://en.wikipedia.org/wiki/Sybil_attack
- **Relevance:** MEDIUM

**Summary:** Family of graph-based Sybil defense algorithms exploiting social trust graph structure. SybilGuard uses random walks to partition honest/Sybil regions. SybilLimit achieves near-optimal O(log n) accepted Sybils per attack edge. SybilRank uses early-stopping random walks with trust propagation from known honest nodes. All assume fast-mixing honest region.

**Overlap with C34:** Graph-based Sybil detection, exploiting structural properties of trust/interaction graphs, assumption that Sybil nodes create few trust relationships.

**Key Differentiators for C34:**
- SybilGuard/Limit/Rank use random-walk trust propagation; C34 uses STA/LTA per-agent triggers feeding PCM residual correlation
- Classic Sybil defenses assume static social graph; C34 handles dynamic verification interaction graphs
- No behavioral baseline or temporal anomaly detection in SybilGuard family
- No multi-channel quorum or epidemiological backward tracing
- C34 detects Sybil through behavioral correlation residuals after structural adjustment; SybilGuard detects through graph partition properties

---

#### PA-08: SybilHunter: Hybrid Graph-Based Sybil Detection

- **Source:** Neurocomputing, Vol 500 (2022)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0925231222006373
- **Relevance:** MEDIUM

**Summary:** Combines graph structure with behavioral feature aggregation for Sybil detection. Constructs weighted-strong-social (WSS) graph based on behavioral similarity. Achieves 0.945 AUC. Key insight: sybil users have different behavioral patterns from benign users.

**Overlap with C34:** Behavioral similarity for Sybil detection, graph-based approach combining structural and behavioral signals.

**Key Differentiators for C34:**
- SybilHunter uses behavioral similarity to strengthen graph; C34 uses structural covariates to explain away expected correlation
- No hierarchical tier structure in SybilHunter
- No STA/LTA temporal detection or epidemiological tracing
- SybilHunter targets social networks; C34 targets verification systems
- C34's PCM explicitly models and removes expected correlation; SybilHunter uses behavioral similarity directly as detection signal

---

#### PA-09: AnoGraph: Sketch-Based Anomaly Detection in Streaming Graphs

- **Source:** Bhatia et al. -- KDD 2023 (Stream-AD group)
- **URL:** https://arxiv.org/abs/2106.04486
- **Relevance:** MEDIUM

**Summary:** Extends count-min sketch to higher-order structure preserving dense subgraph properties. Detects both edge and graph anomalies in streaming graphs with constant memory and time per edge. Uses greedy dense submatrix search with 2-approximation guarantee. Successor to MIDAS.

**Overlap with C34:** Streaming graph anomaly detection with sketch data structures, constant-memory processing, dense subgraph detection as anomaly signal.

**Key Differentiators for C34:**
- AnoGraph detects raw dense subgraphs; C34 detects dense subgraphs only after subtracting PCM-expected correlation
- No hierarchical tier structure
- No behavioral baselines or STA/LTA
- No multi-channel quorum or backward tracing
- AnoGraph is domain-agnostic; C34 is specifically designed for verification system security

---

#### PA-10: Backward Contact Tracing / Epidemiological Source Localization

- **Source:** Kojaku et al., Nature Physics (2021); various source localization papers
- **URL:** https://www.nature.com/articles/s41567-021-01187-2
- **Relevance:** HIGH

**Summary:** Backward contact tracing is shown to be profoundly more effective than forward tracing due to heterogeneity bias. Applied to epidemic source detection on networks using time-reversal backward spreading, active querying, and maximum-likelihood estimation. Graph diffusion source localization methods use invertible graph neural networks and backward inference.

**Overlap with C34:** C34's Tier 3 directly adapts epidemiological backward tracing to identify common causal sources (operators) of multiple anomalous agents. Shared concepts: backward tracing from observed cases, overdispersion analysis for superspreader identification, network-based source localization.

**Key Differentiators for C34:**
- Epidemiological tracing has never been applied to AI verification system security in published literature
- C34 traces from confirmed verification anomalies back to operator-agent common sources; epidemiological work traces from infected patients to patient-zero
- C34's overdispersion analysis targets operator-level clustering; epidemiological overdispersion targets superspreader events
- C34 integrates backward tracing as Tier 3 of a hierarchical pipeline with STA/LTA and PCM feeding into it

---

#### PA-11: Correlation-Based Anomaly Detection with Structural/Causal Adjustment

- **Source:** Multiple: CausalRCA (KDD 2022), CIRCA, Causal Graph Profiling (2025), correlation law anomaly detection (Data & Knowledge Engineering, 2023)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0169023X23000411
- **Relevance:** HIGH

**Summary:** Active research area. Causal inference methods model causal/structural relationships to separate expected from anomalous behavior. CausalRCA uses Causal Bayesian Networks for root cause localization in microservices. Correlation-law approaches define contextual vs. behavioral attributes and detect deviation from expected correlation. Causal graph profiling uses structural divergence between normal and anomalous DAGs.

**Overlap with C34:** Separating expected from anomalous correlation using structural/causal models. Detecting deviation after adjusting for known covariates. Root cause attribution through causal graph analysis.

**Key Differentiators for C34:**
- C34's PCM is a domain-specific structural prior (committee co-membership, epoch overlap, task-type similarity); causal methods learn structure from data
- PCM computes expected correlation from known structural covariates and forms edges only from residuals; causal methods reconstruct full causal graphs
- C34 combines PCM with streaming MIDAS-style edge detection; causal methods typically operate in batch
- No prior work combines structural covariate adjustment with seismographic per-agent triggers and epidemiological backward tracing
- C34's PCM is adversary-aware by design (RQ-1 asks about adversarial robustness of PCM)

---

#### PA-12: EigenTrust Algorithm

- **Source:** Kamvar, Schlosser, Garcia-Molina -- WWW 2003
- **URL:** https://nlp.stanford.edu/pubs/eigentrust.pdf
- **Relevance:** LOW

**Summary:** Reputation management for P2P networks using transitive trust. Global trust values correspond to left principal eigenvector of normalized local trust matrix. Effective against up to 70% malicious collective. Distributed computation with bounded message complexity.

**Overlap with C34:** Distributed trust assessment, resilience against colluding nodes, graph-based approach.

**Key Differentiators for C34:**
- EigenTrust is a reputation/trust system; C34 is an anomaly detection system
- No temporal analysis, STA/LTA, or behavioral baselines
- No structural covariate adjustment or PCM
- No hierarchical detection tiers
- EigenTrust aggregates trust; C34 detects anomalous deviation from expected behavior

---

#### PA-20: Network Diffusion Source Localization

- **Source:** Multiple: Shah & Zaman (2011), Lokhov et al. (2014), backward diffusion papers
- **URL:** https://arxiv.org/abs/2206.09214
- **Relevance:** MEDIUM

**Summary:** Source localization for network diffusion processes. Methods include maximum-likelihood estimation, time-reversal backward spreading, invertible graph diffusion neural networks, active querying strategies, and GCN-based approaches with limited observers. Addresses both single-source and multi-source identification.

**Overlap with C34:** Backward inference from observed state to originating source, network graph-based analysis, handling of incomplete observation (sparse monitors).

**Key Differentiators for C34:**
- Source localization methods target epidemic/information diffusion; C34 targets operator identification from anomalous agent clusters
- C34 uses overdispersion analysis specific to operator-agent cardinality; source localization uses diffusion likelihood
- C34's Tier 3 operates on pre-filtered anomalies from Tiers 1-2; source localization typically operates on raw observation data
- C34 integrates backward tracing with verification-specific domain knowledge

---

#### PA-21: Chi-Squared Anomaly Detection in Network Traffic

- **Source:** Ye (2001), multiple subsequent works
- **URL:** https://onlinelibrary.wiley.com/doi/10.1002/qre.392
- **Relevance:** LOW

**Summary:** Chi-squared statistical tests comparing observed vs. expected frequency distributions for intrusion detection. Builds normal traffic profile, computes departure of recent events from norm, declares anomaly on large deviation. Applied to sliding windows over network traffic features.

**Overlap with C34:** Statistical deviation from expected model, sliding window processing, chi-squared as anomaly metric.

**Key Differentiators for C34:**
- C34 uses STA/LTA ratio (signal amplitude), not chi-squared frequency distribution
- Chi-squared tests compare feature distributions; C34 compares temporal amplitude averages
- No graph structure, structural covariate adjustment, or hierarchical tiers
- No multi-agent or verification system focus

---

#### PA-22: ReCon: Sybil-Resistant Consensus from Reputation

- **Source:** Pervasive and Mobile Computing (2020)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S1574119219304742
- **Relevance:** MEDIUM

**Summary:** Sybil-resistant consensus using reputation-based committee selection. Randomized committee assignment minimizes collusion. Reputation increases on successful BFT rounds, significantly decreases on failures. Diversity enforcement in committee composition.

**Overlap with C34:** Committee-based verification with Sybil resistance, reputation-driven detection, addressing collusion through randomized assignment.

**Key Differentiators for C34:**
- ReCon adjusts committee selection; C34 monitors committee participation patterns for anomalies
- ReCon is a consensus mechanism; C34 is a detection/monitoring system
- No STA/LTA, PCM, or epidemiological tracing
- No multi-channel quorum or structural covariate adjustment

---

### Established Technique

#### PA-04: STA/LTA Algorithm (Seismological First-Break Picking)

- **Source:** Allen (1978) original; widely implemented in ObsPy, Guralp, IRIS
- **URL:** https://cuseistut.readthedocs.io/en/latest/sta_lta/index.html
- **Relevance:** HIGH

**Summary:** Standard seismological technique computing ratio of short-term average to long-term average signal amplitude. Trigger declared when ratio exceeds threshold. O(1) per sample. Universally used in seismic event detection since 1978. Multiple variants: classic, recursive, Z-detect, Carl-STA/LTA. Well-understood false positive characteristics.

**Overlap with C34:** C34's Tier 1 directly adapts STA/LTA from seismology to per-agent verification metric monitoring. Same mathematical formulation of short-window vs. long-window averaging.

**Key Differentiators for C34:**
- STA/LTA has never been applied to multi-agent verification system security in published literature
- C34 adds parallel fixed-baseline detection alongside adaptive STA/LTA for anti-evasion (no seismological precedent)
- C34 applies STA/LTA to verification-specific metrics (claim acceptance rate, committee frequency, behavioral consistency) not seismic amplitude
- C34 chains STA/LTA as Tier 1 trigger feeding into PCM-augmented Tier 2, which has no seismological analog

---

### Patents

#### PA-05: US8887286B2 -- Continuous Anomaly Detection via Behavior Modeling

- **Source:** Adobe Inc. (originally Allied Security Trust). Filed 2013, granted 2014.
- **URL:** https://patents.google.com/patent/US8887286B2/en
- **Relevance:** MEDIUM

**Summary:** Continuous anomaly detection based on multi-dimensional behavioral modeling and heterogeneous information analysis. Builds normalcy profiles, detects deviations via behavioral scores and clustering. Processes structured and unstructured data. Uses relationship graphs for correlation.

**Overlap with C34:** Behavioral baseline comparison, continuous monitoring, deviation scoring, multi-dimensional analysis of entity behavior.

**Key Differentiators for C34:**
- Patent uses holistic organizational profiling; C34 uses per-agent STA/LTA
- No structural covariate adjustment or permitted correlation concept
- No hierarchical three-tier escalation pipeline
- No epidemiological backward tracing
- No multi-channel quorum threshold
- Patent targets insider threat in enterprise; C34 targets verification system integrity in multi-agent platform

---

#### PA-06: US9516053B1 -- Network Security Threat Detection by User/Entity Behavioral Analysis (Splunk UEBA)

- **Source:** Splunk Inc. (now Cisco). Filed 2015, granted 2016.
- **URL:** https://patents.google.com/patent/US9516053B1/en
- **Relevance:** HIGH

**Summary:** Multi-stage detection hierarchy: Stage 1 anomaly detection from behavioral baselines, Stage 2 threat indicator evaluation, Stage 3 confirmed threat determination. Uses adaptive behavioral baselines, entity relationship graphs (Neo4j), probabilistic suffix trees, rarity scoring. Dual processing paths (real-time + batch). Processes millions of events to yield small number of confirmed threats.

**Overlap with C34:** Three-stage hierarchical funnel (anomaly -> indicator -> threat), adaptive behavioral baselines, graph-based entity correlation, dual real-time/batch processing paths, progressive filtering (millions of events -> hundreds of anomalies -> few threats).

**Key Differentiators for C34:**
- Splunk patent uses ML-based UEBA; C34 uses signal-processing STA/LTA
- No concept of permitted correlation or structural covariate adjustment
- Splunk correlates via entity relationship graphs; C34 uses spectrally-clustered neighborhoods with PCM residuals
- No multi-channel quorum (verification/behavioral/infrastructure/economic channels)
- No epidemiological backward tracing with overdispersion analysis
- Splunk targets enterprise SOC; C34 targets distributed AI verification system
- Splunk's Stage 2 is threat indicator evaluation; C34's Tier 2 is regional correlation with PCM

---

### Commercial Products

#### PA-14: Microsoft Sentinel UEBA

- **Source:** Microsoft Corporation
- **URL:** https://learn.microsoft.com/en-us/azure/sentinel/identify-threats-with-entity-behavior-analytics
- **Relevance:** MEDIUM

**Summary:** Enterprise SIEM with User and Entity Behavior Analytics. Machine-learning behavioral baselines for users, hosts, IPs. Investigation Priority Scores (0-10). Attack Chain Detector highlights entities across MITRE tactics. Anomaly scoring with context (geo, device, time). Alert optimization with UEBA-driven severity.

**Overlap with C34:** Behavioral baselines per entity, anomaly scoring with progressive escalation, multi-dimensional behavioral analysis, attack chain detection across multiple stages.

**Key Differentiators for C34:**
- Sentinel uses ML-based UEBA; C34 uses signal-processing STA/LTA
- No structural covariate adjustment or PCM
- No epidemiological backward tracing
- No multi-channel quorum threshold
- Sentinel targets enterprise IT security; C34 targets AI verification system integrity
- Sentinel is centralized cloud SIEM; C34 is designed for decentralized multi-agent platform

---

#### PA-15: Forta Network: Decentralized Threat Detection for Web3

- **Source:** Forta Foundation
- **URL:** https://forta.org/
- **Relevance:** MEDIUM

**Summary:** Decentralized real-time monitoring network for blockchain/Web3. Community-developed detection bots (agents) run on scan nodes processing every transaction and block. ML-powered threat detection including phishing, exploits, anomalous transactions. FORT token staking for node operation. Thousands of detection bots across multiple chains.

**Overlap with C34:** Decentralized multi-agent threat detection, per-agent monitoring bots, real-time streaming anomaly detection, community/distributed security architecture.

**Key Differentiators for C34:**
- Forta monitors on-chain transactions; C34 monitors verification system behavior
- Forta bots are independent; C34 has hierarchical tier coordination (Tier 1 -> 2 -> 3)
- No structural covariate adjustment, PCM, or residual correlation analysis
- No epidemiological backward tracing
- No STA/LTA seismographic technique
- Forta relies on individual bot logic; C34 uses integrated multi-channel quorum

---

#### PA-16: Datadog Anomaly Detection

- **Source:** Datadog Inc.
- **URL:** https://docs.datadoghq.com/monitors/types/anomaly/
- **Relevance:** MEDIUM

**Summary:** Infrastructure monitoring with per-host anomaly detection using multiple algorithms: Agile (adapts quickly), Robust (seasonal patterns), Basic (rolling quantile). Accounts for trends, day-of-week, time-of-day patterns. Outlier monitors detect when one host deviates from group behavior.

**Overlap with C34:** Per-entity baseline anomaly detection, adaptive vs. robust algorithm selection (parallel to C34's fixed + adaptive baseline), outlier detection comparing individual to group.

**Key Differentiators for C34:**
- Datadog uses time-series forecasting algorithms; C34 uses STA/LTA ratio
- Datadog's outlier monitor compares individual to group average; C34's Tier 2 uses PCM residual correlation within spectrally-clustered neighborhoods
- No structural covariate adjustment, epidemiological tracing, or multi-channel quorum
- Datadog monitors infrastructure metrics; C34 monitors verification system integrity
- No hierarchical three-tier escalation pipeline

---

#### PA-18: Chainalysis / Elliptic -- Blockchain Forensics and Graph Tracing

- **Source:** Chainalysis Inc., Elliptic Enterprises Ltd.
- **URL:** https://www.elliptic.co/blockchain-forensics-tools
- **Relevance:** LOW

**Summary:** Blockchain forensics platforms using address clustering, entity attribution, and transaction graph tracing. Chainalysis Reactor maps illicit networks with 134,000+ entity attributions. Elliptic processes 300M+ screenings/quarter across 43 chains with 6.4B+ labeled addresses. Cross-chain tracing, AML compliance, criminal investigation support.

**Overlap with C34:** Graph-based entity attribution, tracing from observed anomaly to source entities, clustering of related addresses/accounts.

**Key Differentiators for C34:**
- Chainalysis/Elliptic focus on financial transaction forensics; C34 focuses on verification system security
- No real-time STA/LTA detection or behavioral baselines
- No structural covariate adjustment or PCM
- No hierarchical three-tier pipeline
- Chainalysis/Elliptic work post-hoc; C34 is real-time continuous monitoring

---

#### PA-24: Palantir Gotham -- Graph Intelligence Platform

- **Source:** Palantir Technologies Inc.
- **URL:** https://www.palantir.com/platforms/gotham/
- **Relevance:** LOW

**Summary:** AI-powered intelligence platform merging structured and unstructured data for entity resolution, graph visualization, threat detection, and pattern identification. Used by defense, intelligence, and law enforcement. Entity resolution across names, addresses, phone numbers. Timeline and map overlay analysis.

**Overlap with C34:** Graph-based entity analysis, pattern detection across heterogeneous data, threat identification from relationship graphs.

**Key Differentiators for C34:**
- Palantir is a general intelligence platform; C34 is a specialized verification security system
- No STA/LTA, PCM, or verification-specific metrics
- No multi-channel quorum or epidemiological backward tracing
- Palantir operates on human intelligence data; C34 operates on AI agent verification data

---

### Academic Framework

#### PA-13: Subjective Logic Trust Networks (Josang)

- **Source:** Josang -- University of Oslo. Book: Subjective Logic (Springer, 2016)
- **URL:** https://en.wikipedia.org/wiki/Subjective_logic
- **Relevance:** MEDIUM

**Summary:** Formal framework for reasoning under epistemic uncertainty using opinion tuples (belief, disbelief, uncertainty). Supports trust transitivity, opinion fusion, and distributed trust network analysis. Binomial opinions map to Beta PDFs; multinomial to Dirichlet. C34's parent system (AAS) uses Subjective Logic as its verification foundation.

**Overlap with C34:** AAS verification system (C5 PCVM) uses Subjective Logic. C34 monitors the health of this verification system. Shared: uncertainty-aware trust, distributed opinion aggregation.

**Key Differentiators for C34:**
- Subjective Logic is the trust model being monitored; C34 is the monitoring system
- No anomaly detection, STA/LTA, or behavioral baselines in Subjective Logic itself
- No structural covariate adjustment or epidemiological tracing
- C34 detects when the Subjective Logic verification system is being attacked/manipulated

---

### Academic Framework and Product

#### PA-17: Numenta HTM (Hierarchical Temporal Memory) Anomaly Detection

- **Source:** Numenta Inc.
- **URL:** https://www.numenta.com/resources/htm/
- **Relevance:** LOW

**Summary:** Biologically-inspired hierarchical temporal memory for streaming anomaly detection. Learns temporal sequences continuously. Anomaly score from predicted vs. actual minicolumn overlap (0-1). Fully unsupervised, online, constant-time per observation. Benchmark framework (NAB) for evaluating streaming detectors.

**Overlap with C34:** Hierarchical processing, per-stream anomaly detection, continuous online learning, streaming operation.

**Key Differentiators for C34:**
- HTM uses cortical column-inspired learning; C34 uses STA/LTA signal processing
- HTM operates on individual time series; C34 has inter-agent correlation analysis via PCM
- No graph structure, Sybil detection, or verification system focus
- No multi-channel quorum or backward tracing

---

### Government Program

#### PA-19: DARPA CINDER / ADAMS -- Insider Threat Detection Programs

- **Source:** DARPA Strategic Technology Office (2010-2012)
- **URL:** https://en.wikipedia.org/wiki/Cyber_Insider_Threat
- **Relevance:** LOW

**Summary:** CINDER models adversary missions rather than individual traits, assuming systems already compromised. ADAMS (Anomaly Detection at Multiple Scales) uses multi-scale behavioral analysis. Both emphasize scalable distributed infrastructure for heterogeneous data correlation over extended periods.

**Overlap with C34:** Mission-based adversary modeling (vs. individual trait monitoring), multi-scale anomaly detection, behavioral deviation from norm.

**Key Differentiators for C34:**
- CINDER/ADAMS target human insider threats; C34 targets AI agent Sybil/collusion
- No STA/LTA, PCM, or epidemiological tracing
- No graph-based structural covariate adjustment
- No multi-channel quorum threshold

---

### Commercial Product and Architecture

#### PA-23: Google BeyondCorp / Zero Trust Continuous Verification

- **Source:** Google LLC
- **URL:** https://cloud.google.com/beyondcorp
- **Relevance:** LOW

**Summary:** Zero-trust architecture with continuous authentication, real-time risk assessment, and behavioral monitoring. Dynamically adjusts access controls based on user/device behavior, geolocation, and other signals. No perimeter trust assumption.

**Overlap with C34:** Continuous behavioral monitoring, dynamic risk scoring, zero-trust assumption (no entity inherently trusted).

**Key Differentiators for C34:**
- BeyondCorp is access control; C34 is anomaly detection for verification systems
- No graph-based correlation, STA/LTA, PCM, or epidemiological tracing
- No multi-agent or decentralized architecture focus
- BeyondCorp controls access; C34 detects attacks on the verification layer itself

---

## Innovation Novelty Assessment

### Innovation 1: Permitted Correlation Model (PCM)

- **Novelty Rating:** HIGH

No direct precedent found. Causal inference methods (CausalRCA, CIRCA) separate expected from anomalous using learned causal structure, but PCM uses pre-specified structural covariates (committee co-membership, epoch overlap, task-type similarity) as a domain-specific structural prior. The concept of computing expected inter-agent correlation from known causes and detecting only residual (unexplained) correlation is novel in the verification security domain. Closest analog is correlation-law anomaly detection (Angiulli, 2023) which separates contextual from behavioral attributes, but does not use structural covariates of the interaction topology itself.

### Innovation 2: Three-Tier Hierarchical Trigger Architecture for Verification Security

- **Novelty Rating:** MEDIUM

Three-tier hierarchical detection is well-established. Splunk UEBA patent (US9516053B1) has a three-stage funnel. HAVEN has three tiers for autonomous vehicles. SentinelAgent has three-tier graph detection for LLM agents. However, the specific combination of seismographic STA/LTA (Tier 1) + PCM residual correlation (Tier 2) + epidemiological backward tracing (Tier 3) applied to verification system security is novel. No prior system combines these three specific methods in a hierarchical pipeline.

### Innovation 3: Fixed-Baseline + Adaptive-Baseline Parallel Detection

- **Novelty Rating:** MEDIUM

Datadog offers Agile (adaptive) and Robust (stable) algorithms as alternatives. Ensemble defense frameworks combine multiple detection methods. However, running fixed and adaptive baselines in parallel specifically for anti-evasion -- where the fixed baseline prevents slow-drift attacks that fool adaptive baselines -- is a specific design choice not found in reviewed prior art for this domain. The seismological STA/LTA literature does not use parallel fixed baselines.

### Innovation 4: Multi-Channel Quorum Threshold (4-Channel, 3-of-4)

- **Novelty Rating:** MEDIUM

Multi-channel anomaly detection exists (MTC-NET, multi-sensor systems). Multi-factor authentication and quorum-based consensus are standard. However, the specific 4-channel design (verification, behavioral, infrastructure, economic) with a 3-of-4 quorum requirement for Sybil/collusion flagging at the regional correlation tier is novel. No prior work uses this exact multi-dimensional quorum for verification system anomaly detection.

### Innovation 5: Epidemiological Backward Tracing for Operator-Agent Source Identification

- **Novelty Rating:** HIGH

Backward contact tracing is well-studied in epidemiology (Kojaku et al., Nature Physics 2021). Network source localization is an active research area. Causal root cause analysis (CausalRCA) traces anomalies to microservice sources. However, applying epidemiological backward tracing with overdispersion analysis specifically to identify operator-level sources of anomalous agent clusters in a verification system is novel. No prior work combines overdispersion analysis with operator-agent topology for this purpose.

### Innovation 6: Streaming Incremental Residual Computation with Dynamic Structural Covariates

- **Novelty Rating:** HIGH

MIDAS provides streaming edge detection. Incremental update strategies for streaming anomaly detection are well-studied. However, maintaining and incrementally updating a PCM (structural covariate model) as the underlying topology changes (agents join/leave committees, epoch boundaries shift, task assignments change) and computing residual correlations in streaming fashion is a novel computational challenge. No prior work addresses streaming residual computation where the structural prior itself is dynamically evolving.

---

## Research Question Mapping

### RQ-1: Can the PCM Be Made Adversarially Robust Against Agents Who Create Structural Cover?

**Relevant Prior Art:**
- PA-11 (causal inference robustness)
- Adversarial ML defense literature
- MIDAS-F anti-poisoning

**Assessment:** Active research area. Adversarial evasion of anomaly detectors is well-studied (GANs for evasion, dummy code injection), but adversarial manipulation of structural covariates specifically (creating fake committee co-memberships to explain away suspicious correlation) is a novel attack vector unique to C34's PCM design. MIDAS-F's conditional merge offers partial precedent for anti-poisoning in streaming detection.

**Gap:** No prior work addresses adversarial creation of structural cover to manipulate a permitted correlation model.

---

### RQ-2: What Minimum Observation Period for PCM Calibration?

**Relevant Prior Art:**
- PA-04 (STA/LTA window sizing)
- PA-16 (Datadog algorithm selection)

**Assessment:** STA/LTA window sizing is well-understood in seismology (typically 1-30 second STA, 60-600 second LTA). Datadog's algorithms have configurable lookback windows. However, PCM calibration requires observing sufficient committee rotations, epoch cycles, and task-type variation -- a domain-specific calibration problem with no direct precedent.

**Gap:** Domain-specific calibration requirements for verification system structural covariates are unstudied.

---

### RQ-3: Streaming Incremental Residual Update Under Adversarial Perturbation?

**Relevant Prior Art:**
- PA-02 (MIDAS streaming)
- PA-09 (AnoGraph streaming)
- Streaming anomaly detection surveys

**Assessment:** MIDAS and AnoGraph provide O(1) streaming detection. Incremental clustering and conditional update strategies exist. But maintaining correct residuals when an adversary actively perturbs the structural covariates is an open problem.

**Gap:** Adversarial perturbation of the structural model underlying residual computation is novel and unaddressed.

---

### RQ-4: Bootstrapping Attack Mitigation Circularity?

**Relevant Prior Art:**
- Bootstrapping trust literature
- TPM trust chain
- 5G authentication bootstrapping

**Assessment:** Trust bootstrapping is a well-known problem. TPM chains solve it for hardware. 5G research identifies the fundamental chicken-and-egg issue. C34 must bootstrap its detection system using the very verification system it monitors -- a specific circularity variant.

**Gap:** Bootstrapping a verification-system security monitor that depends on that verification system's integrity is domain-specific and unaddressed.

---

### RQ-5: End-to-End Latency from Tier 1 Trigger to Tier 3 Confirmed Anomaly?

**Relevant Prior Art:**
- PA-03 (HAVEN: 3.7ms edge latency)
- PA-06 (Splunk progressive filtering)
- PA-14 (Sentinel scoring)

**Assessment:** HAVEN achieves 3.7ms at Tier 1. Splunk processes millions of events to yield confirmed threats. C34's three-tier latency depends on epoch timing (60s settlement ticks, 3600s tidal epochs) which sets hard lower bounds unique to the AAS platform.

**Gap:** Latency analysis for verification-system-specific detection pipeline is novel.

---

### RQ-6: Fixed-Baseline Reconstructibility by Adversaries?

**Relevant Prior Art:**
- Adversarial ML evasion literature
- Model extraction attacks

**Assessment:** Model extraction attacks are well-studied for ML models. Reconstruction of statistical baselines by observing system responses is a known concern. C34's fixed baselines may be reconstructible through probing if not protected.

**Gap:** Specific analysis of STA/LTA fixed-baseline reconstruction in verification context is novel.

---

### RQ-7: Optimal Neighborhood Size and Split Policy?

**Relevant Prior Art:**
- Community detection literature (Louvain method)
- Spectral clustering
- Graph partitioning

**Assessment:** Community detection and graph partitioning are mature fields. Louvain method optimizes modularity. Spectral clustering uses eigenvalues. Dynamic community detection handles evolving graphs. However, optimal neighborhood sizing for PCM-augmented anomaly detection with verification-specific structural covariates is unstudied.

**Gap:** Domain-specific neighborhood optimization for PCM-augmented Tier 2 detection is novel.

---

## Standards and Frameworks

| Standard | Relevance | Notes |
|----------|-----------|-------|
| **NIST Cybersecurity Framework (CSF) 2.0** | LOW | Detect function includes 'Anomalies and Events', 'Security Continuous Monitoring', 'Detection Processes'. C34 aligns with Detect function but goes far beyond framework-level guidance with specific algorithmic architecture. |
| **ISO 27001:2022 Control 8.16 (Monitoring Activities)** | LOW | Requires monitoring of network, system, and application behavior to detect potential security events. C34 is a specific implementation far more detailed than the standard requires. |
| **OpenTelemetry (CNCF)** | LOW | Standard for distributed tracing and observability. C34 could potentially use OpenTelemetry-style instrumentation for Tier 1 data collection, but C34's detection pipeline goes far beyond telemetry collection. |

---

## Open Source Projects

| Project | URL | Relevance | Notes |
|---------|-----|-----------|-------|
| **MIDAS / AnoGraph (Stream-AD)** | https://github.com/Stream-AD/MIDAS | HIGH | C34 explicitly references MIDAS-style streaming detection. Open-source reference implementation exists. C34 uses MIDAS as a component within PCM-augmented Tier 2. |
| **SyPy (Graph-based Sybil Detection)** | https://github.com/boshmaf/sypy | MEDIUM | Open-source implementation of SybilGuard/SybilLimit/SybilRank. Useful as baseline comparison but fundamentally different approach (random-walk trust propagation vs. behavioral anomaly detection). |
| **StreamAD** | https://github.com/Fengrui-Liu/StreamAD | LOW | Online anomaly detection library for time series. Includes multiple algorithms. Could provide baseline comparisons but lacks graph structure and domain specificity. |
| **Numenta NAB (Anomaly Benchmark)** | https://github.com/numenta/NAB | LOW | Standard benchmark for streaming anomaly detection evaluation. Useful for benchmarking Tier 1 STA/LTA detection component. |

---

## Overall Novelty Assessment

**Composite Novelty:** HIGH

**Rationale:** While individual techniques (STA/LTA, graph anomaly detection, backward tracing, streaming detection) have extensive prior art, C34's novelty lies in three areas: (1) The Permitted Correlation Model concept of computing expected inter-agent correlation from structural covariates and detecting only residual anomalies has no direct precedent. (2) The specific combination of seismographic per-agent triggering, PCM-augmented regional correlation with multi-channel quorum, and epidemiological backward tracing in a unified three-tier pipeline is architecturally novel. (3) The application domain -- monitoring the integrity of an AI agent verification system against Sybil/collusion attacks -- is a new problem space that none of the prior art directly addresses. The closest competitor, SentinelAgent (May 2025), shares the three-tier graph-based structure but uses fundamentally different methods (LLM semantic reasoning vs. statistical signal processing) and lacks PCM, multi-channel quorum, and epidemiological tracing.

**Freedom to Operate:** FAVORABLE. No blocking patents found that cover the PCM concept, the specific three-tier combination, or the application to verification system security. The Splunk UEBA patent (US9516053B1) covers behavioral analytics with hierarchical filtering but uses different methods. The Adobe patent (US8887286B2) covers behavioral baseline comparison but lacks structural covariate adjustment. Both are sufficiently differentiated from C34's approach.

**Key Risks:**
- SentinelAgent (2025) establishes prior art for three-tier graph-based anomaly detection in multi-agent systems, potentially limiting broad claims about hierarchical graph detection for MAS security
- MIDAS is explicitly referenced by C34 -- any claims must be clearly scoped as augmenting MIDAS with PCM, not replacing it
- STA/LTA is decades-old prior art -- claims must focus on novel application to verification security, not the technique itself
- Backward tracing / source localization has extensive academic prior art -- claims must focus on operator-agent topology-specific application with overdispersion

---

## Recommendations for FEASIBILITY

1. **PROCEED to FEASIBILITY.** C34's core innovations (PCM, combined pipeline, domain application) are sufficiently novel.

2. **CLAIM STRATEGY:** Center patent-style claims on PCM (structural covariate adjustment for expected correlation) as the primary innovation. Secondary claims on the three-tier combination and multi-channel quorum.

3. **ADDRESS RQ-1 EARLY:** Adversarial robustness of PCM against structural cover creation is the most critical open question with no prior art to guide the answer.

4. **BENCHMARK against MIDAS and SentinelAgent** as primary comparison systems in the specification.

5. **ACKNOWLEDGE STA/LTA provenance** from seismology and backward tracing provenance from epidemiology explicitly -- these are novel applications of established techniques, not new techniques.

---

## Sources Consulted

| Category | Count |
|----------|-------|
| Patents reviewed | 5 |
| Academic papers reviewed | 22 |
| Commercial products reviewed | 8 |
| Open-source projects reviewed | 4 |
| Standards reviewed | 3 |
| **Total findings** | **24** |
