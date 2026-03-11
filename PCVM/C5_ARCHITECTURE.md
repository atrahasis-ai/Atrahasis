# Proof-Carrying Verification Membrane (PCVM) — System Architecture
## C5 DESIGN Document

**Invention ID:** C5
**Concept:** C5-B (Proof-Carrying Verification Membrane)
**Stage:** DESIGN
**Version:** v0.1
**Date:** 2026-03-09
**Status:** DRAFT
**Assessment Council Verdict:** CONDITIONAL_ADVANCE
**Feasibility Score:** Novelty 4/5, Feasibility 3/5, Impact 4/5, Risk 6/10

---

## 1. Executive Summary

The Proof-Carrying Verification Membrane (PCVM) is the execution engine for claim verification within the Tidal Noosphere. It replaces Verichain's replication-based consensus with a graduated verification architecture: every agent output carries a Verification Trace Document (VTD) — a structured evidence package whose form and depth vary by claim class. The membrane checks the VTD rather than re-executing computation.

PCVM operates underneath the Noosphere's governance layer. The Noosphere determines WHAT gets verified (all claims entering durable memory), WHO verifies (VRF-selected committees from pre-stratified diversity pools), and WHEN verification occurs (tidal epoch scheduling). PCVM determines HOW verification executes — by dispatching claims through class-specific verification pathways, composing credibility using Subjective Logic, and defending against adversarial manipulation through random deep-audit and automated probing.

**Core architectural decisions:**

1. **Graduated VTD Model.** Three verification tiers: formal proofs (Tier 1: D-class, C-class), structured evidence (Tier 2: E-class, S-class, P-class, R-class), and structured attestations (Tier 3: H-class, N-class). This replaces the original universal proof-checking claim with an honest graduated model.

2. **Membrane-Assigned Classification.** The membrane, not the producing agent, assigns final claim classifications. Agents propose; the membrane decides. This addresses the Class Downgrade adversarial attack (Attack 3).

3. **Subjective Logic Credibility.** Opinion tuples (b, d, u, a) compose through conjunction, discounting, and consensus operators. Credibility is tracked per agent per claim class.

4. **Random Deep-Audit.** 5-10% of passed VTDs undergo full-replication verification as a deterrence mechanism against forgery and collusion.

5. **Unified Membrane.** A single membrane with graduated depth rather than three separate systems. This preserves membrane sovereignty (INV-1, INV-2), enables cross-class credibility composition, and reduces engineering complexity.

**Honest cost model:** Verification cost drops for Tier 1 classes (0.1x-0.35x of replication). Tier 2 shows moderate improvement (0.5x-0.8x). Tier 3 shows no improvement or increased cost (1.0x-2.0x). System-level cost reduction of 40-60% is achieved through selective verification and downstream trust propagation.

---

## 2. Architectural Position

### 2.1 Stack Position

```
CIOS (orchestration)
    |
    v
Tidal Noosphere (coordination)
    |  Provides: VRF dual defense, constitutional protections,
    |  MQI drift detection, Sentinel Graph, V-class algebra,
    |  tidal epoch scheduling, settlement integration
    |
    v
PCVM (verification) <-- THIS DOCUMENT
    |  Provides: VTD generation/checking, claim classification,
    |  tier-specific verification, credibility composition,
    |  adversarial probing, deep-audit, knowledge admission
    |
    v
Knowledge Cortex (persistent memory)
    |  Provides: BDL persistence, re-verification triggers,
    |  dependency graph, knowledge evolution
    |
    v
Settlement Plane (AIC economy)
       Provides: verification rewards, quality scoring,
       economic incentives for honest verification
```

### 2.2 Sovereignty Boundary

PCVM operates within the Verification Membrane's sovereignty boundary defined by INV-1 and INV-2:

- **INV-1:** No claim enters durable memory without passing PCVM.
- **INV-2:** The membrane cannot be weakened by any non-constitutional action.

PCVM's internal parameters (verification thresholds, VTD schema requirements, audit percentages) are constitutionally protected. Changes require G-class consensus (75% supermajority, 72-hour discussion for HIGH safety class).

### 2.3 Interface Summary

PCVM exposes five integration surfaces:

| Interface | Direction | Protocol |
|-----------|-----------|----------|
| Tidal Noosphere | Inbound: committees, epochs, V-class ops | V-class operation dispatch |
| Knowledge Cortex | Outbound: MCTs, BDLs; Inbound: re-verify triggers | BDL admission protocol |
| Settlement Plane | Outbound: quality scores; Inbound: reward signals | Settlement integration API |
| Sentinel Graph | Outbound: metrics; Inbound: anomaly alerts | Sentinel monitoring protocol |
| ASV (C4) | Inbound: claim semantics, provenance chains | CLM/PRV/EVD token interface |

### 2.4 What PCVM Replaces

| Verichain (deprecated) | PCVM (replacement) |
|------------------------|-------------------|
| Replication-based consensus | VTD proof-checking + evidence evaluation |
| Binary pass/fail | Credibility opinion tuple (b, d, u, a) |
| O(replication) for all claims | Variable cost by claim class |
| Untyped claims | 8-class typed claims with class-specific VTDs |
| Verification result stored as boolean | VTD stored permanently for audit and re-verification |
| No adversarial component | Selective adversarial probing + random deep-audit |
| No credibility propagation | Subjective Logic composition through dependency graphs |

---

## 3. Hard Gate Experiment Designs

The Assessment Council mandated four hard gates. Each must be satisfied before the corresponding design area is finalized.

### 3.1 GATE-1: VTD Feasibility Experiment

#### 3.1.1 Motivation

The VTD model is PCVM's core innovation. If VTDs cannot be constructed at reasonable cost and checked with sufficient error detection, the architecture collapses to a documentation standard rather than a verification membrane. This gate validates that VTDs provide genuine verification value.

#### 3.1.2 Experiment Setup

**Claim corpus:** 80 claims total, 10 per claim class. Claims sourced from C1-C4 pipeline outputs with the following distribution:

| Class | Source | Claim Examples |
|-------|--------|---------------|
| D (10) | C3 hash computations, scheduling proofs | "Hash ring lookup returns agent X for key K" |
| E (10) | C4 prior art citations, C3 landscape claims | "GPT-4 scores 86.4% on MMLU" |
| S (10) | C3 load balance statistics, C5 cost model claims | "Bounded-loads hashing achieves max/avg < 1.15" |
| H (10) | C3 architectural decisions, C4 design choices | "Microservices architecture is preferred" |
| N (10) | C3 constitutional parameters, C4 ethical positions | "Privacy takes precedence over analytics" |
| P (10) | C3 PTP protocol steps, C4 pipeline stage traces | "Research followed 5-step RESEARCH protocol" |
| R (10) | C3 I-confluence proofs, C5 logical arguments | "If A implies B and B implies C, then A implies C" |
| C (10) | C3 governance compliance, regulatory claims | "System complies with EU AI Act Article 11" |

**Error injection:** For each class, 3 of 10 claims contain deliberate errors:
- 1 factual error (wrong value, false citation)
- 1 logical error (invalid inference, unsupported conclusion)
- 1 omission error (missing critical evidence or counterevidence)

**VTD construction:** Each claim is paired with a VTD constructed according to the class-specific schema (Section 6). Construction cost is measured in tokens (LLM API calls) and wall-clock time.

#### 3.1.3 Procedure

For each claim:

1. **Construct VTD.** Generate VTD according to class schema. Record: token count for VTD construction (C_vtd), time elapsed, VTD size in bytes.

2. **Check VTD (automated).** Run structural validation, completeness check, consistency check, and grounding check. Record: token count for checking (C_check), time elapsed, verdict (pass/fail with reason).

3. **Check VTD (human baseline).** Three human evaluators independently assess each claim+VTD pair. Record: time per evaluator, verdict, confidence.

4. **Replicate (baseline).** Re-execute the task that produced the claim. Record: token count for replication (C_replicate), time elapsed, whether replication detects the injected error.

5. **Compare.** For each claim, record:
   - Did VTD checking detect the error? (true/false)
   - Did replication detect the error? (true/false)
   - Cost ratio: (C_vtd + C_check) / C_replicate
   - Human agreement with automated verdict (kappa)

#### 3.1.4 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Error detection rate (VTD checking) | >= 80% across all 24 error-injected claims |
| Per-class error detection | >= 2 of 3 errors detected for at least 6 of 8 classes |
| Cost ratio (VTD construction + checking vs replication) | < 0.50 for at least 4 of 8 classes |
| VTD structural validity rate | >= 95% of VTDs pass schema validation |
| Human-automated agreement | Cohen's kappa >= 0.70 |

#### 3.1.5 Kill Criteria

- **KILL-G1-A:** VTD checking achieves < 80% error detection rate at < 50% replication cost for fewer than 4 of 8 classes. The VTD model provides insufficient value.
- **KILL-G1-B:** Error detection for any Tier 1 class (D, C) falls below 90%. Formal proof checking must be near-perfect for decidable classes.
- **KILL-G1-C:** VTD construction cost exceeds 100% of original claim production cost for any class. The overhead is prohibitive.

#### 3.1.6 Fallback

If GATE-1 fails, descope PCVM to Tier 1 classes only (D, P, C) where proof-checking provides clear value. Tier 2 and Tier 3 revert to enhanced replication with structured metadata.

---

### 3.2 GATE-2: Claim Classification Reliability

#### 3.2.1 Motivation

The 8-class taxonomy's value depends on reliable classification. If claims cannot be consistently classified, differential proof obligations become meaningless. The Adversarial Report (Attack 3) identifies classification gaming as a HIGH-severity attack.

#### 3.2.2 Experiment Setup

**Claim corpus:** 200 claims, 25 per class, sourced from C1-C4 pipeline outputs and synthetic generation. Claims include:
- 160 unambiguous claims (20 per class, clearly belonging to one class)
- 40 ambiguous claims (5 per class, plausibly belonging to 2+ classes)

**Classifiers:** 5 independent classifiers:
- 3 human domain experts (trained on taxonomy documentation)
- 2 LLM-based classifiers (prompted with taxonomy definition and examples)

**Classification protocol:**
1. Each classifier receives: claim text, claim context (source document), and taxonomy reference card.
2. Each classifier assigns: primary class, optional secondary class, confidence (1-5).
3. Classifiers work independently with no communication.

#### 3.2.3 Procedure

1. Each classifier classifies all 200 claims independently.
2. Compute Fleiss' kappa for all 5 classifiers across 200 claims.
3. Compute per-class kappa (agreement on "is this class X?" for each class).
4. Analyze confusion matrix: which class pairs are most commonly confused?
5. For ambiguous claims: compute whether classifiers agree on primary or secondary class.
6. Test membrane-assigned classification: run a 6th classifier (membrane simulator) that uses majority vote of the 5 classifiers as ground truth, then measures agreement with individual classifiers.

#### 3.2.4 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Fleiss' kappa (all classifiers, all claims) | >= 0.60 (substantial agreement) |
| Per-class kappa | >= 0.55 for at least 6 of 8 classes |
| Unambiguous claim accuracy | >= 85% of unambiguous claims correctly classified by >= 4 of 5 classifiers |
| Ambiguous claim secondary agreement | >= 60% of ambiguous claims have secondary class agreement among >= 3 of 5 classifiers |
| Membrane classifier accuracy vs majority vote | >= 0.85 |

#### 3.2.5 Kill Criteria

- **KILL-G2-A:** Fleiss' kappa < 0.60. The taxonomy is too ambiguous for reliable classification.
- **KILL-G2-B:** Any class has per-class kappa < 0.40 (below "fair agreement"). That class is not reliably distinguishable.

#### 3.2.6 Fallback

If GATE-2 fails at kappa < 0.60, simplify taxonomy:
- Merge H + N into "Judgment" class
- Merge E + S into "Evidence-Based" class
- Keep D, P/C (merged), R
- Result: 5-class taxonomy. Re-test with same corpus.

If kappa < 0.50 (RED flag), the 8-class taxonomy is fundamentally unstable. Redesign with 3 classes aligned to verification tiers.

---

### 3.3 GATE-3: Credibility Propagation Stability

#### 3.3.1 Motivation

Subjective Logic composition must converge stably when propagated through knowledge graph dependencies. If small changes in one claim's credibility cascade unboundedly through the graph, the credibility system is unusable.

#### 3.3.2 Experiment Setup

**Dependency graph:** 500 claims connected by dependency edges. Graph structure:
- 500 nodes (claims), classified across all 8 classes proportionally
- ~1,500 directed edges (average out-degree 3, representing "claim A depends on claims B, C, D")
- 50 cycles of length 3-7 (representing mutual dependencies)
- 20 "hub" claims with in-degree > 15 (highly-cited foundational claims)
- 10 "leaf" claims with out-degree 0 (terminal empirical observations)

**Initial credibility assignment:**
- Leaf claims: opinion tuple assigned from uniform random in valid space
- All other claims: credibility computed by propagation from dependencies

**Perturbation protocol:**
- Select a random non-leaf claim
- Perturb its local evidence: shift belief by delta_b in [-0.1, +0.1], adjust u correspondingly
- Propagate credibility changes through the graph
- Measure: number of iterations to convergence, maximum cascade magnitude at each graph distance

#### 3.3.3 Procedure

1. **Initialize graph.** Assign random valid opinion tuples to leaf claims. Propagate using Subjective Logic conjunction (for dependent claims) and discounting (for agent-reported claims). Use iterative dampening with alpha = 0.85.

2. **Measure convergence.** Record iterations until all claims' opinion tuples change by < epsilon = 0.001 between iterations. Record maximum change per iteration.

3. **Perturbation sweep.** For each of 100 random perturbations:
   a. Apply perturbation to one claim.
   b. Re-propagate.
   c. Record: iterations to re-convergence, cascade magnitude at distance 1, 2, 3, 4, 5+.
   d. Record: maximum change experienced by any claim in the graph.

4. **Stress test.** Apply 10 simultaneous perturbations (different claims). Measure convergence behavior.

5. **Scale test.** Repeat with 2,000-claim and 5,000-claim graphs (same density ratios).

#### 3.3.4 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| Initial convergence | < 100 iterations for 500-claim graph |
| Re-convergence after single perturbation | < 50 iterations |
| Cascade attenuation | delta_b = 0.1 perturbation causes < 0.03 change at distance >= 3 |
| No oscillation | Monotonic convergence (no change reversal after iteration 10) |
| Scale behavior | Convergence iterations grow < O(N) with graph size |
| Stress convergence | 10 simultaneous perturbations converge in < 150 iterations |

#### 3.3.5 Kill Criteria

- **KILL-G3-A:** Propagation does not converge within 100 iterations on 500-claim graph. Subjective Logic composition is unsuitable for this graph topology.
- **KILL-G3-B:** A 0.1 change in one claim's belief cascades to > 0.3 change in claims at graph distance > 3. The composition algebra amplifies rather than attenuates uncertainty.
- **KILL-G3-C:** Oscillation detected (non-monotonic convergence) in > 5% of perturbation trials. The dampening factor is insufficient.

#### 3.3.6 Fallback

If GATE-3 fails:
1. Replace Subjective Logic with min-credibility chains (credibility of a claim = minimum credibility of any dependency). Simpler, guaranteed to converge, but loses uncertainty information.
2. Abandon continuous re-verification. Credibility is computed once at verification time and not updated when dependencies change.
3. Increase dampening (alpha = 0.70). Re-test. If still fails, composition algebra is fundamentally unsuitable.

---

### 3.4 GATE-4: Adversarial Probing Effectiveness

#### 3.4.1 Motivation

Adversarial probing is PCVM's defense against VTD forgery and strategic omission. If probing does not meaningfully improve error detection over VTD-only checking, the probing subsystem adds cost without value.

#### 3.4.2 Experiment Setup

**Claim corpus:** 100 claims across Tier 2 and Tier 3 classes (probing is not applied to Tier 1):
- 15 E-class, 15 S-class, 15 P-class, 15 R-class, 20 H-class, 20 N-class
- 30 claims (30%) contain inserted errors of varying sophistication:
  - 10 obvious errors (factual mistakes, broken citations)
  - 10 subtle errors (valid-looking but incorrect statistics, plausible but unsupported reasoning)
  - 10 adversarial errors (deliberately crafted to resist probing: inoculated VTDs per Attack 4)

**Verification conditions (each claim evaluated under all three):**
1. **Replication only:** Re-execute the task. Check if output matches. Record: cost, error detected (y/n).
2. **VTD-only:** Check VTD structural validity, completeness, consistency, grounding. No probing. Record: cost, error detected (y/n).
3. **VTD + adversarial probing:** Full PCVM pipeline including automated probing. Record: cost, error detected (y/n), probe type that detected error.

#### 3.4.3 Procedure

1. For each claim, run all three verification conditions.
2. Compute per-condition: precision, recall, F1 score.
3. Compute cost ratios: VTD-only / replication, VTD+probing / replication.
4. Analyze by error sophistication: does probing improve detection of subtle and adversarial errors more than obvious ones?
5. Analyze by claim class: which classes benefit most from probing?
6. Record probe type effectiveness: which probe types (counterexample search, assumption exposure, source challenge, logical fallacy detection) contribute most to error detection?

#### 3.4.4 Success Criteria

| Criterion | Threshold |
|-----------|-----------|
| VTD+probing F1 | > 0.80 overall |
| VTD+probing F1 for adversarial errors | > 0.60 |
| VTD+probing cost | < 2x replication cost overall |
| Probing marginal value | VTD+probing F1 > VTD-only F1 by at least 0.10 |
| Per-class probing value | Probing improves F1 for at least 4 of 6 probed classes |

#### 3.4.5 Kill Criteria

- **KILL-G4-A:** VTD+probing F1 < 0.80 or cost > 2x replication. Probing is not cost-effective.
- **KILL-G4-B:** VTD+probing F1 is not statistically significantly better than VTD-only F1 (p > 0.05). Probing adds cost without value.
- **KILL-G4-C:** Adversarial error detection F1 < 0.40. Probing cannot handle sophisticated adversaries.

#### 3.4.6 Fallback

If GATE-4 fails:
1. Replace automated probing with ensemble verification (multiple independent VTD checks by different verifiers). Lower sophistication but potentially higher error detection through diversity.
2. Reserve probing for only the highest-stakes claims (top 10% by declared importance). Reduce cost exposure.
3. If probing is fundamentally ineffective, rely on deep-audit (random replication) as the sole adversarial defense.

---

## 4. Component Architecture

### 4.1 VTD Engine

**Purpose:** Generates, validates, and stores Verification Trace Documents. The VTD Engine is the core data structure manager for PCVM.

**Inputs:**
- `claim`: the agent's output claim (CLM token from ASV)
- `agent_id`: producing agent identifier
- `proposed_class`: agent's proposed claim classification
- `evidence_bundle`: raw evidence the agent provides (sources, traces, logs)
- `vtd_schema`: class-specific VTD schema (from Schema Registry)

**Outputs:**
- `vtd`: constructed VTD conforming to class-specific schema
- `vtd_hash`: content-addressable hash of VTD for deduplication and reference
- `structural_validity`: boolean result of schema validation
- `completeness_score`: fractional completeness of required fields [0.0, 1.0]

**Internal Components:**

```
+------------------------------------------------------------------+
|                         VTD ENGINE                                |
|                                                                   |
|  +----------------+    +------------------+    +---------------+  |
|  | Schema Registry|    | VTD Constructor  |    | VTD Validator |  |
|  | (8 class       |--->| (assembles VTD   |--->| (structural,  |  |
|  |  schemas,      |    |  from evidence   |    |  completeness,|  |
|  |  versioned)    |    |  bundle)         |    |  consistency) |  |
|  +----------------+    +------------------+    +-------+-------+  |
|                                                        |          |
|  +----------------+    +------------------+    +-------v-------+  |
|  | VTD Store      |<---| Hash Computer    |<---| Grounding     |  |
|  | (content-      |    | (SHA-256 of      |    | Checker       |  |
|  |  addressed,    |    |  canonical VTD)  |    | (terminal     |  |
|  |  append-only)  |    |                  |    |  claim refs)  |  |
|  +----------------+    +------------------+    +---------------+  |
+------------------------------------------------------------------+
```

**Schema Registry:** Stores versioned JSON schemas for each of the 8 claim classes. Schemas are constitutionally protected (G-class changes only). Each schema defines:
- Required fields for that class
- Optional fields
- Field types and constraints
- Size limits per field (addressing Attack 7: VTD Explosion)
- Counter-evidence requirements (addressing Attack 2: Strategic Omission)

**VTD Constructor:** Assembles a VTD from the agent's evidence bundle:

```
function construct_vtd(claim, evidence_bundle, schema):
    vtd = new VTD()
    vtd.header = {
        claim_hash: hash(claim),
        producer_id: claim.agent_id,
        proposed_class: claim.proposed_class,
        assigned_class: null,  // filled by Claim Classifier
        timestamp: now(),
        epoch: current_epoch(),
        vtd_version: schema.version
    }

    vtd.evidence = map_evidence_to_schema(evidence_bundle, schema)

    vtd.counter_evidence = {
        considered: evidence_bundle.counter_evidence || [],
        search_performed: evidence_bundle.counter_search_log || false,
        none_found_attestation: len(evidence_bundle.counter_evidence) == 0
    }

    vtd.metadata = {
        construction_cost_tokens: track_tokens(),
        size_bytes: sizeof(vtd),
        dependency_claims: extract_claim_references(evidence_bundle)
    }

    return vtd
```

**VTD Validator:** Performs four sequential checks:

1. **Structural validation:** VTD conforms to JSON schema for assigned class. All required fields present, correct types.
2. **Completeness check:** All required evidence fields populated with non-trivial content. Completeness score = filled_required_fields / total_required_fields.
3. **Consistency check:** No internal contradictions in evidence chain. Sources cited consistently. Numerical values consistent across references.
4. **Grounding check:** Every terminal claim in the evidence chain either (a) references a verified claim with credibility >= class threshold, (b) is a constitutional axiom, or (c) is an empirical observation with cited source.

**VTD Size Limits (per class, addressing Attack 7):**

| Class | Max VTD Size | Max Sources | Max Reasoning Steps | Rationale |
|-------|-------------|-------------|--------------------|-----------|
| D | 10 KB | N/A | N/A | Proof traces are compact |
| E | 50 KB | 20 | N/A | Source-heavy but bounded |
| S | 30 KB | 10 | N/A | Statistical metadata is structured |
| H | 100 KB | 15 | 50 | Reasoning traces can be lengthy |
| N | 80 KB | 10 | 30 | Value analysis with stakeholder mapping |
| P | 40 KB | N/A | N/A | Process logs are structured |
| R | 30 KB | N/A | 100 | Long inference chains possible |
| C | 50 KB | 20 | N/A | Requirement mappings can be detailed |

Claims exceeding size limits are rejected with guidance to decompose into smaller claims.

**VTD Store:** Content-addressed, append-only storage. VTDs are never deleted (audit trail requirement). VTDs are indexed by:
- `vtd_hash` (primary key)
- `claim_hash` (lookup by claim)
- `producer_id` (lookup by agent)
- `assigned_class` (lookup by class)
- `epoch` (temporal queries)
- `credibility_tuple` (range queries on belief/uncertainty)

**Failure Modes:**
- *Schema version mismatch:* VTD constructed against older schema version. Accept if backward-compatible; reject if breaking change. Grace period: 5 epochs after schema update.
- *Evidence bundle incomplete:* Constructor produces VTD with completeness < 1.0. Validator flags. Claim enters "provisional" state pending evidence supplementation.
- *VTD Store full:* Archival policy moves VTDs older than retention window (configurable, default 1000 epochs) to cold storage. Active VTDs always in hot storage.

---

### 4.2 Claim Classifier

**Purpose:** Assigns each claim to one of 8 claim classes based on its epistemic status and verification modality. Implements membrane-assigned classification (REQ-2) where the membrane makes the final classification decision.

**Classification Protocol:**

```
function classify_claim(claim, proposed_class, agent_credibility):
    // Phase 1: Feature extraction
    features = extract_classification_features(claim)
    // Features include:
    //   - linguistic markers (quantifiers, hedges, value terms)
    //   - structural markers (citations, statistics, logical connectives)
    //   - context markers (source document type, agent role)
    //   - epistemic markers (certainty expressions, evidence references)

    // Phase 2: Multi-classifier ensemble
    classifier_votes = []
    for classifier in [rule_based_classifier, llm_classifier_1, llm_classifier_2]:
        vote = classifier.classify(claim, features)
        classifier_votes.append(vote)

    // Phase 3: Membrane decision
    majority_class = majority_vote(classifier_votes)
    confidence = agreement_fraction(classifier_votes)

    // Phase 4: Agent proposal comparison
    if proposed_class == majority_class:
        assigned_class = majority_class
        classification_flag = AGREED
    elif proposed_class in secondary_classes(classifier_votes):
        // Agent proposed a class that at least one classifier agrees with
        assigned_class = majority_class  // membrane wins
        classification_flag = OVERRIDDEN_MINOR
    else:
        // Agent proposed a class no classifier agrees with
        assigned_class = majority_class
        classification_flag = OVERRIDDEN_MAJOR
        log_classification_dispute(claim, proposed_class, majority_class)

    // Phase 5: Multi-class handling
    secondary = detect_secondary_classes(features, classifier_votes)
    if len(secondary) > 0:
        // Claim spans multiple classes
        // VTD must satisfy ALL applicable proof obligations
        assigned_classes = [assigned_class] + secondary

    return ClassificationResult(
        primary_class = assigned_class,
        secondary_classes = secondary,
        confidence = confidence,
        flag = classification_flag,
        classifier_votes = classifier_votes
    )
```

**Rule-Based Classifier:** Deterministic rules derived from the epistemic status x verification modality matrix:

| Feature Pattern | Assigned Class |
|----------------|---------------|
| Contains computation trace + deterministic inputs/outputs | D |
| Cites external sources as primary evidence | E |
| Contains statistical test results (p-values, CIs, sample sizes) | S |
| Expresses judgment with alternatives considered | H |
| Invokes values, ethics, or constitutional principles | N |
| References process log or procedural steps | P |
| Contains explicit logical premises and inference steps | R |
| Maps to regulatory requirements or compliance criteria | C |

**LLM Classifiers:** Two independent LLM instances prompted with:
- Taxonomy definition with examples (from Section 6)
- The claim text and context
- Instruction to classify and provide confidence

Using two independent LLM classifiers provides defense-in-depth against individual classifier bias.

**Classification Dispute Resolution:**

When `classification_flag == OVERRIDDEN_MAJOR`:
1. Dispute is logged with full context (claim, proposed class, assigned class, classifier votes).
2. Agent is notified of override with explanation.
3. Agent may request re-classification with additional context (one re-try per claim).
4. Disputes accumulate per agent. Agents with > 20% OVERRIDDEN_MAJOR rate trigger Sentinel Graph review.
5. Aggregate disputes feed taxonomy refinement (if a class pair is consistently confused, consider merger or clearer differentiation).

**Anti-Gaming Measures (addressing Attack 3: Class Downgrade):**

1. **Agent does not control final class.** The membrane decides.
2. **Class downgrade detection.** If an agent consistently proposes lower-tier classes than the membrane assigns, a pattern emerges. Agents with downgrade rate > 30% receive credibility penalty.
3. **Re-classification at audit.** During deep-audit (Section 4.8), the claim is re-classified by an independent classifier. If the audit classification disagrees with the original, the original verification result is invalidated.

**Failure Modes:**
- *Classifier disagreement (all three vote differently):* Assign the class with highest prior probability for the claim's context. Flag for human review.
- *Novel claim type:* If no class achieves > 0.5 confidence, assign H-class (heuristic) as default and flag for taxonomy review.
- *Classifier model degradation:* Sentinel Graph monitors classification accuracy via deep-audit re-classification agreement. If accuracy drops below 0.75, trigger classifier retraining.

---

### 4.3 Verification Dispatcher

**Purpose:** Routes classified claims to the appropriate tier-specific verification pathway. The dispatcher is the central coordination point within PCVM.

**Dispatch Logic:**

```
function dispatch_verification(claim, vtd, classification, committee):
    tier = get_tier(classification.primary_class)

    // Determine verification depth based on claim stakes
    stakes = assess_stakes(claim)  // LOW, MEDIUM, HIGH, CRITICAL
    probe_required = should_probe(tier, stakes, producer_credibility(claim.agent_id))

    // Route to tier-specific verifier
    match tier:
        case TIER_1:
            result = proof_checker.verify(claim, vtd, committee)
            // No probing for Tier 1 (decidable verification)

        case TIER_2:
            result = evidence_evaluator.evaluate(claim, vtd, committee)
            if probe_required:
                probe_result = adversarial_prober.probe(claim, vtd, classification)
                result = merge_results(result, probe_result)

        case TIER_3:
            result = attestation_reviewer.review(claim, vtd, committee)
            // Tier 3 always probed (adversarial probing is integral)
            probe_result = adversarial_prober.probe(claim, vtd, classification)
            result = merge_results(result, probe_result)

    // Deep-audit lottery
    if random() < deep_audit_rate(classification.primary_class):
        queue_deep_audit(claim, vtd, result)

    // Compose credibility opinion
    opinion = credibility_engine.compose(result, committee, classification)

    // Knowledge admission decision
    if opinion.projected_probability() >= admission_threshold(classification.primary_class):
        mct = issue_mct(claim, vtd, opinion)
        knowledge_gate.admit(claim, mct, vtd)
    else:
        reject(claim, vtd, opinion, result.reasons)

    return VerificationOutcome(claim, opinion, result, mct_or_rejection)
```

**Stakes Assessment:**

```
function assess_stakes(claim):
    factors = {
        dependency_count: count_claims_depending_on(claim),
        producer_class_credibility: get_class_credibility(claim.agent_id, claim.class),
        claim_scope: estimate_scope(claim),  // LOCAL, PARCEL, LOCUS, GLOBAL
        constitutional_relevance: check_constitutional_reference(claim)
    }

    score = weighted_sum(factors, weights={
        dependency_count: 0.3,      // high-dependency claims are high-stakes
        producer_class_credibility: -0.2,  // low credibility = higher scrutiny
        claim_scope: 0.3,           // broader scope = higher stakes
        constitutional_relevance: 0.2  // constitutional claims are high stakes
    })

    if score > 0.7: return CRITICAL
    if score > 0.5: return HIGH
    if score > 0.3: return MEDIUM
    return LOW
```

**Probing Trigger Logic:**

```
function should_probe(tier, stakes, producer_credibility):
    if tier == TIER_1: return false   // Tier 1 is decidable; probing unnecessary
    if tier == TIER_3: return true    // Tier 3 always probed
    // Tier 2: probe based on stakes and credibility
    if stakes >= HIGH: return true
    if stakes == MEDIUM and producer_credibility < 0.6: return true
    if random() < base_probe_rate: return true  // random probing for deterrence
    return false
```

Where `base_probe_rate` is a constitutional parameter (default: 0.15, meaning 15% of MEDIUM/LOW-stakes Tier 2 claims are randomly probed).

**Failure Modes:**
- *Committee unavailable:* Defer verification to next epoch. Claim enters pending queue. If pending for > 3 epochs, assign emergency committee via VRF re-draw.
- *Verification timeout:* If verification does not complete within epoch, partial result is stored. Remaining verification continues in next epoch. Claim remains provisional.
- *Dispatcher overload:* Priority queue ensures HIGH and CRITICAL stakes claims are processed first. LOW stakes claims may be deferred during high-load epochs.

---

### 4.4 Proof Checker (Tier 1)

**Purpose:** Verifies Tier 1 claims (D-class, C-class) through machine-checkable proof validation. This is where the "proof-carrying" name most accurately applies.

**D-Class Verification Protocol:**

```
function verify_d_class(claim, vtd, committee):
    // Step 1: Parse proof object from VTD
    proof = vtd.evidence.proof_object
    inputs = vtd.evidence.inputs
    expected_output = claim.value

    // Step 2: Verify proof structure
    if not valid_proof_format(proof):
        return Rejection("Invalid proof format")

    // Step 3: Check proof (sublinear — check proof, don't recompute)
    match proof.type:
        case COMPUTATION_TRACE:
            // Verify trace is internally consistent
            // Spot-check random intermediate steps (not all)
            check_points = select_random_checkpoints(proof.trace, count=5)
            for cp in check_points:
                if not recompute_step(cp.input, cp.operation) == cp.output:
                    return Rejection("Trace verification failed at step " + cp.index)
            // Verify final output matches claim
            if proof.trace.final_output != expected_output:
                return Rejection("Output mismatch")

        case FORMAL_CERTIFICATE:
            // Machine-check proof certificate (e.g., Coq/Lean proof term)
            if not proof_kernel.check(proof.certificate, claim.proposition):
                return Rejection("Proof certificate invalid")

        case HASH_PREIMAGE:
            // Verify hash(preimage) == claimed_hash
            if hash(proof.preimage) != expected_output:
                return Rejection("Hash mismatch")

    // Step 4: Committee attestation
    // Each committee member independently runs Steps 1-3
    // Aggregate: unanimous agreement required for D-class
    attestations = collect_committee_attestations(committee, claim, vtd)
    if not all(a.verdict == VERIFIED for a in attestations):
        return Rejection("Committee disagreement", attestations)

    return Verified(
        opinion = (b=1.0, d=0.0, u=0.0, a=0.5),  // D-class: binary
        proof_type = proof.type,
        verification_cost = sum(a.cost for a in attestations)
    )
```

**C-Class Verification Protocol:**

```
function verify_c_class(claim, vtd, committee):
    // Step 1: Parse compliance mapping from VTD
    regulation = vtd.evidence.regulation_reference
    requirements = vtd.evidence.requirement_mapping
    evidence = vtd.evidence.conformance_evidence

    // Step 2: Verify regulation reference
    if not constitutional_registry.contains(regulation):
        return Rejection("Unknown regulation: " + regulation.id)

    // Step 3: Verify requirement completeness
    known_requirements = constitutional_registry.get_requirements(regulation)
    mapped_requirements = set(r.id for r in requirements)
    missing = known_requirements - mapped_requirements
    if len(missing) > 0:
        return Rejection("Missing requirement mappings: " + missing)

    // Step 4: Verify each requirement mapping
    for req in requirements:
        if not evidence_covers_requirement(evidence[req.id], req):
            return Rejection("Insufficient evidence for " + req.id)

    // Step 5: Committee attestation
    attestations = collect_committee_attestations(committee, claim, vtd)
    threshold = 0.8  // C-class: 80% committee agreement (not unanimous)
    if fraction_verified(attestations) < threshold:
        return Rejection("Below committee threshold", attestations)

    return Verified(
        opinion = (b=fraction_verified(attestations), d=1-fraction_verified(attestations), u=0.0, a=0.5),
        compliance_status = COMPLIANT,
        verification_cost = sum(a.cost for a in attestations)
    )
```

**Performance Characteristics:**
- D-class verification cost: ~0.01x-0.11x of replication (sublinear proof checking)
- C-class verification cost: ~0.15x-0.35x of replication (checklist verification)
- Average verification time: < 1 second for D-class, < 5 seconds for C-class

**Failure Modes:**
- *Proof format unrecognized:* Fall back to full replication. Log for schema extension.
- *Proof kernel unavailable:* Queue for next epoch when kernel is available. Do not approximate formal verification.
- *Spot-check failure:* Any single spot-check failure immediately rejects the claim. No tolerance for partial proof validity.

---

### 4.5 Evidence Evaluator (Tier 2)

**Purpose:** Evaluates Tier 2 claims (E-class, S-class, P-class, R-class) through structured evidence assessment. This is where PCVM provides moderate cost improvement with richer verification metadata than replication.

**E-Class (Empirical) Verification Protocol:**

```
function verify_e_class(claim, vtd, committee):
    sources = vtd.evidence.source_citations

    // Step 1: Mandatory source verification (REQ-1)
    for source in sources:
        // Actually fetch and check cited sources
        source_check = verify_source(source)
        if not source_check.accessible:
            flag_inaccessible_source(source)
        if source_check.accessible:
            if not source_check.quote_matches:
                return Rejection("Quote mismatch: " + source.url)
            if not source_check.content_hash_matches:
                flag_content_changed(source, source_check.current_hash)

    // Step 2: Cross-reference check
    cross_refs = vtd.evidence.cross_references
    confirming = sum(1 for cr in cross_refs if cr.confirms)
    contradicting = sum(1 for cr in cross_refs if not cr.confirms)

    // Step 3: Counter-evidence assessment (Attack 2 mitigation)
    counter = vtd.counter_evidence
    if not counter.search_performed:
        credibility_penalty = 0.1  // penalize claims that didn't search for counter-evidence
    elif len(counter.considered) == 0 and counter.none_found_attestation:
        credibility_penalty = 0.05  // mild skepticism for "no counter-evidence found"
    else:
        credibility_penalty = 0.0

    // Step 4: Compute evidence strength
    evidence_strength = compute_evidence_strength(
        sources_verified = sum(1 for s in sources if verify_source(s).valid),
        total_sources = len(sources),
        cross_refs_confirming = confirming,
        cross_refs_contradicting = contradicting,
        recency = min(s.retrieved_date for s in sources)
    )

    // Step 5: Committee evaluation
    attestations = collect_committee_attestations(committee, claim, vtd)
    committee_agreement = weighted_agreement(attestations)

    return Verified(
        opinion = compute_opinion(evidence_strength, committee_agreement, credibility_penalty),
        source_verification_results = source_checks,
        verification_cost = sum(a.cost for a in attestations)
    )
```

**Source Verification Protocol (REQ-1 implementation):**

```
function verify_source(source):
    result = SourceVerification()

    // Level 1: Accessibility
    response = fetch(source.url, timeout=10s)
    result.accessible = response.status == 200

    if not result.accessible:
        // Try archive.org fallback
        archive_url = "https://web.archive.org/web/" + source.url
        response = fetch(archive_url, timeout=10s)
        result.accessible = response.status == 200
        result.from_archive = true

    if not result.accessible:
        return result  // Cannot verify inaccessible source

    // Level 2: Content hash comparison
    result.current_hash = hash(response.body)
    result.content_hash_matches = (result.current_hash == source.content_hash)

    // Level 3: Quote accuracy
    if source.quoted_text:
        result.quote_matches = fuzzy_match(source.quoted_text, response.body, threshold=0.9)

    // Level 4: Contextual relevance
    result.contextually_relevant = assess_relevance(source.relevance_justification, response.body)

    return result
```

**S-Class (Statistical) Verification Protocol:**

```
function verify_s_class(claim, vtd, committee):
    stats = vtd.evidence.statistical_tests

    // Step 1: Test appropriateness
    for test in stats:
        if not appropriate_test(test.type, test.data_description, test.assumptions):
            return Rejection("Inappropriate test: " + test.type + " for " + test.data_description)

    // Step 2: Assumption verification
    for test in stats:
        for assumption in test.assumptions:
            check = verify_assumption(assumption, test.assumption_checks)
            if check.violated:
                flag_assumption_violation(assumption, check.evidence)

    // Step 3: Arithmetic verification
    for test in stats:
        recomputed = recompute_test_statistic(test.type, test.summary_statistics)
        if abs(recomputed.statistic - test.statistic) > 0.01:
            return Rejection("Test statistic mismatch: reported=" + test.statistic + " computed=" + recomputed.statistic)
        if abs(recomputed.p_value - test.p_value) > 0.005:
            return Rejection("P-value mismatch")

    // Step 4: Effect size and CI validation
    if claim.effect_size:
        if not ci_contains(stats.confidence_interval, claim.effect_size):
            return Rejection("Claimed effect size outside CI")

    // Step 5: Counter-evidence (same as E-class)
    // Step 6: Committee evaluation (same as E-class)

    return Verified(opinion, statistical_validity_report, verification_cost)
```

**P-Class (Process) Verification Protocol:**

```
function verify_p_class(claim, vtd, committee):
    process_log = vtd.evidence.process_log
    process_spec = get_process_specification(vtd.evidence.process_spec_id)

    // Step 1: Spec existence
    if not process_spec:
        return Rejection("Unknown process specification: " + vtd.evidence.process_spec_id)

    // Step 2: Step completeness
    required_steps = process_spec.required_steps
    logged_steps = set(step.id for step in process_log.steps)
    missing = required_steps - logged_steps
    if len(missing) > 0 and not all_justified(missing, process_log.deviations):
        return Rejection("Missing steps without justification: " + missing)

    // Step 3: Step sequence
    if not valid_sequence(process_log.steps, process_spec.sequence_constraints):
        return Rejection("Step sequence violation")

    // Step 4: Timestamp plausibility
    for step in process_log.steps:
        if step.duration < process_spec.min_duration(step.id):
            flag_implausibly_fast(step)
        if step.duration > process_spec.max_duration(step.id) * 10:
            flag_implausibly_slow(step)

    // Step 5: Deviation justification
    for deviation in process_log.deviations:
        if not adequate_justification(deviation.justification, deviation.step):
            flag_unjustified_deviation(deviation)

    return Verified(opinion, conformance_report, verification_cost)
```

**R-Class (Reasoning) Verification Protocol:**

```
function verify_r_class(claim, vtd, committee):
    premises = vtd.evidence.premises
    inferences = vtd.evidence.inference_steps
    assumptions = vtd.evidence.assumptions

    // Step 1: Logical validity
    for inference in inferences:
        if not valid_inference_rule(inference.rule, inference.from_premises, inference.conclusion):
            return Rejection("Invalid inference at step: " + inference.id)

    // Step 2: Premise support
    for premise in premises:
        if premise.support_type == "verified_claim":
            ref_claim = lookup_claim(premise.support_ref)
            if not ref_claim or ref_claim.credibility.b < premise_threshold:
                flag_weak_premise(premise)
        elif premise.support_type == "assumption":
            if premise.id not in [a.id for a in assumptions]:
                return Rejection("Undeclared assumption used as premise: " + premise.id)

    // Step 3: Assumption disclosure completeness
    // Check for hidden assumptions (premises with no support and not declared)
    unsupported = [p for p in premises if not p.support_type and p.id not in assumptions]
    if len(unsupported) > 0:
        flag_hidden_assumptions(unsupported)

    // Step 4: Conclusion derivability
    if not derives(inferences, premises, claim.proposition):
        return Rejection("Conclusion does not follow from premises via stated inferences")

    return Verified(opinion, logical_validity_report, verification_cost)
```

**Failure Modes:**
- *Source temporarily unavailable:* Retry with exponential backoff (3 attempts). If still unavailable, mark source as UNVERIFIABLE. Claim proceeds with increased uncertainty (u += 0.1).
- *Statistical test type unknown:* Flag for human review. Do not reject — the test may be valid but unfamiliar.
- *Process specification version mismatch:* Verify against the version active at the time the process was executed, not the current version.

---

### 4.6 Attestation Reviewer (Tier 3)

**Purpose:** Reviews Tier 3 claims (H-class, N-class) through structured attestation evaluation combined with mandatory adversarial probing. This is where PCVM provides quality improvement rather than cost reduction.

**H-Class (Heuristic) Verification Protocol:**

```
function verify_h_class(claim, vtd, committee):
    alternatives = vtd.evidence.alternatives_considered
    criteria = vtd.evidence.evaluation_criteria
    precedents = vtd.evidence.precedents_cited
    confidence = vtd.evidence.stated_confidence
    uncertainty_sources = vtd.evidence.uncertainty_sources

    // Step 1: Alternatives genuineness
    if len(alternatives) < 2:
        return Rejection("Fewer than 2 alternatives considered")
    for alt in alternatives:
        if not genuine_alternative(alt, claim):
            flag_strawman_alternative(alt)

    // Step 2: Criteria appropriateness
    context = extract_context(claim)
    if not criteria_match_context(criteria, context):
        flag_criteria_mismatch(criteria, context)

    // Step 3: Evaluation consistency
    for alt in alternatives:
        for criterion in criteria:
            evaluation = vtd.evidence.evaluation_matrix[alt][criterion]
            if not internally_consistent(evaluation, vtd.evidence):
                flag_inconsistent_evaluation(alt, criterion, evaluation)

    // Step 4: Precedent verification
    for precedent in precedents:
        if not verify_precedent_exists(precedent):
            flag_fabricated_precedent(precedent)
        if not verify_precedent_relevance(precedent, claim):
            flag_irrelevant_precedent(precedent)

    // Step 5: Confidence calibration
    if confidence > 0.9 and len(uncertainty_sources) == 0:
        flag_overconfidence(claim, confidence)

    // Step 6: Counter-evidence (mandatory for Tier 3)
    if not vtd.counter_evidence.search_performed:
        credibility_penalty = 0.15  // heavier penalty for Tier 3

    // Step 7: Committee deliberation
    // H-class committees engage in structured disagreement:
    // Each member produces independent assessment, then cross-review
    assessments = collect_independent_assessments(committee, claim, vtd)
    cross_review = facilitate_cross_review(assessments)
    final_opinion = synthesize_deliberation(assessments, cross_review)

    return Verified(final_opinion, deliberation_record, verification_cost)
```

**N-Class (Normative) Verification Protocol:**

```
function verify_n_class(claim, vtd, committee):
    values = vtd.evidence.value_framework
    constitutional_refs = vtd.evidence.constitutional_references
    stakeholders = vtd.evidence.stakeholder_analysis
    alternatives = vtd.evidence.alternative_positions

    // Step 1: Constitutional alignment
    for ref in constitutional_refs:
        if not constitutional_registry.valid_reference(ref):
            return Rejection("Invalid constitutional reference: " + ref.id)
        if not ref_supports_claim(ref, claim):
            flag_misapplied_reference(ref, claim)

    // Step 2: Stakeholder completeness
    affected_parties = infer_affected_parties(claim)
    covered_parties = set(s.group for s in stakeholders)
    uncovered = affected_parties - covered_parties
    if len(uncovered) > 0:
        flag_missing_stakeholders(uncovered)

    // Step 3: Value framework consistency
    if not internally_consistent_values(values):
        flag_value_contradiction(values)

    // Step 4: Alternative position engagement
    for alt in alternatives:
        if not genuinely_engaged(alt):
            flag_dismissed_alternative(alt)

    // Step 5: Committee deliberation (N-class uses governance-aware committee)
    // N-class verification includes constitutional compliance check
    constitutional_check = verify_constitutional_compliance(claim, constitutional_refs)
    assessments = collect_independent_assessments(committee, claim, vtd)

    // N-class opinion: b/d represent constitutional alignment, not truth
    final_opinion = synthesize_normative_opinion(
        assessments, constitutional_check,
        base_rate = constitutional_registry.base_rate(claim.domain)
    )

    return Verified(final_opinion, constitutional_compliance_report, verification_cost)
```

**Structured Disagreement Protocol (for Tier 3 committees):**

Tier 3 verification committees do not simply vote pass/fail. They engage in a structured deliberation:

1. **Independent assessment** (parallel): Each committee member reviews the VTD independently and produces an assessment with opinion tuple and written rationale.

2. **Cross-review** (sequential): Each member reviews one other member's assessment and provides a response (agree/disagree with reason).

3. **Synthesis**: The membrane synthesizes the deliberation into a final opinion using cumulative fusion of individual opinions weighted by cross-review agreement.

4. **Dissent recording**: Dissenting opinions are preserved in the verification record. If a committee member's dissent is later validated (by deep-audit or re-verification), their class-specific credibility increases.

This protocol costs more than simple voting but produces richer verification metadata for Tier 3 claims where the "truth" is not binary.

---

### 4.7 Credibility Engine

**Purpose:** Implements Subjective Logic credibility composition and propagation. Tracks per-agent, per-class credibility and propagates credibility through knowledge graph dependencies.

**Core Data Structures:**

```
OpinionTuple:
    b: float  // belief, in [0, 1]
    d: float  // disbelief, in [0, 1]
    u: float  // uncertainty, in [0, 1]
    a: float  // base rate (prior), in [0, 1]
    // Constraint: b + d + u = 1.0

    projected_probability(): float
        return b + a * u  // expected probability given uncertainty

AgentCredibility:
    agent_id: AgentID
    class_credibilities: Map<ClaimClass, OpinionTuple>
    // REQ-3: per-class trust tracking
    // Agent's D-class credibility does NOT transfer to H-class

ClaimCredibility:
    claim_hash: Hash
    opinion: OpinionTuple
    dependencies: List<ClaimHash>
    last_propagated: Epoch
```

**Subjective Logic Operators:**

```
// Conjunction: omega_A AND omega_B (Josang's multiplication)
function conjoin(w_A: OpinionTuple, w_B: OpinionTuple) -> OpinionTuple:
    b = w_A.b * w_B.b
    d = w_A.d + w_B.d - w_A.d * w_B.d
    u = w_A.b * w_B.u + w_B.b * w_A.u + w_A.u * w_B.u
    a = w_A.a * w_B.a
    return normalize(b, d, u, a)

// Discounting: agent X reports opinion w_A, we have trust w_X in agent X
function discount(w_X: OpinionTuple, w_A: OpinionTuple) -> OpinionTuple:
    b = w_X.b * w_A.b
    d = w_X.b * w_A.d
    u = w_X.d + w_X.u + w_X.b * w_A.u
    a = w_A.a
    return OpinionTuple(b, d, u, a)

// Cumulative Fusion: combining independent opinions about the same claim
function fuse(w_A: OpinionTuple, w_B: OpinionTuple) -> OpinionTuple:
    if w_A.u == 0 and w_B.u == 0:
        // Both dogmatic — use weighted average by base rate
        return average(w_A, w_B)

    k = w_A.u + w_B.u - w_A.u * w_B.u  // normalization factor
    b = (w_A.b * w_B.u + w_B.b * w_A.u) / k
    d = (w_A.d * w_B.u + w_B.d * w_A.u) / k
    u = (w_A.u * w_B.u) / k
    a = (w_A.a * w_B.u + w_B.a * w_A.u - (w_A.a + w_B.a) * w_A.u * w_B.u) / k
    return OpinionTuple(b, d, u, a)

// Normalization: ensure b + d + u = 1
function normalize(b, d, u, a) -> OpinionTuple:
    total = b + d + u
    if total == 0: return OpinionTuple(0, 0, 1, a)
    return OpinionTuple(b/total, d/total, u/total, a)
```

**Credibility Propagation:**

When a claim's credibility changes (new verification result, dependency update, deep-audit finding), the change propagates to dependent claims:

```
function propagate_credibility(changed_claim: ClaimHash, new_opinion: OpinionTuple):
    queue = PriorityQueue()  // priority by graph distance
    queue.push((changed_claim, new_opinion, 0))
    visited = {}
    dampening = 0.85  // PageRank-style dampening

    while not queue.empty():
        (claim, opinion, distance) = queue.pop()
        if claim in visited: continue
        visited[claim] = opinion

        // Find claims that depend on this claim
        dependents = knowledge_graph.get_dependents(claim)
        for dep in dependents:
            // Recompute dependent's credibility
            dep_dependencies = knowledge_graph.get_dependencies(dep)
            dep_opinions = [visited.get(d, get_current_opinion(d)) for d in dep_dependencies]

            // Conjoin all dependency opinions
            combined = dep_opinions[0]
            for op in dep_opinions[1:]:
                combined = conjoin(combined, op)

            // Apply dampening
            dampened = OpinionTuple(
                b = combined.b * dampening,
                d = combined.d * dampening,
                u = 1.0 - combined.b * dampening - combined.d * dampening,
                a = combined.a
            )

            // Check convergence: if change is < epsilon, stop propagating
            current = get_current_opinion(dep)
            delta = max(abs(dampened.b - current.b), abs(dampened.d - current.d), abs(dampened.u - current.u))
            if delta > EPSILON:
                update_opinion(dep, dampened)
                queue.push((dep, dampened, distance + 1))
            // else: converged at this node, no further propagation
```

**Class-Specific Credibility (REQ-3):**

Agent credibility is tracked per claim class. This prevents reputation laundering (Attack 5):

```
function get_agent_class_credibility(agent_id, claim_class) -> OpinionTuple:
    // Each agent has 8 independent credibility scores
    return agent_credibility_store.get(agent_id, claim_class)
    // Default for new agents: (b=0.0, d=0.0, u=1.0, a=0.5) — full uncertainty

function update_agent_class_credibility(agent_id, claim_class, verification_result):
    current = get_agent_class_credibility(agent_id, claim_class)

    // Positive result: increase belief slightly
    if verification_result.passed:
        evidence = OpinionTuple(b=0.1, d=0.0, u=0.9, a=0.5)
    // Negative result: increase disbelief more strongly (asymmetric)
    else:
        evidence = OpinionTuple(b=0.0, d=0.2, u=0.8, a=0.5)
    // Deep-audit failure: strong credibility hit
    if verification_result.deep_audit_failed:
        evidence = OpinionTuple(b=0.0, d=0.5, u=0.5, a=0.5)

    updated = fuse(current, evidence)
    agent_credibility_store.set(agent_id, claim_class, updated)
```

**Credibility Decay (class-specific):**

| Class | Decay Model | Half-Life | Trigger |
|-------|-------------|-----------|---------|
| D | None | Infinite | Never (deterministic proofs don't expire) |
| E | Time-based | 90-365 days (domain-dependent) | Calendar |
| S | Data-triggered | N/A | New data availability in same domain |
| H | Time-based | 180 days | Calendar |
| N | Constitutional | N/A | Constitutional amendment only |
| P | Spec-triggered | N/A | Process specification change |
| R | Premise-triggered | N/A | Any premise credibility change |
| C | Regulation-triggered | N/A | Regulation change or audit cycle |

```
function apply_decay(claim: ClaimCredibility, current_epoch: Epoch):
    class = claim.assigned_class
    match class:
        case D: return  // no decay
        case E:
            age = current_epoch - claim.verified_epoch
            half_life = domain_half_life(claim.domain)
            decay_factor = 0.5 ^ (age / half_life)
            claim.opinion.b *= decay_factor
            claim.opinion.u = 1.0 - claim.opinion.b - claim.opinion.d
        case S:
            if new_data_available(claim.domain, claim.verified_epoch):
                claim.opinion.u = min(1.0, claim.opinion.u + 0.2)
                claim.opinion.b = max(0.0, claim.opinion.b - 0.1)
                claim.opinion.d = 1.0 - claim.opinion.b - claim.opinion.u
        // ... similar patterns for other classes
```

**Failure Modes:**
- *Propagation cycle detected:* Dampening factor (0.85) guarantees convergence even in cycles. Maximum iteration count (100) prevents runaway computation.
- *Opinion underflow:* If b, d, u all approach 0 due to numerical issues, reset to (0, 0, 1, a) — full uncertainty.
- *Mass cascading event:* If a high-hub claim's credibility changes drastically, many claims update simultaneously. Rate limiter: process at most 100 propagation events per epoch. Remainder queued for next epoch.

---

### 4.8 Deep-Audit Subsystem

**Purpose:** Randomly selects passed VTDs for full-replication re-verification. Serves as a deterrence mechanism against VTD forgery (Attack 1) and collusion (Attack 8).

**Audit Selection:**

```
function select_audit_claims(epoch: Epoch) -> List<ClaimHash>:
    // Get all claims verified in the last audit_window epochs
    recent_claims = get_claims_verified_in_range(epoch - AUDIT_WINDOW, epoch)

    // Base audit rate per class
    audit_rates = {
        D: 0.03,   // Low: D-class proof checking is reliable
        E: 0.10,   // High: E-class source forgery is the primary threat
        S: 0.08,
        H: 0.10,   // High: hardest to verify
        N: 0.10,
        P: 0.05,   // Moderate: process logs are hard to forge
        R: 0.07,
        C: 0.05
    }

    selected = []
    for claim in recent_claims:
        base_rate = audit_rates[claim.assigned_class]

        // Adjust rate based on risk factors
        adjusted_rate = base_rate
        if claim.producer_credibility < 0.5:
            adjusted_rate *= 1.5  // audit low-credibility agents more
        if claim.classification_flag == OVERRIDDEN_MAJOR:
            adjusted_rate *= 2.0  // audit classification disputes more
        if sentinel_flagged(claim.producer_id):
            adjusted_rate *= 3.0  // audit sentinel-flagged agents heavily

        // Cap at 30% to avoid excessive audit cost
        adjusted_rate = min(adjusted_rate, 0.30)

        if random() < adjusted_rate:
            selected.append(claim)

    return selected
```

**Audit Protocol:**

```
function execute_deep_audit(claim: ClaimHash):
    vtd = vtd_store.get(claim)
    original_result = get_verification_result(claim)

    // Step 1: Re-classify (independent classifier)
    re_classification = classify_claim_independent(claim)
    if re_classification.primary_class != vtd.assigned_class:
        flag_classification_error(claim, vtd.assigned_class, re_classification)

    // Step 2: Full replication
    replicated_output = replicate_task(claim.original_task)
    replication_matches = compare_outputs(claim.value, replicated_output)

    // Step 3: Independent VTD check (new committee, not original verifiers)
    audit_committee = vrf_select_audit_committee(claim, exclude=original_result.committee)
    independent_result = dispatch_verification(claim, vtd, re_classification, audit_committee)

    // Step 4: Cross-reference with original
    agreement = compare_results(original_result, independent_result)

    // Step 5: Verdict
    if not replication_matches or not agreement.consistent:
        // AUDIT FAILURE
        audit_failure(claim, original_result, independent_result, replication_matches)
    else:
        // AUDIT PASS
        audit_pass(claim)

    return AuditResult(claim, replication_matches, agreement, re_classification)
```

**Audit Failure Consequences:**

```
function audit_failure(claim, original_result, audit_result, replication_matches):
    // 1. Revoke claim's MCT
    revoke_mct(claim)

    // 2. Credibility penalty for producer
    producer = claim.producer_id
    update_agent_class_credibility(producer, claim.assigned_class,
        VerificationResult(passed=false, deep_audit_failed=true))

    // 3. Credibility penalty for original verifiers
    for verifier in original_result.committee:
        if verifier.attestation.verdict == VERIFIED:
            // Verifier endorsed a claim that failed audit
            update_agent_class_credibility(verifier.id, claim.assigned_class,
                VerificationResult(passed=false, deep_audit_failed=false))

    // 4. Sentinel Graph notification
    sentinel.report_audit_failure(claim, producer, original_result.committee)

    // 5. Propagate credibility change to dependent claims
    propagate_credibility(claim, OpinionTuple(b=0.0, d=0.8, u=0.2, a=0.5))

    // 6. Trigger re-verification of claims from same producer in same class
    producer_claims = get_recent_claims_by(producer, claim.assigned_class, window=50_epochs)
    for pc in producer_claims:
        queue_re_verification(pc, priority=HIGH)
```

**Collusion Detection via Deep-Audit (Attack 8 mitigation):**

The Sentinel Graph uses audit results to detect collusion patterns:

```
function detect_collusion(audit_results: List<AuditResult>, window: int):
    // Build pairwise endorsement matrix
    endorsement_pairs = {}
    for result in audit_results:
        producer = result.claim.producer_id
        for verifier in result.original_committee:
            if verifier.verdict == VERIFIED:
                pair = (producer, verifier.id)
                endorsement_pairs[pair] = endorsement_pairs.get(pair, 0) + 1

    // Statistical test: is any pair's endorsement rate significantly above random?
    for (producer, verifier), count in endorsement_pairs.items():
        expected = estimate_random_endorsement_rate(producer, verifier, window)
        if count > expected * 3 and count > 5:  // 3x random rate and at least 5 instances
            flag_potential_collusion(producer, verifier, count, expected)

    // Cluster detection: find groups of agents that mutually endorse above baseline
    endorsement_graph = build_endorsement_graph(endorsement_pairs)
    clusters = find_dense_subgraphs(endorsement_graph, min_density=0.7, min_size=3)
    for cluster in clusters:
        flag_collusion_cluster(cluster)
```

**Performance:**
- Audit overhead: 5-10% of total verification cost (configurable)
- Audit latency: audits run asynchronously, results available within 1-3 epochs
- Storage: audit results stored permanently alongside VTDs

---

### 4.9 Knowledge Admission Gate

**Purpose:** Issues Membrane Certificates (MCTs) for verified claims and interfaces with the Knowledge Cortex for BDL persistence. This is the final checkpoint before a claim enters durable memory.

**MCT Structure:**

```
MembraneCertificate:
    mct_id: UUID
    claim_hash: Hash
    vtd_hash: Hash
    assigned_class: ClaimClass
    opinion: OpinionTuple          // final credibility from Credibility Engine
    verification_tier: Tier        // 1, 2, or 3
    verification_method: String    // "proof_check", "evidence_eval", "attestation_review"
    committee: List<AgentID>       // VRF-selected committee members
    committee_attestations: List<Attestation>
    adversarial_probing: Optional<ProbingResult>
    deep_audit_status: PENDING | PASSED | FAILED | NOT_SELECTED
    epoch_verified: Epoch
    expiration: Optional<Epoch>    // based on class-specific decay
    dependencies: List<ClaimHash>  // claims this claim depends on
    supersedes: Optional<ClaimHash> // if this claim replaces a previous one
    mct_signature: Signature       // membrane's cryptographic signature
```

**Admission Protocol:**

```
function admit_to_knowledge(claim, mct, vtd):
    // Step 1: Admission threshold check
    threshold = admission_threshold(mct.assigned_class)
    if mct.opinion.projected_probability() < threshold:
        return Rejection("Below admission threshold: " +
            mct.opinion.projected_probability() + " < " + threshold)

    // Step 2: Contradiction check
    contradictions = knowledge_cortex.check_contradictions(claim)
    if len(contradictions) > 0:
        // Do not automatically reject — flag for resolution
        for c in contradictions:
            create_contradiction_record(claim, c)
        // If contradicted claim has lower credibility, admit new claim
        // If contradicted claim has higher credibility, reject new claim
        for c in contradictions:
            existing_opinion = get_current_opinion(c.hash)
            if existing_opinion.projected_probability() > mct.opinion.projected_probability():
                return Rejection("Contradicts higher-credibility claim: " + c.hash)

    // Step 3: Supersession handling
    if mct.supersedes:
        superseded = knowledge_cortex.get_claim(mct.supersedes)
        if superseded:
            mark_superseded(superseded, claim)
            // Propagate credibility update to dependents of superseded claim
            propagate_credibility(superseded.hash,
                OpinionTuple(b=0.0, d=0.0, u=1.0, a=0.5))

    // Step 4: BDL creation
    bdl = Bundle(
        claim = claim,
        mct = mct,
        vtd_ref = vtd.hash,  // reference, not copy (VTD stored separately)
        admitted_epoch = current_epoch(),
        bundle_type = claim_to_bundle_type(mct.assigned_class)
    )

    // Step 5: Persist to Knowledge Cortex
    knowledge_cortex.persist(bdl)

    // Step 6: Update dependency graph
    for dep in mct.dependencies:
        knowledge_cortex.add_dependency_edge(claim.hash, dep)

    // Step 7: Settlement notification
    settlement_plane.report_verification(
        producer = claim.agent_id,
        verifiers = mct.committee,
        quality_score = mct.opinion.projected_probability(),
        class = mct.assigned_class
    )

    return Admitted(bdl)
```

**Admission Thresholds (per class):**

| Class | Threshold | Rationale |
|-------|-----------|-----------|
| D | 0.95 | Deterministic claims should be near-certain |
| E | 0.60 | Empirical claims tolerate moderate uncertainty |
| S | 0.65 | Statistical claims slightly higher bar than empirical |
| H | 0.50 | Heuristic claims accept significant uncertainty |
| N | 0.50 | Normative claims verified for consistency, not truth |
| P | 0.80 | Process conformance should be high-confidence |
| R | 0.75 | Logical reasoning should be high-confidence |
| C | 0.90 | Compliance claims require high confidence |

**Re-Verification Triggers (from Knowledge Cortex):**

The Knowledge Cortex can trigger re-verification of admitted claims when:
1. A dependency's credibility drops below threshold
2. A contradiction is discovered with a newly admitted claim
3. Credibility decay crosses the re-verification threshold
4. Deep-audit reveals systematic issues with the producer or verifier
5. An external event invalidates a class of claims (regulation change for C-class, new data for S-class)

```
function handle_reverification_trigger(trigger):
    claim = knowledge_cortex.get_claim(trigger.claim_hash)
    reason = trigger.reason

    match reason:
        case DEPENDENCY_DEGRADED:
            // Re-propagate credibility
            propagate_credibility(trigger.dependency_hash, trigger.new_opinion)
            // If propagated credibility drops below threshold, flag
            updated_opinion = get_current_opinion(claim.hash)
            if updated_opinion.projected_probability() < readmission_threshold(claim.class):
                queue_re_verification(claim, priority=MEDIUM)

        case CONTRADICTION_DISCOVERED:
            // Both claims need review
            queue_re_verification(claim, priority=HIGH)
            queue_re_verification(trigger.contradicting_claim, priority=HIGH)

        case DECAY_THRESHOLD:
            // Claim has decayed below readmission threshold
            queue_re_verification(claim, priority=LOW)

        case DEEP_AUDIT_SYSTEMATIC:
            // Producer found unreliable — re-verify all their claims
            queue_batch_re_verification(trigger.affected_claims, priority=HIGH)
```

---

## 5. Integration Contracts

### 5.1 Tidal Noosphere Interface

PCVM integrates with the Tidal Noosphere through the V-class operation pathway. The Noosphere provides governance; PCVM provides execution.

**V-Class Operation Flow:**

```
Noosphere                              PCVM
--------                              ----
1. Agent submits claim (CLM)
   with proposed class
        |
        v
2. Noosphere schedules
   verification for epoch E+1
   (1-epoch commit delay)
        |
        v
3. VRF Engine selects committee -----> 4. PCVM receives:
   from pre-stratified pools              - claim + evidence bundle
   Apply dual defense:                    - committee assignment
   commit-reveal + diversity pools        - epoch context
        |                                     |
        v                                     v
                                         5. Claim Classifier assigns class
                                         6. VTD Engine constructs VTD
                                         7. Dispatcher routes to tier verifier
                                         8. Verification executes
                                         9. Credibility composed
                                         10. Admission decision
                                              |
11. Noosphere receives MCT  <------------- MCT or Rejection
    or Rejection
        |
        v
12. MCT -> Knowledge Cortex (BDL)
    Rejection -> Agent notification
    MQI metrics -> Sentinel Graph
```

**Interface Contract:**

```
// Noosphere -> PCVM: Verification Request
VerificationRequest:
    claim: CLM                     // ASV claim token
    evidence_bundle: EvidenceBundle // raw evidence from agent
    proposed_class: ClaimClass     // agent's proposed classification
    committee: List<AgentID>       // VRF-selected committee
    committee_proof: VRFProof      // cryptographic proof of selection
    epoch: Epoch                   // verification epoch
    stakes_hint: Optional<StakesLevel> // Noosphere's assessment of claim importance
    locus_id: LocusID              // which locus this claim belongs to
    parcel_id: ParcelID            // which parcel within locus

// PCVM -> Noosphere: Verification Result
VerificationResult:
    claim_hash: Hash
    verdict: ADMITTED | REJECTED | PROVISIONAL
    mct: Optional<MembraneCertificate>
    opinion: OpinionTuple
    assigned_class: ClaimClass
    classification_flag: AGREED | OVERRIDDEN_MINOR | OVERRIDDEN_MAJOR
    verification_cost: TokenCount
    audit_selected: bool           // whether this claim was selected for deep audit
    mqi_contribution: MQIMetrics   // metrics for Sentinel Graph

// Error cases
VerificationError:
    COMMITTEE_UNAVAILABLE          // not enough committee members responded
    VTD_CONSTRUCTION_FAILED        // evidence bundle insufficient for VTD
    VERIFICATION_TIMEOUT           // verification did not complete in epoch
    SCHEMA_VERSION_MISMATCH        // VTD schema version incompatible
```

**Epoch Alignment:**

PCVM operates on the Noosphere's tidal epoch clock (1-hour default, NTP-synchronized):

| Phase | Timing | PCVM Activity |
|-------|--------|--------------|
| Epoch start | T+0 | Receive verification requests for claims committed in previous epoch |
| Verification window | T+0 to T+50min | Execute verification pipeline |
| Audit selection | T+50min | Select deep-audit claims from completed verifications |
| Settlement reporting | T+55min | Report quality scores to Settlement Plane |
| Epoch close | T+60min | Finalize results, propagate credibility updates |

Claims that do not complete verification within the epoch window enter provisional state and continue in the next epoch.

**VRF Committee Integration:**

PCVM does not select committees — the Noosphere's VRF Engine does. PCVM validates the committee assignment:

```
function validate_committee(committee, committee_proof, claim_hash, epoch):
    // Verify VRF proof is valid
    if not ecvrf_verify(committee_proof, claim_hash, epoch):
        return INVALID_PROOF

    // Verify committee members are from different strata
    strata = get_strata_assignments(committee)
    if len(set(strata.lineage)) < ceil(len(committee) / 4):
        return INSUFFICIENT_DIVERSITY

    // Verify no member exceeds 15% weight cap
    for member in committee:
        if member.weight > 0.15:
            return WEIGHT_CAP_EXCEEDED

    return VALID
```

**MQI Metrics (PCVM -> Sentinel Graph):**

PCVM contributes the following metrics to the Membrane Quality Index:

```
PCVMMQIMetrics:
    // Per-epoch, per-locus
    vtd_rejection_rate: float      // fraction of VTDs that fail structural validation
    classification_override_rate: float  // fraction of claims where membrane overrides agent
    adversarial_probe_trigger_rate: float // fraction of claims that trigger probing
    probe_detection_rate: float    // fraction of probed claims where probe finds issues
    deep_audit_failure_rate: float // fraction of audited claims that fail
    credibility_distribution: HistogramBuckets  // distribution of opinion tuples
    class_distribution: Map<ClaimClass, int>    // claim volume per class
    average_verification_cost: float  // tokens per verification
    committee_response_rate: float    // fraction of committee members that responded
    verification_completion_rate: float // fraction completed within epoch
```

**MQI Response Tiers (triggered by Sentinel Graph):**

| MQI Condition | PCVM Response |
|--------------|---------------|
| Conservative mode (1 metric degraded) | Increase base probe rate by 50%. Reduce admission thresholds by 0.05. |
| Alert mode (3+ metrics degraded) | Probe ALL claims (not just selected). Increase deep-audit rate to 15%. |
| Lockdown (sustained degradation) | Halt new admissions. Re-verify most recent 100 claims. Resume only on Sentinel Graph clearance. |

---

### 5.2 Knowledge Cortex Interface

PCVM is the sole gateway for claims entering the Knowledge Cortex (INV-1).

**BDL Admission Protocol:**

```
// PCVM -> Knowledge Cortex: Admit Claim
AdmitRequest:
    bundle: Bundle                 // claim + MCT + VTD reference
    dependency_edges: List<(ClaimHash, ClaimHash)>  // this claim depends on these
    supersession: Optional<SupersessionRecord>

// Knowledge Cortex -> PCVM: Admission Acknowledgment
AdmitResponse:
    status: PERSISTED | CONFLICT | STORAGE_ERROR
    bdl_id: Optional<BundleID>
    conflicts: Optional<List<ConflictRecord>>

// Knowledge Cortex -> PCVM: Re-verification Trigger
ReverificationTrigger:
    claim_hash: ClaimHash
    reason: DEPENDENCY_DEGRADED | CONTRADICTION_DISCOVERED |
            DECAY_THRESHOLD | DEEP_AUDIT_SYSTEMATIC |
            EXTERNAL_INVALIDATION
    context: TriggerContext        // details about what changed
    priority: LOW | MEDIUM | HIGH
```

**Dependency Graph Contract:**

The Knowledge Cortex maintains the claim dependency graph. PCVM reads this graph for credibility propagation:

```
// PCVM reads from Knowledge Cortex
knowledge_cortex.get_dependencies(claim_hash) -> List<ClaimHash>
knowledge_cortex.get_dependents(claim_hash) -> List<ClaimHash>
knowledge_cortex.get_claim(claim_hash) -> Optional<Claim>
knowledge_cortex.check_contradictions(claim) -> List<ContradictionRecord>

// PCVM writes to Knowledge Cortex
knowledge_cortex.add_dependency_edge(from_hash, to_hash)
knowledge_cortex.add_contradiction_edge(hash_a, hash_b)
knowledge_cortex.mark_superseded(old_hash, new_hash)
knowledge_cortex.update_credibility(claim_hash, new_opinion)
```

---

### 5.3 Settlement Plane Interface

PCVM reports verification quality to the Settlement Plane for economic incentive alignment.

**Settlement Integration:**

```
// PCVM -> Settlement Plane: Verification Report
VerificationReport:
    epoch: Epoch
    producer_id: AgentID
    verifier_ids: List<AgentID>
    claim_class: ClaimClass
    quality_score: float           // opinion.projected_probability()
    verification_cost: TokenCount
    deep_audit_result: Optional<PASSED | FAILED>
    classification_accuracy: Optional<bool>  // from re-classification audit

// Settlement weight (from Noosphere spec):
//   w_verify = 0.40 (40% of settlement score is verification quality)
//
// PCVM quality score maps to verification_quality component:
//   verification_quality = mean(quality_scores) * method_diversity_bonus
//   where method_diversity_bonus rewards verifiers across multiple claim classes
```

**Economic Incentives Alignment:**

| Actor | Incentive | Mechanism |
|-------|-----------|-----------|
| Producer | Produce accurate claims with complete VTDs | Quality score affects 40% of settlement. Deep-audit failures penalize future scores. |
| Verifier | Perform thorough verification | Endorsing a claim that fails deep-audit reduces verifier quality score. |
| Prober | Find genuine errors | Probers who detect errors that deep-audit confirms receive quality bonus. |
| Honest agent | Maintain high class-specific credibility | Credibility affects future verification weight (discounting operator). |

---

### 5.4 Sentinel Graph Interface

PCVM feeds the Sentinel Graph with metrics for anomaly detection and receives alerts for defensive response.

**PCVM -> Sentinel Graph:**

```
// Periodic metrics (per epoch)
sentinel.report_mqi_metrics(locus_id, pcvm_mqi_metrics)

// Event-based reports
sentinel.report_audit_failure(claim_hash, producer_id, committee)
sentinel.report_classification_dispute(claim_hash, proposed, assigned)
sentinel.report_collusion_indicator(agent_pair, endorsement_count, expected_rate)
sentinel.report_probe_detection(claim_hash, probe_type, finding)
```

**Sentinel Graph -> PCVM:**

```
// Anomaly alerts
sentinel.on_alert(COLLUSION_DETECTED, agent_cluster) ->
    pcvm.increase_audit_rate(agent_cluster, multiplier=3.0)
    pcvm.invalidate_recent_verifications(agent_cluster, window=20_epochs)

sentinel.on_alert(VERIFICATION_AFFINITY_ANOMALY, agent_pair) ->
    pcvm.flag_agent_pair(agent_pair)
    pcvm.exclude_pair_from_same_committee(agent_pair, duration=50_epochs)

sentinel.on_alert(MQI_DEGRADATION, locus_id, severity) ->
    pcvm.enter_response_tier(locus_id, severity)
    // CONSERVATIVE, ALERT, or LOCKDOWN per Section 5.1

sentinel.on_alert(SYBIL_CLUSTER_DETECTED, agent_ids) ->
    pcvm.suspend_agents(agent_ids)
    pcvm.queue_re_verification(claims_by_agents(agent_ids))
```

**Verification Affinity Matrix:**

The Sentinel Graph maintains a verification affinity matrix tracking which agents verify which other agents' claims:

```
Affinity[i][j] = number of times agent j has verified agent i's claims
                 in the last N epochs

Expected[i][j] = (total_verifications_by_j * total_claims_by_i) / total_verifications

Anomaly_score[i][j] = (Affinity[i][j] - Expected[i][j]) / sqrt(Expected[i][j])
// Chi-squared-like statistic; scores > 3.0 flagged for investigation
```

---

### 5.5 ASV Interface (C4)

PCVM consumes ASV semantic tokens and extends them with verification metadata.

**Claim Semantics:**

ASV provides the CLM (Claim), EVD (Evidence), PRV (Provenance), and VRF (Verification) token types. PCVM maps these to its internal structures:

```
// ASV CLM token -> PCVM Claim
function from_asv_claim(clm_token):
    return Claim(
        content = clm_token.credentialSubject,
        provenance = clm_token.prv_chain,
        proposed_class = infer_class_from_asv_type(clm_token.type),
        agent_id = clm_token.issuer,
        evidence_refs = clm_token.evd_references
    )

// PCVM MCT -> ASV VRF token
function to_asv_verification(mct):
    return VRFToken(
        claim_ref = mct.claim_hash,
        verification_status = mct.verdict,
        confidence = mct.opinion.projected_probability(),
        opinion_tuple = {
            belief: mct.opinion.b,
            disbelief: mct.opinion.d,
            uncertainty: mct.opinion.u,
            base_rate: mct.opinion.a
        },
        verification_method = mct.verification_method,
        epoch = mct.epoch_verified,
        vtd_ref = mct.vtd_hash
    )
```

**Provenance Chain Integration:**

ASV provenance chains (PRV tokens) are consumed by PCVM's Grounding Checker. Terminal nodes in the provenance chain must resolve to either verified claims (with MCTs) or constitutional axioms:

```
function check_provenance_grounding(prv_chain):
    for terminal in prv_chain.terminals():
        if terminal.type == "verified_claim":
            mct = lookup_mct(terminal.ref)
            if not mct or mct.opinion.projected_probability() < grounding_threshold:
                return GroundingFailure(terminal, "Unverified or low-credibility terminal")
        elif terminal.type == "constitutional_axiom":
            if not constitutional_registry.contains(terminal.ref):
                return GroundingFailure(terminal, "Unknown constitutional axiom")
        elif terminal.type == "empirical_observation":
            if not terminal.source:
                return GroundingFailure(terminal, "Empirical observation without source")
        else:
            return GroundingFailure(terminal, "Unknown terminal type: " + terminal.type)
    return GroundingSuccess()
```

---

## 6. VTD Specifications per Claim Class

This section provides concrete JSON schemas and examples for each of the 8 claim classes.

### 6.1 D-Class VTD (Deterministic)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/d-class/v1",
  "type": "VTD_D_CLASS",
  "header": {
    "claim_hash": "sha256:a1b2c3...",
    "producer_id": "agent-007",
    "assigned_class": "D",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "proof": {
    "type": "COMPUTATION_TRACE",
    "inputs": [
      {"name": "message", "value": "hello", "type": "string"}
    ],
    "algorithm": "SHA-256",
    "trace": [
      {"step": 1, "operation": "pad_message", "input": "hello", "output": "68656c6c6f80..."},
      {"step": 2, "operation": "parse_blocks", "input": "68656c6c6f80...", "output": ["block_0"]},
      {"step": 3, "operation": "compress", "input": "block_0", "output": "2cf24dba..."}
    ],
    "final_output": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
  },
  "metadata": {
    "construction_cost_tokens": 45,
    "size_bytes": 892,
    "dependency_claims": []
  }
}
```

**Example verification:** Verifier spot-checks step 3 by running SHA-256 compression on block_0. If output matches, step is valid. Final output compared against claim. Total cost: ~5% of full recomputation.

### 6.2 E-Class VTD (Empirical)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/e-class/v1",
  "type": "VTD_E_CLASS",
  "header": {
    "claim_hash": "sha256:d4e5f6...",
    "producer_id": "agent-012",
    "assigned_class": "E",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "source_citations": [
      {
        "url": "https://openai.com/research/gpt-4",
        "retrieved": "2026-03-01T14:22:00Z",
        "content_hash": "sha256:abc123...",
        "quoted_text": "GPT-4 achieves 86.4% on MMLU",
        "quote_context": "Table 1: Benchmark Results",
        "relevance_justification": "Direct benchmark score from model developer"
      },
      {
        "url": "https://paperswithcode.com/sota/question-answering-on-mmlu",
        "retrieved": "2026-03-01T14:25:00Z",
        "content_hash": "sha256:def456...",
        "quoted_text": "GPT-4: 86.4%",
        "quote_context": "Leaderboard entry",
        "relevance_justification": "Independent confirmation from benchmark aggregator"
      }
    ],
    "cross_references": [
      {"source_index": 1, "confirms": true, "note": "Independent confirmation"}
    ]
  },
  "counter_evidence": {
    "search_performed": true,
    "search_description": "Searched for contradicting benchmark reports and methodology critiques",
    "considered": [
      {
        "source": "https://arxiv.org/abs/2405.xxxxx",
        "claim": "MMLU benchmark has contamination issues",
        "relevance": "Questions whether the 86.4% score is inflated",
        "response": "Valid concern but does not change the reported score, only its interpretation"
      }
    ]
  },
  "metadata": {
    "construction_cost_tokens": 320,
    "size_bytes": 2100,
    "dependency_claims": []
  }
}
```

### 6.3 S-Class VTD (Statistical)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/s-class/v1",
  "type": "VTD_S_CLASS",
  "header": {
    "claim_hash": "sha256:g7h8i9...",
    "producer_id": "agent-019",
    "assigned_class": "S",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "dataset": {
      "n": 500,
      "source": "Simulation of bounded-loads hash ring with N=10, epsilon=0.15",
      "sampling_method": "1000 trials with random seeds",
      "population_description": "Task assignments under UNIFORM distribution"
    },
    "statistical_tests": [
      {
        "type": "one-sample t-test",
        "hypothesis": "mean(max_load/avg_load) < 1.15",
        "test_statistic": -8.42,
        "p_value": 0.0001,
        "degrees_of_freedom": 999,
        "summary_statistics": {
          "mean": 1.087,
          "std": 0.023,
          "min": 1.031,
          "max": 1.142
        }
      }
    ],
    "effect_size": {
      "point_estimate": 1.087,
      "confidence_interval_95": [1.082, 1.092]
    },
    "assumptions": [
      {"name": "normality", "check": "Shapiro-Wilk p=0.34", "status": "satisfied"},
      {"name": "independence", "check": "trials use independent random seeds", "status": "satisfied"}
    ]
  },
  "counter_evidence": {
    "search_performed": true,
    "considered": [
      {
        "source": "ADVERSARIAL distribution results",
        "claim": "Under adversarial key selection, max/avg reaches 1.22",
        "relevance": "Claim is specific to UNIFORM distribution; adversarial is a separate claim",
        "response": "Acknowledged; claim scope limited to UNIFORM distribution"
      }
    ]
  },
  "metadata": {
    "construction_cost_tokens": 280,
    "size_bytes": 1800,
    "dependency_claims": ["sha256:simulation_setup_claim"]
  }
}
```

### 6.4 H-Class VTD (Heuristic)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/h-class/v1",
  "type": "VTD_H_CLASS",
  "header": {
    "claim_hash": "sha256:j0k1l2...",
    "producer_id": "agent-023",
    "assigned_class": "H",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "alternatives_considered": [
      {
        "id": "alt-1",
        "description": "Unified membrane (PCVM as proposed)",
        "evaluation": {
          "engineering_complexity": "Single system, graduated depth. Moderate complexity.",
          "credibility_composition": "Full cross-class composition possible",
          "membrane_sovereignty": "Single checkpoint preserves INV-1/INV-2",
          "total_system_cost": "Higher per-unit but lower system-level"
        }
      },
      {
        "id": "alt-2",
        "description": "Three-tier split (proof-checker + evidence evaluator + documentation standard)",
        "evaluation": {
          "engineering_complexity": "Three simpler systems but coordination overhead",
          "credibility_composition": "Cross-system composition requires additional interface",
          "membrane_sovereignty": "Three checkpoints — sovereignty model unclear",
          "total_system_cost": "Lower per-unit but higher coordination cost"
        }
      }
    ],
    "evaluation_criteria": [
      "engineering_complexity",
      "credibility_composition",
      "membrane_sovereignty",
      "total_system_cost"
    ],
    "decision_rationale": "Unified membrane preferred: preserves INV-1/INV-2 sovereignty, enables cross-class credibility, lower total engineering complexity despite higher per-component complexity.",
    "precedents_cited": [
      {
        "system": "TLS/SSL",
        "context": "Unified security layer with graduated cipher suites rather than separate protocols per security level",
        "relevance": "Demonstrates value of unified membrane with graduated capabilities"
      }
    ],
    "stated_confidence": 0.72,
    "uncertainty_sources": [
      "Unified-vs-split comparison is theoretical; no empirical data yet",
      "Engineering complexity estimates may be inaccurate"
    ]
  },
  "counter_evidence": {
    "search_performed": true,
    "considered": [
      {
        "source": "Assessment Council Skeptic Position",
        "claim": "Split architecture is more honest about different verification natures",
        "relevance": "Directly challenges the unified approach",
        "response": "Valid concern. Unified approach accepts this tradeoff for sovereignty and composition benefits. REQ-5 mandates comparative analysis."
      }
    ]
  },
  "metadata": {
    "construction_cost_tokens": 680,
    "size_bytes": 3200,
    "dependency_claims": ["sha256:noosphere_inv1", "sha256:noosphere_inv2"]
  }
}
```

### 6.5 N-Class VTD (Normative)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/n-class/v1",
  "type": "VTD_N_CLASS",
  "header": {
    "claim_hash": "sha256:m3n4o5...",
    "producer_id": "agent-031",
    "assigned_class": "N",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "value_framework": {
      "type": "deontological",
      "primary_principle": "User autonomy and data minimization",
      "justification": "Aligned with constitutional commitment to privacy-by-default"
    },
    "constitutional_references": [
      {
        "id": "CONST-007",
        "text": "The system shall implement privacy-by-default for all user data",
        "applicability": "Direct — claim asserts privacy precedence",
        "intent_annotation": "Prevent analytics-driven erosion of user privacy"
      }
    ],
    "stakeholder_analysis": [
      {
        "group": "End users",
        "impact": "positive",
        "description": "Increased privacy protection, reduced data exposure"
      },
      {
        "group": "Analytics team",
        "impact": "negative",
        "description": "Reduced data access for analytics and optimization"
      },
      {
        "group": "System administrators",
        "impact": "neutral",
        "description": "Implementation complexity roughly equivalent either way"
      }
    ],
    "alternative_positions": [
      {
        "position": "Analytics should take precedence for system optimization",
        "engagement": "This position conflicts with CONST-007. While system optimization is valuable, constitutional parameters are sovereign. Optimization must occur within privacy constraints, not override them.",
        "strength_acknowledged": "Analytics-first approach would improve recommendation quality by ~15% based on similar systems"
      }
    ]
  },
  "counter_evidence": {
    "search_performed": true,
    "considered": [
      {
        "source": "GDPR Article 6(1)(f) — legitimate interests",
        "claim": "Analytics may be justified under legitimate interests balancing",
        "relevance": "Legal framework that could support analytics precedence",
        "response": "Constitutional parameter CONST-007 is stricter than GDPR minimum. The system's constitutional commitment exceeds legal requirements."
      }
    ]
  },
  "metadata": {
    "construction_cost_tokens": 520,
    "size_bytes": 2800,
    "dependency_claims": ["sha256:const_007_claim"]
  }
}
```

### 6.6 P-Class VTD (Process)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/p-class/v1",
  "type": "VTD_P_CLASS",
  "header": {
    "claim_hash": "sha256:p6q7r8...",
    "producer_id": "agent-015",
    "assigned_class": "P",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "process_spec_id": "RESEARCH_PROTOCOL_v2",
    "process_log": {
      "steps": [
        {
          "id": 1,
          "name": "source_identification",
          "started": "2026-03-09T10:00:00Z",
          "completed": "2026-03-09T10:15:00Z",
          "inputs": ["query: bounded-loads consistent hashing"],
          "outputs": ["12 candidate sources identified"],
          "tools": ["web_search", "arxiv_api"]
        },
        {
          "id": 2,
          "name": "source_evaluation",
          "started": "2026-03-09T10:15:00Z",
          "completed": "2026-03-09T10:45:00Z",
          "inputs": ["12 candidate sources"],
          "outputs": ["7 sources retained, 5 excluded with reasons"],
          "tools": ["document_reader"]
        },
        {
          "id": 3,
          "name": "synthesis",
          "started": "2026-03-09T10:45:00Z",
          "completed": "2026-03-09T11:30:00Z",
          "inputs": ["7 retained sources"],
          "outputs": ["research_report_draft_v1"],
          "tools": ["text_generation"]
        },
        {
          "id": 4,
          "name": "cross_validation",
          "started": "2026-03-09T11:30:00Z",
          "completed": "2026-03-09T11:50:00Z",
          "inputs": ["research_report_draft_v1", "7 retained sources"],
          "outputs": ["3 claims verified, 1 claim corrected"],
          "tools": ["document_reader", "web_search"]
        },
        {
          "id": 5,
          "name": "final_review",
          "started": "2026-03-09T11:50:00Z",
          "completed": "2026-03-09T12:00:00Z",
          "inputs": ["corrected_report"],
          "outputs": ["final_research_report"],
          "tools": []
        }
      ],
      "deviations": []
    }
  },
  "metadata": {
    "construction_cost_tokens": 150,
    "size_bytes": 1400,
    "dependency_claims": ["sha256:research_protocol_v2"]
  }
}
```

### 6.7 R-Class VTD (Reasoning)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/r-class/v1",
  "type": "VTD_R_CLASS",
  "header": {
    "claim_hash": "sha256:s9t0u1...",
    "producer_id": "agent-027",
    "assigned_class": "R",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "premises": [
      {
        "id": "P1",
        "content": "Subjective Logic cumulative fusion converges for finite evidence sets",
        "support_type": "verified_claim",
        "support_ref": "sha256:josang_theorem_7_3",
        "credibility": 0.92
      },
      {
        "id": "P2",
        "content": "PCVM's dependency graphs are finite (bounded by knowledge cortex size)",
        "support_type": "verified_claim",
        "support_ref": "sha256:cortex_finite_bound",
        "credibility": 0.88
      },
      {
        "id": "P3",
        "content": "Iterative dampening with alpha < 1 guarantees convergence for cyclic graphs",
        "support_type": "verified_claim",
        "support_ref": "sha256:pagerank_convergence_proof",
        "credibility": 0.95
      }
    ],
    "inference_steps": [
      {
        "id": "I1",
        "from_premises": ["P1", "P2"],
        "rule": "universal_instantiation",
        "conclusion": "Subjective Logic fusion converges for PCVM's DAG subgraphs",
        "justification": "P1 applies to finite evidence sets; P2 establishes PCVM graphs are finite"
      },
      {
        "id": "I2",
        "from_premises": ["P3"],
        "rule": "conditional_application",
        "conclusion": "PCVM's cyclic subgraphs converge with dampening alpha=0.85",
        "justification": "P3 guarantees convergence for any alpha < 1; 0.85 < 1"
      },
      {
        "id": "I3",
        "from_premises": ["I1", "I2"],
        "rule": "conjunction_introduction",
        "conclusion": "PCVM's complete dependency graph (DAGs + cycles) converges under Subjective Logic with dampening",
        "justification": "DAGs converge by I1; cycles converge by I2; complete graph is union of DAGs and cycles"
      }
    ],
    "assumptions": [
      {
        "id": "A1",
        "content": "Classical logic (excluded middle, no paraconsistency)",
        "justification": "Standard assumption for formal reasoning"
      },
      {
        "id": "A2",
        "content": "Dampening factor is applied uniformly (no per-node adaptation)",
        "justification": "Simplifying assumption; per-node adaptation may improve convergence but is not required"
      }
    ]
  },
  "counter_evidence": {
    "search_performed": true,
    "considered": [
      {
        "source": "Skeptic position on credibility composition",
        "claim": "Subjective Logic is unvalidated for epistemic claim verification",
        "relevance": "Challenges P1's applicability to this domain",
        "response": "P1 is about mathematical convergence properties, which are domain-independent. The domain-specific question is whether the composed values are meaningful, which is separate from convergence."
      }
    ]
  },
  "metadata": {
    "construction_cost_tokens": 380,
    "size_bytes": 2400,
    "dependency_claims": ["sha256:josang_theorem_7_3", "sha256:cortex_finite_bound", "sha256:pagerank_convergence_proof"]
  }
}
```

### 6.8 C-Class VTD (Compliance)

```json
{
  "$schema": "https://pcvm.atrahasis.org/schemas/vtd/c-class/v1",
  "type": "VTD_C_CLASS",
  "header": {
    "claim_hash": "sha256:v2w3x4...",
    "producer_id": "agent-033",
    "assigned_class": "C",
    "epoch": 1042,
    "vtd_version": "1.0"
  },
  "evidence": {
    "regulation_reference": {
      "id": "EU_AI_ACT_2024_1689",
      "name": "EU AI Act",
      "article": "11",
      "title": "Technical Documentation"
    },
    "requirement_mapping": [
      {
        "requirement_id": "11.1.a",
        "requirement_text": "A general description of the AI system",
        "evidence_type": "document",
        "evidence_ref": "system_description_v3.pdf",
        "evidence_hash": "sha256:doc_hash_1",
        "compliance_status": "COMPLIANT",
        "last_reviewed": "2026-03-01"
      },
      {
        "requirement_id": "11.1.b",
        "requirement_text": "A detailed description of the elements of the AI system and of the process for its development",
        "evidence_type": "document",
        "evidence_ref": "development_process_v2.pdf",
        "evidence_hash": "sha256:doc_hash_2",
        "compliance_status": "COMPLIANT",
        "last_reviewed": "2026-03-01"
      }
    ],
    "gaps": [],
    "assessor_qualifications": "EU AI Act compliance training completed 2026-01-15"
  },
  "metadata": {
    "construction_cost_tokens": 200,
    "size_bytes": 1600,
    "dependency_claims": ["sha256:eu_ai_act_article_11_requirements"]
  }
}
```

---

## 7. Adversarial Defense Architecture

This section addresses all 5 attacks identified in the Adversarial Report, plus the additional mitigations required by the Assessment Council.

### 7.1 Attack 1: VTD Forgery ("Confident Liar") — CRITICAL

**Threat model:** Agent produces a structurally valid VTD with fabricated evidence. The VTD passes schema validation but contains false source citations, invented statistics, or fabricated reasoning.

**Defense layers (defense-in-depth):**

```
Layer 1: Structural Validation (automated, all claims)
    VTD conforms to schema? Required fields present? Types correct?
    Cost: negligible
    Catches: malformed forgeries, lazy attempts

Layer 2: Mandatory Source Verification (automated, E-class)
    Actually fetch cited URLs. Compare content hashes. Check quote accuracy.
    Cost: moderate (network I/O)
    Catches: fabricated citations, dead links, misquoted sources

Layer 3: Cross-Reference Checking (automated, E/S/R-class)
    Do independent sources confirm the claim?
    Cross-references consistent with primary sources?
    Cost: moderate
    Catches: claims with no independent support

Layer 4: Adversarial Probing (automated, Tier 2/3)
    Generate targeted challenges: counterexample search, assumption exposure,
    source challenge, logical fallacy detection.
    Cost: moderate-high
    Catches: sophisticated forgeries that resist structural checking

Layer 5: Committee Evaluation (human-equivalent, all claims)
    VRF-selected committee members independently assess VTD.
    Diverse committee composition prevents shared blind spots.
    Cost: O(committee_size)
    Catches: domain-specific forgeries that automated systems miss

Layer 6: Random Deep-Audit (replication, 5-10%)
    Full task replication for randomly selected passed claims.
    Cost: high (but applied to only 5-10% of claims)
    Catches: anything that slipped through Layers 1-5
    Deterrence: agents know any claim may be audited
```

**Expected detection rates by forgery sophistication:**

| Forgery Level | Description | Detection Rate |
|---------------|-------------|---------------|
| Naive | Wrong schema, missing fields | >99% (Layer 1) |
| Basic | Valid schema, dead links | >95% (Layer 2) |
| Moderate | Valid links, misquoted content | >85% (Layer 2-3) |
| Sophisticated | Real sources, misleading interpretation | >70% (Layer 3-4) |
| Expert | Inoculated against probing | >50% (Layer 5-6) |

The honest admission: expert-level forgeries may evade individual verification instances. The defense is probabilistic, not absolute. Deep-audit provides the backstop: over time, repeated forgery by the same agent will be detected, and credibility penalties compound.

### 7.2 Attack 2: Strategic Omission — HIGH

**Threat model:** Agent produces valid VTD that deliberately omits unfavorable evidence.

**Defense:**

1. **Counter-evidence requirement in VTD schema.** All Tier 2 and Tier 3 VTDs must include a `counter_evidence` section with:
   - `search_performed`: boolean (was a counter-evidence search conducted?)
   - `search_description`: string (what was searched for?)
   - `considered`: list of counter-evidence items with response
   - `none_found_attestation`: boolean (explicit attestation that no counter-evidence was found)

2. **Credibility penalties for empty counter-evidence:**
   - No search performed: -0.15 credibility for Tier 3, -0.10 for Tier 2
   - Search performed, nothing found: -0.05 (mild skepticism)
   - Search performed, counter-evidence addressed: no penalty

3. **Adversarial probe: mandatory counter-evidence search.** One probe type specifically searches for counter-evidence to the claim. If the probe finds counter-evidence that the VTD does not address, the claim is flagged for committee re-evaluation.

4. **Temporal defense.** As more claims enter the knowledge graph, contradictions with omitted evidence become discoverable. The Knowledge Cortex's contradiction detection (Section 4.9) catches omissions retroactively.

### 7.3 Attack 3: Class Downgrade — HIGH

**Threat model:** Agent deliberately misclassifies a claim to get easier verification.

**Defense: Membrane-Assigned Classification (REQ-2)**

The membrane, not the agent, assigns the final claim class. Defense implemented in Claim Classifier (Section 4.2):

1. Agent proposes class.
2. Membrane's multi-classifier ensemble independently classifies.
3. Membrane's classification wins in all cases.
4. Disagreements logged and tracked per agent.
5. Agents with systematic downgrade patterns (>30% rate) receive credibility penalty.
6. Deep-audit includes re-classification check.

**Why this is sufficient:** The agent cannot control the classification outcome. The membrane's classification accuracy (target: kappa >= 0.60 from GATE-2) is imperfect but independent of agent manipulation. Systematic gaming by the agent creates a detectable pattern.

### 7.4 Attack 4: Probe Evasion ("Inoculation") — HIGH

**Threat model:** Agent pre-fabricates responses to anticipated probe strategies, making the VTD appear robust against probing without actually being substantively tested.

**Defense: Dynamic Probe Generation**

```
function generate_probes(claim, vtd, classification):
    probes = []

    // Component 1: Fixed probe library (per class)
    // Known attack patterns that apply to this class
    library_probes = probe_library.get(classification.primary_class)
    probes.extend(sample(library_probes, count=2))

    // Component 2: Dynamic probe generation (LLM-generated)
    // Probes generated specifically for THIS claim, not from a library
    dynamic_prompt = f"""
    Given claim: {claim.content}
    Given VTD: {vtd.evidence}
    Generate 2 adversarial challenges that:
    1. Test assumptions the VTD does not explicitly address
    2. Search for counterexamples specific to this claim's domain
    3. Challenge the weakest link in the evidence chain
    Do NOT use standard challenge templates.
    """
    dynamic_probes = llm_generate(dynamic_prompt, prober_agent_id)
    probes.extend(dynamic_probes)

    // Component 3: Meta-probe (inoculation detection)
    meta_probe = MetaProbe(
        check = "Does the VTD contain pre-fabricated responses to standard probe patterns?",
        detection = "Responses that exactly match anticipated challenges are flagged as suspiciously convenient",
        threshold = "If >80% of VTD responses match template patterns, flag as potential inoculation"
    )
    probes.append(meta_probe)

    return probes
```

**Key principle:** Probing agents are VRF-selected (unpredictable) and use strategies not fully disclosed to producing agents. The dynamic generation component ensures that no fixed library can be completely inoculated against.

### 7.5 Attack 8: Mutual Endorsement (Collusion) — CRITICAL

**Threat model:** Multiple agents cooperate to validate each other's fraudulent VTDs.

**Defense (multi-layered):**

1. **VRF dual defense** (from Noosphere): Committee members drawn from pre-stratified diversity pools. Colluding agents distributed across pools proportionally. Probability of all-colluder committee for K=7: f^7 where f is collusion fraction.

2. **Committee size minimums:**

| Stakes Level | Minimum Committee Size | All-Colluder Probability (f=0.1) |
|-------------|----------------------|--------------------------------|
| LOW | 3 | 0.001 |
| MEDIUM | 5 | 0.00001 |
| HIGH | 7 | 0.0000001 |
| CRITICAL | 9 | 0.000000001 |

3. **Sentinel Graph collusion detection** (Section 4.8):
   - Pairwise endorsement correlation analysis
   - Dense subgraph detection in endorsement network
   - Anomaly scores for agent pairs exceeding 3x random baseline

4. **Random deep-audit with independent committee:**
   - Audit committee explicitly excludes original committee members
   - If audit result contradicts original, both producer and original committee penalized

5. **Cross-parcel audit sampling:**
   - Claims verified within the same parcel are cross-audited by agents from different parcels
   - Prevents intra-parcel collusion rings

6. **Temporal correlation analysis:**
   - Track endorsement patterns over rolling 50-epoch windows
   - Agents that consistently endorse each other flagged within ~20 epochs

**Deterrence model:** Even if a colluding committee passes a fraudulent claim, the 5-10% deep-audit rate means that over 20 claims, the expected number of audits is 1-2. A single audit failure triggers re-verification of all claims by the same producer AND credibility penalties for all endorsing verifiers. The expected cost of collusion (loss of credibility, settlement penalties, potential suspension) exceeds the benefit.

### 7.6 Attack 5: Reputation Laundering — MEDIUM

**Defense: Class-Specific Credibility (REQ-3)**

Agent credibility tracked per claim class (Section 4.7). An agent's D-class credibility (earned through easy deterministic proofs) does not transfer to H-class claims (requiring judgment verification).

```
// Discounting uses class-specific trust
function discount_for_class(agent_id, claim_class, agent_opinion):
    trust = get_agent_class_credibility(agent_id, claim_class)
    return discount(trust, agent_opinion)
    // Agent with high D-class trust but low H-class trust
    // gets heavy discounting on H-class claims
```

### 7.7 Attack 6: Constitutional Interpretation Exploitation — MEDIUM

**Defense:**

1. **Intent annotations.** Every constitutional parameter includes a natural-language intent annotation explaining what the parameter is trying to achieve, not just its formal specification.

2. **Constitutional case law.** Boundary interpretations are recorded as precedent claims (N-class). Over time, the body of case law reduces exploitable ambiguity.

3. **Spirit check in adversarial probing.** One probe type specifically checks whether the claim satisfies the constitutional parameter's intent, not just its letter.

### 7.8 Attack 7: VTD Explosion — MEDIUM

**Defense: Size Limits and Resource Budgets**

1. Per-class VTD size limits (Section 4.1, VTD Size Limits table).
2. Per-agent verification budget per epoch: each agent may submit at most `MAX_CLAIMS_PER_EPOCH` claims (default: 50).
3. Claims exceeding size limits are rejected with decomposition guidance.
4. Priority queue: HIGH and CRITICAL stakes claims processed first during high-load epochs.

### 7.9 Attack 9: Tier Collapse (Strategic) — HIGH

**Defense: Unified Architecture Validation (REQ-5)**

The architecture addresses the tier collapse critique through three mechanisms:

1. **Cross-class credibility composition.** Only possible in a unified membrane. If Tier 3 claims' credibility feeds into Tier 2 claims' dependency graphs (e.g., a statistical claim depends on a heuristic methodology choice), splitting into separate systems breaks this composition.

2. **Membrane sovereignty preservation.** INV-1 requires a single verification checkpoint. Three systems require coordination, creating sovereignty gaps at the boundaries.

3. **Measured honesty.** The architecture openly acknowledges that Tier 3 verification provides quality improvement (auditability, structured disagreement) rather than cost reduction. This is a feature description, not a defense — PCVM's value for Tier 3 is auditability, and the architecture says so explicitly.

The REQ-5 unified-vs-split analysis quantifies:

| Dimension | Unified Membrane | Three-Tier Split |
|-----------|-----------------|-----------------|
| Engineering complexity | 1 system with graduated depth | 3 systems + coordination layer |
| Credibility composition | Native cross-class composition | Requires cross-system bridge |
| Membrane sovereignty | Single checkpoint (INV-1 clean) | Three checkpoints (sovereignty model unclear) |
| Audit trail | Single VTD format family | Three document formats |
| Total system cost | Higher per-unit, lower system-level | Lower per-unit, higher coordination |

### 7.10 Attack 10: Bootstrap Problem — MEDIUM

**Defense: Bootstrap Protocol (REC-1)**

```
function bootstrap_system():
    // Phase 1: Seed Claims (manual)
    seed_claims = load_seed_corpus()  // 100-500 manually verified claims
    for claim in seed_claims:
        opinion = OpinionTuple(b=0.8, d=0.0, u=0.2, a=0.5)  // high initial credibility
        mct = create_bootstrap_mct(claim, opinion)
        knowledge_cortex.persist(Bundle(claim, mct))

    // Phase 2: Bootstrap Verification (first 50 epochs)
    // During bootstrap, all claims use enhanced verification:
    set_bootstrap_mode(true)
    //   - Deep-audit rate increased to 20% (vs normal 5-10%)
    //   - HIGH-stakes claims fall back to replication
    //   - Credibility propagation uses conservative dampening (alpha=0.70)
    //   - Agent credibility starts at full uncertainty (b=0, d=0, u=1, a=0.5)

    // Phase 3: Steady State Transition
    // After 50 epochs, if:
    //   - average credibility > 0.5
    //   - audit failure rate < 10%
    //   - classification agreement kappa > 0.55
    // then exit bootstrap mode
    set_bootstrap_mode(false)
    // Reduce deep-audit rate to normal
    // Allow full credibility propagation
    // Agent credibility transitions based on accumulated evidence
```

**Expected bootstrap duration:** 50-100 epochs (50-100 hours at 1-hour epochs). During this period, verification is more expensive and conservative. This is acceptable for system initialization.

---

## 8. Scalability Architecture

### 8.1 Scale Targets

| Phase | Agent Count | Claims/Epoch | VTDs/Epoch | Parcels |
|-------|------------|-------------|-----------|---------|
| Phase 1 (MVP) | 10-100 | 50-500 | 50-500 | 1-5 |
| Phase 2 | 100-1K | 500-5K | 500-5K | 5-50 |
| Phase 3 | 1K-10K | 5K-50K | 5K-50K | 50-500 |
| Phase 4 (aspiration) | 10K-100K | 50K-500K | 50K-500K | 500-5K |

### 8.2 Scaling Bottlenecks and Mitigations

**Source verification (E-class):** Network I/O for fetching cited sources. Mitigation: source verification cache shared across verifiers. If source was verified within the last 10 epochs, reuse cached result.

**Credibility propagation:** O(edges) per propagation event. At 50K claims with average degree 3, that is 150K edges. Mitigation: batch propagation at epoch boundary (not per-claim). Rate limiter: max 100 propagation events per epoch.

**Deep-audit:** 5-10% of claims require full replication. At 50K claims/epoch, that is 2,500-5,000 replications. Mitigation: asynchronous audit (results in 1-3 epochs, not real-time). Audit queue with priority ordering.

**VTD storage:** At 50K VTDs/epoch averaging 2KB each, that is ~100MB/epoch or ~876GB/year. Mitigation: cold storage for VTDs older than retention window. Hot storage for active VTDs only.

**Sentinel Graph affinity matrix:** O(V^2) where V is verifier count. At 10K verifiers, 100M entries. Mitigation: approximate methods (locality-sensitive hashing for correlation detection). Track only statistically significant pairs.

### 8.3 Parallelization Strategy

PCVM verification is embarrassingly parallel at the claim level: each claim's verification is independent (until credibility propagation). The dispatcher can process claims in parallel across available compute:

```
// Per-epoch verification pipeline
function process_epoch(verification_requests):
    // Phase 1: Classification (parallel)
    classifications = parallel_map(classify_claim, verification_requests)

    // Phase 2: VTD construction (parallel)
    vtds = parallel_map(construct_vtd, zip(verification_requests, classifications))

    // Phase 3: Tier-specific verification (parallel)
    results = parallel_map(verify, zip(verification_requests, vtds, classifications))

    // Phase 4: Credibility composition (sequential per dependency chain, parallel across chains)
    opinions = batch_compose_credibility(results)

    // Phase 5: Admission decisions (parallel)
    admissions = parallel_map(admit, zip(results, opinions))

    // Phase 6: Credibility propagation (batched, at epoch boundary)
    propagate_all_changes(admissions)
```

---

## 9. Security Model

### 9.1 Threat Model

**Adversary capabilities:**
- Controls up to f < 0.33 of agents (BFT assumption inherited from Noosphere)
- Can produce arbitrary VTDs (no restriction on content)
- Can observe public system state (claim hashes, committee assignments after selection)
- Cannot predict VRF outputs before epoch boundary
- Cannot forge VRF proofs
- Cannot break SHA-256 or ECVRF cryptographic primitives

**Assets protected:**
- Knowledge graph integrity (no false claims admitted)
- Credibility system accuracy (no undeserved reputation)
- Constitutional sovereignty (no unauthorized parameter changes)
- Audit trail completeness (no evidence destruction)

### 9.2 Security Properties

| Property | Guarantee | Mechanism |
|----------|-----------|-----------|
| Claim integrity | No unauthorized modification of admitted claims | Content-addressed VTD store, MCT signatures |
| Verification integrity | Committee cannot be manipulated | VRF dual defense (commit-reveal + pre-stratified pools) |
| Audit trail immutability | VTDs cannot be deleted or modified after submission | Append-only VTD store, content-addressed by hash |
| Credibility accuracy | Agent credibility reflects actual verification history | Per-class tracking, deep-audit calibration |
| Classification independence | Agent cannot control final classification | Membrane-assigned classification |
| Collusion resistance | Colluding minority detected within ~20 epochs | Sentinel Graph affinity matrix, cross-parcel audit |
| Forgery deterrence | Fabricated VTDs detected probabilistically | Source verification + deep-audit (5-10%) |

### 9.3 Cryptographic Components

| Component | Primitive | Standard |
|-----------|-----------|----------|
| VTD content addressing | SHA-256 | FIPS 180-4 |
| VRF committee selection | ECVRF | RFC 9381 |
| MCT signatures | Ed25519 | RFC 8032 |
| Source content hashing | SHA-256 | FIPS 180-4 |
| Randomness beacon | VRF chain | Inherited from Noosphere |

### 9.4 Trust Assumptions

1. **The membrane itself is honest.** PCVM code is constitutionally protected and auditable. This is an infrastructure trust assumption, not a claim about individual agents.
2. **Constitutional axioms are correct.** The constitutional foundation is assumed valid. Errors in constitutional parameters propagate through all claims that depend on them.
3. **Source accessibility.** Source verification assumes cited URLs are accessible. If sources become permanently inaccessible, E-class claims depending on them degrade gracefully (increased uncertainty, not immediate rejection).
4. **LLM classifier reliability.** Classification accuracy depends on LLM capability. Degradation in LLM quality degrades classification quality. Monitored via GATE-2 metrics.

---

## 10. Architectural Decisions

### 10.1 AD-1: Unified Membrane vs. Three-Tier Split

**Decision:** Unified membrane with graduated verification depth.

**Alternatives considered:**
- (A) Unified membrane (chosen)
- (B) Three separate systems: proof-checker, evidence evaluator, documentation standard

**Rationale:**
- Membrane sovereignty (INV-1, INV-2) requires single checkpoint
- Cross-class credibility composition only works in unified system
- Engineering one system with graduated depth is simpler than coordinating three
- Single VTD format family reduces integration complexity

**Tradeoff accepted:** Tier 3 verification within PCVM is genuinely more expensive than replication. The architecture accepts this cost for auditability and sovereignty benefits.

**Validation:** REQ-5 mandates comparative analysis. If split architecture is >30% simpler with <10% capability loss, reconsider.

### 10.2 AD-2: Subjective Logic vs. Alternatives

**Decision:** Adopt Josang's Subjective Logic for credibility composition.

**Alternatives considered:**
- (A) Subjective Logic (chosen)
- (B) Bayesian networks
- (C) Dempster-Shafer theory
- (D) Novel custom algebra

**Rationale:**
- Subjective Logic explicitly represents uncertainty (not just point probabilities)
- Well-defined operators for trust in multi-agent systems (discounting, fusion)
- Proven convergence properties for finite evidence sets
- Avoids risk of inventing unproven mathematics (option D)
- Better suited to trust management than Dempster-Shafer (option C)
- Handles explicit uncertainty better than Bayesian (option B)

**Tradeoff accepted:** Subjective Logic was designed for trust management, not epistemic claim verification. The domain adaptation (especially N-class where b/d represent constitutional alignment) is novel and unvalidated.

**Validation:** GATE-3 tests convergence and stability. If Subjective Logic fails gates, fallback to min-credibility chains.

### 10.3 AD-3: Membrane-Assigned Classification

**Decision:** Membrane assigns final claim class; agents propose.

**Alternatives considered:**
- (A) Membrane assigns (chosen)
- (B) Agent self-classifies
- (C) Joint classification (agent and membrane must agree)
- (D) Committee classifies

**Rationale:**
- Agent self-classification enables gaming (Attack 3)
- Joint classification creates deadlocks on disagreement
- Committee classification adds O(committee) cost to classification step
- Membrane classification is efficient and prevents gaming

**Tradeoff accepted:** Membrane classification accuracy is imperfect (target kappa >= 0.60). Some claims will be misclassified, leading to wrong-tier verification. Deep-audit re-classification provides retroactive correction.

### 10.4 AD-4: Random Deep-Audit Rate

**Decision:** 5-10% of passed VTDs undergo full-replication audit, with class-specific rates.

**Alternatives considered:**
- (A) Fixed 5-10% random (chosen, with risk-adjusted variation)
- (B) 100% audit (full replication for everything)
- (C) 0% audit (trust the VTD pipeline)
- (D) Targeted-only audit (audit only flagged claims)

**Rationale:**
- 100% audit negates the cost advantage of VTDs entirely
- 0% audit provides no forgery deterrence
- Targeted-only audit misses unflagged forgeries
- Random 5-10% provides deterrence (any claim may be audited) at acceptable cost

**Tradeoff accepted:** 5-10% audit rate means 90-95% of forgeries that evade Layers 1-5 will not be caught in a single epoch. Over multiple epochs and multiple claims by the same agent, cumulative detection probability increases. This is a probabilistic defense, not a guarantee.

### 10.5 AD-5: Adversarial Probing as Integral Component

**Decision:** Include automated adversarial probing as an integral PCVM component, not an optional extension.

**Alternatives considered:**
- (A) Integral probing (chosen)
- (B) Optional probing module
- (C) No probing (rely on committee evaluation and deep-audit)
- (D) Human-only adversarial review

**Rationale:**
- Probing addresses VTD forgery and strategic omission at lower cost than full replication
- Optional probing creates incentive to disable it during cost pressure
- No probing leaves a defense gap between structural checking and deep-audit
- Human review does not scale

**Tradeoff accepted:** Probing adds cost. For some claim classes, total verification cost with probing exceeds replication cost. GATE-4 validates that probing provides sufficient marginal value (F1 improvement >= 0.10 over VTD-only).

### 10.6 AD-6: 8-Class Taxonomy

**Decision:** 8 claim classes derived from epistemic status x verification modality matrix.

**Alternatives considered:**
- (A) 8 classes (chosen)
- (B) 3 classes aligned to verification tiers
- (C) Continuous classification (no discrete classes)
- (D) Extensible taxonomy with initial 4-5 classes

**Rationale:**
- 3 classes too coarse — D-class and C-class have fundamentally different verification
- Continuous classification prevents differential proof obligations
- 8 classes derived from principled matrix rather than ad hoc selection
- Extensible by adding cells to the matrix if new claim types emerge

**Tradeoff accepted:** 8 classes may be too many for reliable automated classification (GATE-2 tests this). Fallback: merge confused class pairs to reach 5-class taxonomy.

---

## 11. Traceability Appendix

### 11.1 Feasibility Conditions Mapping

| Condition ID | Condition | Architecture Section | Status |
|-------------|-----------|---------------------|--------|
| GATE-1 | VTD Feasibility Experiment | Section 3.1 | Experiment designed |
| GATE-2 | Claim Classification Reliability | Section 3.2 | Experiment designed |
| GATE-3 | Credibility Propagation Stability | Section 3.3 | Experiment designed |
| GATE-4 | Adversarial Probing Effectiveness | Section 3.4 | Experiment designed |
| REQ-1 | Mandatory Source Verification | Section 4.5 (verify_source), 7.1 Layer 2 | Implemented |
| REQ-2 | Membrane-Assigned Classification | Section 4.2 (classify_claim), 7.3 | Implemented |
| REQ-3 | Class-Specific Agent Credibility | Section 4.7 (AgentCredibility), 7.6 | Implemented |
| REQ-4 | Random Deep-Audit Protocol | Section 4.8 | Implemented |
| REQ-5 | Unified vs. Split Architecture | Section 7.9, AD-1 | Analysis provided |
| REC-1 | Bootstrap Protocol | Section 7.10 | Implemented |
| REC-2 | Constitutional Parameter Draft | Deferred to specification stage | Pending |
| REC-3 | VTD Size Limits | Section 4.1 (VTD Size Limits table) | Implemented |

### 11.2 Adversarial Report Mapping

| Attack # | Attack Name | Severity | Architecture Section | Mitigation Status |
|----------|-------------|----------|---------------------|-------------------|
| 1 | VTD Forgery (Confident Liar) | CRITICAL | Section 7.1 | 6-layer defense-in-depth |
| 2 | Strategic Omission | HIGH | Section 7.2 | Counter-evidence requirement + probing |
| 3 | Class Downgrade | HIGH | Section 7.3 | Membrane-assigned classification |
| 4 | Probe Evasion (Inoculation) | HIGH | Section 7.4 | Dynamic probe generation + meta-probe |
| 5 | Reputation Laundering | MEDIUM | Section 7.6 | Class-specific credibility |
| 6 | Constitutional Exploitation | MEDIUM | Section 7.7 | Intent annotations + case law |
| 7 | VTD Explosion | MEDIUM | Section 7.8 | Size limits + resource budgets |
| 8 | Mutual Endorsement (Collusion) | CRITICAL | Section 7.5 | VRF + Sentinel + deep-audit + cross-parcel |
| 9 | Tier Collapse | HIGH | Section 7.9 | Unified architecture with honest acknowledgment |
| 10 | Bootstrap Problem | MEDIUM | Section 7.10 | Seed claims + bootstrap mode |

### 11.3 Noosphere Invariant Compliance

| Invariant | PCVM Compliance |
|-----------|----------------|
| INV-1: No claim enters durable memory without passing membrane | Knowledge Admission Gate (Section 4.9) is sole entry point |
| INV-2: Membrane cannot be weakened by non-constitutional action | PCVM parameters are G-class protected |
| INV-7: Tidal function version is verified claim within membrane | PCVM can verify tidal function versions as C-class or R-class claims |

### 11.4 Component Dependency Graph

```
                    +-------------------+
                    | Tidal Noosphere   |
                    | (VRF, epochs,     |
                    |  committees)      |
                    +--------+----------+
                             |
                    +--------v----------+
                    | Verification      |
                    | Dispatcher (4.3)  |
                    +--------+----------+
                             |
              +--------------+--------------+
              |              |              |
    +---------v---+  +-------v------+ +----v-----------+
    | Claim       |  | VTD Engine   | | Adversarial    |
    | Classifier  |  | (4.1)        | | Prober (via    |
    | (4.2)       |  |              | | Dispatcher)    |
    +------+------+  +------+-------+ +-------+--------+
           |                |                  |
           |         +------v-------+          |
           |         | Tier-Specific |          |
           |         | Verifiers:    |<---------+
           |         | 4.4 Proof     |
           |         | 4.5 Evidence  |
           |         | 4.6 Attest.   |
           |         +------+-------+
           |                |
           |         +------v-------+
           +-------->| Credibility  |
                     | Engine (4.7) |
                     +------+-------+
                            |
              +-------------+-------------+
              |                           |
    +---------v---------+     +-----------v---------+
    | Knowledge         |     | Deep-Audit          |
    | Admission Gate    |     | Subsystem (4.8)     |
    | (4.9)             |     +---------------------+
    +---------+---------+
              |
    +---------v---------+
    | Knowledge Cortex  |
    | (BDL persistence) |
    +-------------------+
```

### 11.5 Constitutional Parameters (Draft, per REC-2)

The following constitutional parameters govern PCVM's operation. All are G-class protected (75% supermajority to modify).

| Parameter ID | Name | Default Value | Description |
|-------------|------|---------------|-------------|
| PCVM-001 | admission_threshold_D | 0.95 | Minimum projected probability for D-class admission |
| PCVM-002 | admission_threshold_E | 0.60 | Minimum projected probability for E-class admission |
| PCVM-003 | admission_threshold_S | 0.65 | Minimum projected probability for S-class admission |
| PCVM-004 | admission_threshold_H | 0.50 | Minimum projected probability for H-class admission |
| PCVM-005 | admission_threshold_N | 0.50 | Minimum projected probability for N-class admission |
| PCVM-006 | admission_threshold_P | 0.80 | Minimum projected probability for P-class admission |
| PCVM-007 | admission_threshold_R | 0.75 | Minimum projected probability for R-class admission |
| PCVM-008 | admission_threshold_C | 0.90 | Minimum projected probability for C-class admission |
| PCVM-009 | deep_audit_rate_base | 0.07 | Base deep-audit rate (adjusted per class) |
| PCVM-010 | base_probe_rate | 0.15 | Random probe rate for MEDIUM/LOW-stakes Tier 2 |
| PCVM-011 | dampening_factor | 0.85 | Credibility propagation dampening |
| PCVM-012 | max_claims_per_agent_per_epoch | 50 | Resource budget per agent |
| PCVM-013 | classification_override_penalty_threshold | 0.30 | Agent downgrade rate triggering penalty |
| PCVM-014 | collusion_anomaly_threshold | 3.0 | Chi-squared-like score for flagging agent pairs |
| PCVM-015 | committee_size_LOW | 3 | Committee size for LOW-stakes claims |
| PCVM-016 | committee_size_MEDIUM | 5 | Committee size for MEDIUM-stakes claims |
| PCVM-017 | committee_size_HIGH | 7 | Committee size for HIGH-stakes claims |
| PCVM-018 | committee_size_CRITICAL | 9 | Committee size for CRITICAL-stakes claims |
| PCVM-019 | vtd_max_size_D | 10240 | Max VTD size in bytes for D-class |
| PCVM-020 | vtd_max_size_E | 51200 | Max VTD size in bytes for E-class |
| PCVM-021 | vtd_max_size_S | 30720 | Max VTD size in bytes for S-class |
| PCVM-022 | vtd_max_size_H | 102400 | Max VTD size in bytes for H-class |
| PCVM-023 | vtd_max_size_N | 81920 | Max VTD size in bytes for N-class |
| PCVM-024 | vtd_max_size_P | 40960 | Max VTD size in bytes for P-class |
| PCVM-025 | vtd_max_size_R | 30720 | Max VTD size in bytes for R-class |
| PCVM-026 | vtd_max_size_C | 51200 | Max VTD size in bytes for C-class |
| PCVM-027 | bootstrap_audit_rate | 0.20 | Deep-audit rate during bootstrap |
| PCVM-028 | bootstrap_dampening | 0.70 | Conservative dampening during bootstrap |
| PCVM-029 | convergence_epsilon | 0.001 | Credibility propagation convergence threshold |
| PCVM-030 | max_propagation_iterations | 100 | Maximum credibility propagation iterations |
| PCVM-031 | source_verification_timeout | 10000 | Source fetch timeout in milliseconds |
| PCVM-032 | audit_window_epochs | 10 | Window for deep-audit claim selection |

---

*Architecture document completed 2026-03-09. Architecture Designer, Atrahasis Agent System v2.0.*
*Protocol: DESIGN Stage v2.0*
*Traceability: All 4 gates designed, all 5 adversarial attacks addressed, all 12 feasibility conditions mapped.*
