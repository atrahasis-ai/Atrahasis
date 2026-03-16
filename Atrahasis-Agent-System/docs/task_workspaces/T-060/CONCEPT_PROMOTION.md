# T-060 Concept Promotion Record

## Promoted Concept
- **Concept ID:** IC-2+ (merged IC-1 + IC-2)
- **Invention ID:** C35
- **Title:** Seismographic Sentinel with PCM-Augmented Tier 2
- **Promoted at:** 2026-03-12
- **Approved by:** User (HITL gate)

## Concept Summary
Three-tier hierarchical detection pipeline for security and anomaly detection:
- Tier 1: Per-agent STA/LTA with fixed + adaptive baselines
- Tier 2: PCM residuals within triggered neighborhoods + 4-channel quorum threshold
- Tier 3: Epidemiological backward tracing from confirmed anomalies

## Scores at Promotion
- Novelty: 3.5-4.0 (merged estimate)
- Feasibility: 4.0 (merged estimate)

## Conditions Carried Forward
- C-1: Tier 2 emits raw + residual values (auditability)
- C-2: PCM includes "unmodeled correlation" category at reduced severity
- C-3: PCM coverage fallback to raw IC-2 below 0.70 threshold
- D-1: PCM is precomputed lookup, refreshed at CONSOLIDATION_CYCLE cadence

## Monitoring Flags
- MF-1: If Tier 2 quorum integration insufficient at DESIGN, revisit IC-3 adaptive topology
- MF-2: Validate PCM convergence bounds at RESEARCH
- MF-3: Determine if composition novelty is sufficient or IC-1 elements needed
- MF-4: Red Team fixed-baseline reconstructibility at FEASIBILITY

## Rejected/Absorbed Concepts
- IC-3 (Quorum Resonance Graph): Dissolved by majority. Multi-channel quorum threshold absorbed into IC-2 Tier 2. Adaptive topology rejected as adversarially fragile.
