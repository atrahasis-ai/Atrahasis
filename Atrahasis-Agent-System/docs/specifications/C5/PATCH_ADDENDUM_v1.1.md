# PCVM Patch Addendum v1.1

## Errata and Corrections to C5 Master Tech Spec v1.0.0

**Date:** 2026-03-10
**Applies to:** C5 MASTER_TECH_SPEC.md v1.0.0
**Status:** NORMATIVE PATCH -- all sections below supersede corresponding sections of the base specification
**Cross-references:** C9 Reconciliation (K-class addition)

---

## PA-F19: Corrected Cost Claim (Abstract)

**Severity:** HIGH
**Applies to:** Abstract (line 19), Section 14 Conclusion (line 1222)

The abstract claims "system-level verification cost reduction of 40-60%" but Section 12.2 calculates a weighted average cost of 0.83x (17% savings) before trust propagation. The 40-60% figure is a projected estimate that depends on downstream trust propagation assumptions (average citation count of 3, full avoidance of re-verification for cited claims) that are neither guaranteed nor empirically validated. The abstract MUST lead with the calculated figure and qualify the projected one.

### Corrected Abstract Paragraph (replaces final sentence of Abstract)

> System-level verification cost is approximately 0.83x of universal replication (a 17% reduction), calculated from the weighted cost across all eight claim classes including deep-audit overhead. This modest direct savings reflects the honest cost of Tier 3 claims (H-class and N-class), which consume 1.5x-2.0x of replication cost and constitute approximately 20% of claim volume. The deeper cost advantage emerges through downstream trust propagation: when verified claims are cited by subsequent claims, the citing claims inherit credibility without triggering re-verification of their dependencies. Under the assumption that each verified claim is cited an average of 3 times (a figure that requires empirical validation during pilot deployment), effective system cost drops to approximately 0.40x-0.60x of universal replication. The 40-60% figure is therefore a projected long-term savings contingent on citation density, not a guaranteed per-epoch reduction.

### Corrected Conclusion Paragraph (replaces corresponding sentence in Section 14)

Replace:

> The system-level cost reduction of 40-60% (accounting for downstream trust propagation) is meaningful but not transformative.

With:

> The system-level direct cost reduction of 17% (0.83x of replication) is modest. With downstream trust propagation -- contingent on empirical validation of citation density assumptions -- projected savings reach 40-60%. The value proposition is therefore not primarily cost but quality: VTDs produce richer verification metadata than binary pass/fail, credibility opinions propagate through knowledge graphs to give downstream consumers calibrated confidence, and adversarial probing exposes weaknesses that replication-based consensus would miss.

---

## PA-F20: Classification Signature Definitions

**Severity:** HIGH (blocks implementation)
**Applies to:** Section 5.3, specifically the `CLASSIFICATION_SIGNATURES[cls]` reference in `classify_claim()` pseudocode

The pseudocode references `CLASSIFICATION_SIGNATURES[cls]` with `.markers` and `.exclusion` fields but never defines them. Below is the complete definition for all 8 classes. Each signature contains structural text patterns (matched against `claim.text` and VTD `proof_body` field names) that indicate or exclude a class. Pattern matching uses case-insensitive substring or regex matching against the claim text and VTD structure.

### Definition

```python
# Each signature has:
#   markers:   list of (pattern, weight) tuples. A pattern match contributes
#              its weight toward the class score. Patterns are regex.
#   exclusion: list of patterns. ANY match disqualifies this class (score = 0).
#
# count_matching_markers() returns sum of weights for matched marker patterns.
# len(sig.markers) returns sum of all possible weights (for normalization).

CLASSIFICATION_SIGNATURES = {

    "D": ClassificationSignature(
        markers=[
            (r"\b(comput|calculat|hash|sort|encrypt|decrypt|deterministic)\b", 1.0),
            (r"\b(algorithm|function|output\s+equals?|result\s+is)\b", 0.8),
            (r"\b(SHA-?\d+|MD5|AES|RSA|CRC)\b", 1.0),
            (r"\b(recomput|replay|reproduce|identical)\b", 0.7),
            (r"\b(given\s+input|for\s+input|on\s+input)\b", 0.6),
            # VTD structural: proof_body has computation + inputs + output fields
            (r"__vtd_has_field:computation", 1.0),
            (r"__vtd_has_field:proof_type", 0.8),
        ],
        exclusion=[
            r"\b(recommend|should|ought|ethic|moral|stakeholder)\b",
            r"\b(heuristic|judgment|opinion|believe|estimate|approximate)\b",
            r"\b(survey|sample|population|p-value|confidence\s+interval)\b",
            r"\b(observed|measured|experiment|benchmark\s+score)\b",
        ]
    ),

    "E": ClassificationSignature(
        markers=[
            (r"\b(observed|measured|recorded|reported|found\s+that)\b", 1.0),
            (r"\b(benchmark|experiment|study\s+shows?|data\s+shows?)\b", 1.0),
            (r"\b(source|citation|according\s+to|per\s+\w+\s+report)\b", 0.8),
            (r"\b(empirical|evidence|finding|result)\b", 0.7),
            (r"\b(score[ds]?\s+\d|achieve[ds]?\s+\d|percent|rate\s+of)\b", 0.8),
            (r"\b(as\s+of\s+\d{4}|in\s+\d{4}|published)\b", 0.6),
            # VTD structural: proof_body has sources + evidence_chain
            (r"__vtd_has_field:sources", 1.0),
            (r"__vtd_has_field:evidence_chain", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|sort\s+of\s+\[|given\s+input)\b",
            r"\b(p-value|confidence\s+interval|regression|hypothesis\s+test)\b",
            r"\b(should|ought|recommend|ethic|normative)\b",
        ]
    ),

    "S": ClassificationSignature(
        markers=[
            (r"\b(statistic|p-value|confidence\s+interval|significance)\b", 1.0),
            (r"\b(sample\s+size|population|regression|correlation)\b", 1.0),
            (r"\b(hypothesis|null|alternative\s+hypothesis|test\s+shows?)\b", 0.9),
            (r"\b(mean|median|standard\s+deviation|variance|effect\s+size)\b", 0.8),
            (r"\b(chi-squared|t-test|ANOVA|Mann-Whitney|Wilcoxon)\b", 1.0),
            (r"\b(dataset|n\s*=\s*\d+|sampling)\b", 0.7),
            # VTD structural: proof_body has dataset + methodology + results
            (r"__vtd_has_field:dataset", 1.0),
            (r"__vtd_has_field:methodology", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash|encrypt)\b",
            r"\b(should|ought|recommend|ethic|normative)\b",
            r"\b(process\s+was\s+followed|step\s+\d+\s+executed)\b",
        ]
    ),

    "H": ClassificationSignature(
        markers=[
            (r"\b(recommend|suggest|advise|best\s+practice)\b", 1.0),
            (r"\b(heuristic|judgment|expert\s+opinion|pragmatic)\b", 1.0),
            (r"\b(trade-?off|alternative|option|weigh|criterion)\b", 0.9),
            (r"\b(architecture\s+decision|design\s+choice|approach)\b", 0.8),
            (r"\b(prefer|favor|better\s+suited|most\s+appropriate)\b", 0.8),
            (r"\b(confidence|uncertain|risk|failure\s+mode)\b", 0.6),
            # VTD structural: proof_body has alternatives + criteria + evaluation
            (r"__vtd_has_field:alternatives", 1.0),
            (r"__vtd_has_field:criteria", 0.8),
            (r"__vtd_has_field:evaluation", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|sort\s+of\s+\[)\b",
            r"\b(ethic|moral|normative|value\s+framework|stakeholder\s+impact)\b",
            r"\b(regulation|compliance|Article\s+\d+)\b",
        ]
    ),

    "N": ClassificationSignature(
        markers=[
            (r"\b(ethic|moral|normative|value|principle)\b", 1.0),
            (r"\b(should|ought|right|wrong|fair|just|equitable)\b", 0.9),
            (r"\b(stakeholder|impact\s+on|affected\s+part(y|ies))\b", 0.8),
            (r"\b(constitutional|governance|policy|guideline)\b", 0.8),
            (r"\b(deontolog|consequential|virtue\s+ethic|care\s+ethic)\b", 1.0),
            (r"\b(consent|autonomy|transparency|accountability)\b", 0.7),
            # VTD structural: proof_body has value_framework + stakeholder_analysis
            (r"__vtd_has_field:value_framework", 1.0),
            (r"__vtd_has_field:stakeholder_analysis", 0.9),
            (r"__vtd_has_field:constitutional_refs", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash|comput\w+\s+result)\b",
            r"\b(p-value|sample\s+size|regression)\b",
            r"\b(benchmark\s+score|measured|experiment)\b",
        ]
    ),

    "P": ClassificationSignature(
        markers=[
            (r"\b(process|procedure|protocol|pipeline|workflow)\b", 1.0),
            (r"\b(step\s+\d+|phase\s+\d+|stage\s+\d+)\b", 0.9),
            (r"\b(followed|executed|completed|adhered\s+to)\b", 0.8),
            (r"\b(conformance|compliance\s+with\s+process|deviat)\b", 0.9),
            (r"\b(log|trace|timestamp|audit\s+trail)\b", 0.7),
            (r"\b(specification\s+\w+\s+was|per\s+SOP|per\s+spec)\b", 0.8),
            # VTD structural: proof_body has process_spec + steps
            (r"__vtd_has_field:process_spec", 1.0),
            (r"__vtd_has_field:steps", 0.9),
            (r"__vtd_has_field:conformance_summary", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of)\b",
            r"\b(ethic|moral|normative|stakeholder)\b",
            r"\b(recommend|suggest|best\s+practice)\b",
        ]
    ),

    "R": ClassificationSignature(
        markers=[
            (r"\b(therefore|hence|thus|it\s+follows|because|since)\b", 0.9),
            (r"\b(premise|conclusion|argument|infer|deduc|induc)\b", 1.0),
            (r"\b(modus\s+ponens|syllogism|contrapositive|reductio)\b", 1.0),
            (r"\b(if\s+.+then|implies|entails|necessitates)\b", 0.8),
            (r"\b(logical|valid|sound|fallacy|assumption)\b", 0.8),
            (r"\b(proof\s+by|derive|establish\s+that)\b", 0.7),
            # VTD structural: proof_body has premises + inferences
            (r"__vtd_has_field:premises", 1.0),
            (r"__vtd_has_field:inferences", 1.0),
            (r"__vtd_has_field:logical_assessment", 0.8),
        ],
        exclusion=[
            r"\b(deterministic|hash\s+of|encrypt)\b",
            r"\b(ethic|moral|normative|stakeholder)\b",
            r"\b(p-value|sample\s+size|regression)\b",
            r"\b(recommend|suggest|best\s+practice|trade-?off)\b",
        ]
    ),

    "C": ClassificationSignature(
        markers=[
            (r"\b(comply|compliance|compliant|conform)\b", 1.0),
            (r"\b(regulation|regulatory|Article\s+\d+|Section\s+\d+)\b", 1.0),
            (r"\b(EU\s+AI\s+Act|GDPR|NIST|ISO\s+\d+|SOC\s+\d)\b", 1.0),
            (r"\b(requirement\s+\w+\s+(met|satisfied)|satisfies)\b", 0.9),
            (r"\b(audit|gap\s+analysis|remediation)\b", 0.7),
            (r"\b(constitutional\s+parameter|CONST-\d+)\b", 0.8),
            # VTD structural: proof_body has regulation + requirements
            (r"__vtd_has_field:regulation", 1.0),
            (r"__vtd_has_field:requirements", 0.9),
            (r"__vtd_has_field:compliance_status", 0.8),
        ],
        exclusion=[
            r"\b(recommend|suggest|best\s+practice|heuristic)\b",
            r"\b(ethic|moral|normative\s+framework)\b",
            r"\b(p-value|sample\s+size|hypothesis\s+test)\b",
            r"\b(observed|measured|benchmark\s+score)\b",
        ]
    ),
}
```

### Matching Functions

```python
def count_matching_markers(claim_text: str, vtd: VTD, markers: list) -> float:
    """Returns sum of weights for markers that match claim text or VTD structure."""
    score = 0.0
    for pattern, weight in markers:
        if pattern.startswith("__vtd_has_field:"):
            field_name = pattern.split(":")[1]
            if hasattr(vtd.proof_body, field_name) and \
               getattr(vtd.proof_body, field_name) is not None:
                score += weight
        else:
            if re.search(pattern, claim_text, re.IGNORECASE):
                score += weight
    return score

def max_possible_score(markers: list) -> float:
    """Returns sum of all weights (normalization denominator)."""
    return sum(weight for _, weight in markers)
```

### Updated classify_claim (replaces Section 5.3 structural analysis block)

```python
    # Step 2: Structural analysis against classification signatures
    structural_scores = {}
    for cls in ClaimClass:
        sig = CLASSIFICATION_SIGNATURES[cls]
        # Check exclusions first
        excluded = False
        for excl_pattern in sig.exclusion:
            if re.search(excl_pattern, claim.text, re.IGNORECASE):
                excluded = True
                break
        if excluded:
            structural_scores[cls] = 0.0
        else:
            matched = count_matching_markers(claim.text, vtd, sig.markers)
            structural_scores[cls] = matched / max_possible_score(sig.markers)
    structural_class = max(structural_scores, key=structural_scores.get)
```

---

## PA-F21: Conservatism Ordering Clarification

**Severity:** HIGH
**Applies to:** Section 5.3, paragraph after the `classify_claim()` pseudocode (line 502)

### Replacement Text

The original text states:

> The **most conservative class** (highest verification cost) is selected when all three inputs disagree. Conservatism ordering: H > N > E > S > R > P > C > D.

Replace with:

> The **most conservative class** is selected when all three classification inputs disagree. Per C9 reconciliation, the conservatism ordering is:
>
> **H > N > K > E > S > R > P > C > D**
>
> "Most conservative" means "requires the most rigorous verification," not "most expensive." The ordering reflects verification rigor -- the degree to which mechanical checking is insufficient and human judgment, empirical grounding, or structured reasoning is required:
>
> - **H, N (highest rigor):** These classes require human expert judgment that cannot be reduced to algorithmic checking. H-class demands evaluation of whether alternatives were genuinely considered and whether criteria are appropriate -- judgments that resist formalization. N-class demands assessment of constitutional alignment and stakeholder impact -- inherently value-laden evaluations. Defaulting a disputed claim to H or N forces the most thorough verification pathway.
>
> - **K (high rigor):** Knowledge Consolidation claims synthesize across multiple source quanta and agents. Verification must confirm provenance diversity and reasoning chain validity -- checks that require cross-referencing multiple knowledge artifacts, not just evaluating a single evidence chain.
>
> - **E, S (moderate rigor):** These classes require empirical evidence that can be partially checked mechanically (source verification, arithmetic recomputation) but ultimately depend on assessing source reliability and methodological soundness -- judgments that go beyond formal proof.
>
> - **R, P (structured rigor):** These classes admit structured checking: logical validity for R-class, trace conformance for P-class. While not fully decidable (soundness requires premise evaluation), the verification steps are well-defined and largely mechanical.
>
> - **C, D (lowest rigor, formally decidable):** These classes can be mechanically verified. D-class through computation replay, C-class through rule matching against a finite requirement set. Defaulting a disputed claim to C or D would be insufficiently rigorous for any claim that might actually require judgment or evidence.
>
> Note that this ordering intentionally diverges from cost ordering. H-class verification (2.0x) is more expensive than E-class (0.8x), but the conservatism ordering is not about cost -- it is about the consequence of under-verifying. A heuristic claim verified only at D-class rigor would pass without any assessment of alternatives or uncertainty, producing a dangerously overconfident result. The ordering ensures that ambiguous claims receive enough scrutiny.

### Updated Conservatism Function

```python
CONSERVATISM_ORDER = {
    "H": 8, "N": 7, "K": 6, "E": 5, "S": 4, "R": 3, "P": 2, "C": 1, "D": 0
}

def most_conservative_class(classes: list) -> str:
    """Return the class requiring the most rigorous verification."""
    return max(classes, key=lambda c: CONSERVATISM_ORDER[c])
```

---

## PA-F22: Circular E-class Verification Fix (Level 4 Optional)

**Severity:** MEDIUM
**Applies to:** Section 6.2, E-class mandatory source verification (REQ-1), specifically the Level 4 check (line 603)

### Problem

Level 4 ("contextual relevance") of E-class source verification calls `assess_relevance()`, which itself requires understanding whether a source supports a claim -- the same judgment the overall verification is trying to make. This creates a verification regress: to verify a claim, you must assess relevance; to assess relevance, you must understand the claim's relationship to its evidence, which is itself the object of verification.

### Fix

Level 4 is removed from routine verification and made an optional adversarial-probe-triggered check. Levels 1-3 (URL accessibility, content hash, quote accuracy) are sufficient for routine verification because they mechanically confirm that the cited source exists, has not changed, and contains the quoted text. Contextual relevance -- whether the source actually supports the claim's conclusion -- is a semantic judgment better suited to adversarial probing, where a dedicated prober can invest the cognitive budget to evaluate relevance without creating circular verification dependencies.

### Corrected Pseudocode (replaces Section 6.2 E-class source verification)

```python
def verify_source(source, probe_mode=False):
    """
    Verify an E-class source citation.

    Levels 1-3 run during routine verification.
    Level 4 runs ONLY when probe_mode=True (triggered by adversarial probing).

    Args:
        source: Source citation from VTD proof_body.sources
        probe_mode: If True, include Level 4 contextual relevance check.
                    Set to True only during adversarial probing, not routine
                    verification, to avoid verification regress.
    """
    result = SourceVerificationResult()

    # Level 1: URL accessibility (with archive.org fallback)
    response = fetch(source.url, timeout=10_000)
    if not response.accessible:
        response = fetch("https://web.archive.org/web/" + source.url)
    result.accessible = response.accessible
    if not result.accessible:
        result.verdict = "INACCESSIBLE"
        return result

    # Level 2: Content hash comparison
    current_hash = SHA256(response.body)
    result.content_unchanged = (current_hash == source.content_hash)
    if not result.content_unchanged:
        result.content_drift = True  # Flag but do not fail; content may
                                      # have been updated legitimately

    # Level 3: Quote accuracy (fuzzy match, threshold 0.9)
    result.quote_found = fuzzy_match(source.quoted_text, response.body,
                                      threshold=0.9)
    if not result.quote_found:
        result.verdict = "QUOTE_NOT_FOUND"
        return result

    # Level 4: Contextual relevance -- OPTIONAL, probe-triggered only
    if probe_mode:
        result.relevance = assess_relevance(
            source.relevance_justification, response.body)
        if result.relevance.score < 0.5:
            result.verdict = "IRRELEVANT_SOURCE"
            return result

    result.verdict = "VERIFIED"
    return result
```

### Integration with Adversarial Probing

When an adversarial prober selects the SC (Source Challenge) probe type for an E-class claim, the prober invokes `verify_source(source, probe_mode=True)` for each source, which activates Level 4. This ensures contextual relevance is evaluated, but only by a dedicated prober with a separate cognitive budget, breaking the verification regress.

---

## PA-F23: Probe Budget Token Definition

**Severity:** MEDIUM (blocks implementation)
**Applies to:** Section 7.5, Probing Budget Allocation (line 748-759)

### Problem

The spec references "tokens" as the unit for probe budgets but never defines what a token is or how it maps to system costs.

### Definition

**1 probe token = 1 AIC (Atrahasis Intelligence Coin).**

A probe token represents the cost of one atomic verification operation performed by a prober. The Settlement Plane denominates all PCVM costs in AIC; probe budgets are denominated in the same unit to enable direct cost accounting.

### Mapping: Probe Operations to AIC Cost

| Operation | AIC Cost | Description |
|-----------|----------|-------------|
| Source fetch + hash check | 2 AIC | HTTP GET + SHA-256 comparison |
| Quote fuzzy match | 3 AIC | Substring matching with threshold |
| Contextual relevance assessment (Level 4) | 15 AIC | Semantic analysis of source-claim relationship |
| Counterexample generation (CX) | 25 AIC | Generate and evaluate a specific counterexample |
| Assumption exposure (AE) | 20 AIC | Identify and articulate unstated assumption |
| Logical fallacy check (LF) | 15 AIC | Check one inference step for named fallacies |
| Boundary probe (BP) | 20 AIC | Construct and evaluate one edge case |
| Meta-probe (inoculation check) | 10 AIC | Assess whether VTD responses appear pre-fabricated |

### Budget Calculation Formula

```python
def compute_probe_budget(claim_class: str, risk_level: str,
                         agent_credibility: float) -> int:
    """
    Compute total probe budget in AIC.

    Returns:
        Budget in AIC (1 AIC = 1 probe token). This is the maximum
        the prober may spend on verification operations for this claim.
        Unspent budget is not charged to the Settlement Plane.
    """
    BASE_BUDGETS_AIC = {
        "E": 500, "S": 400, "P": 200, "R": 400,
        "H": 800, "N": 700, "K": 600  # K-class added per C9
    }
    RISK_MULTIPLIERS = {
        "LOW": 0.5, "MEDIUM": 1.0, "HIGH": 2.0, "CRITICAL": 3.0
    }
    base = BASE_BUDGETS_AIC[claim_class]
    risk_factor = RISK_MULTIPLIERS[risk_level]
    # Low-credibility agents get more probing (range 1.0 to 2.0)
    credibility_factor = 2.0 - min(max(agent_credibility, 0.0), 1.0)
    raw_budget = base * risk_factor * credibility_factor
    return min(int(raw_budget), 5000)  # 5000 AIC hard cap
```

### Settlement Integration

- Probe budget is **reserved** from the Settlement Plane when probing is initiated.
- Only **actually spent** AIC is charged. If a prober spends 300 AIC of a 500 AIC budget, the remaining 200 AIC is released.
- The producing agent bears 0% of probe cost (probing is a system verification cost).
- Probe costs are distributed across verification committee members' epoch settlement as a shared system expense.
- Probers who find confirmed errors (FALSIFIED or WEAKENED verdict) receive a quality bonus of 10% of the spent budget from the Settlement Plane's verification reward pool.

---

## PA-F24: Cost Model Separation (Producer vs. Verifier)

**Severity:** MEDIUM
**Applies to:** Section 12.1, Cost Model per Claim Class (line 1154)

### Problem

Section 12.1 reports "VTD Construction" and "VTD Checking" costs but does not specify who bears each cost. The VTD construction cost is borne by the producing agent (it is part of producing the claim). The VTD checking cost is borne by the verification committee (it is part of verification). These are economically distinct: the producer invests upfront to make verification cheaper; the verifier pays to check the proof.

### Corrected Cost Table

| Class | Producer Cost (VTD construction) | Verifier Cost (VTD checking, per committee member) | Total Verifier Cost (full committee) | Total System Cost vs. Replication |
|-------|----------------------------------|-----------------------------------------------------|--------------------------------------|-----------------------------------|
| D | 0.05x | 0.017x | 0.05x (3 members) | 0.10x |
| C | 0.15x | 0.067x | 0.20x (3 members) | 0.35x |
| E | 0.30x | 0.10x | 0.50x (5 members) | 0.80x |
| S | 0.20x | 0.06x | 0.30x (5 members) | 0.50x |
| P | 0.15x | 0.04x | 0.20x (5 members) | 0.35x |
| R | 0.20x | 0.08x | 0.40x (5 members) | 0.60x |
| H | 0.50x | 0.214x | 1.50x (7 members) | 2.00x |
| N | 0.40x | 0.157x | 1.10x (7 members) | 1.50x |
| K | 0.25x | 0.10x | 0.50x (5 members) | 0.75x |

Notes:
- "x" = cost of one full replication by one agent.
- Producer Cost is the marginal cost of constructing the VTD beyond producing the claim itself.
- Verifier Cost per member = Total Verifier Cost / committee size.
- Total System Cost = Producer Cost + Total Verifier Cost (but NOT Producer Cost * committee size, since the producer constructs the VTD once).

### Corrected Cost Formulas

```python
def producer_cost(claim_class: str) -> float:
    """Cost to the producing agent for VTD construction, in units of
    one-agent replication cost. This cost is borne ONCE by the producer."""
    PRODUCER_COSTS = {
        "D": 0.05, "C": 0.15, "E": 0.30, "S": 0.20,
        "P": 0.15, "R": 0.20, "H": 0.50, "N": 0.40, "K": 0.25
    }
    return PRODUCER_COSTS[claim_class]

def verifier_cost_per_member(claim_class: str) -> float:
    """Cost to ONE verification committee member for VTD checking,
    in units of one-agent replication cost."""
    VERIFIER_COSTS_TOTAL = {
        "D": 0.05, "C": 0.20, "E": 0.50, "S": 0.30,
        "P": 0.20, "R": 0.40, "H": 1.50, "N": 1.10, "K": 0.50
    }
    COMMITTEE_SIZES = {
        "D": 3, "C": 3, "E": 5, "S": 5,
        "P": 5, "R": 5, "H": 7, "N": 7, "K": 5
    }
    return VERIFIER_COSTS_TOTAL[claim_class] / COMMITTEE_SIZES[claim_class]

def total_system_cost(claim_class: str) -> float:
    """Total system cost for verifying one claim, in units of
    one-agent replication cost.
    = producer_cost (once) + verifier_cost_per_member * committee_size."""
    pc = producer_cost(claim_class)
    VERIFIER_COSTS_TOTAL = {
        "D": 0.05, "C": 0.20, "E": 0.50, "S": 0.30,
        "P": 0.20, "R": 0.40, "H": 1.50, "N": 1.10, "K": 0.50
    }
    return pc + VERIFIER_COSTS_TOTAL[claim_class]
```

### Settlement Plane Cost Attribution

| Cost Component | Borne By | Settlement Mechanism |
|---------------|----------|---------------------|
| VTD Construction | Producing agent | Deducted from producer's epoch budget; offset by quality score rewards |
| VTD Checking | Each committee member | Compensated from verification reward pool (per-claim payment) |
| Adversarial Probing | System (shared) | Distributed across committee members' epoch settlement |
| Deep-Audit | System (shared) | Funded from deep-audit reserve (2% of total epoch AIC) |

---

## PA-F29: K-class (Knowledge Consolidation) Verification Pathway

**Severity:** MEDIUM
**Applies to:** New subsection after Section 6.2. Also requires updates to Section 5.2 (class definitions), Section 8.2 (opinion initialization), Section 9.1 (admission thresholds), Appendix C (parameters), and the VTD envelope schema (Section 4.5).

### Background

C9 reconciliation introduced K-class (Knowledge Consolidation) for claims that synthesize knowledge from multiple source quanta across multiple agents. K-class occupies the conservatism ordering between N and E (see PA-F21). K-class is Tier 2 (STRUCTURED_EVIDENCE) because verification can be partially mechanized through provenance checking and reasoning chain validation, but requires judgment for coherence assessment.

### 5.2 Addition: K-class Definition

**K-class (Knowledge Consolidation).** A claim that synthesizes information from multiple source quanta contributed by multiple agents into a consolidated knowledge artifact. The synthesis must demonstrate provenance diversity (no single agent or parcel dominates), a traceable reasoning chain from sources to conclusion, and a falsification statement articulating what evidence would refute the consolidation. Verification checks provenance diversity, reasoning chain validity, falsification statement quality, and cross-domain coherence. Examples: literature synthesis across agent contributions, architectural pattern consolidation, cross-domain risk assessment. Tier: STRUCTURED_EVIDENCE.

### Committee Selection

- **Tier:** 2 (STRUCTURED_EVIDENCE)
- **Committee size:** 5 members
- **Diversity requirement:** At least 2 members from different domain pools than the producing agent. At least 1 member must have verified claims in a domain covered by the source quanta.
- **Prober allocation:** 1 prober (standard Tier 2), with probe types CX, AE, SC.

### K-class VTD Proof Body Schema

```json
{
  "$id": "https://pcvm.atrahasis.dev/schema/v1/vtd-k-class.schema.json",
  "title": "K-class Proof Body",
  "description": "Knowledge Consolidation evidence. Tier 2: STRUCTURED_EVIDENCE.",
  "type": "object",
  "required": [
    "source_quanta", "synthesis_chain", "falsification_statement",
    "voting_record", "provenance_summary"
  ],
  "properties": {
    "source_quanta": {
      "type": "array",
      "minItems": 5,
      "items": {
        "type": "object",
        "required": ["claim_id", "contributing_agent", "parcel_id",
                      "contribution_summary"],
        "properties": {
          "claim_id": { "type": "string" },
          "contributing_agent": { "type": "string" },
          "parcel_id": { "type": "string" },
          "domain": { "type": "string" },
          "contribution_summary": { "type": "string", "maxLength": 500 },
          "credibility_at_synthesis": {
            "type": "number", "minimum": 0, "maximum": 1
          }
        }
      }
    },
    "provenance_summary": {
      "type": "object",
      "required": ["total_agents", "total_parcels", "max_agent_share"],
      "properties": {
        "total_agents": { "type": "integer", "minimum": 5 },
        "total_parcels": { "type": "integer", "minimum": 3 },
        "max_agent_share": {
          "type": "number", "minimum": 0, "maximum": 0.30,
          "description": "No single agent may contribute >30% of source quanta"
        },
        "domain_coverage": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "synthesis_chain": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["step_id", "input_quanta", "reasoning", "output"],
        "properties": {
          "step_id": { "type": "string" },
          "input_quanta": {
            "type": "array",
            "items": { "type": "string" },
            "minItems": 1,
            "description": "claim_ids of source quanta consumed by this step"
          },
          "reasoning": {
            "type": "string",
            "description": "How the input quanta were combined or reconciled"
          },
          "reconciliation_notes": {
            "type": "string",
            "description": "How conflicts between sources were resolved"
          },
          "output": {
            "type": "string",
            "description": "The intermediate or final consolidated statement"
          }
        }
      }
    },
    "falsification_statement": {
      "type": "object",
      "required": ["statement", "conditions"],
      "properties": {
        "statement": {
          "type": "string",
          "description": "What evidence would refute this consolidation?"
        },
        "conditions": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["condition", "impact"],
            "properties": {
              "condition": { "type": "string" },
              "impact": {
                "type": "string",
                "enum": ["INVALIDATES", "WEAKENS", "NARROWS_SCOPE"]
              }
            }
          }
        },
        "testable": { "type": "boolean", "default": true }
      }
    },
    "voting_record": {
      "type": "object",
      "required": ["passes"],
      "properties": {
        "passes": {
          "type": "array",
          "minItems": 3,
          "maxItems": 3,
          "items": {
            "type": "object",
            "required": ["pass_number", "voters", "outcome"],
            "properties": {
              "pass_number": { "type": "integer", "minimum": 1, "maximum": 3 },
              "voters": {
                "type": "array",
                "items": {
                  "type": "object",
                  "required": ["agent_id", "vote"],
                  "properties": {
                    "agent_id": { "type": "string" },
                    "vote": {
                      "type": "string",
                      "enum": ["APPROVE", "REJECT", "ABSTAIN",
                               "REQUEST_REVISION"]
                    },
                    "rationale": { "type": "string" }
                  }
                }
              },
              "outcome": {
                "type": "string",
                "enum": ["PASSED", "FAILED", "REVISED"]
              }
            }
          }
        }
      }
    }
  },
  "additionalProperties": false
}
```

### K-class Verification Protocol

```python
def verify_k_class(vtd: VTD, committee: Set[AgentId],
                    epoch: EpochNum) -> VerificationResult:
    body = vtd.proof_body
    checks = []

    # --- Step 1: Provenance Diversity Check ---
    # Verify that source quanta are genuinely diverse.
    unique_agents = set(sq.contributing_agent for sq in body.source_quanta)
    unique_parcels = set(sq.parcel_id for sq in body.source_quanta)

    if len(unique_agents) < 5:
        return VerificationResult(
            status="REJECTED",
            reason="Insufficient agent diversity: need >=5, got " +
                   str(len(unique_agents)),
            opinion=Opinion(b=0, d=0.8, u=0.2, a=0.6))

    if len(unique_parcels) < 3:
        return VerificationResult(
            status="REJECTED",
            reason="Insufficient parcel diversity: need >=3, got " +
                   str(len(unique_parcels)),
            opinion=Opinion(b=0, d=0.8, u=0.2, a=0.6))

    # Check max agent share
    agent_counts = Counter(sq.contributing_agent for sq in body.source_quanta)
    total_quanta = len(body.source_quanta)
    max_share = max(agent_counts.values()) / total_quanta
    if max_share > 0.30:
        return VerificationResult(
            status="REJECTED",
            reason=f"Agent concentration too high: {max_share:.0%} > 30%",
            opinion=Opinion(b=0, d=0.7, u=0.3, a=0.6))

    # Verify declared provenance matches actual
    if body.provenance_summary.total_agents != len(unique_agents):
        checks.append(("provenance_mismatch", -0.15))
    if body.provenance_summary.total_parcels != len(unique_parcels):
        checks.append(("provenance_mismatch", -0.15))
    if body.provenance_summary.max_agent_share < max_share - 0.01:
        checks.append(("provenance_understated", -0.20))

    # Verify each source quantum exists and has adequate credibility
    for sq in body.source_quanta:
        source_opinion = lookup_claim_credibility(sq.claim_id)
        if source_opinion is None:
            checks.append(("missing_source_" + sq.claim_id, -0.10))
        elif expected_probability(source_opinion) < 0.50:
            checks.append(("low_cred_source_" + sq.claim_id, -0.05))

    provenance_score = max(0.0, 1.0 + sum(p for _, p in checks))

    # --- Step 2: Reasoning Chain Validity ---
    # Each synthesis step must reference valid input quanta and produce
    # a coherent output.
    valid_quanta_ids = set(sq.claim_id for sq in body.source_quanta)
    chain_score = 1.0

    for step in body.synthesis_chain:
        # Check that input quanta are valid references
        for qid in step.input_quanta:
            if qid not in valid_quanta_ids:
                chain_score -= 0.15  # References non-existent source

        # Check reasoning is non-empty and substantive
        if len(step.reasoning.strip()) < 50:
            chain_score -= 0.10  # Too terse to evaluate

        # Check that output is non-trivially derived (not just copying input)
        if len(step.input_quanta) > 1 and not step.reconciliation_notes:
            chain_score -= 0.05  # Multi-source step without reconciliation

        # Each step's output becomes a valid reference for subsequent steps
        valid_quanta_ids.add(step.step_id)

    chain_score = max(0.0, chain_score)

    # --- Step 3: Falsification Statement Quality ---
    falsification_score = 1.0

    if not body.falsification_statement.statement or \
       len(body.falsification_statement.statement.strip()) < 30:
        falsification_score -= 0.40  # Trivial or empty falsification

    if len(body.falsification_statement.conditions) < 1:
        falsification_score -= 0.30  # No specific conditions

    # Check that at least one condition would INVALIDATE (not just weaken)
    has_invalidating = any(
        c.impact == "INVALIDATES"
        for c in body.falsification_statement.conditions
    )
    if not has_invalidating:
        falsification_score -= 0.20  # No condition that could fully refute

    # Check testability
    if not body.falsification_statement.testable:
        falsification_score -= 0.15  # Unfalsifiable statement

    falsification_score = max(0.0, falsification_score)

    # --- Step 4: Cross-Domain Coherence Assessment ---
    # This is the committee judgment step. Each committee member
    # independently assesses whether the synthesis is coherent.
    coherence_opinions = []
    for member in committee:
        member_opinion = member.assess_k_class_coherence(
            source_quanta=body.source_quanta,
            synthesis_chain=body.synthesis_chain,
            falsification=body.falsification_statement,
            voting_record=body.voting_record
        )
        coherence_opinions.append(member_opinion)

    coherence_fused = cumulative_fusion_all(coherence_opinions)

    # --- Step 5: Voting Record Validation ---
    voting_penalty = 0.0
    if len(body.voting_record.passes) < 3:
        voting_penalty = 0.20  # Must have 3-pass record

    for pass_record in body.voting_record.passes:
        if len(pass_record.voters) < 3:
            voting_penalty += 0.05  # Insufficient voter participation

    # --- Step 6: Compose Final Opinion ---
    # Weighted combination of mechanical checks and committee judgment
    mechanical_score = (
        0.30 * provenance_score +
        0.30 * chain_score +
        0.20 * falsification_score +
        0.20 * (1.0 - voting_penalty)
    )

    # Build mechanical opinion
    mechanical_opinion = Opinion(
        b=mechanical_score * 0.8,
        d=(1.0 - mechanical_score) * 0.6,
        u=1.0 - mechanical_score * 0.8 - (1.0 - mechanical_score) * 0.6,
        a=0.6  # K-class base rate
    )
    mechanical_opinion = normalize(mechanical_opinion)

    # Conjoin mechanical checks with committee coherence assessment
    combined = conjunction(mechanical_opinion, coherence_fused)

    return VerificationResult(
        status="VERIFIED" if expected_probability(combined) >= 0.70
               else "REJECTED",
        opinion=combined
    )
```

### MCT Output for K-class

- **SL opinion initialization:** Initial uncertainty >= 0.4 (reflecting the inherent uncertainty of knowledge synthesis).
- **Base rate (a):** 0.6 (higher than D/E/S default of 0.5, lower than H-class 0.7, reflecting that consolidation has moderate prior probability of being sound).
- **Admission threshold:** 0.70 (between E-class 0.60 and P-class 0.80, reflecting that consolidation requires higher confidence than raw empirical claims but lower than process conformance).

### Updates to Other Sections

**Section 4.5 VTD envelope schema** -- add "K" to the `suggested_class` and `assigned_class` enums:
```json
"enum": ["D", "E", "S", "H", "N", "P", "R", "C", "K"]
```

**Section 4.5 VTD Size Limits** -- add K-class:

| Class | Max Size | Rationale |
|-------|----------|-----------|
| K | 75 KB | Source quanta refs + synthesis chain can be substantial |

**Section 7.1 Probe types** -- add K-class:

| Class | Probe Types |
|-------|-------------|
| K | CX, AE, SC |

**Section 7.5 Probe budget** -- add K-class:

| Class | Base Budget (tokens/AIC) |
|-------|--------------------------|
| K | 600 |

**Section 8.2 Opinion initialization** -- add K-class:

| Class | Verified Opinion | Initial Opinion | Decay Model |
|-------|-----------------|-----------------|-------------|
| K | Full tuple | (0, 0, 1, 0.6) | Half-life (270 days) + on source credibility change |

**Section 8.6 Decay** -- add K-class:
- **K-class:** Half-life decay (270 days). Also triggered when any source quantum's credibility drops below 0.50 or when more than 20% of source quanta have been superseded.

**Section 9.1 Admission thresholds** -- add K-class:

| Class | Threshold | Rationale |
|-------|-----------|-----------|
| K | 0.70 | Consolidation requires higher confidence than raw empirical claims |

**Section 10.1 Committee sizes** -- update:
- K-class uses Tier 2 committee size: 5 members.

---

## PA-F30: Parameter Defaults

**Severity:** LOW
**Applies to:** Appendix C and various sections throughout

The following 10 critical parameters are referenced in the spec but lack explicit defaults. Defaults are provided with rationale.

| # | Parameter | Default | Section | Rationale |
|---|-----------|---------|---------|-----------|
| 1 | `E_CLASS_HALF_LIFE_DAYS` | 180 | 8.6 | Midpoint of stated range (90-365). Empirical data becomes stale within 6 months for most AI/tech domains. Tunable per-domain. |
| 2 | `H_CLASS_HALF_LIFE_DAYS` | 180 | 8.6 | Already stated in Section 8.6 but not in Appendix C. Heuristic recommendations age as technology evolves. |
| 3 | `FUZZY_MATCH_THRESHOLD` | 0.90 | 6.2 | Mentioned in source verification pseudocode. Allows 10% character-level edit distance for minor formatting differences in quoted text. |
| 4 | `SOURCE_FETCH_TIMEOUT_MS` | 10000 | 6.2 | 10-second HTTP timeout. Balances thoroughness against verification latency. |
| 5 | `CLASSIFICATION_AGREEMENT_MAJORITY` | 2 | 5.3 | Two of three classification signals must agree for majority seal. Implicit but never stated as a parameter. |
| 6 | `DOWNGRADE_RATE_PENALTY_THRESHOLD` | 0.30 | 5.5 | Section 5.5 states ">30%" but does not declare it as a configurable parameter. |
| 7 | `DOWNGRADE_RATE_PENALTY_AMOUNT` | 0.10 | 5.5 | Credibility penalty for agents who consistently propose lower-tier classes. 0.10 is meaningful but not career-ending. |
| 8 | `CITATION_AUDIT_WEIGHT_LOG_BASE` | 2 | 6.4 | The `log2` in citation-weighted audit bias. Base-2 means a claim with 3 citations has ~2x the audit rate. |
| 9 | `BOOTSTRAP_SEED_CLAIMS` | 200 | 11.2 | Midpoint of stated range (100-500). Enough to establish initial credibility graph without excessive manual curation. |
| 10 | `BOOTSTRAP_DEEP_AUDIT_MULTIPLIER` | 2.0 | 11.2 | First 100 epochs use 2x deep-audit rate (14% instead of 7%). Stated in Attack 10 defense but not parameterized. |

### Appendix C Addition

These parameters should be added to the Configurable Parameters Table:

| Parameter | Default | Range | Governance |
|-----------|---------|-------|------------|
| E_CLASS_HALF_LIFE_DAYS | 180 | [90, 365] | Operational |
| H_CLASS_HALF_LIFE_DAYS | 180 | [90, 365] | Operational |
| K_CLASS_HALF_LIFE_DAYS | 270 | [120, 540] | Operational |
| FUZZY_MATCH_THRESHOLD | 0.90 | [0.80, 0.98] | Operational |
| SOURCE_FETCH_TIMEOUT_MS | 10000 | [5000, 30000] | Operational |
| CLASSIFICATION_MAJORITY_COUNT | 2 | [2, 3] | G-class |
| DOWNGRADE_RATE_PENALTY_THRESHOLD | 0.30 | [0.15, 0.50] | Operational |
| DOWNGRADE_RATE_PENALTY_AMOUNT | 0.10 | [0.05, 0.25] | Operational |
| CITATION_AUDIT_LOG_BASE | 2 | [2, 10] | Operational |
| BOOTSTRAP_SEED_CLAIMS | 200 | [100, 500] | G-class |
| BOOTSTRAP_AUDIT_MULTIPLIER | 2.0 | [1.5, 4.0] | Operational |
| K_CLASS_ADMISSION_THRESHOLD | 0.70 | [0.60, 0.85] | G-class |
| K_CLASS_SOURCE_CRED_FLOOR | 0.50 | [0.30, 0.70] | Operational |
| K_CLASS_MAX_AGENT_SHARE | 0.30 | [0.15, 0.50] | G-class |

---

## PA-F31: MCT cls_id Format Definition

**Severity:** LOW
**Applies to:** Section 9.1, MCT schema, specifically the `cls_id` field (line 938)

### Problem

The MCT schema declares a `cls_id` field of type string but provides no format definition. The existing `mct_id` has a defined pattern (`^mct:[a-f0-9]{16}$`) but `cls_id` does not.

### Definition

The `cls_id` is a unique identifier for the classification decision that produced the assigned class. It encodes the claim class, the epoch in which classification occurred, a hash of the classification committee's inputs, and a nonce for uniqueness.

**Format:** `mct:<claim_class>:<epoch>:<committee_hash>:<nonce>`

| Component | Type | Description |
|-----------|------|-------------|
| `mct` | literal | Fixed prefix identifying this as an MCT classification ID |
| `claim_class` | string, one of D/E/S/H/N/P/R/C/K | The assigned claim class |
| `epoch` | integer | The epoch in which classification was performed |
| `committee_hash` | hex, 8 chars | First 8 hex characters of SHA-256(sorted committee member IDs) |
| `nonce` | integer | Monotonically increasing counter within the epoch, starting at 1 |

**JSON Schema patch for `cls_id`:**

```json
"cls_id": {
  "type": "string",
  "pattern": "^mct:[DESHNPRCK]:[0-9]+:[a-f0-9]{8}:[0-9]+$",
  "description": "Classification ID: mct:<class>:<epoch>:<committee_hash>:<nonce>"
}
```

**Examples:**

- `mct:D:1042:a3f8c012:1` -- D-class claim, epoch 1042, first classification of the epoch
- `mct:K:2001:7b29e4d1:47` -- K-class claim, epoch 2001, 47th classification of the epoch
- `mct:H:500:ee01ff34:3` -- H-class claim, epoch 500, third classification

**Construction pseudocode:**

```python
def generate_cls_id(assigned_class: str, epoch: int,
                     committee: Set[AgentId],
                     epoch_counter: AtomicCounter) -> str:
    sorted_ids = sorted(committee)
    committee_hash = SHA256("|".join(sorted_ids).encode())[:8]  # first 8 hex
    nonce = epoch_counter.increment()
    return f"mct:{assigned_class}:{epoch}:{committee_hash}:{nonce}"
```

---

## PA-F32: Deep-Audit Stratified Sampling Caveat

**Severity:** LOW
**Applies to:** Section 6.4, Deep-Audit Protocol (line 649-674)

### Problem

The deep-audit statistical guarantees (">99% probability of detection within 65 epochs") assume that forged claims are independent events with uniform distribution. If forged claims are correlated -- produced by the same agent, within the same domain, or targeting the same knowledge subgraph -- simple random sampling at 5-10% may systematically under-sample some clusters and over-sample others.

### Caveat and Mitigation

Insert after the "Statistical guarantees" paragraph (after line 673):

> **Correlated claim caveat.** The detection probability formula P(detected within T epochs) = 1 - (1 - r)^T assumes independent claim quality. This assumption breaks when claims are correlated -- for example, when a single agent produces many claims in the same epoch, or when multiple agents submit claims about the same knowledge domain using shared source material.
>
> For correlated claims, PCVM SHOULD use stratified sampling rather than simple random sampling. The stratification dimensions are:
>
> 1. **Agent stratum:** Claims from the same producing agent are grouped. At least one claim per agent-epoch pair with >= 3 claims SHOULD be audited.
> 2. **Domain stratum:** Claims within the same knowledge locus (first two path segments) are grouped. At least one claim per locus-epoch pair with >= 5 claims SHOULD be audited.
> 3. **Dependency stratum:** Claims sharing >= 2 common dependencies are grouped. At least one claim per dependency cluster SHOULD be audited.
>
> Stratified sampling ensures that a coordinated attack targeting a single domain or executed by a single agent cannot evade audit through statistical luck.

### Stratified Selection Pseudocode

```python
def select_for_deep_audit_stratified(passed_claims, epoch,
                                      audit_rate=0.07):
    """
    Stratified deep-audit selection. Guarantees minimum coverage per
    stratum while maintaining the overall audit rate.
    """
    audit_seed = SHA256(b"DEEP_AUDIT" + uint64_be(epoch) + vrf_seed(epoch))

    # Phase 1: Stratify claims
    agent_strata = group_by(passed_claims, key=lambda c: c.producing_agent)
    domain_strata = group_by(passed_claims, key=lambda c: c.locus[:2])

    # Phase 2: Mandatory stratum coverage
    mandatory = set()
    for agent, claims in agent_strata.items():
        if len(claims) >= 3:
            # Deterministically select one per agent stratum
            stratum_hash = SHA256(audit_seed + agent.encode())
            idx = uint256_from_bytes(stratum_hash) % len(claims)
            mandatory.add(claims[idx].claim_id)

    for domain, claims in domain_strata.items():
        if len(claims) >= 5:
            stratum_hash = SHA256(audit_seed + domain.encode())
            idx = uint256_from_bytes(stratum_hash) % len(claims)
            mandatory.add(claims[idx].claim_id)

    # Phase 3: Fill remaining audit budget with random selection
    target_count = max(len(mandatory),
                       int(audit_rate * len(passed_claims)))
    remaining_budget = target_count - len(mandatory)

    remaining_claims = [c for c in passed_claims
                        if c.claim_id not in mandatory]
    random_selected = set()
    for claim in remaining_claims:
        if len(random_selected) >= remaining_budget:
            break
        selection_hash = SHA256(audit_seed + claim.claim_id.encode())
        effective_rate = audit_rate * (1 + log2(1 + claim.citation_count))
        if uint256_from_bytes(selection_hash) < int(effective_rate * 2**256):
            random_selected.add(claim.claim_id)

    return mandatory | random_selected
```

---

## Summary of Changes

| Finding | Severity | Section(s) Modified | Nature of Fix |
|---------|----------|--------------------|----|
| F19 | HIGH | Abstract, Section 14 | Corrected cost claim: leads with 17%, qualifies 40-60% as projected |
| F20 | HIGH | Section 5.3 | Defined CLASSIFICATION_SIGNATURES for all 8 classes with markers and exclusions |
| F21 | HIGH | Section 5.3 | Clarified conservatism ordering rationale; updated to H>N>K>E>S>R>P>C>D per C9 |
| F22 | MEDIUM | Section 6.2 | Made Level 4 source verification optional, triggered only by adversarial probing |
| F23 | MEDIUM | Section 7.5 | Defined 1 token = 1 AIC; mapped probe operations to AIC costs |
| F24 | MEDIUM | Section 12.1 | Separated producer cost (VTD construction) from verifier cost (VTD checking) |
| F29 | MEDIUM | Sections 5.2, 6.2, 7, 8, 9, Appendix C | Complete K-class verification pathway with schema, protocol, and parameters |
| F30 | LOW | Appendix C | Defined 10 critical parameter defaults with rationale |
| F31 | LOW | Section 9.1 | Defined cls_id format: mct:<class>:<epoch>:<committee_hash>:<nonce> |
| F32 | LOW | Section 6.4 | Added stratified sampling caveat and pseudocode for correlated claims |

---

*Patch Addendum v1.1 completed 2026-03-10. Specification Writer, Atrahasis Agent System v2.0.*
*Applies to: C5 PCVM Master Tech Spec v1.0.0.*
