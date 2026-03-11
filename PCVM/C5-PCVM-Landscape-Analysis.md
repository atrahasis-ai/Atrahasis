# C5 — Proof-Carrying Verification Membrane (PCVM)
# Landscape Analysis Report
### Atrahasis Agent System v2.0 | Landscape Analyst
### Date: 2026-03-09

---

## 1. Competitive Landscape Map

The verification-for-AI-agents space is fragmented across six distinct categories. No single player occupies the exact niche PCVM targets.

### Category A: Agent Frameworks (Orchestration-First, Verification-Minimal)
| Player | Verification Approach | Gap vs. PCVM |
|--------|----------------------|--------------|
| **LangGraph** (LangChain) | State persistence, reducer logic for concurrent updates. No proof artifacts. | No claim-level verification; trusts LLM outputs implicitly |
| **CrewAI** | Role-based agent teams. Guardrails via prompting. | No structured proof obligations per output |
| **AutoGen** (Microsoft) | Multi-agent conversation patterns, group debate. | Consensus via dialogue, not formal proof |
| **OpenAI Swarm/Assistants** | Tool-use validation, function calling schemas. | Schema enforcement only; no verification trace |
| **Google A2A Protocol** | Agent interoperability standard. Agent Cards for capability declaration. | Interop protocol, not a verification layer |
| **Anthropic MCP** | Tool-context protocol (donated to Linux Foundation AAIF, Dec 2025). | Context delivery, not output verification |

**Key finding:** All major agent frameworks treat verification as an afterthought. The dominant paradigm remains "trust the LLM + optional guardrails." None produce structured, machine-checkable proof artifacts attached to outputs.

### Category B: AI Safety and Alignment Verification
| Player | Approach | Gap vs. PCVM |
|--------|----------|--------------|
| **Anthropic Constitutional AI** | Constitutional classifiers; reduced jailbreak success to 4.4%. Sabotage risk reports. | Focuses on input filtering and behavioral alignment, not output proof artifacts |
| **OpenAI Red Teaming** | Internal + external red teams. Joint evaluation with Anthropic (Summer 2025). | Evaluation-time testing, not continuous runtime verification |
| **METR** | External accountability reviews for frontier models. | Model-level evaluation, not per-output verification |
| **ARC Evals** | Capability evaluations for dangerous AI behaviors. | Pre-deployment testing, not runtime proof-carrying |
| **MATS (ML Alignment Theory Scholars)** | Academic alignment research pipeline. | Research, not operational infrastructure |

**Key finding:** The alignment community focuses on pre-deployment evaluations and model-level safety, not on per-output verification traces. PCVM's claim-class taxonomy with output-level proof obligations is architecturally distinct from anything in this category.

### Category C: Formal Verification and zkML
| Player | Approach | Gap vs. PCVM |
|--------|----------|--------------|
| **EZKL** | Converts ML models to ZKP circuits. 65x faster than RISC Zero. GPU-optimized. | Proves correct model execution, not claim validity of outputs |
| **Modulus Labs** | On-chain ML verification, up to 18M parameter models. | Proves inference integrity, not semantic correctness of claims |
| **Giza** | Verifiable ML on Starknet via Cairo. | Same as above: computational integrity, not semantic verification |
| **ProofNet++** | Hybrid neural-symbolic proof generation for formal verification. | Academic; generates code proofs, not agent output proofs |

**Key finding:** zkML proves "this model ran correctly" but not "the output is factually correct and well-supported." PCVM addresses the semantic gap that zkML cannot: proving that claims have adequate evidence, citations check out, and reasoning is sound.

### Category D: Decentralized Verification Networks
| Player | Approach | Gap vs. PCVM |
|--------|----------|--------------|
| **Bittensor** | Yuma Consensus for scoring model outputs. 128 subnets. Staked TAO validation. | Economic consensus on output quality, not structured proof traces |
| **Ritual** | Verifiable AI inference via Infernet oracles. ZKPs + TEEs + optimistic ML. | Computational integrity proofs for on-chain AI, not semantic claim verification |
| **Chainlink** | AI oracles with multi-node LLM consensus for fact extraction. Staking for security. | Cross-verifies extracted facts via node consensus, not proof artifacts |
| **Truebit** | Cryptographic transcripts of AI agent decisions. Secure runtime execution. | Closest to proof-carrying in spirit; but focused on smart contract execution, not general agent outputs |
| **Ocean Protocol** | Data marketplace with compute-to-data. | Data provenance, not output verification |

**Key finding:** Decentralized networks verify computational integrity through economic incentives and cryptographic proofs of execution. None implement PCVM's concept of structured Verification Trace Documents with claim-class-specific proof obligations.

### Category E: Regulatory and Compliance Frameworks
| Player | Approach | Gap vs. PCVM |
|--------|----------|--------------|
| **EU AI Act** | Mandatory compliance by Aug 2026 for high-risk AI. Technical documentation, risk management, post-market monitoring. | Defines requirements but not verification architecture |
| **NIST AI RMF** | Voluntary framework: Govern, Map, Measure, Manage. TEVV discipline. | Process framework, not a technical verification membrane |
| **ISO/IEC 42001** | AI management system certification. | Organizational standard, not output-level verification |
| **ISO/IEC 42006:2025** | Audit and certification body requirements. | Audit process standard |
| **NIST AI Agent Standards Initiative** (Feb 2026) | Three pillars: industry standards, open-source protocols, agent security research. | Just launched; focus on identity/authorization, not output verification |
| **OMB M-26-04** | Federal agencies must request model cards, evaluation artifacts, system cards. | Documentation requirements, not runtime proof-carrying |

**Key finding:** Regulators are demanding "operational evidence" (not just screenshots and declarations) but have not specified how that evidence should be structured. PCVM's VTD format could become the de facto answer to this regulatory gap.

### Category F: Agent Observability and Trust Startups
| Player | Approach | Gap vs. PCVM |
|--------|----------|--------------|
| **Monte Carlo** | Agent Observability (GA). Input/output contract verification. LLM-as-judge monitors. | Observability and monitoring, not proof-carrying artifacts. Reactive, not constitutive. |
| **t54 Labs** | Agent identity, KYA ("know your agent"), risk scoring. $5M seed (Ripple, Franklin Templeton). | Agent identity layer, not output verification |
| **Promptfoo** | AI red-teaming and evaluation tooling. | Testing tool, not runtime verification membrane |
| **Attestable Audits** (arxiv) | TEE-based benchmark verification with cryptographic attestation to public registry. | Benchmark-level attestation, not per-output proof traces |

**Key finding:** Monte Carlo is the closest commercial analog in spirit -- treating agent trust as an input/output contract -- but implements it as observability (watching from outside) rather than proof-carrying (built into the output itself). This is the critical architectural distinction.

---

## 2. Direct Competitors

**There are no direct competitors implementing PCVM's full architecture.** No existing system combines:
1. Structured, machine-checkable proof artifacts attached to every agent output
2. An 8-class claim taxonomy with class-specific proof obligations
3. Adversarial probing for high-stakes claims
4. Constitutional protections for membrane parameters
5. Continuous re-verification with citation-weighted sampling

The closest partial competitors:

### Truebit (30% overlap)
- Cryptographic transcripts of agentic decisions
- Secure runtime verification
- **Missing:** Claim taxonomy, semantic verification, adversarial probing, constitutional protections

### Monte Carlo Agent Observability (25% overlap)
- Input/output trust contract
- LLM-as-judge evaluation of outputs
- **Missing:** Proof artifacts carried with output, claim taxonomy, constitutional immutability, re-verification

### Ritual Infernet (20% overlap)
- Verifiable inference oracles with multiple proof methods (ZKP, TEE, optimistic)
- **Missing:** Semantic claim verification, claim taxonomy, designed for blockchain not general agent systems

### Chainlink AI Oracles (15% overlap)
- Multi-node consensus on AI-extracted facts
- **Missing:** Structured proof traces, claim taxonomy, adversarial probing

---

## 3. Adjacent Competitors

These solve related but architecturally different problems:

### A. Computational Integrity Provers
**EZKL, Modulus Labs, Giza** -- Prove that a specific model was run correctly on specific inputs. Necessary but insufficient: PCVM needs to verify that the *claims* in an output are well-supported, not just that the computation was performed correctly. PCVM could potentially integrate zkML as one proof method within its membrane.

### B. Alignment Evaluation Frameworks
**Anthropic Constitutional AI, METR, ARC Evals** -- Test model behavior at evaluation time. PCVM operates at runtime on every output, not periodically during evaluations. These are complementary, not competitive.

### C. Agent Interoperability Protocols
**Google A2A, Anthropic MCP, AAIF** -- Enable agent communication and tool use. PCVM could layer on top of these protocols: A2A delivers the message, PCVM verifies the message carries adequate proof. MCP provides tool context, PCVM verifies the output derived from that context is well-supported.

### D. Regulatory Compliance Platforms
**EU AI Act tooling, NIST AI RMF implementations** -- Define what evidence is needed. PCVM defines how that evidence is structured and carried. VTDs could become the compliance artifact format that regulators implicitly require but have not yet specified.

### E. Data Observability
**Monte Carlo, Datadog AI monitoring** -- Watch agent behavior from the outside. PCVM embeds verification into the output itself. Observability is retrospective; proof-carrying is constitutive.

---

## 4. Gap Analysis

### What PCVM provides that nothing else does:

| Capability | PCVM | Nearest Alternative | Gap Size |
|-----------|------|---------------------|----------|
| **Per-output structured proof artifacts (VTDs)** | Core architecture | Monte Carlo (observability logs, not proof artifacts) | Large |
| **8-class claim taxonomy with class-specific proof obligations** | Core architecture | None | No alternative exists |
| **Adversarial probing for high-stakes claims** | Built-in supplement | Anthropic red teaming (pre-deployment only) | Large |
| **Constitutional immutability of membrane parameters** | Core architecture | None | No alternative exists |
| **Continuous re-verification with citation-weighted sampling** | Core architecture | None | No alternative exists |
| **Proof-checker membrane (not consensus engine)** | Core architecture | Bittensor Yuma Consensus (economic, not proof-based) | Large |
| **Integration with coordination fabric (Tidal Noosphere)** | Designed for | None (no equivalent coordination fabric) | Unique |
| **Semantic claim verification (not just computational integrity)** | Core architecture | zkML (computational only) | Large |

### The fundamental gap PCVM fills:
The industry has bifurcated into two camps:
1. **"Trust the LLM"** -- Agent frameworks that rely on prompting, guardrails, and post-hoc observability
2. **"Verify the computation"** -- zkML systems that prove model execution integrity

Neither addresses the middle ground: **verifying that the semantic content of an agent's output is well-supported, correctly reasoned, and adequately evidenced.** PCVM occupies this unexploited architectural niche.

---

## 5. Market Timing

### Window of Opportunity: 12-18 months (March 2026 - September 2027)

**Favorable timing signals:**

1. **Regulatory pressure is accelerating.** EU AI Act high-risk obligations enforce August 2026. NIST AI Agent Standards Initiative launched February 2026. OMB M-26-04 requires evaluation artifacts from federal AI deployments. Regulators are demanding "operational evidence" but have not specified the format -- creating a standards vacuum PCVM can fill.

2. **Agent frameworks lack built-in verification.** Despite massive investment, LangGraph, CrewAI, AutoGen, and OpenAI Swarm treat verification as optional guardrails. Gartner projects 40% of enterprise applications will have embedded agents by end of 2026, but the verification infrastructure for those agents does not exist.

3. **The AAIF standardization effort is early-stage.** The Agentic AI Foundation (Linux Foundation) was formed in December 2025. NIST's initiative launched February 2026. Standards development typically takes 2-3 years. PCVM can establish a de facto standard before formal standards ossify.

4. **zkML has proven the concept of verifiable AI but not the semantic layer.** EZKL, Modulus, and Giza have demonstrated that cryptographic verification of AI inference is practical. The market understands "verifiable AI" as a category. PCVM extends this concept from computational integrity to semantic integrity.

5. **Enterprise AI deployment is outpacing trust infrastructure.** CB Insights reports AI agent M&A surged 10x YoY in 2025. Bessemer identifies evaluation as "one of the biggest unsolved bottlenecks in enterprise AI deployment." Monte Carlo's Agent Observability going GA signals market demand for verification tooling.

**Timing risks:**

1. **Major framework vendors could add verification layers.** If Microsoft (AutoGen), Google (A2A), or Anthropic (MCP) add proof-carrying verification to their frameworks, the window narrows significantly. Current trajectory suggests this is 18-24 months away at minimum, as their focus remains on interoperability and orchestration.

2. **NIST could define a competing standard.** The AI Agent Standards Initiative could specify an output verification format that differs from VTDs. However, NIST's process is industry-led and slow -- PCVM could be submitted as input to shape the standard.

3. **zkML projects could expand into semantic verification.** EZKL or Ritual could extend beyond computational integrity proofs. However, their architectural DNA is cryptographic proof of computation, not semantic claim verification -- a significant pivot would be required.

---

## 6. Strategic Positioning

### Primary positioning: "The Verification Membrane for the Agentic Era"

PCVM should position itself at the intersection of three market forces:

```
                    Regulatory Compliance
                    (EU AI Act, NIST)
                         /    \
                        /      \
                       /        \
    Agent Frameworks  /   PCVM   \  Verifiable AI
    (LangGraph,      /  occupies  \ (zkML, Ritual,
     CrewAI, A2A)   /  this nexus  \ Chainlink)
                   /________________\
                   Enterprise AI Trust
                   (Monte Carlo, t54)
```

### Positioning recommendations:

**1. Complement, don't compete with agent frameworks.**
PCVM is not an agent framework. It is a verification layer that sits on top of any framework. Position as "the verification membrane that makes LangGraph/CrewAI/AutoGen outputs trustworthy." This avoids head-to-head competition with well-funded orchestration platforms.

**2. Extend zkML from computational to semantic integrity.**
Acknowledge zkML's contribution (and potentially integrate EZKL for computational integrity proofs as one VTD proof method). Position PCVM as "the semantic layer above zkML" -- proving not just that the model ran correctly, but that its claims are well-supported.

**3. Provide the compliance artifact regulators need but haven't specified.**
VTDs should be designed to map directly to EU AI Act Article 11 (technical documentation), NIST AI RMF TEVV requirements, and OMB M-26-04 evaluation artifact requirements. Position PCVM as "the verification format that makes AI compliance auditable."

**4. Lead the NIST AI Agent Standards Initiative input process.**
The NIST Request for Information on AI Agent Security is due March 9, 2026 (today). The ITL AI Agent Identity and Authorization Concept Paper feedback is due April 2, 2026. PCVM's VTD format and claim taxonomy should be submitted as standards input.

**5. Differentiate from observability.**
Monte Carlo's Agent Observability is the closest commercial category. PCVM's key differentiator: observability watches from outside; proof-carrying embeds verification into the output itself. Observability tells you something went wrong after the fact. Proof-carrying prevents unverified claims from propagating.

### Positioning statement:
> "PCVM is the first verification membrane that requires AI agent outputs to carry machine-checkable proof artifacts. Unlike observability tools that monitor from outside, PCVM embeds structured verification traces into every output -- making unverified claims impossible to propagate through the agent ecosystem."

---

## 7. Risk Assessment

### Tier 1: High Probability, High Impact

**R1. Platform incumbents add verification features (Probability: 60% within 24 months)**
Microsoft, Google, or Anthropic could add output verification to AutoGen, A2A, or MCP respectively. The AAIF standardization effort (Linux Foundation) provides a natural venue for this. **Mitigation:** Establish PCVM as the reference implementation before platform vendors converge. Submit VTD format to AAIF and NIST as proposed standards. Design PCVM to integrate with (not replace) these platforms.

**R2. "Good enough" observability satisfies enterprise demand (Probability: 50%)**
Monte Carlo's Agent Observability and similar tools may satisfy most enterprise buyers who want visibility into agent behavior without the architectural overhead of proof-carrying. Many enterprises may prefer "monitor and fix" over "prevent and prove." **Mitigation:** Target high-stakes verticals first (healthcare, legal, financial, defense) where "good enough" observability is demonstrably insufficient and regulatory requirements demand proof artifacts.

### Tier 2: Medium Probability, High Impact

**R3. NIST defines a competing output verification standard (Probability: 30% within 18 months)**
The AI Agent Standards Initiative could produce an output verification format that differs from VTDs. **Mitigation:** Actively participate in the NIST process. Submit VTD format as input. Shape the standard rather than compete with it.

**R4. zkML projects expand into semantic verification (Probability: 25% within 18 months)**
EZKL or Ritual could extend their verification beyond computational integrity to semantic claim verification. **Mitigation:** Integrate zkML as a proof method within PCVM (making them complementary rather than competitive). PCVM's claim taxonomy and adversarial probing are difficult to replicate from a cryptographic-proof starting point.

### Tier 3: Low Probability, High Impact

**R5. A breakthrough in LLM reliability makes verification unnecessary (Probability: 10%)**
If LLMs become sufficiently reliable that their outputs rarely require verification, the market for PCVM shrinks. **Mitigation:** Even perfectly reliable models benefit from verifiable trust chains for regulatory compliance and inter-organizational accountability. The EU AI Act requires evidence regardless of model reliability.

**R6. Decentralized verification networks achieve semantic verification (Probability: 15%)**
Bittensor subnets or similar networks could develop semantic verification through economic incentives rather than formal proof. **Mitigation:** PCVM's constitutional protections and deterministic proof-checking are architecturally superior to probabilistic economic consensus for high-stakes verification.

### Tier 4: Strategic Dependencies

**R7. Tidal Noosphere integration dependency**
PCVM is designed to integrate with the Tidal Noosphere coordination fabric. If Tidal Noosphere adoption is slow, PCVM must function as a standalone verification layer. **Mitigation:** Design PCVM with a clean interface that operates independently of Tidal Noosphere, with Noosphere integration as an enhancement rather than a requirement.

---

## Appendix: Key Market Data Points

- **40%** of enterprise applications will have embedded AI agents by end of 2026 (Gartner)
- **$236 billion** projected AI agent market by 2034 (WEF)
- **10x** YoY increase in AI agent M&A activity in 2025 (CB Insights)
- **August 2, 2026**: EU AI Act high-risk obligations enforcement date
- **February 17, 2026**: NIST AI Agent Standards Initiative launched
- **December 2025**: Anthropic donated MCP to Linux Foundation AAIF
- **50+** technology partners supporting Google A2A protocol
- **$500M+** staked in Chainlink Economics 2.0
- **128** active Bittensor subnets (97% increase since early 2025)

---

## Sources

- [AI Agent Frameworks Compared 2026 - Arsum](https://arsum.com/blog/posts/ai-agent-frameworks/)
- [Top 10 AI Agent Frameworks 2026 - O-Mega](https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026)
- [Production Multi-Agent AI Security 2026 - Medium](https://medium.com/@nraman.n6/production-multi-agent-ai-security-the-2026-implementation-guide-00f81ebc675b)
- [TRiSM for Agentic AI - ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666651026000069)
- [AI Agents with Decentralized Identifiers - arXiv](https://arxiv.org/html/2511.02841v1)
- [Google A2A Protocol Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [The 2026 AI Agent Protocol Wars - Prof. Hung-Yi Chen](https://www.hungyichen.com/en/insights/ai-agent-protocol-wars)
- [NIST AI Agent Standards Initiative](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)
- [NIST AI Agent Standards Initiative Detail](https://www.nist.gov/caisi/ai-agent-standards-initiative)
- [Agentic AI Foundation - IntuitionLabs](https://intuitionlabs.ai/articles/agentic-ai-foundation-open-standards)
- [The Definitive Guide to ZKML 2025 - ICME](https://blog.icme.io/the-definitive-guide-to-zkml-2025/)
- [State of EZKL 2025](https://blog.ezkl.xyz/post/state_of_ezkl/)
- [Trust But Verify: ZKML - Medium](https://medium.com/@gafowler/trust-but-verify-verifiable-ai-and-the-dawn-of-zkml-9f4afd12a6a0)
- [Ritual Foundation](https://ritualfoundation.com/blog/unveiling-ritual)
- [Ritual Network Architecture - Mitosis University](https://university.mitosis.org/inside-ritual-network-the-architecture-use-cases-and-community-powering-ritualnet/)
- [Bittensor Ultimate Guide 2026](https://www.tao.media/the-ultimate-guide-to-bittensor-2026/)
- [Bittensor Protocol Analysis - arXiv](https://arxiv.org/html/2507.02951v1)
- [Chainlink AI Oracles](https://blog.chain.link/ai-oracles/)
- [Truebit Verification](https://truebit.io/)
- [EU AI Act Compliance Guide 2026 - Sombra](https://sombrainc.com/blog/ai-regulations-2026-eu-ai-act)
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [Global AI Governance Comparison 2026](https://gaicc.org/blog/ai-governance-comparison-eu-ai-act-nist-iso-42001/)
- [AI Governance Controls Briefing - Evidence Gap](https://internetworkdefense.com/ai-governance-controls-briefing-2026-03-06-evidence-gap/)
- [Attestable Audits - arXiv](https://arxiv.org/html/2506.23706v1)
- [t54 Labs Seed Round - The Block](https://www.theblock.co/post/391273/ripple-franklin-templeton-ai-agent-trust-startup-t54-labs)
- [AI Agents Worth $236B by 2034 - WEF](https://www.weforum.org/stories/2026/01/ai-agents-trust/)
- [AI Agent Predictions 2026 - CB Insights](https://www.cbinsights.com/research/ai-agent-predictions-2026/)
- [Monte Carlo Agent Observability](https://www.montecarlodata.com/blog-agent-observability/)
- [Redefining AI Agent Trust - Monte Carlo](https://www.montecarlodata.com/blog-redefining-agent-trust-input-output)
- [Anthropic Constitutional Classifiers](https://www.anthropic.com/research/constitutional-classifiers)
- [Anthropic Sabotage Risk Report Summer 2025](https://alignment.anthropic.com/2025/sabotage-risk-report/2025_pilot_risk_report.pdf)
- [Anthropic-OpenAI Joint Safety Evaluation - OpenAI](https://openai.com/index/openai-anthropic-safety-evaluation/)
- [AI Will Make Formal Verification Mainstream - Kleppmann](https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html)
- [Certified Proof Checker for DNN Verification](https://drops.dagstuhl.de/storage/00lipics/lipics-vol352-itp2025/LIPIcs.ITP.2025.1/LIPIcs.ITP.2025.1.pdf)
- [Huawei Agent Protocol Stack](https://www.crnasia.com/news/2026/networking/huawei-open-sources-the-protocol-stack-that-could-standardize-how-ai-agents-talk-to-each-other)
- [2025 AI Agent Security Landscape - Obsidian Security](https://www.obsidiansecurity.com/blog/ai-agent-market-landscape)
