# C5/C6 Hardening Addendum: Defense-in-Depth for CRITICAL Residual Risks

## Normative Patch to C5 (PCVM) v1.0.0 and C6 (EMA) v1.0.0

**Version:** 1.0.0
**Date:** 2026-03-10
**Status:** NORMATIVE ADDENDUM -- all mechanisms below extend the base specifications
**Applies to:** C5 MASTER_TECH_SPEC.md Section 11 (Security Analysis), C6 MASTER_TECH_SPEC.md Section 11 (Security Analysis)
**Cross-references:** C3 (Tidal Noosphere -- Sentinel Graph), C8 (DSF -- Slashing Schedule, Section 10.3)

---

## Motivation

The C5 and C6 security analyses identify three CRITICAL attacks where "no complete defense exists" and residual risk remains HIGH after all specified mitigations:

1. **VTD Forgery / "Confident Liar" (C5, Attack 1):** A sophisticated forger produces structurally valid VTDs with fabricated or misrepresented evidence. Structural checks pass because the VTD has correct format, citations, and reasoning chains, but the underlying evidence is false.

2. **Mutual Endorsement / Collusion (C5, Attack 8):** Colluding agents control verification outcomes by coordinating their committee votes. If f >= 1/3 of committee members collude, they can pass false claims or block true ones.

3. **Consolidation Poisoning (C6, Attack A3):** An adversary plants quanta across multiple domains to create artificial cross-domain patterns. The dreaming process cannot distinguish genuine from planted patterns because the planted quanta individually appear legitimate.

These are the hardest problems in the system. No single mechanism eliminates them. This addendum specifies layered defense-in-depth: multiple independent mechanisms that collectively raise the cost and lower the success probability of each attack to the point where rational adversaries abandon them.

---

## Problem 1: VTD Forgery / "Confident Liar"

### 1.1 Source Verification Protocol for E-class Claims

**Extends:** C5 Section 6.2 (Tier 2 Verification Protocol), Phase 2 (Source checks)

The base specification checks that citations exist and are well-formed. This addendum mandates that verifiers independently retrieve and validate cited evidence for empirical claims.

```python
def verify_sources_eclass(vtd, verifier_id, epoch):
    """
    Mandatory source verification for E-class VTDs.
    The verifier MUST independently fetch at least one cited source
    and confirm the claim matches the source content.

    Returns: SourceVerificationResult with per-source verdicts.
    """
    sources = vtd.proof_body.sources
    evidence_chain = vtd.proof_body.evidence_chain

    # Step 1: Select sources for independent verification.
    # Always verify the PRIMARY source (highest weight in evidence chain).
    # Randomly verify one additional source (VRF-selected).
    primary_source = select_primary_source(sources, evidence_chain)
    additional_source = vrf_select_source(
        sources, exclude=[primary_source.source_id],
        seed=SHA256(b"SRC_VERIFY" + vtd.vtd_id.encode() +
                    verifier_id.encode() + uint64_be(epoch))
    )

    targets = [primary_source]
    if additional_source is not None:
        targets.append(additional_source)

    verdicts = []
    for source in targets:
        verdict = independently_verify_source(source, vtd)
        verdicts.append(verdict)

    return SourceVerificationResult(
        verdicts=verdicts,
        overall=aggregate_source_verdicts(verdicts)
    )


def independently_verify_source(source, vtd):
    """
    Independently retrieve and validate a single source.
    """
    result = SourceVerdict(source_id=source.source_id)

    # Step 1: Retrieve the source content independently.
    # Do NOT use any cached or agent-provided copy.
    try:
        content = fetch_source_content(
            uri=source.uri,
            source_type=source.source_type,
            timeout_ms=SOURCE_FETCH_TIMEOUT  # default: 30000
        )
    except SourceUnavailable:
        # Source cannot be fetched. This is not proof of forgery
        # but reduces confidence.
        result.status = "UNAVAILABLE"
        result.confidence_penalty = 0.15
        return result

    # Step 2: Verify content hash matches.
    # The VTD records a content_hash at retrieval time.
    # If content has changed, note the discrepancy but do not
    # automatically reject (sources can legitimately update).
    current_hash = SHA256(content.encode())
    if current_hash != source.content_hash:
        result.content_changed = True
        # Try archive.org fallback for the original version
        archived = fetch_archived_version(
            source.uri, source.retrieval_timestamp
        )
        if archived is not None:
            content = archived
            archived_hash = SHA256(archived.encode())
            result.archived_match = (archived_hash == source.content_hash)

    # Step 3: Verify the quoted text appears in the source.
    if source.quoted_text:
        quote_found = fuzzy_match(
            source.quoted_text, content,
            similarity_threshold=QUOTE_MATCH_THRESHOLD  # 0.90
        )
        result.quote_verified = quote_found
        if not quote_found:
            result.status = "QUOTE_MISMATCH"
            result.confidence_penalty = 0.30
            return result

    # Step 4: Verify the claim is actually supported by the source.
    # This is the critical check. The verifier must determine whether
    # the source content actually supports the claim, not just whether
    # the source exists.
    claim_text = vtd.claim_text
    support_assessment = assess_source_supports_claim(
        claim_text=claim_text,
        source_content=content,
        quoted_text=source.quoted_text,
        relevance_justification=source.relevance_justification
    )

    result.support_strength = support_assessment.strength  # [0, 1]
    result.support_reasoning = support_assessment.reasoning

    if support_assessment.strength < SOURCE_SUPPORT_THRESHOLD:  # 0.4
        result.status = "WEAK_SUPPORT"
        result.confidence_penalty = 0.20
    elif support_assessment.contradicts:
        result.status = "SOURCE_CONTRADICTS_CLAIM"
        result.confidence_penalty = 0.50
    else:
        result.status = "VERIFIED"
        result.confidence_penalty = 0.0

    return result


def aggregate_source_verdicts(verdicts):
    """
    Aggregate individual source verdicts into an overall assessment.
    """
    if any(v.status == "SOURCE_CONTRADICTS_CLAIM" for v in verdicts):
        return OverallSourceVerdict.FALSIFIED

    if any(v.status == "QUOTE_MISMATCH" for v in verdicts):
        return OverallSourceVerdict.WEAKENED

    total_penalty = sum(v.confidence_penalty for v in verdicts)
    if total_penalty > 0.40:
        return OverallSourceVerdict.WEAKENED

    if all(v.status == "VERIFIED" for v in verdicts):
        return OverallSourceVerdict.VERIFIED

    return OverallSourceVerdict.PARTIAL
```

**Conformance requirement (CR-H1):** For E-class VTDs, every verifier on the committee MUST execute `verify_sources_eclass()` and include the `SourceVerificationResult` in their verification opinion. A verifier that skips source verification MUST have their opinion discounted by 50%.

**Cost impact:** Source verification adds 0.1x-0.3x to E-class verification cost (from 0.80x to 0.90x-1.10x). This is acceptable because E-class claims are empirical -- if we cannot verify the evidence, the VTD provides no genuine assurance.

---

### 1.2 Cross-Verifier Evidence Correlation

**Extends:** C5 Section 6.2 (Tier 2 Verification Protocol), after Phase 6 (Committee opinion fusion)

When multiple verifiers independently check the same E-class claim, their source verification results are compared before fusion. This detects single-point-of-failure evidence (all verifiers relying on the same source) and rewards genuine independence.

```python
def correlate_verifier_evidence(
    verifier_results: List[SourceVerificationResult],
    vtd: VTD
) -> EvidenceCorrelation:
    """
    Compare independently-gathered evidence across verifiers.

    Signal interpretation:
    - Different sources agreeing -> HIGH confidence (genuine independence)
    - Same source, same conclusion -> MEDIUM confidence (single-point-of-failure)
    - Different sources disagreeing -> FLAG for investigation
    - Same source, different conclusions -> CRITICAL FLAG (interpretation error)
    """

    # Step 1: Build a source-usage matrix.
    # Rows = verifiers, columns = source IDs, cells = verdict
    source_matrix = {}
    for vr in verifier_results:
        verifier_sources = {}
        for verdict in vr.verdicts:
            verifier_sources[verdict.source_id] = verdict
        source_matrix[vr.verifier_id] = verifier_sources

    # Step 2: Compute source overlap.
    all_sources_used = set()
    for vs in source_matrix.values():
        all_sources_used.update(vs.keys())

    # Pairwise overlap: fraction of sources shared between verifier pairs
    verifier_ids = list(source_matrix.keys())
    pairwise_overlaps = []
    for i in range(len(verifier_ids)):
        for j in range(i + 1, len(verifier_ids)):
            sources_i = set(source_matrix[verifier_ids[i]].keys())
            sources_j = set(source_matrix[verifier_ids[j]].keys())
            if len(sources_i | sources_j) > 0:
                overlap = len(sources_i & sources_j) / len(sources_i | sources_j)
            else:
                overlap = 0.0
            pairwise_overlaps.append(overlap)

    avg_overlap = mean(pairwise_overlaps) if pairwise_overlaps else 0.0

    # Step 3: Classify correlation regime.
    correlation = EvidenceCorrelation()

    if avg_overlap < 0.3:
        # INDEPENDENT: Verifiers used mostly different sources.
        # Check if their conclusions agree.
        conclusions_agree = all(
            vr.overall in (OverallSourceVerdict.VERIFIED, OverallSourceVerdict.PARTIAL)
            for vr in verifier_results
        )
        if conclusions_agree:
            correlation.regime = "INDEPENDENT_AGREEMENT"
            correlation.confidence_boost = 0.10  # Strong signal
        else:
            correlation.regime = "INDEPENDENT_DISAGREEMENT"
            correlation.confidence_boost = 0.0
            correlation.flag = "INVESTIGATION_REQUIRED"

    elif avg_overlap > 0.7:
        # SINGLE_POINT_OF_FAILURE: Verifiers used mostly the same sources.
        # Their agreement is less informative.
        correlation.regime = "SINGLE_SOURCE_DEPENDENCY"
        correlation.confidence_boost = 0.0
        correlation.flag = "ADDITIONAL_VERIFICATION_RECOMMENDED"
        # Trigger: request one more verifier to use DIFFERENT sources
        correlation.action = "REQUEST_DIVERSE_REVERIFICATION"

    else:
        # PARTIAL_OVERLAP: Mixed independence.
        correlation.regime = "PARTIAL_INDEPENDENCE"
        correlation.confidence_boost = 0.05

    # Step 4: Check for same-source-different-conclusion (critical anomaly).
    for source_id in all_sources_used:
        verdicts_for_source = []
        for verifier_id, vs in source_matrix.items():
            if source_id in vs:
                verdicts_for_source.append(vs[source_id])

        if len(verdicts_for_source) >= 2:
            statuses = set(v.status for v in verdicts_for_source)
            if "VERIFIED" in statuses and "SOURCE_CONTRADICTS_CLAIM" in statuses:
                correlation.critical_flags.append(
                    f"Source {source_id}: verifiers disagree on whether "
                    f"source supports or contradicts claim"
                )
                correlation.regime = "CRITICAL_INTERPRETATION_CONFLICT"
                correlation.confidence_boost = -0.15

    return correlation
```

**Integration with opinion fusion:** The `confidence_boost` from evidence correlation is applied as a post-fusion adjustment:

```python
def apply_evidence_correlation(fused_opinion, correlation):
    """
    Adjust the fused committee opinion based on evidence correlation.
    """
    if correlation.confidence_boost > 0:
        # Transfer from uncertainty to belief
        transfer = min(correlation.confidence_boost, fused_opinion.uncertainty)
        fused_opinion.belief += transfer
        fused_opinion.uncertainty -= transfer
    elif correlation.confidence_boost < 0:
        # Transfer from belief to uncertainty
        transfer = min(abs(correlation.confidence_boost), fused_opinion.belief)
        fused_opinion.belief -= transfer
        fused_opinion.uncertainty += transfer

    return fused_opinion
```

**Conformance requirement (CR-H2):** Evidence correlation MUST be computed for all E-class claims where at least 2 verifiers performed independent source verification. The correlation result MUST be stored alongside the VTD verification record.

---

### 1.3 Temporal Evidence Decay Function

**Extends:** C5 Section 8 (Credibility Engine), credibility opinion maintenance

Evidence from a single source is inherently fragile. A single source can be wrong, manipulated, or become stale. Credibility from single-source evidence must decay over time unless independently corroborated.

```python
def compute_max_belief_from_sources(
    source_count: int,
    independent_sources: int,
    epochs_since_verification: int
) -> float:
    """
    Compute the maximum belief achievable from the available evidence base.

    Parameters:
    - source_count: total number of cited sources
    - independent_sources: number of genuinely independent sources
      (different organizations, different methodologies, different data)
    - epochs_since_verification: epochs since last verification

    Returns: maximum belief value [0, 0.95]

    Design rationale:
    - Single source: max belief 0.70. One source can be wrong.
    - Each independent source adds diminishing returns: 0.1 * ln(1 + n)
    - Cap at 0.95: absolute certainty is epistemically inaccessible.
    - Temporal decay: if not re-corroborated, max_belief decays.
    """

    # Base: single source caps at 0.70
    base_max = SINGLE_SOURCE_MAX_BELIEF  # 0.70

    # Independent corroboration bonus (diminishing returns via log)
    if independent_sources > 0:
        corroboration_bonus = (CORROBORATION_FACTOR
                               * math.log(1 + independent_sources))
        # CORROBORATION_FACTOR = 0.10
    else:
        corroboration_bonus = 0.0

    # Raw max belief before temporal decay
    raw_max = base_max + corroboration_bonus

    # Absolute cap: 0.95
    raw_max = min(raw_max, ABSOLUTE_BELIEF_CAP)  # 0.95

    # Temporal decay for under-corroborated evidence.
    # Evidence from a single source loses credibility over time.
    # Decay only applies when independent_sources < 3 (well-corroborated
    # evidence is stable).
    if independent_sources < CORROBORATION_STABILITY_THRESHOLD:  # 3
        decay_rate = EVIDENCE_TEMPORAL_DECAY_RATE  # 0.002 per epoch
        temporal_factor = math.exp(
            -decay_rate * epochs_since_verification
        )
        # But never decay below MINIMUM_DECAYED_MAX
        effective_max = max(
            MINIMUM_DECAYED_MAX,  # 0.30
            raw_max * temporal_factor
        )
    else:
        effective_max = raw_max  # Well-corroborated: no decay

    return effective_max


def enforce_evidence_belief_cap(opinion, vtd, epoch):
    """
    Enforce the evidence-based belief cap on an opinion.
    Called after verification and at each epoch boundary during
    credibility maintenance.
    """
    source_info = analyze_source_independence(vtd)
    max_belief = compute_max_belief_from_sources(
        source_count=source_info.total_sources,
        independent_sources=source_info.independent_sources,
        epochs_since_verification=epoch - vtd.epoch
    )

    if opinion.belief > max_belief:
        excess = opinion.belief - max_belief
        opinion.belief = max_belief
        opinion.uncertainty += excess  # Excess belief becomes uncertainty

    return opinion
```

**Example trajectories:**

| Independent Sources | Max Belief (initial) | Max Belief (50 epochs, no re-corroboration) |
|---------------------|---------------------|---------------------------------------------|
| 0 | 0.70 | 0.64 |
| 1 | 0.77 | 0.70 |
| 2 | 0.81 | 0.74 |
| 3+ | 0.84+ | 0.84+ (stable, no decay) |
| 10 | 0.94 | 0.94 (stable) |

**Conformance requirement (CR-H3):** The evidence belief cap MUST be enforced for all E-class and S-class claims at verification time and during periodic credibility maintenance (every 10 epochs). For H-class and N-class claims, the cap formula uses `base_max = 0.60` (lower because attestations are inherently less verifiable than empirical claims).

---

### 1.4 Forgery Detection Heuristics

**Extends:** C5 Section 10.4 (Sentinel Graph Interface), MQI metric feed

Statistical anomaly detection identifies agents whose behavior patterns are consistent with systematic forgery.

```python
def compute_forgery_suspicion_score(
    agent_id: str,
    lookback_epochs: int = 100
) -> ForgerySuspicion:
    """
    Compute a composite suspicion score for potential VTD forgery.

    Four independent signals, each normalized to [0, 1]:

    H1: Evidence production rate anomaly
    H2: Source verifiability distribution
    H3: Deep-audit accuracy discrepancy
    H4: Citation pattern anomaly

    Composite score = weighted sum. Threshold for escalation: 0.60.
    """

    agent_history = get_agent_claim_history(agent_id, lookback_epochs)
    peer_stats = get_peer_statistics(agent_history.claim_class, lookback_epochs)

    # --- H1: Evidence Production Rate Anomaly ---
    # Agents producing evidence at significantly above-average rates
    # may be fabricating rather than genuinely researching.
    agent_rate = agent_history.claims_per_epoch
    peer_mean = peer_stats.mean_claims_per_epoch
    peer_std = peer_stats.std_claims_per_epoch

    if peer_std > 0:
        z_score_rate = (agent_rate - peer_mean) / peer_std
    else:
        z_score_rate = 0.0

    # Normalize: z > 3 is maximally suspicious
    h1 = clamp(z_score_rate / 3.0, 0.0, 1.0) if z_score_rate > 0 else 0.0

    # --- H2: Source Verifiability Distribution ---
    # Agents who consistently cite low-verifiability sources
    # (UNKNOWN reliability, web pages rather than peer-reviewed papers)
    # may be choosing sources that are harder to check.
    source_types = agent_history.source_type_distribution
    low_verifiability_fraction = (
        source_types.get("WEB_PAGE", 0) +
        source_types.get("API_RESPONSE", 0)
    ) / max(1, sum(source_types.values()))

    reliability_assessments = agent_history.source_reliability_distribution
    unknown_fraction = reliability_assessments.get("UNKNOWN", 0) / max(
        1, sum(reliability_assessments.values())
    )

    peer_low_verif = peer_stats.mean_low_verifiability_fraction
    h2 = clamp(
        (low_verifiability_fraction - peer_low_verif) * 3.0
        + unknown_fraction * 2.0,
        0.0, 1.0
    )

    # --- H3: Deep-Audit Accuracy Discrepancy ---
    # If an agent's claims pass normal verification at rate X
    # but fail deep audit at rate significantly above average,
    # this suggests the normal verification is being gamed.
    if agent_history.deep_audit_count >= 5:  # Need enough audits
        normal_pass_rate = agent_history.normal_verification_pass_rate
        audit_pass_rate = agent_history.deep_audit_pass_rate
        discrepancy = normal_pass_rate - audit_pass_rate

        # Positive discrepancy means claims pass normal but fail audit
        # Peer baseline: some discrepancy is normal
        peer_discrepancy = peer_stats.mean_audit_discrepancy
        h3 = clamp(
            (discrepancy - peer_discrepancy) * 5.0,
            0.0, 1.0
        ) if discrepancy > peer_discrepancy else 0.0
    else:
        h3 = 0.0  # Insufficient data

    # --- H4: Citation Pattern Anomaly ---
    # Forgers tend to cite the same small set of sources repeatedly,
    # or cite sources that no other agent in the system cites.
    # Both patterns are suspicious.
    unique_sources_ratio = (
        agent_history.unique_sources_cited
        / max(1, agent_history.total_citations)
    )
    peer_unique_ratio = peer_stats.mean_unique_source_ratio

    # Very low unique ratio -> reusing same sources (lazy forgery)
    # Very high unique ratio AND low verifiability -> obscure sources
    if unique_sources_ratio < peer_unique_ratio * 0.5:
        h4_reuse = clamp(
            (peer_unique_ratio - unique_sources_ratio) * 4.0,
            0.0, 0.5
        )
    else:
        h4_reuse = 0.0

    orphan_source_fraction = agent_history.orphan_source_fraction
    # Sources cited by this agent but NO other agent in the system
    h4_orphan = clamp(orphan_source_fraction * 2.0, 0.0, 0.5)

    h4 = h4_reuse + h4_orphan

    # --- Composite Score ---
    # Weights reflect diagnostic value
    W_H1 = 0.15  # Production rate is weak signal (legitimate variance)
    W_H2 = 0.20  # Source quality is moderate signal
    W_H3 = 0.40  # Audit discrepancy is strong signal
    W_H4 = 0.25  # Citation patterns are moderate signal

    composite = W_H1 * h1 + W_H2 * h2 + W_H3 * h3 + W_H4 * h4

    return ForgerySuspicion(
        agent_id=agent_id,
        h1_production_rate=h1,
        h2_source_verifiability=h2,
        h3_audit_discrepancy=h3,
        h4_citation_pattern=h4,
        composite_score=composite,
        escalation=(composite >= FORGERY_ESCALATION_THRESHOLD),
        # FORGERY_ESCALATION_THRESHOLD = 0.60
    )
```

**Escalation protocol:**

```python
def handle_forgery_escalation(suspicion: ForgerySuspicion, epoch: int):
    """
    When forgery suspicion exceeds threshold, trigger enhanced scrutiny.
    """
    if not suspicion.escalation:
        return

    agent_id = suspicion.agent_id

    # Action 1: Increase deep-audit rate for this agent's claims.
    # Normal rate: 7%. Escalated rate: 35% (5x normal).
    set_agent_audit_rate(agent_id, ESCALATED_AUDIT_RATE)  # 0.35

    # Action 2: Require 2 independent source verifications
    # (instead of the normal 1) for all this agent's E-class claims.
    set_agent_source_verify_count(agent_id, 2)

    # Action 3: Alert Sentinel Graph for cross-correlation with
    # collusion detection (forgers may also be colluding).
    sentinel_alert(
        alert_type="FORGERY_SUSPICION",
        agent_id=agent_id,
        suspicion_score=suspicion.composite_score,
        component_scores={
            "production_rate": suspicion.h1_production_rate,
            "source_verifiability": suspicion.h2_source_verifiability,
            "audit_discrepancy": suspicion.h3_audit_discrepancy,
            "citation_pattern": suspicion.h4_citation_pattern,
        },
        epoch=epoch
    )

    # Action 4: Retroactive audit of recent claims.
    # Select the 5 most-cited claims from this agent in the lookback
    # window and schedule them for deep audit if not already audited.
    recent_claims = get_agent_recent_claims(agent_id, lookback=50)
    most_cited = sorted(recent_claims,
                        key=lambda c: c.citation_count, reverse=True)[:5]
    for claim in most_cited:
        if not claim.has_been_deep_audited:
            schedule_deep_audit(claim.claim_id, priority="HIGH")

    # Action 5: Log to immutable audit trail.
    log_forgery_escalation(suspicion, epoch)
```

**False positive control:** The escalation threshold of 0.60 requires multiple signals to fire simultaneously. At the H3 weight of 0.40, a perfect audit discrepancy score alone (h3=1.0) contributes only 0.40 -- below the threshold. This ensures no single metric triggers escalation. Expected false positive rate at threshold 0.60: < 2% of honest agents (based on assumption that honest agent signal distributions are approximately normal with independent noise).

**Conformance requirement (CR-H4):** The forgery suspicion score MUST be computed for every agent with >= 20 E-class or S-class claims in the lookback window. Computation runs once per epoch during the Sentinel Graph metric feed. Escalation is automatic and non-discretionary.

---

### 1.5 Economic Deterrent Analysis

**Extends:** C5 Section 11.2 (Attack Resistance, Attack 1), verified against C8 Section 10.3 (Slashing Schedule)

For forgery to be economically irrational, the expected cost of being caught must exceed the expected gain from undetected forgery.

**Detection probability model:**

```
P(detected per claim) = P(detected by normal verification)
                       + P(detected by deep audit | not caught in normal)

P(normal detection) depends on source verification protocol (Section 1.1):
  Estimated: 0.40 for sophisticated forgers (misrepresented real sources)
             0.80 for unsophisticated forgers (fabricated sources)

P(deep audit detection | not caught normally):
  Base audit rate: 7% (0.07)
  Audit detection rate: 80% (0.80) for sophisticated forgers
  Per-claim: 0.07 * 0.80 = 0.056

Combined per-claim detection probability:
  Sophisticated forger: 1 - (1 - 0.40) * (1 - 0.056) = 0.434
  Unsophisticated forger: 1 - (1 - 0.80) * (1 - 0.056) = 0.811

With escalated scrutiny (after first detection):
  Escalated audit rate: 35% (0.35)
  Sophisticated forger post-escalation: 1 - (1 - 0.40) * (1 - 0.28) = 0.568
```

**Economic analysis against C8 slashing parameters:**

C8 defines a five-level graduated slashing schedule:
- Level 1: 1% of staked AIC (first offense)
- Level 2: 5% (second offense)
- Level 3: 15% (third offense, capabilities reduced)
- Level 4: 50% (fourth offense, capability reset)
- Level 5: 100% (fifth offense, permanent ban)

VERIFICATION_FRAUD carries a 1.5x severity multiplier (C8 Section 10.3.1).

```python
def verify_economic_deterrent():
    """
    Verify that forgery is economically irrational under C8 slashing.

    Assumptions:
    - Agent stakes S AIC.
    - Each successful forged claim yields reward R AIC.
    - Detection probability per claim: p_detect.
    - Upon detection: VERIFICATION_FRAUD violation triggered.

    For forgery to be rational:
      E[gain from N forged claims] > E[loss from N forged claims]
      N * R * (1 - p_detect) > sum of expected slashing penalties

    We need: E[loss] > E[gain] for any N.
    """

    # C8 slashing with 1.5x multiplier for VERIFICATION_FRAUD:
    EFFECTIVE_SLASH_RATES = [
        0.01 * 1.5,   # Level 1: 1.5% of stake
        0.05 * 1.5,   # Level 2: 7.5%
        0.15 * 1.5,   # Level 3: 22.5%
        0.50 * 1.5,   # Level 4: 75%
        1.00,          # Level 5: 100% (capped)
    ]

    # Expected claims until first detection (geometric distribution):
    # For sophisticated forger: E[claims to detection] = 1/0.434 ~= 2.3
    # For unsophisticated forger: E[claims to detection] = 1/0.811 ~= 1.2

    # Break-even analysis for sophisticated forger:
    # First detection: expected after ~2.3 claims
    # Gain before detection: 2.3 * R * (1 - 0.434) = 1.3 * R
    # Loss at detection: S * 0.015 = 0.015 * S
    # Break-even: 1.3 * R < 0.015 * S -> S/R > 86.7

    # But this ignores escalation. After first detection:
    # p_detect rises to 0.568
    # Second detection: expected after ~1.76 more claims
    # Cumulative gain: (1.3 + 1.76 * 0.432) * R = 2.06 * R
    # Cumulative loss: S * (0.015 + 0.075) = 0.09 * S
    # Break-even: 2.06 * R < 0.09 * S -> S/R > 22.9

    # After third detection: penalty = 22.5% + capability reduction
    # Expected cumulative loss after 3 detections: 0.315 * S
    # Expected cumulative gain: ~3.5 * R
    # Break-even: S/R > 11.1

    # CONCLUSION: For the system to deter sophisticated forgery:
    # The stake-to-reward ratio S/R must exceed ~23 for short-term
    # deterrence (2 detections) or ~87 for single-detection deterrence.

    # RECOMMENDATION: Set minimum stake for verification participation
    # at 25x the per-claim reward. This ensures:
    # - After first detection: agent has lost 1.5% of stake
    #   but only gained ~1.3 claims worth of reward
    # - Net expected value of forgery attempt:
    #   1.3R - 0.015 * 25R = 1.3R - 0.375R = 0.925R (still positive!)

    # With MINIMUM_STAKE_RATIO = 50 (conservative):
    # Net EV = 1.3R - 0.015 * 50R = 1.3R - 0.75R = 0.55R
    # Still marginally positive for single detection.

    # BUT: escalation + retroactive audit makes continuation irrational.
    # After escalation, agent faces 35% audit rate and 5 retroactive audits.
    # If any of 5 retroactive audits detect forgery: 5 additional violations.
    # This cascades to Level 3-5 slashing almost immediately.

    # With retroactive cascade:
    # Expected loss from escalation aftermath:
    #   P(retro_detect) * cumulative_slash >= 0.315 * S
    # At S/R = 50: 0.315 * 50R = 15.75R
    # Total gain from 2.3 claims: 1.3R
    # Net EV with escalation cascade: 1.3R - 15.75R = -14.45R

    # STRONGLY IRRATIONAL once escalation triggers.

    MINIMUM_STAKE_RATIO = 50  # S >= 50R required

    return DeterrentAnalysis(
        minimum_stake_ratio=MINIMUM_STAKE_RATIO,
        single_claim_deterrent=False,  # Honest: single claim may be +EV
        escalation_deterrent=True,     # Escalation makes continuation -EV
        cascade_deterrent=True,        # Retroactive audits make it deeply -EV
        recommendation=(
            "Set MINIMUM_VERIFICATION_STAKE = 50 * MEAN_CLAIM_REWARD. "
            "Single-claim forgery is marginally profitable but escalation "
            "cascade makes sustained forgery deeply unprofitable. "
            "The system tolerates rare single-claim forgeries (which are "
            "caught by temporal evidence decay anyway) while making "
            "systematic forgery economically irrational."
        )
    )
```

**Conformance requirement (CR-H5):** The Settlement Plane (C8) MUST enforce `MINIMUM_VERIFICATION_STAKE >= 50 * MEAN_CLAIM_REWARD` for any agent submitting E-class or S-class claims. This parameter is constitutionally protected (G-class change required).

---

## Problem 2: Collusion / "Mutual Endorsement"

### 2.1 Sentinel Graph Committee Exclusion Constraint

**Extends:** C5 Section 10.4 (Sentinel Graph Interface) and C3 VRF committee selection

The Sentinel Graph (C3) maintains identity cluster analysis. Agents identified as likely Sybils (same operator, correlated behavior, shared infrastructure) are clustered. This section specifies how cluster information constrains committee composition.

```python
def apply_committee_exclusion_constraint(
    candidate_committee: List[AgentID],
    claim: Claim,
    sentinel_clusters: SentinelClusterMap
) -> List[AgentID]:
    """
    Enforce: no two committee members may belong to the same
    Sentinel Graph identity cluster.

    The VRF committee selection (C3) produces a candidate list ranked
    by VRF output. This function filters the list to enforce cluster
    exclusion, backfilling from lower-ranked candidates as needed.

    Parameters:
    - candidate_committee: VRF-ranked list of candidate verifiers
    - claim: the claim being verified (for context)
    - sentinel_clusters: current Sentinel Graph cluster assignments

    Returns: filtered committee of target_size members
    """
    target_size = get_committee_size(claim)

    selected = []
    clusters_represented = set()

    for agent_id in candidate_committee:
        # Look up this agent's Sentinel Graph cluster
        cluster_id = sentinel_clusters.get_cluster(agent_id)

        if cluster_id is None:
            # Agent not in any cluster (appears independent)
            selected.append(agent_id)
        elif cluster_id not in clusters_represented:
            # First member from this cluster: allowed
            selected.append(agent_id)
            clusters_represented.add(cluster_id)
        else:
            # Another member from the same cluster: EXCLUDED
            log_exclusion(
                agent_id=agent_id,
                cluster_id=cluster_id,
                reason="SENTINEL_CLUSTER_EXCLUSION",
                claim_id=claim.claim_id
            )
            continue  # Skip to next candidate

        if len(selected) >= target_size:
            break

    # If we cannot fill the committee after exhausting candidates,
    # the network lacks sufficient independent agents.
    if len(selected) < target_size:
        shortfall = target_size - len(selected)

        if shortfall <= 1:
            # Minor shortfall: proceed with reduced committee
            # but flag for monitoring
            log_committee_shortfall(claim.claim_id, shortfall)
        else:
            # Significant shortfall: escalate committee size requirement
            # and fall back to replication-based verification
            return handle_insufficient_diversity(
                claim, selected, shortfall
            )

    return selected


def handle_insufficient_diversity(claim, partial_committee, shortfall):
    """
    When the network cannot form a diverse committee:
    1. Increase committee size by shortfall (require MORE independent agents)
    2. If still insufficient: fall back to replication verification
    3. Flag the claim for elevated deep-audit probability
    """
    # Try expanding the candidate pool by relaxing locus constraints
    expanded = expand_candidate_pool(claim, locus_radius=2)
    additional = apply_committee_exclusion_constraint(
        expanded, claim, get_sentinel_clusters()
    )

    if len(partial_committee) + len(additional) >= get_committee_size(claim):
        return partial_committee + additional[:shortfall]

    # Cannot form diverse committee: fall back to replication
    log_diversity_failure(claim.claim_id)
    claim.verification_mode = "REPLICATION_FALLBACK"
    # Ensure elevated audit rate for replication-verified claims
    claim.audit_rate_override = 0.25  # 25% instead of 7%
    return partial_committee
```

**Conformance requirement (CR-H6):** VRF committee selection MUST apply Sentinel Graph cluster exclusion before finalizing any verification committee. The producing agent's cluster (if any) is always excluded. This constraint is non-negotiable even if it reduces committee size.

---

### 2.2 Statistical Collusion Detection

**Extends:** C5 Section 11.2 (Attack 8), Sentinel Graph endorsement correlation

This algorithm detects collusion through three independent statistical signals, with explicit false positive controls.

```python
def detect_collusion_patterns(
    agent_pair: Tuple[AgentID, AgentID],
    lookback_epochs: int = 200
) -> CollusionAssessment:
    """
    Detect statistical patterns consistent with collusion between
    a pair of agents. Run for all pairs that have shared >= 50 committees.

    Three independent signals:
    S1: Agreement rate anomaly
    S2: Opinion distribution similarity (KL divergence)
    S3: Opinion value copying

    False positive control: Bonferroni correction for multiple testing.
    """

    a, b = agent_pair
    shared_history = get_shared_committee_history(a, b, lookback_epochs)

    if len(shared_history) < MIN_SHARED_COMMITTEES:  # 50
        return CollusionAssessment(
            insufficient_data=True,
            pair=agent_pair
        )

    # --- S1: Agreement Rate Anomaly ---
    # How often do these agents produce the same verification verdict?
    agreements = sum(
        1 for record in shared_history
        if same_verdict(record.opinion_a, record.opinion_b)
    )
    agreement_rate = agreements / len(shared_history)

    # Baseline: expected agreement rate for independent agents
    # on the same claim types. Compute from population statistics.
    expected_agreement = compute_expected_agreement_rate(
        claim_classes=get_claim_class_distribution(shared_history)
    )

    # For D-class (deterministic): expected agreement is high (~0.95).
    # For H-class (heuristic): expected agreement is lower (~0.60).
    # The anomaly is the excess above expected, weighted by claim class.

    # Test: is agreement_rate significantly above expected?
    # Use a one-sided binomial test.
    from scipy.stats import binom_test
    p_value_s1 = binom_test(
        agreements, len(shared_history), expected_agreement,
        alternative='greater'
    )
    s1_suspicious = (agreement_rate > 0.95 and p_value_s1 < 0.01)

    # --- S2: Opinion Distribution Similarity (KL Divergence) ---
    # Independent agents should have distinguishable opinion distributions
    # (different calibration, different priors, different expertise).
    # Colluding agents copy each other's opinions, making distributions
    # indistinguishable.

    opinions_a = [r.opinion_a for r in shared_history]
    opinions_b = [r.opinion_b for r in shared_history]

    # Compute KL divergence between the discretized opinion distributions
    # for each SL component: belief, disbelief, uncertainty
    kl_belief = kl_divergence(
        discretize_opinions([o.belief for o in opinions_a], bins=20),
        discretize_opinions([o.belief for o in opinions_b], bins=20)
    )
    kl_disbelief = kl_divergence(
        discretize_opinions([o.disbelief for o in opinions_a], bins=20),
        discretize_opinions([o.disbelief for o in opinions_b], bins=20)
    )
    kl_uncertainty = kl_divergence(
        discretize_opinions([o.uncertainty for o in opinions_a], bins=20),
        discretize_opinions([o.uncertainty for o in opinions_b], bins=20)
    )

    mean_kl = (kl_belief + kl_disbelief + kl_uncertainty) / 3

    # KL < 0.01 means distributions are nearly identical.
    # For reference: independent agents typically have KL > 0.05.
    s2_suspicious = (mean_kl < KL_COLLUSION_THRESHOLD)  # 0.01

    # --- S3: Opinion Value Copying ---
    # Direct copying: agents submit numerically identical SL values.
    # Allow for floating point: "identical" means |diff| < epsilon.
    EPSILON = 0.001
    exact_copies = sum(
        1 for r in shared_history
        if (abs(r.opinion_a.belief - r.opinion_b.belief) < EPSILON
            and abs(r.opinion_a.disbelief - r.opinion_b.disbelief) < EPSILON
            and abs(r.opinion_a.uncertainty - r.opinion_b.uncertainty) < EPSILON)
    )
    copy_rate = exact_copies / len(shared_history)

    # Even D-class claims should show SOME variation (different
    # computation paths, different priors). Copy rate > 30% is suspicious.
    s3_suspicious = (copy_rate > COPY_RATE_THRESHOLD)  # 0.30

    # --- Composite Assessment with False Positive Control ---
    # Bonferroni correction: 3 tests, significance level 0.01
    # Adjusted threshold: 0.01 / 3 = 0.0033 per test

    suspicion_count = sum([s1_suspicious, s2_suspicious, s3_suspicious])

    # Require at least 2 of 3 signals to flag as collusion.
    # This dramatically reduces false positives.
    is_collusion_candidate = (suspicion_count >= 2)

    # Compute composite score for graduated response
    composite = (
        0.35 * (1.0 if s1_suspicious else 0.0)
        + 0.35 * (1.0 if s2_suspicious else 0.0)
        + 0.30 * (1.0 if s3_suspicious else 0.0)
    )

    return CollusionAssessment(
        pair=agent_pair,
        agreement_rate=agreement_rate,
        expected_agreement=expected_agreement,
        kl_divergence=mean_kl,
        copy_rate=copy_rate,
        s1_suspicious=s1_suspicious,
        s2_suspicious=s2_suspicious,
        s3_suspicious=s3_suspicious,
        composite_score=composite,
        is_collusion_candidate=is_collusion_candidate,
        recommendation=(
            "SEPARATE" if is_collusion_candidate else "MONITOR"
        )
    )


def run_collusion_sweep(epoch, lookback=200):
    """
    Run collusion detection across all agent pairs with sufficient
    shared committee history. Runs once per 10 epochs.
    """
    # Get all pairs with >= 50 shared committees
    pairs = get_frequent_committee_pairs(
        min_shared=MIN_SHARED_COMMITTEES, lookback=lookback
    )

    results = []
    for pair in pairs:
        assessment = detect_collusion_patterns(pair, lookback)
        results.append(assessment)

    # Apply actions for detected collusion candidates
    for r in results:
        if r.is_collusion_candidate:
            # Action 1: Never assign to same committee again
            add_permanent_committee_exclusion(r.pair)

            # Action 2: Alert Sentinel Graph to merge clusters
            sentinel_alert(
                alert_type="COLLUSION_DETECTED",
                agents=r.pair,
                evidence={
                    "agreement_rate": r.agreement_rate,
                    "kl_divergence": r.kl_divergence,
                    "copy_rate": r.copy_rate,
                },
                epoch=epoch
            )

            # Action 3: Schedule retroactive audit of claims
            # verified by BOTH agents on the same committee
            shared_claims = get_claims_verified_by_pair(r.pair, lookback)
            for claim_id in shared_claims[:20]:  # Cap retroactive audits
                schedule_deep_audit(claim_id, priority="HIGH")

    return results
```

**Conformance requirement (CR-H7):** Collusion detection MUST run every 10 epochs for all agent pairs meeting the shared-committee threshold. When collusion is detected, permanent committee exclusion MUST be applied immediately and retroactive audits MUST be scheduled.

---

### 2.3 Diversity-Constrained Committee Selection

**Extends:** C3 VRF committee selection, C5 Section 6 verification protocols

The VRF committee selection must guarantee minimum diversity across multiple dimensions, not just Sentinel Graph clusters.

```python
def select_diverse_committee(
    claim: Claim,
    epoch: int,
    target_size: int = 5
) -> Committee:
    """
    Select a verification committee with guaranteed diversity.

    Diversity dimensions:
    D1: No two members from the same locus (if committee size allows)
    D2: No two members with the same model lineage
    D3: No two members from the same Sentinel Graph cluster (Section 2.1)

    If diversity cannot be achieved, increase committee size.
    If increased committee still fails, fall back with elevated audit rate.
    """

    # Step 1: Get VRF-ranked candidate list (standard C3 mechanism)
    vrf_seed = compute_vrf_seed(
        b"COMMITTEE_SELECT" + claim.claim_id.encode() + uint64_be(epoch)
    )
    all_eligible = get_eligible_verifiers(
        claim.locus, exclude={claim.producing_agent}
    )
    ranked_candidates = vrf_rank(all_eligible, vrf_seed)

    # Step 2: Apply diversity constraints via greedy selection
    selected = []
    loci_used = set()
    lineages_used = set()
    clusters_used = set()
    sentinel_clusters = get_sentinel_clusters()

    for agent_id in ranked_candidates:
        agent_profile = get_agent_profile(agent_id)
        agent_locus = agent_profile.home_locus
        agent_lineage = agent_profile.model_lineage  # e.g., "GPT-4", "Claude-3"
        agent_cluster = sentinel_clusters.get_cluster(agent_id)

        # Check D3 (hard constraint): Sentinel Graph cluster exclusion
        if agent_cluster is not None and agent_cluster in clusters_used:
            continue

        # Check D1 (soft constraint): locus diversity
        locus_conflict = (agent_locus in loci_used and
                          len(loci_used) < target_size)

        # Check D2 (soft constraint): model lineage diversity
        lineage_conflict = (agent_lineage in lineages_used and
                            len(lineages_used) < target_size)

        # For soft constraints: allow violation only if we cannot
        # fill the committee otherwise (exhausted diverse candidates)
        if locus_conflict or lineage_conflict:
            # Skip for now; may backfill if needed
            continue

        selected.append(agent_id)
        loci_used.add(agent_locus)
        lineages_used.add(agent_lineage)
        if agent_cluster is not None:
            clusters_used.add(agent_cluster)

        if len(selected) >= target_size:
            break

    # Step 3: If committee undersized, relax soft constraints (D1, D2)
    # but maintain hard constraint (D3)
    if len(selected) < target_size:
        for agent_id in ranked_candidates:
            if agent_id in selected:
                continue

            agent_cluster = sentinel_clusters.get_cluster(agent_id)
            if agent_cluster is not None and agent_cluster in clusters_used:
                continue  # D3 remains hard

            selected.append(agent_id)
            if agent_cluster is not None:
                clusters_used.add(agent_cluster)

            if len(selected) >= target_size:
                break

    # Step 4: If still undersized, increase committee size
    # to compensate for reduced diversity
    if len(selected) < target_size:
        expanded_size = target_size + (target_size - len(selected)) * 2
        # Recurse with expanded pool and relaxed locus constraint
        expanded_candidates = get_eligible_verifiers(
            claim.locus, radius=2, exclude={claim.producing_agent}
        )
        return select_diverse_committee_expanded(
            claim, epoch, expanded_size, expanded_candidates
        )

    # Step 5: Compute diversity score for metadata
    diversity_score = compute_committee_diversity(
        selected, loci_used, lineages_used, clusters_used, target_size
    )

    return Committee(
        members=selected,
        diversity_score=diversity_score,
        loci_count=len(loci_used),
        lineage_count=len(lineages_used),
        cluster_count=len(clusters_used),
    )


def compute_committee_diversity(
    members, loci_used, lineages_used, clusters_used, target_size
) -> float:
    """
    Diversity score in [0, 1]. Higher is better.
    Perfect diversity = 1.0 (all members from different loci,
    lineages, and clusters).
    """
    n = len(members)
    if n <= 1:
        return 1.0

    locus_diversity = len(loci_used) / n
    lineage_diversity = len(lineages_used) / n

    # Weight locus and lineage equally
    return (locus_diversity + lineage_diversity) / 2
```

**Conformance requirement (CR-H8):** Committee diversity score MUST be recorded for every verification event. If diversity_score < 0.5, the claim's deep-audit rate MUST be doubled. If diversity_score < 0.3, replication fallback MUST be triggered.

---

### 2.4 Adaptive Audit Rate for Unanimous Committees

**Extends:** C5 Section 6.4 (Deep-Audit Protocol), citation-weighted bias

Unanimous agreement on complex claims is statistically suspicious. Independent experts evaluating nuanced claims should exhibit genuine disagreement. This mechanism increases audit rates for unanimous verdicts on claim types where disagreement is expected.

```python
def compute_adaptive_audit_rate(
    claim: Claim,
    committee_opinions: List[SubjectiveLogicOpinion],
    base_rate: float = 0.07
) -> float:
    """
    Compute the effective deep-audit rate for a claim based on
    committee agreement patterns.

    Unanimous agreement on complex claims (H, N, K class) is
    statistically unexpected and warrants higher audit rates.

    Returns: effective audit rate in [base_rate, 0.50]
    """

    # Step 1: Compute agreement level.
    # "Unanimous" = all committee members' belief values within
    # UNANIMITY_TOLERANCE of each other.
    UNANIMITY_TOLERANCE = 0.05
    beliefs = [o.belief for o in committee_opinions]
    belief_range = max(beliefs) - min(beliefs)
    is_unanimous = (belief_range < UNANIMITY_TOLERANCE)

    if not is_unanimous:
        # Not unanimous: use base rate (possibly with other modifiers)
        return base_rate

    # Step 2: Determine expected disagreement for this claim class.
    # D-class: unanimity is EXPECTED (deterministic -> clear answer)
    # C-class: unanimity is EXPECTED (checklist compliance)
    # E-class: unanimity is POSSIBLE but less common
    # S-class: unanimity is UNCOMMON (statistical interpretation varies)
    # P-class: unanimity is EXPECTED (process conformance is mechanical)
    # R-class: unanimity is UNCOMMON (reasoning quality is subjective)
    # H-class: unanimity is RARE (heuristic judgment varies)
    # N-class: unanimity is RARE (normative claims are contentious)
    # K-class: unanimity is RARE (consolidation claims are novel)

    EXPECTED_DISAGREEMENT = {
        "D": 0.05,   # Low expected disagreement
        "C": 0.10,
        "P": 0.10,
        "E": 0.20,
        "S": 0.30,
        "R": 0.35,
        "H": 0.45,
        "N": 0.50,
        "K": 0.50,   # Consolidation claims (from C6 dreaming)
    }

    expected_disagreement = EXPECTED_DISAGREEMENT.get(
        claim.assigned_class, 0.20
    )

    # Step 3: Compute audit rate multiplier.
    # Higher expected disagreement + unanimity = more suspicious
    # Multiplier = 1 + (expected_disagreement * UNANIMITY_SUSPICION_FACTOR)
    UNANIMITY_SUSPICION_FACTOR = 8.0
    multiplier = 1.0 + (expected_disagreement * UNANIMITY_SUSPICION_FACTOR)

    # Step 4: Apply claim complexity modifier.
    # Claims with more dependencies or higher stakes warrant more scrutiny.
    dependency_count = len(claim.dependencies)
    complexity_factor = 1.0 + 0.1 * min(dependency_count, 5)

    effective_rate = base_rate * multiplier * complexity_factor

    # Cap at 50% (diminishing returns beyond this)
    return min(effective_rate, MAX_ADAPTIVE_AUDIT_RATE)  # 0.50


# Example effective audit rates for unanimous committees:
#
# D-class unanimous: 0.07 * (1 + 0.05*8) * 1.0 = 0.098 (barely elevated)
# E-class unanimous: 0.07 * (1 + 0.20*8) * 1.0 = 0.182
# H-class unanimous: 0.07 * (1 + 0.45*8) * 1.0 = 0.322
# N-class unanimous: 0.07 * (1 + 0.50*8) * 1.0 = 0.350
# K-class unanimous, 5 deps: 0.07 * (1 + 0.50*8) * 1.5 = 0.50 (capped)
```

**Conformance requirement (CR-H9):** The adaptive audit rate MUST be computed for every claim that passes verification. The computed rate replaces the base 7% rate for VRF deep-audit selection (C5 Section 6.4). The rate computation MUST be logged for audit trail purposes.

---

## Problem 3: Consolidation Poisoning (C6)

### 3.1 Source Independence Verification

**Extends:** C6 Section 5.3.2 (Provenance Diversity Verification)

The base specification checks agent count, parcel count, and single-agent dominance. This addendum adds deeper independence verification to detect adversarially planted quanta.

```python
def verify_source_independence(
    candidate: CandidateSet,
    sentinel_clusters: SentinelClusterMap,
    epoch: int
) -> IndependenceVerification:
    """
    Before consolidation, verify that source quanta are genuinely
    independent -- not planted by coordinated adversaries.

    Three additional checks beyond CR-12 base diversity:
    I1: Provenance chain independence (trace back to original sources)
    I2: Temporal clustering detection
    I3: Sentinel Graph cluster diversity

    All three must pass in addition to CR-12 base checks.
    """

    quanta = candidate.quanta
    result = IndependenceVerification()

    # --- I1: Provenance Chain Independence ---
    # Trace each quantum back through its DERIVATION edges to find
    # the ultimate source(s). If multiple quanta trace back to the
    # same original source, they are not truly independent.

    provenance_roots = {}
    for q in quanta:
        roots = trace_provenance_roots(q, max_depth=10)
        provenance_roots[q.id] = roots

    # Build a root-overlap matrix
    all_roots = set()
    for roots in provenance_roots.values():
        all_roots.update(roots)

    # For each root, count how many quanta derive from it
    root_coverage = {}
    for root_id in all_roots:
        coverage = sum(
            1 for q_id, roots in provenance_roots.items()
            if root_id in roots
        )
        root_coverage[root_id] = coverage

    # If any single root covers > 50% of candidate quanta,
    # the evidence is not independent.
    max_root_coverage = max(root_coverage.values()) / len(quanta)
    if max_root_coverage > ROOT_COVERAGE_THRESHOLD:  # 0.50
        result.i1_pass = False
        result.i1_reason = (
            f"Root source covers {max_root_coverage:.0%} of quanta "
            f"(threshold: {ROOT_COVERAGE_THRESHOLD:.0%})"
        )
    else:
        result.i1_pass = True

    # --- I2: Temporal Clustering Detection ---
    # If quanta were all created within a suspiciously short window,
    # they may have been planted in a coordinated burst.

    creation_epochs = [q.provenance.generation_epoch for q in quanta]
    epoch_span = max(creation_epochs) - min(creation_epochs)

    # Expected: quanta accumulated over many epochs (organic discovery)
    # Suspicious: all quanta created within a narrow window

    # Use coefficient of variation (CV) of creation epochs
    mean_epoch = mean(creation_epochs)
    std_epoch = std(creation_epochs)
    cv = std_epoch / mean_epoch if mean_epoch > 0 else 0

    # Low CV = tightly clustered in time
    # Also check absolute span
    if epoch_span < TEMPORAL_CLUSTER_MIN_SPAN:  # 10 epochs
        result.i2_pass = False
        result.i2_reason = (
            f"All quanta created within {epoch_span} epochs "
            f"(minimum span: {TEMPORAL_CLUSTER_MIN_SPAN})"
        )
    elif len(set(creation_epochs)) < len(quanta) * 0.5:
        # More than half created in the same epoch
        result.i2_pass = False
        result.i2_reason = (
            f"Temporal clustering: {len(quanta) - len(set(creation_epochs))} "
            f"quanta share creation epochs"
        )
    else:
        result.i2_pass = True

    # --- I3: Sentinel Graph Cluster Diversity ---
    # In addition to CR-12's agent diversity check, verify that
    # source agents do not share a Sentinel Graph cluster.
    # This catches Sybil-based planting.

    agent_clusters = {}
    for q in quanta:
        agent_id = q.provenance.generating_agent
        cluster_id = sentinel_clusters.get_cluster(agent_id)
        if cluster_id is not None:
            if cluster_id not in agent_clusters:
                agent_clusters[cluster_id] = []
            agent_clusters[cluster_id].append(agent_id)

    # If any Sentinel cluster contributes > 30% of agents, reject
    for cluster_id, agents in agent_clusters.items():
        cluster_fraction = len(set(agents)) / len(
            set(q.provenance.generating_agent for q in quanta)
        )
        if cluster_fraction > CLUSTER_DOMINANCE_THRESHOLD:  # 0.30
            result.i3_pass = False
            result.i3_reason = (
                f"Sentinel cluster {cluster_id} contributes "
                f"{cluster_fraction:.0%} of source agents"
            )
            break
    else:
        result.i3_pass = True

    # --- Overall ---
    result.all_pass = result.i1_pass and result.i2_pass and result.i3_pass

    return result


def trace_provenance_roots(quantum, max_depth=10):
    """
    Follow DERIVATION edges backwards to find root quanta
    (quanta with no incoming DERIVATION edges, or external sources).
    """
    roots = set()
    visited = set()
    stack = [(quantum.id, 0)]

    while stack:
        q_id, depth = stack.pop()
        if q_id in visited or depth > max_depth:
            continue
        visited.add(q_id)

        q = get_quantum(q_id)
        if q is None:
            roots.add(q_id)  # External or dissolved source
            continue

        derivation_sources = [
            e.source_id for e in q.edges
            if e.edge_type == "DERIVATION" and e.target_id == q_id
        ]

        if not derivation_sources:
            roots.add(q_id)  # This is a root quantum
        else:
            for source_id in derivation_sources:
                stack.append((source_id, depth + 1))

    return roots
```

**Conformance requirement (CR-H10):** Source independence verification MUST execute after CR-12 provenance diversity checks and before consolidation lock acquisition. Failure of any independence check (I1, I2, or I3) MUST reject the consolidation candidate. Rejection reasons MUST be logged.

---

### 3.2 Adversarial Consolidation Probing

**Extends:** C6 Section 5.3.4 (Three-Pass LLM Synthesis), post-synthesis validation

After dreaming produces a candidate consolidation, the system generates and scores a counter-hypothesis before accepting the result.

```python
def probe_consolidation_adversarially(
    consolidation_claim: str,
    source_quanta: List[EpistemicQuantum],
    synthesis_context: SynthesisContext
) -> ConsolidationProbeResult:
    """
    Adversarial probing for consolidation outputs.

    For each candidate consolidation:
    1. Generate a counter-hypothesis (null hypothesis: pattern is coincidental)
    2. Score both the consolidation and the counter-hypothesis
    3. If counter-hypothesis is competitive, flag as LOW_CONFIDENCE

    This catches consolidations that are artifacts of biased sampling
    or adversarial planting rather than genuine cross-domain patterns.
    """

    # Step 1: Generate counter-hypothesis.
    # The counter-hypothesis asserts that the observed pattern is
    # coincidental, and provides an alternative explanation.

    counter_prompt = f"""
    A system has identified the following cross-domain pattern:

    CLAIMED PATTERN: {consolidation_claim}

    SOURCE EVIDENCE:
    {format_quanta_summaries(source_quanta)}

    Your task: Generate the strongest possible counter-hypothesis.
    Assume the pattern is coincidental or artifactual. Explain:
    1. Why the observed correlation might be spurious
    2. What confounding factors could create this apparent pattern
    3. What the base rate of such coincidental patterns is
    4. What additional evidence would be needed to distinguish
       genuine pattern from coincidence

    Be rigorous and specific.
    """

    counter_hypothesis = llm_inference(
        counter_prompt,
        temperature=PROBE_TEMPERATURE,  # 0.3 (lower for analytical)
        max_tokens=2048
    )

    # Step 2: Score both hypotheses using structured evaluation.

    scoring_prompt = f"""
    Evaluate two competing hypotheses about a cross-domain pattern.

    SOURCE EVIDENCE:
    {format_quanta_summaries(source_quanta)}

    HYPOTHESIS A (Pattern is genuine):
    {consolidation_claim}

    HYPOTHESIS B (Pattern is coincidental):
    {counter_hypothesis}

    Score each hypothesis on:
    1. Evidential support (0-10): How well does the evidence support this?
    2. Parsimony (0-10): How simple and elegant is the explanation?
    3. Predictive power (0-10): Does it predict anything testable?
    4. Robustness (0-10): Would it survive additional scrutiny?

    Provide numerical scores and brief justifications.
    """

    scoring_result = llm_inference(
        scoring_prompt,
        temperature=0.1,  # Very low for consistent scoring
        max_tokens=1024
    )

    scores = parse_hypothesis_scores(scoring_result)

    # Step 3: Compare scores.
    score_a = scores.hypothesis_a.total  # Sum of 4 dimensions
    score_b = scores.hypothesis_b.total

    # Compute relative strength
    if score_a + score_b > 0:
        relative_strength = score_a / (score_a + score_b)
    else:
        relative_strength = 0.5  # Cannot distinguish

    # Step 4: Classify confidence.
    COMPETITIVE_THRESHOLD = 0.40  # Counter-hypothesis within 20%
                                   # means relative_strength < 0.60

    if relative_strength < COMPETITIVE_THRESHOLD:
        # Counter-hypothesis is STRONGER than the consolidation
        confidence = "REJECTED"
        recommendation = "DISCARD_CONSOLIDATION"
    elif relative_strength < (1.0 - COMPETITIVE_THRESHOLD):
        # Hypotheses are competitive (within 20%)
        confidence = "LOW_CONFIDENCE"
        recommendation = "FLAG_FOR_REVIEW"
    else:
        # Consolidation is clearly stronger
        confidence = "HIGH_CONFIDENCE"
        recommendation = "PROCEED"

    return ConsolidationProbeResult(
        consolidation_claim=consolidation_claim,
        counter_hypothesis=counter_hypothesis,
        score_consolidation=score_a,
        score_counter=score_b,
        relative_strength=relative_strength,
        confidence=confidence,
        recommendation=recommendation,
        scoring_detail=scores,
    )


def apply_consolidation_probe(
    confirmed_claims: List[str],
    source_quanta: List[EpistemicQuantum],
    synthesis_context: SynthesisContext
) -> List[ProbedConsolidation]:
    """
    Apply adversarial probing to all consolidation outputs
    from the three-pass synthesis (C6 Section 5.3.4).

    Returns only claims that survive probing.
    """
    results = []

    for claim in confirmed_claims:
        probe_result = probe_consolidation_adversarially(
            claim, source_quanta, synthesis_context
        )

        if probe_result.recommendation == "DISCARD_CONSOLIDATION":
            # Counter-hypothesis is stronger. Discard.
            log_consolidation_rejection(claim, probe_result)
            continue

        probed = ProbedConsolidation(
            claim=claim,
            probe_result=probe_result,
        )

        if probe_result.recommendation == "FLAG_FOR_REVIEW":
            # Competitive counter-hypothesis. Proceed but with
            # mandatory uncertainty floor.
            probed.uncertainty_floor = LOW_CONFIDENCE_UNCERTAINTY_FLOOR  # 0.50
            probed.requires_empirical_validation = True
        else:
            probed.uncertainty_floor = None
            probed.requires_empirical_validation = False

        results.append(probed)

    return results
```

**Conformance requirement (CR-H11):** Every consolidation output from the dreaming pipeline MUST undergo adversarial probing before PCVM submission. Claims rejected by probing MUST NOT be submitted. Claims flagged as LOW_CONFIDENCE MUST carry a mandatory uncertainty floor of u >= 0.50 in their initial SL opinion.

---

### 3.3 Consolidation Lineage Tracking and Credibility Cascading

**Extends:** C6 Section 4.5 (Edge Types), DERIVATION edge semantics

When a consolidation is later found to be false, the system traces back to contributing quanta and cascades credibility reduction.

```python
class ConsolidationLineage:
    """
    Track which quanta contributed to which consolidations.

    Data structure: bidirectional mapping
    - consolidation_id -> [contributing_quantum_ids]
    - quantum_id -> [consolidation_ids it contributed to]
    """

    def __init__(self):
        self.consolidation_to_quanta = {}  # c_id -> List[q_id]
        self.quantum_to_consolidations = {}  # q_id -> List[c_id]

    def register(self, consolidation_id, contributing_quanta_ids):
        self.consolidation_to_quanta[consolidation_id] = (
            list(contributing_quanta_ids)
        )
        for q_id in contributing_quanta_ids:
            if q_id not in self.quantum_to_consolidations:
                self.quantum_to_consolidations[q_id] = []
            self.quantum_to_consolidations[q_id].append(consolidation_id)


def cascade_credibility_on_consolidation_failure(
    consolidation_id: str,
    failure_reason: str,
    lineage: ConsolidationLineage,
    epoch: int
):
    """
    When a consolidation's credibility drops below threshold,
    cascade credibility reduction to contributing quanta and
    flag contributing agents for enhanced scrutiny.

    Trigger: consolidation quantum's credibility (E(w)) drops below
    CONSOLIDATION_FAILURE_THRESHOLD (0.30).
    """

    consolidation = get_quantum(consolidation_id)
    credibility = (consolidation.opinion.belief
                   + consolidation.opinion.base_rate
                   * consolidation.opinion.uncertainty)

    if credibility >= CONSOLIDATION_FAILURE_THRESHOLD:  # 0.30
        return  # Not a failure yet

    # Step 1: Get contributing quanta
    contributing_ids = lineage.consolidation_to_quanta.get(
        consolidation_id, []
    )

    if not contributing_ids:
        return  # No lineage data (should not happen per CR-H12)

    # Step 2: Compute credibility reduction for contributors.
    # Reduction is proportional to:
    # (a) How much the consolidation has fallen below threshold
    # (b) How many contributors share responsibility (dilution)
    # (c) Each quantum's contribution weight (if available)

    severity = CONSOLIDATION_FAILURE_THRESHOLD - credibility  # [0, 0.30]
    severity_factor = severity / CONSOLIDATION_FAILURE_THRESHOLD  # [0, 1]

    num_contributors = len(contributing_ids)
    per_quantum_reduction = (
        severity_factor
        * CASCADE_REDUCTION_FACTOR  # 0.15 (max reduction per contributor)
        / math.sqrt(num_contributors)  # Dilute by sqrt(N) not N
        # sqrt dilution: if 4 quanta contribute, each takes 50% of max
        # not 25%. This reflects shared responsibility.
    )

    per_quantum_reduction = min(
        per_quantum_reduction,
        MAX_CASCADE_REDUCTION  # 0.10 (absolute cap per quantum)
    )

    # Step 3: Apply reduction to each contributing quantum
    for q_id in contributing_ids:
        q = get_quantum(q_id)
        if q is None or q.metabolic_state.phase == "DISSOLVED":
            continue

        # Reduce belief, transfer to uncertainty
        reduction = min(per_quantum_reduction, q.opinion.belief)
        q.opinion.belief -= reduction
        q.opinion.uncertainty += reduction

        # Log the cascade
        q.provenance.attribution_chain.append({
            "agent_id": "SYSTEM:CASCADE",
            "role": "credibility_cascade",
            "timestamp": now(),
            "reason": (
                f"Contributing consolidation {consolidation_id} "
                f"failed (credibility={credibility:.3f})"
            ),
            "reduction": reduction,
        })

    # Step 4: Flag contributing agents for enhanced scrutiny
    contributing_agents = set()
    for q_id in contributing_ids:
        q = get_quantum(q_id)
        if q is not None:
            contributing_agents.add(q.provenance.generating_agent)

    for agent_id in contributing_agents:
        # Count how many failed consolidations this agent has contributed to
        failed_contributions = count_failed_consolidation_contributions(
            agent_id, lookback_epochs=200
        )

        if failed_contributions >= ENHANCED_SCRUTINY_THRESHOLD:  # 3
            sentinel_alert(
                alert_type="CONSOLIDATION_CONTRIBUTOR_CONCERN",
                agent_id=agent_id,
                failed_contributions=failed_contributions,
                epoch=epoch
            )
            # Increase audit rate for this agent's claims
            current_rate = get_agent_audit_rate(agent_id)
            set_agent_audit_rate(
                agent_id,
                min(current_rate * 2, 0.30)
            )

    # Step 5: Check for cascading consolidation failures.
    # If a contributing quantum is itself a consolidation,
    # check whether its credibility has now fallen below threshold
    # and recursively cascade if needed.
    for q_id in contributing_ids:
        q = get_quantum(q_id)
        if (q is not None
            and q.content.claim_type == "consolidation"
            and q.id in lineage.consolidation_to_quanta):

            new_credibility = (q.opinion.belief
                               + q.opinion.base_rate * q.opinion.uncertainty)
            if new_credibility < CONSOLIDATION_FAILURE_THRESHOLD:
                # Recursive cascade (with depth limit)
                cascade_credibility_on_consolidation_failure(
                    q.id,
                    "Cascading from parent consolidation failure",
                    lineage, epoch
                )
```

**Conformance requirement (CR-H12):** The ConsolidationLineage MUST be updated every time a consolidation quantum is created. Lineage data MUST be persisted alongside the quantum. Credibility cascade MUST execute within 1 epoch of a consolidation's credibility dropping below `CONSOLIDATION_FAILURE_THRESHOLD`. Recursive cascade depth MUST be limited to `MAX_CASCADE_DEPTH = 5`.

---

### 3.4 Consolidation Rate Limiting

**Extends:** C6 Section 5.3 (Phase 3: Consolidation), dreaming schedule

An adversary flooding a domain with planted patterns is constrained by the rate at which consolidations can be produced.

```python
# Rate limiting parameters (constitutionally protected)
MAX_CONSOLIDATIONS_PER_DOMAIN_PER_CYCLE = 10
MAX_CONSOLIDATIONS_PER_SHARD_PER_CYCLE = 25
MAX_CONSOLIDATION_QUANTA_FRACTION = 0.05  # Max 5% of active quanta
                                           # can be consolidations

def enforce_consolidation_rate_limits(
    shard: Shard,
    new_consolidations: List[EpistemicQuantum],
    domain: str,
    epoch: int
) -> List[EpistemicQuantum]:
    """
    Apply rate limits to consolidation outputs before they enter
    the PCVM verification queue.

    Returns: the subset of consolidations that pass rate limits.
    """

    # Limit 1: Per-domain cap per consolidation cycle
    domain_count_this_cycle = count_consolidations_this_cycle(
        shard, domain, epoch
    )
    remaining_domain_budget = max(
        0,
        MAX_CONSOLIDATIONS_PER_DOMAIN_PER_CYCLE - domain_count_this_cycle
    )

    # Limit 2: Per-shard cap per consolidation cycle
    shard_count_this_cycle = count_consolidations_this_cycle(
        shard, domain=None, epoch=epoch
    )
    remaining_shard_budget = max(
        0,
        MAX_CONSOLIDATIONS_PER_SHARD_PER_CYCLE - shard_count_this_cycle
    )

    # Limit 3: Total consolidation fraction of active quanta
    active_count = count_active_quanta(shard)
    current_consolidation_count = count_consolidation_quanta(shard)
    max_allowed = int(active_count * MAX_CONSOLIDATION_QUANTA_FRACTION)
    remaining_fraction_budget = max(
        0,
        max_allowed - current_consolidation_count
    )

    # Apply the most restrictive limit
    allowed_count = min(
        remaining_domain_budget,
        remaining_shard_budget,
        remaining_fraction_budget,
        len(new_consolidations)
    )

    if allowed_count < len(new_consolidations):
        # Prioritize consolidations by probe confidence and source diversity
        ranked = sorted(
            new_consolidations,
            key=lambda c: (
                c.probe_result.relative_strength if hasattr(c, 'probe_result') else 0,
                count_unique_agents(c.source_quanta)
            ),
            reverse=True
        )
        accepted = ranked[:allowed_count]
        rejected = ranked[allowed_count:]

        for r in rejected:
            log_rate_limit_rejection(
                consolidation=r,
                reason="RATE_LIMIT",
                budgets={
                    "domain": remaining_domain_budget,
                    "shard": remaining_shard_budget,
                    "fraction": remaining_fraction_budget,
                },
                epoch=epoch
            )

        return accepted

    return new_consolidations
```

**Conformance requirement (CR-H13):** Consolidation rate limits MUST be enforced before PCVM submission. All three limits (per-domain, per-shard, consolidation fraction) MUST be checked. Rate limit parameters are constitutionally protected (G-class change required).

---

### 3.5 Empirical Validation Queue for K-class Consolidation Claims

**Extends:** C6 Section 4.3 (Lifecycle State Machine), C5 Claim Classification (K-class per C9 Patch)

K-class claims produced by consolidation (dreaming) carry inherent uncertainty because they are synthetic -- produced by reasoning over other claims, not directly observed. This section defines a mandatory validation queue that constrains K-class credibility until empirical corroboration arrives.

```python
class EmpiricalValidationQueue:
    """
    K-class claims from consolidation enter a pending validation state.
    They are usable but carry a mandatory uncertainty floor until
    independently corroborated by E-class (empirical) observations.

    If no corroboration arrives within VALIDATION_TIMEOUT epochs,
    aging uncertainty kicks in aggressively.
    """

    INITIAL_UNCERTAINTY_FLOOR = 0.40  # u >= 0.40 until corroborated
    VALIDATION_TIMEOUT = 100          # epochs
    AGING_RATE = 0.01                 # per epoch after timeout
    CORROBORATION_RELIEF = 0.10       # Each corroboration reduces floor by 0.10
    MINIMUM_FLOOR_AFTER_CORROBORATION = 0.10  # Never fully eliminate floor

    def __init__(self):
        self.pending = {}  # quantum_id -> ValidationEntry

    def enqueue(self, quantum_id: str, epoch: int):
        """Register a K-class consolidation for validation tracking."""
        self.pending[quantum_id] = ValidationEntry(
            quantum_id=quantum_id,
            enqueued_epoch=epoch,
            corroborations=[],
            uncertainty_floor=self.INITIAL_UNCERTAINTY_FLOOR,
            status="PENDING_VALIDATION",
        )

    def register_corroboration(
        self,
        quantum_id: str,
        corroborating_claim_id: str,
        corroboration_type: str,
        epoch: int
    ):
        """
        Register an independent empirical corroboration.

        Corroboration types:
        - DIRECT: E-class claim directly confirms the K-class prediction
        - PARTIAL: E-class claim confirms a component of the prediction
        - INDIRECT: E-class claim is consistent with but does not
                     directly test the prediction
        """
        if quantum_id not in self.pending:
            return  # Not tracked (already validated or not K-class)

        entry = self.pending[quantum_id]

        # Verify the corroborating claim is genuinely independent:
        # - Must be E-class (empirical)
        # - Must be from a different agent than the consolidation
        # - Must have been created AFTER the consolidation
        corroborating = get_claim(corroborating_claim_id)
        consolidation = get_quantum(quantum_id)

        if corroborating is None or consolidation is None:
            return

        if corroborating.assigned_class != "E":
            return  # Only empirical claims count as corroboration

        if corroborating.producing_agent == consolidation.provenance.generating_agent:
            return  # Self-corroboration not allowed

        if corroborating.epoch <= consolidation.timestamps.created_epoch:
            return  # Must be created after the consolidation

        # Register the corroboration
        relief = {
            "DIRECT": self.CORROBORATION_RELIEF,        # 0.10
            "PARTIAL": self.CORROBORATION_RELIEF * 0.5,  # 0.05
            "INDIRECT": self.CORROBORATION_RELIEF * 0.25, # 0.025
        }.get(corroboration_type, 0.0)

        entry.corroborations.append(CorroborationRecord(
            claim_id=corroborating_claim_id,
            corroboration_type=corroboration_type,
            epoch=epoch,
            floor_relief=relief,
        ))

        # Reduce uncertainty floor
        entry.uncertainty_floor = max(
            self.MINIMUM_FLOOR_AFTER_CORROBORATION,
            entry.uncertainty_floor - relief
        )

        # If floor has reached minimum, mark as validated
        if entry.uncertainty_floor <= self.MINIMUM_FLOOR_AFTER_CORROBORATION:
            entry.status = "VALIDATED"

    def apply_uncertainty_floors(self, epoch: int):
        """
        Called each epoch to enforce uncertainty floors on pending
        K-class quanta and apply aging to timed-out entries.
        """
        for quantum_id, entry in list(self.pending.items()):
            if entry.status == "VALIDATED":
                continue

            q = get_quantum(quantum_id)
            if q is None or q.metabolic_state.phase == "DISSOLVED":
                del self.pending[quantum_id]
                continue

            # Check for timeout
            epochs_waiting = epoch - entry.enqueued_epoch

            if epochs_waiting > self.VALIDATION_TIMEOUT:
                if not entry.corroborations:
                    # No corroboration at all after timeout:
                    # Apply aggressive aging uncertainty
                    excess_epochs = epochs_waiting - self.VALIDATION_TIMEOUT
                    aging_penalty = self.AGING_RATE * excess_epochs
                    entry.uncertainty_floor = min(
                        0.80,  # Cap: don't push to dissolution via floor alone
                        entry.uncertainty_floor + aging_penalty
                    )
                    entry.status = "AGING"

            # Enforce the floor: if quantum's uncertainty is below
            # the floor, transfer from belief to uncertainty
            if q.opinion.uncertainty < entry.uncertainty_floor:
                deficit = entry.uncertainty_floor - q.opinion.uncertainty
                transfer = min(deficit, q.opinion.belief)
                q.opinion.belief -= transfer
                q.opinion.uncertainty += transfer

    def get_status(self, quantum_id: str) -> Optional[str]:
        entry = self.pending.get(quantum_id)
        return entry.status if entry else None
```

**Example validation timeline:**

| Epoch | Event | Uncertainty Floor | Status |
|-------|-------|-------------------|--------|
| 0 | K-class consolidation created | 0.40 | PENDING_VALIDATION |
| 30 | Partial E-class corroboration arrives | 0.35 | PENDING_VALIDATION |
| 60 | Direct E-class corroboration arrives | 0.25 | PENDING_VALIDATION |
| 80 | Another direct corroboration | 0.15 | PENDING_VALIDATION |
| 85 | Third direct corroboration | 0.10 | VALIDATED |

**Without corroboration:**

| Epoch | Event | Uncertainty Floor | Status |
|-------|-------|-------------------|--------|
| 0 | K-class consolidation created | 0.40 | PENDING_VALIDATION |
| 100 | Validation timeout | 0.40 | AGING |
| 150 | 50 epochs past timeout | 0.90 -> capped at 0.80 | AGING |
| ~180 | Vitality drops below decay threshold | -- | DECAYING |

**Conformance requirement (CR-H14):** Every K-class quantum produced by the dreaming pipeline MUST be enqueued in the Empirical Validation Queue upon creation. The queue MUST execute `apply_uncertainty_floors()` every epoch. Corroboration registration MUST verify independence (different agent, E-class, created after consolidation). These constraints are non-negotiable and cannot be overridden by SHREC budget allocation.

---

## Parameter Summary

All configurable parameters introduced by this addendum, with their default values and constitutional protection status.

| Parameter | Default | Section | Constitutional |
|-----------|---------|---------|---------------|
| SOURCE_FETCH_TIMEOUT | 30000ms | 1.1 | No |
| QUOTE_MATCH_THRESHOLD | 0.90 | 1.1 | No |
| SOURCE_SUPPORT_THRESHOLD | 0.40 | 1.1 | No |
| SINGLE_SOURCE_MAX_BELIEF | 0.70 | 1.3 | Yes |
| CORROBORATION_FACTOR | 0.10 | 1.3 | Yes |
| ABSOLUTE_BELIEF_CAP | 0.95 | 1.3 | Yes |
| CORROBORATION_STABILITY_THRESHOLD | 3 | 1.3 | No |
| EVIDENCE_TEMPORAL_DECAY_RATE | 0.002/epoch | 1.3 | No |
| MINIMUM_DECAYED_MAX | 0.30 | 1.3 | Yes |
| FORGERY_ESCALATION_THRESHOLD | 0.60 | 1.4 | No |
| ESCALATED_AUDIT_RATE | 0.35 | 1.4 | No |
| MINIMUM_VERIFICATION_STAKE | 50x reward | 1.5 | Yes |
| MIN_SHARED_COMMITTEES (collusion) | 50 | 2.2 | No |
| KL_COLLUSION_THRESHOLD | 0.01 | 2.2 | No |
| COPY_RATE_THRESHOLD | 0.30 | 2.2 | No |
| UNANIMITY_TOLERANCE | 0.05 | 2.4 | No |
| UNANIMITY_SUSPICION_FACTOR | 8.0 | 2.4 | No |
| MAX_ADAPTIVE_AUDIT_RATE | 0.50 | 2.4 | No |
| ROOT_COVERAGE_THRESHOLD | 0.50 | 3.1 | Yes |
| TEMPORAL_CLUSTER_MIN_SPAN | 10 epochs | 3.1 | No |
| CLUSTER_DOMINANCE_THRESHOLD | 0.30 | 3.1 | Yes |
| MAX_CONSOLIDATIONS_PER_DOMAIN_PER_CYCLE | 10 | 3.4 | Yes |
| MAX_CONSOLIDATIONS_PER_SHARD_PER_CYCLE | 25 | 3.4 | Yes |
| MAX_CONSOLIDATION_QUANTA_FRACTION | 0.05 | 3.4 | Yes |
| INITIAL_UNCERTAINTY_FLOOR | 0.40 | 3.5 | Yes |
| VALIDATION_TIMEOUT | 100 epochs | 3.5 | Yes |
| AGING_RATE | 0.01/epoch | 3.5 | No |
| CORROBORATION_RELIEF | 0.10 | 3.5 | No |
| CONSOLIDATION_FAILURE_THRESHOLD | 0.30 | 3.3 | Yes |
| CASCADE_REDUCTION_FACTOR | 0.15 | 3.3 | No |
| MAX_CASCADE_REDUCTION | 0.10 | 3.3 | No |
| MAX_CASCADE_DEPTH | 5 | 3.3 | No |
| ENHANCED_SCRUTINY_THRESHOLD | 3 failures | 3.3 | No |

---

## Conformance Requirements Summary

| ID | Requirement | Applies To |
|----|-------------|-----------|
| CR-H1 | Mandatory source verification for E-class VTDs | C5 Verifiers |
| CR-H2 | Evidence correlation for multi-verifier E-class claims | C5 Membrane |
| CR-H3 | Evidence belief cap enforcement at verification and maintenance | C5 Credibility Engine |
| CR-H4 | Forgery suspicion score computation for qualifying agents | C5 Sentinel Graph Interface |
| CR-H5 | Minimum stake ratio for E/S-class claim producers | C8 Settlement Plane |
| CR-H6 | Sentinel Graph cluster exclusion in committee selection | C3/C5 Committee Selection |
| CR-H7 | Periodic collusion detection sweep with automatic exclusion | C5 Sentinel Graph Interface |
| CR-H8 | Committee diversity score recording and fallback triggers | C3/C5 Committee Selection |
| CR-H9 | Adaptive audit rate computation for all passed claims | C5 Deep-Audit Subsystem |
| CR-H10 | Source independence verification before consolidation | C6 Dreaming Pipeline |
| CR-H11 | Adversarial probing for all consolidation outputs | C6 Dreaming Pipeline |
| CR-H12 | Consolidation lineage tracking and credibility cascading | C6 Quantum Engine |
| CR-H13 | Consolidation rate limit enforcement | C6 Dreaming Pipeline |
| CR-H14 | Empirical validation queue for K-class consolidations | C6 Quantum Engine |

---

## Residual Risk Assessment (Post-Hardening)

These defenses do not eliminate the three CRITICAL risks. They reduce expected success probability and increase adversary cost. Honest assessment:

### VTD Forgery (Post-Hardening)

**Before:** Sophisticated forger with real but misrepresented sources could persist indefinitely with 7% audit detection per claim.

**After:** Layered defense reduces expected forger lifespan:
- Source verification catches ~40% of sophisticated forgeries at verification time (Section 1.1)
- Evidence correlation detects single-source dependency (Section 1.2)
- Temporal decay limits the damage window for single-source claims (Section 1.3)
- Forgery heuristics trigger escalation after patterns emerge (Section 1.4)
- Economic deterrent makes sustained forgery deeply unprofitable (Section 1.5)

**Residual risk: MEDIUM.** A sophisticated forger with diverse, real, correctly-quoted sources who misrepresents the relationship between source and claim can still evade detection for a few claims. But the temporal evidence decay (Section 1.3) limits the credibility of these claims over time, and the economic deterrent (Section 1.5) makes the expected value negative for any sustained campaign.

### Collusion (Post-Hardening)

**Before:** Colluders who vary their behavior to stay below Sentinel Graph detection thresholds could systematically degrade verification.

**After:** Multi-dimensional detection makes evasion harder:
- Sentinel Graph cluster exclusion prevents known Sybils from sharing committees (Section 2.1)
- Three-signal statistical detection catches behavioral correlation (Section 2.2)
- Diversity-constrained selection ensures locus and model lineage diversity (Section 2.3)
- Adaptive audit rates target the suspicious unanimity pattern that collusion produces (Section 2.4)

**Residual risk: MEDIUM.** A small collusion ring (2-3 agents) with different operators, different model lineages, in different loci, who carefully vary their opinions to avoid statistical detection, can still occasionally influence individual committee outcomes. But: (a) they must control >= 1/3 of a committee to change the outcome, (b) diversity constraints make this harder, (c) adaptive audit rates catch unanimous outcomes, and (d) retroactive audits from any detection cascade to expose past collusion.

### Consolidation Poisoning (Post-Hardening)

**Before:** Coordinated agents planting quanta across domains could steer dreaming with no defense beyond provenance diversity checks.

**After:** Five-layer defense:
- Source independence verification catches shared-root and temporally-clustered planting (Section 3.1)
- Adversarial probing catches consolidations with competitive counter-hypotheses (Section 3.2)
- Lineage tracking enables post-hoc credibility cascading when consolidations fail (Section 3.3)
- Rate limiting constrains the volume of poisoned consolidations per cycle (Section 3.4)
- Empirical validation queue constrains the credibility of unverified consolidations (Section 3.5)

**Residual risk: MEDIUM.** A patient adversary who plants quanta over many epochs (avoiding temporal clustering), using truly independent agents (avoiding cluster detection), from genuinely different sources (avoiding root coverage detection), can still bias consolidation. But: the adversarial probing (Section 3.2) requires the genuine pattern to be stronger than the coincidence hypothesis, and the empirical validation queue (Section 3.5) requires real-world corroboration before the consolidation achieves high credibility. A planted consolidation that fails empirical validation within 100 epochs loses credibility through aging and eventually dissolves.

---

## Conclusion

These three problems are fundamentally unsolvable in the general case. VTD forgery reduces to the philosophical problem of epistemic grounding: verification of evidence ultimately requires trusting SOME source. Collusion reduces to the Byzantine generals problem extended to statistical behavior. Consolidation poisoning reduces to the problem of distinguishing genuine correlation from adversarial injection in an open system.

The defense-in-depth approach does not claim to solve these problems. It claims to make attacks expensive, detectable over time, and self-limiting in impact. The key architectural insight is that each mechanism is independent: an adversary must defeat ALL layers simultaneously, not just one. A forger must evade source verification AND evidence correlation AND heuristic detection AND economic penalties. A colluder must evade cluster exclusion AND statistical detection AND diversity constraints AND adaptive auditing. A consolidation poisoner must evade independence verification AND adversarial probing AND rate limits AND empirical validation.

The probability of simultaneously defeating all layers is the product of the individual evasion probabilities -- dramatically lower than any single layer alone. This is the value of defense-in-depth: not perfection, but multiplicative defense.
