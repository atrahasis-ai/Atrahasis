# FEASIBILITY VERDICT — C5-B Proof-Carrying Verification Membrane (PCVM)

## Date: 2026-03-09
## Council: Advocate, Skeptic, Arbiter

---

## Advocate Position

PCVM deserves advancement to DESIGN. It is the most architecturally necessary invention in the Atrahasis pipeline — not the most novel, not the most feasible, but the most necessary. The Tidal Noosphere (C3) has an empty socket where Verichain used to sit. That socket must be filled with something better than replication-based consensus. PCVM is the only candidate that has been through the full research pipeline, and the refined concept demonstrates genuine intellectual honesty that strengthens rather than weakens the proposal.

### 1. The Refinement Is Itself Evidence of Quality

The most telling feature of the refined PCVM concept is what it concedes. The original proposal claimed universal proof-checking across all claim classes. The refined concept admits this is false and introduces a graduated model: formal proofs for decidable classes, structured evidence for empirical/statistical/reasoning classes, structured attestations for heuristic/normative classes. The cost model honestly reports that 3 of 8 classes show no cost improvement over replication.

This honesty is strategic, not a weakness. An invention that survives its own scrutiny and emerges with narrower but defensible claims is more likely to succeed than one that maintains grandiose claims through the pipeline. The Science Assessment scored 3.2/5; the refinement directly addresses all three critical gaps — non-deterministic proof theory (graduated VTD model), credibility composition (Subjective Logic adoption), and computational cost (honest per-class analysis). The gaps are not solved, but they are bounded and specified.

### 2. Architectural Necessity Drives Value Beyond Novelty

The Tidal Noosphere architecture (C3) specifies a Verification Membrane as constitutionally sovereign (INV-1, INV-2). Verichain, the original membrane, used replication-based consensus — re-execute the computation and compare results. This has three fundamental problems:

1. **Cost:** Replication costs O(n) where n is the number of verifiers. At Noosphere scale (1K-10K agents), this is prohibitive for every claim.
2. **Non-determinism:** LLM outputs are non-deterministic. Replicating an LLM generation and comparing results is unreliable because two runs of the same prompt produce different outputs. Verichain was designed for deterministic computation.
3. **Depth:** Replication checks "did I get the same answer?" but not "is this answer well-supported?" Two identical wrong answers produce a false positive.

PCVM addresses all three: variable-cost verification per class, evidence-based evaluation that handles non-determinism, and structured proof obligations that check support, not just agreement. Even if PCVM's novel contributions are modest, the alternative — continuing with Verichain — is untenable for the Noosphere architecture.

### 3. The Four Genuinely Novel Components

The prior art report (confidence 4/5) identifies four LARGE novelty gaps:

1. **VTDs as persistent, machine-checkable proof artifacts for AI agent outputs** — no existing system produces these. FactScore and SAFE produce ephemeral scores. CLOVER is limited to code. PCC targets deterministic programs.

2. **8-class epistemic claim taxonomy with class-specific proof obligations** — no prior system classifies AI claims by epistemic type and assigns differential verification requirements. The refined matrix derivation (epistemic status x verification modality) provides the principled grounding the Science Assessment demanded.

3. **Adversarial probing of proof artifacts** — existing red-teaming targets models; PCVM targets the verification traces themselves. Proof-directed adversarial testing has no precedent.

4. **Integration with multi-agent governance** (Tidal Noosphere constitutional protections, VRF dual defense, Sentinel Graph) — no existing verification system integrates with a governance framework at this level.

These four components, taken together, occupy a genuinely unoccupied architectural niche between "trust the LLM" and "verify the computation."

### 4. The Market Window Is Real and Aligned

The landscape analysis identifies a 12-18 month window (March 2026 - September 2027):
- EU AI Act high-risk obligations enforce August 2026
- NIST AI Agent Standards Initiative launched February 2026
- Enterprise AI deployment outpacing trust infrastructure
- No existing system provides structured, per-output verification artifacts

VTDs map directly to what regulators are demanding but have not yet specified: structured operational evidence of AI system trustworthiness. PCVM is not selling verification speed — it is selling structured auditability that satisfies compliance requirements that every enterprise AI deployment will face within 18 months.

### 5. The Adversarial Report Confirms Survivability

The Adversarial Analyst found 2 CRITICAL attacks (VTD forgery, collusion) and 3 HIGH attacks, issuing CONDITIONAL_SURVIVAL. This is comparable to C3's adversarial findings. Critically, all 10 attacks have specified mitigations — none is identified as architecturally fatal. The mitigations are engineering challenges, not theoretical impossibilities:
- Random deep-audit protocol (standard in compliance systems)
- Membrane-assigned classification (architectural decision)
- Class-specific credibility (design decision)
- Collusion detection (statistical methods exist)

No invention at the feasibility stage is attack-proof. The question is whether the attacks are addressable. They are.

**Advocate's recommendation:** ADVANCE to DESIGN. PCVM fills the Noosphere's verification socket with a more capable, more honest, and more auditable system than Verichain. The novelty is genuine, the market window is real, the risks are bounded, and the architectural necessity is urgent.

---

## Skeptic Position

The Advocate makes PCVM sound like the obvious next step. Let me push back on the narrative. PCVM is not bad — it is underdetermined. The refined concept is more honest than the original, but that honesty also exposes how much remains unresolved. The question is whether PCVM at the feasibility stage is a well-scoped invention with identified implementation challenges, or a research program masquerading as an engineering project.

### 1. The Graduated Model Concedes the Core Claim

The original PCVM proposal claimed: "Verification cost drops from O(replication) to O(proof-checking)." The refined concept admits this holds for only 3 of 8 classes (D, P, C). For the remaining 5 classes, the value proposition is:
- "Structured auditability" (a documentation benefit, not a verification benefit)
- "Forced articulation of reasoning" (a process benefit, not a verification benefit)
- "Downstream trust propagation" (unquantified and theoretical)

The Adversarial Analyst's Attack 9 (Tier Collapse) makes the strongest version of this critique: PCVM for H-class and N-class claims is a documentation standard, not a verification membrane. The honest cost model shows H-class VTD verification costs 2x replication. You are paying twice as much for what amounts to better-organized notes.

This does not make PCVM worthless. It makes PCVM smaller than claimed. The actual invention is:
- A proof-checker for D/P/C classes (valuable, but scope is narrow)
- A structured evidence evaluation framework for E/S/R classes (valuable, but the advantage over existing approaches like SAFE/FactScore is incremental)
- A documentation standard for H/N classes (valuable, but this is C4/ASV territory, not a verification membrane)

The Advocate may respond that the unified architecture is the value. I am skeptical. A unified architecture that treats documentation and proof-checking as the same operation is not elegant — it is a category error. Proofs and attestations are fundamentally different things. Calling them both "VTDs" does not make them equivalent.

### 2. The Science Assessment Score Is 3.2/5 — The Lowest in the Pipeline

The Science Assessment scored PCVM at 3.2/5 overall soundness. For comparison:
- C3 (Tidal Noosphere) received soundness 4/5 with coherence 3/5
- C4 (ASV) had its science assessed more favorably on theoretical grounding

PCVM's 3.2 breaks down as:
- Theoretical grounding of individual claims: 3.8 (decent)
- Cross-claim coherence: 3.0 (marginal)
- Empirical evidence: 2.5 (weak)
- Formal completeness: 2.0 (critically weak)
- Practical feasibility: 3.5 (decent)

The formal completeness score of 2.0 is alarming. This is the dimension that matters most for a proof-carrying architecture. A proof-carrying system whose formal foundations score 2.0/5 is an oxymoron. The refined concept addresses this by adopting Subjective Logic (an existing algebra) and reframing VTDs as "structured evidence" rather than "proofs," but these are concessions that narrow the claim, not resolutions that strengthen the foundations.

### 3. Two CRITICAL Adversarial Attacks Remain

The VTD Forgery attack (Attack 1) and the Mutual Endorsement attack (Attack 8) are both rated CRITICAL with HIGH residual risk. Let me emphasize what "HIGH residual risk" means after mitigation:

**VTD Forgery:** If the membrane must actually fetch and verify every cited source to detect forgery, verification cost for E-class claims approaches or exceeds replication cost. The "random deep-audit" mitigation (5-10% of VTDs get full replication) is essentially admitting that for a percentage of claims, you still need replication. PCVM becomes "mostly proof-checking with occasional replication" — an improvement over "all replication" but less dramatic than claimed.

**Collusion:** In any system where N agents verify each other's work, a colluding minority can systematically degrade verification integrity. The Sentinel Graph's statistical detection helps, but sophisticated colluders can stay below detection thresholds. This is a fundamental limitation of all peer-verification systems, and PCVM does not transcend it.

The Advocate argues these attacks have "specified mitigations." Specified, yes. Solved, no. The mitigations are research challenges that may or may not succeed. Collusion detection in multi-agent systems is an active research area with no proven general solution.

### 4. The Credibility Composition Algebra Is Borrowed, Not Proven for This Domain

The refined concept adopts Josang's Subjective Logic, which is a legitimate framework for trust management. However, Subjective Logic was designed for trust in multi-agent communication systems — "do I trust Agent X?" — not for epistemic claim verification — "is Claim A true, given evidence E?"

These are different questions. Trust is about the reliability of the source. Credibility is about the support for the claim. Subjective Logic handles the first well; its applicability to the second is assumed, not demonstrated.

The claim-class adaptations (e.g., "N-class: b/d represent constitutional alignment, not truth") are the refined concept's attempt to bridge this gap, but they are novel modifications to Subjective Logic that have not been validated. If you modify a proven algebra for a new domain, you inherit the algebra's operators but not its correctness guarantees.

Experiment 3 (credibility propagation stability) is the right test, but it must be a hard gate, not a monitoring flag. If Subjective Logic does not converge stably for PCVM's claim dependency graphs, the credibility composition is not just incomplete — it is wrong, and the continuous re-verification story collapses.

### 5. The "Architectural Necessity" Argument Is Compelling but Dangerous

The Advocate's strongest point is that the Noosphere needs a verification membrane, Verichain is deprecated, and PCVM is the only candidate. This is true. But "there is no alternative" is a dangerous basis for advancing an invention. It incentivizes lowering the bar.

The alternative to PCVM is not "no verification." It is a simpler verification architecture that does not attempt to be a proof-carrying membrane for all claim classes. Consider:
- D/P/C classes: machine-checkable verification (proof-checking)
- E/S/R classes: structured evidence evaluation with mandatory adversarial probing
- H/N classes: peer review with structured documentation

This three-tier system achieves the same outcomes as PCVM without claiming to be a unified "proof-carrying membrane." It is less architecturally elegant but more honest about the different natures of these verification tasks.

**Skeptic's recommendation:** CONDITIONAL_ADVANCE with significant conditions. PCVM's direction is right, but the formal foundations are too weak for an invention that claims "proof-carrying" in its name. The Science Assessment's 3.2/5 and the adversarial report's two CRITICAL findings should not be papered over by the architectural necessity argument. If the formal foundations cannot be strengthened in DESIGN, the invention should be descoped to a "Structured Verification Membrane" without the proof-carrying claim.

---

## Arbiter Verdict

### Decision: CONDITIONAL_ADVANCE

### Verdict Justification

The Advocate and Skeptic illuminate a real tension at the heart of PCVM: it is architecturally necessary but formally underdetermined. The verification socket in the Tidal Noosphere must be filled. PCVM is the right shape to fill it. But the formal foundations — the proof theory, the composition algebra, the cost model — are not yet solid enough to justify the "proof-carrying" label for all claim classes.

After weighing all evidence — the refined concept, the adversarial report, the prior art (confidence 4/5, four LARGE novelty gaps), the landscape analysis (no direct competitor, 12-18 month window), and the science assessment (3.2/5 overall, 2.0/5 formal completeness) — I find that PCVM should advance to DESIGN with conditions that address the formal gaps and the adversarial findings.

**On the graduated model:** The Skeptic is right that the graduated VTD model (Tier 1/2/3) concedes the universal proof-carrying claim. The Advocate is right that the concession is honest and strategically sound. The refined concept's candor about cost realities — admitting that H-class VTDs cost more than replication — builds confidence rather than eroding it. I accept the graduated model but require that the DESIGN stage explicitly test whether the unified membrane architecture provides measurable value over a three-tier split.

**On the Science Assessment score:** 3.2/5 is the lowest soundness score in the pipeline. The Skeptic correctly identifies the 2.0/5 formal completeness as alarming for a "proof-carrying" architecture. However, the Science Assessment also notes that the gaps are "fillable, not fundamental" — a crucial distinction. The theoretical grounding of individual claims (3.8/5) and practical feasibility (3.5/5) provide a foundation. The formal completeness gap is what the DESIGN stage is for. The gate experiments proposed by the Science Assessment are the right mechanism to determine whether these gaps can be filled.

**On adversarial findings:** Two CRITICAL attacks with HIGH residual risk after mitigation. This is serious but not disqualifying. C3 (Tidal Noosphere) also had critical adversarial findings and advanced. The key question is whether the mitigations are implementable. For VTD forgery, the random deep-audit protocol is a standard compliance mechanism. For collusion, the Sentinel Graph's statistical detection is feasible with known techniques (correlation analysis, anomaly detection). Neither requires unsolved research — they require careful engineering.

**On the Tier Collapse attack:** The Skeptic's sharpest critique and the Adversarial Analyst's Attack 9 raise a genuine architectural question: should PCVM be one unified system or three separate systems (proof-checker, evidence evaluator, documentation standard)? I side with the Advocate here: the unified architecture is correct because (1) credibility composition across claim classes only works in a unified system, (2) the membrane's sovereignty (INV-1, INV-2) requires a single verification checkpoint, not three parallel systems, and (3) engineering one system with graduated depth is simpler than engineering three systems with coordination between them. However, this architectural decision must be validated in DESIGN through the unified-vs-split experiment specified below.

**On the "proof-carrying" name:** I agree with the Skeptic that PCVM's name overpromises for Tier 2 and Tier 3 classes. However, renaming at this stage creates continuity problems in the pipeline. The DESIGN stage should adopt the internal terminology "Structured Verification Membrane" or "Evidence-Carrying Verification Membrane" for Tier 2/3, while preserving "Proof-Carrying" for Tier 1. The external name can be finalized in SPECIFICATION.

**On architectural necessity:** The Advocate is right that the Noosphere needs this membrane, and the Skeptic is right that necessity should not lower the bar. I resolve this by keeping the bar where it is (the gates below are strict) while acknowledging that if PCVM fails its gates, the consequence is not "no verification" but "design a simpler verification system from scratch" — a significant setback but not a dead end.

### Final Scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Novelty | 4/5 | Four LARGE novelty gaps confirmed by prior art research (confidence 4/5). VTDs for AI agent outputs, 8-class taxonomy with differential proof obligations, adversarial probing of proof artifacts, and governance-integrated verification membrane are all architecturally novel. The prior art search found no system combining even two of these components. Not 5 because the PCC inspiration is acknowledged prior art and the individual verification techniques (source checking, statistical test validation, logic checking) are established. |
| Feasibility | 3/5 | The graduated VTD model is implementable. Subjective Logic is a proven framework. VTD schemas are definable in JSON. Integration with Tidal Noosphere is architecturally specified. Not 4 because: (a) the formal completeness score is 2.0/5, meaning the foundations need substantial work in DESIGN, (b) the credibility composition algebra is borrowed and unvalidated for this domain, (c) the adversarial probing system requires solving the inoculation and weak-adversary problems, (d) the cost model admits that verification is more expensive than replication for 3 of 8 classes. |
| Impact | 4/5 | PCVM fills a genuine architectural gap (verification membrane for the Noosphere) and a genuine market gap (structured verification artifacts for regulatory compliance). If successful, PCVM provides the first structured, per-output verification system for AI agent ecosystems. The EU AI Act and NIST timing creates a real adoption opportunity. Not 5 because the honest cost model limits the efficiency gains and the system's value for H/N classes is auditability rather than verification — important but less transformative. |
| Risk | 6/10 | Two CRITICAL adversarial attacks with HIGH residual risk. Science Assessment at 3.2/5 (lowest in pipeline). Formal completeness at 2.0/5. Credibility composition unvalidated for this domain. Cost model shows no improvement for 3 of 8 classes. Platform incumbents at 60% probability within 24 months. Partially offset by: genuine novelty gaps, regulatory tailwind, architectural necessity, and addressable (not fundamental) formal gaps. |
| Risk Level | MEDIUM-HIGH | Higher than C4 (MEDIUM) due to formal completeness concerns and two CRITICAL adversarial findings. Lower than C3's initial risk (7/10 MEDIUM-HIGH) because PCVM has fewer integration dependencies (it integrates with one system, not three). The risk is concentrated in formal foundations, not in engineering complexity. |

### Required Actions (CONDITIONAL_ADVANCE)

1. **[GATE] VTD Feasibility Experiment (Experiment 1 — before Phase 2).** Construct VTDs for 10 representative agent outputs per claim class (80 total). Measure VTD construction cost, VTD checking cost, and error detection rate. **Kill criterion:** If VTD checking achieves <80% error detection rate at <50% of replication cost for fewer than 4 of 8 claim classes, the VTD model is insufficiently valuable to justify the architectural overhead. Descope to a simpler verification system.

2. **[GATE] Claim Classification Reliability (Experiment 2 — before Phase 2).** Test the 8-class taxonomy with 200 claims, 5 classifiers (3 human, 2 LLM). **Kill criterion:** If Fleiss' kappa < 0.60 (below "substantial agreement"), the taxonomy is too ambiguous for automated classification. Simplify to 4-5 classes (merge H+N, merge E+S, keep D, P/C, R) and re-test.

3. **[GATE] Credibility Propagation Stability (Experiment 3 — before Phase 2).** Implement Subjective Logic composition on a 500-claim dependency graph. **Kill criterion:** If propagation does not converge within 100 iterations, or if a 0.1 change in one claim's credibility cascades to >0.3 change in claims at graph distance >3, the composition algebra is unsuitable. Evaluate alternatives (min-credibility chains, simplified Bayesian) or abandon continuous re-verification.

4. **[GATE] Adversarial Probing Effectiveness (Experiment 4 — before Phase 3).** Compare error detection: replication vs. VTD-only vs. VTD+adversarial probing on 100 claims (30% with inserted errors). **Kill criterion:** If VTD+adversarial probing does not achieve F1 > 0.80 with total cost < 2x replication, adversarial probing does not provide sufficient value over simpler approaches.

5. **[REQUIRED] Mandatory Source Verification Protocol.** DESIGN must specify how the membrane verifies cited sources in E-class VTDs. At minimum: URL accessibility check, content hash comparison, quote accuracy verification. This is a hard engineering requirement, not optional.

6. **[REQUIRED] Membrane-Assigned Classification.** DESIGN must specify that the membrane assigns final claim classifications. Producing agents propose; the membrane decides. Classification disagreements are logged and contribute to taxonomy refinement.

7. **[REQUIRED] Class-Specific Agent Credibility.** DESIGN must implement per-class credibility tracking. Agent trust for D-class does not transfer to H-class. The discounting operator applies class-specific trust.

8. **[REQUIRED] Random Deep-Audit Protocol.** DESIGN must specify a random deep-audit mechanism where 5-10% of passed VTDs are re-verified via full replication. Results feed into collusion detection and deterrence.

9. **[REQUIRED] Unified vs. Split Architecture Validation.** DESIGN must include a comparative analysis: unified membrane (PCVM as proposed) vs. three-tier split (proof-checker + evidence evaluator + documentation standard). The analysis must quantify: engineering complexity, credibility composition capability, membrane sovereignty maintenance, and total system cost. If the split architecture is more than 30% simpler with less than 10% capability loss, the split is preferred.

10. **[RECOMMENDED] Bootstrap Protocol.** Define cold-start procedure with 100-500 manually verified seed claims and fallback verification during bootstrap.

11. **[RECOMMENDED] Constitutional Parameter Draft.** Produce 30+ constitutional parameters during early DESIGN, validated against C1-C4 claims via Experiment 5.

12. **[RECOMMENDED] VTD Size Limits.** Define per-class VTD size limits to prevent explosion attacks.

### Monitoring Flags

| Flag | Severity | Trigger | Action |
|------|----------|---------|--------|
| Formal Completeness Failure | RED | Any of Gates 1-4 fail their kill criteria | Descope invention. Extract viable components (D/P/C proof-checking, adversarial probing) as features for Noosphere. Do not pursue unified membrane. |
| Taxonomy Instability | RED | Experiment 2 kappa < 0.50 | Kill the 8-class taxonomy. Redesign with fewer, more robust classes. |
| Credibility Divergence | RED | Experiment 3 shows oscillation or unbounded cascade | Abandon Subjective Logic for credibility composition. Evaluate simpler alternatives or drop continuous re-verification. |
| Cost Overrun | AMBER | Total system cost with PCVM exceeds 80% of replication cost | Reassess value proposition. PCVM's value must come from quality improvement, not cost reduction. Document this explicitly and evaluate whether quality improvement alone justifies the architecture. |
| Platform Convergence | AMBER | A major framework (A2A, MCP, AutoGen) adds structured per-output verification artifacts | Evaluate contribution vs. competition strategy. If the platform's approach is compatible, align PCVM's VTD format. If incompatible, assess market viability. |
| Adversarial Weakness | AMBER | Experiment 4 shows adversarial probing F1 < VTD-only F1 | Adversarial probing is not adding value. Evaluate whether probing should be replaced with ensemble verification or human review. |
| Collusion Detection Failure | AMBER | Sentinel Graph fails to detect simulated collusion with f > 0.15 within 50 epochs | Strengthen collusion detection or increase deep-audit percentage. If detection fails at f > 0.10, collusion is a systemic risk. |
| Regulatory Alignment | INFO | EU AI Act implementing guidance or NIST AI Agent Standards specify output verification requirements | Align VTD format with specific regulatory requirements. This is a positive signal for PCVM's market positioning. |

### Verdict JSON

```json
{
  "invention_id": "C5",
  "concept": "C5-B",
  "concept_name": "Proof-Carrying Verification Membrane (PCVM)",
  "verdict": "CONDITIONAL_ADVANCE",
  "date": "2026-03-09",
  "scores": {
    "novelty": 4,
    "feasibility": 3,
    "impact": 4,
    "risk": 6,
    "risk_level": "MEDIUM-HIGH"
  },
  "conditions": [
    {
      "id": "GATE-1",
      "type": "GATE",
      "description": "VTD Feasibility Experiment — construct and check VTDs for 80 claims (10 per class), measure cost and error detection",
      "kill_criterion": "VTD checking achieves <80% error detection at <50% replication cost for fewer than 4 of 8 classes"
    },
    {
      "id": "GATE-2",
      "type": "GATE",
      "description": "Claim Classification Reliability — 200 claims, 5 classifiers, Fleiss' kappa measurement",
      "kill_criterion": "Fleiss' kappa < 0.60"
    },
    {
      "id": "GATE-3",
      "type": "GATE",
      "description": "Credibility Propagation Stability — Subjective Logic on 500-claim dependency graph",
      "kill_criterion": "No convergence within 100 iterations, or cascade >0.3 at distance >3"
    },
    {
      "id": "GATE-4",
      "type": "GATE",
      "description": "Adversarial Probing Effectiveness — error detection comparison on 100 claims",
      "kill_criterion": "VTD+probing F1 < 0.80 or cost > 2x replication"
    },
    {
      "id": "REQ-1",
      "type": "REQUIRED",
      "description": "Mandatory Source Verification Protocol for E-class VTDs"
    },
    {
      "id": "REQ-2",
      "type": "REQUIRED",
      "description": "Membrane-Assigned Classification — membrane decides final class, agents propose"
    },
    {
      "id": "REQ-3",
      "type": "REQUIRED",
      "description": "Class-Specific Agent Credibility — per-class trust tracking"
    },
    {
      "id": "REQ-4",
      "type": "REQUIRED",
      "description": "Random Deep-Audit Protocol — 5-10% of passed VTDs re-verified via replication"
    },
    {
      "id": "REQ-5",
      "type": "REQUIRED",
      "description": "Unified vs. Split Architecture Validation — comparative analysis of unified membrane vs. three-tier split"
    },
    {
      "id": "REC-1",
      "type": "RECOMMENDED",
      "description": "Bootstrap Protocol with 100-500 seed claims"
    },
    {
      "id": "REC-2",
      "type": "RECOMMENDED",
      "description": "Constitutional Parameter Draft — 30+ parameters validated against C1-C4"
    },
    {
      "id": "REC-3",
      "type": "RECOMMENDED",
      "description": "VTD Size Limits per claim class"
    }
  ],
  "monitoring_flags": [
    {
      "flag": "Formal Completeness Failure",
      "severity": "RED",
      "trigger": "Any of Gates 1-4 fail",
      "action": "Descope to components; do not pursue unified membrane"
    },
    {
      "flag": "Taxonomy Instability",
      "severity": "RED",
      "trigger": "Experiment 2 kappa < 0.50",
      "action": "Kill 8-class taxonomy; redesign with fewer classes"
    },
    {
      "flag": "Credibility Divergence",
      "severity": "RED",
      "trigger": "Experiment 3 shows oscillation or unbounded cascade",
      "action": "Abandon Subjective Logic; evaluate alternatives"
    },
    {
      "flag": "Cost Overrun",
      "severity": "AMBER",
      "trigger": "System cost exceeds 80% of replication",
      "action": "Reassess value proposition; pivot to quality-over-cost argument"
    },
    {
      "flag": "Platform Convergence",
      "severity": "AMBER",
      "trigger": "Major framework adds structured per-output verification",
      "action": "Evaluate contribution vs. competition"
    },
    {
      "flag": "Adversarial Weakness",
      "severity": "AMBER",
      "trigger": "Probing F1 < VTD-only F1",
      "action": "Replace probing with ensemble verification or human review"
    },
    {
      "flag": "Collusion Detection Failure",
      "severity": "AMBER",
      "trigger": "Sentinel fails to detect collusion at f > 0.15",
      "action": "Strengthen detection or increase deep-audit percentage"
    },
    {
      "flag": "Regulatory Alignment",
      "severity": "INFO",
      "trigger": "Regulators specify output verification requirements",
      "action": "Align VTD format with regulatory requirements"
    }
  ]
}
```

---

*Feasibility verdict completed 2026-03-09. Assessment Council: Advocate, Skeptic, Arbiter.*
*Protocol: Assessment Council v2.0*
