# TRIBUNAL_LOG.md
# Atrahasis Agent System — Council Transcript Archive
# Version: 1.0

---

## PURPOSE

This file is the **append-only transcript archive** for:

- Ideation Council deliberations
- Assessment Council deliberations

It is maintained by the **Chronicler**.

**Important:** The Opening Brief does *not* read this file by default.
Read-first condensed memory lives in:

- `docs/SESSION_BRIEF.md`
- `docs/DECISIONS.md`
- `docs/PATTERN_REGISTER.md`

This file is consulted only when:
- a specific decision needs original reasoning
- an assessment dispute needs a transcript reference
- a post-mortem requires deep review

---

## CANONICAL TAXONOMY (v1.0)

- **Novelty Score:** 1–5
- **Feasibility Score:** 1–5
- **Decision:** ADVANCE | CONDITIONAL_ADVANCE | PIVOT | REJECT
- **Risk Score:** 1–10 (LOW 1–2, MEDIUM 3–4, HIGH 5–6, CRITICAL 7–10)

---

## TEMPLATE — Ideation Council Entry

```markdown
---
SESSION: IDEATION-<INVENTION_ID>-<SEQ>
Date: YYYY-MM-DD
Domain: <Problem Domain>
Trigger: Initial | Reconvening | Pivot
---

## INPUT
- Problem statement: ...
- Research data (if reconvening): [...]
- Constraints: [...]

## COUNCIL SUMMARY (5–10 lines)
- (Chronicler summary)
- (Must include: key concepts, novelty assessment, dissent)

## ROUND 1 — OPENING POSITIONS
**Visionary:** ...
**Systems Thinker:** ...
**Critic:** ...

## ROUND 2 — CHALLENGE
- ...

## ROUND 3 — SYNTHESIS
- Consensus:
- Dissent record:

## OUTPUT (YAML)
```yaml
IDEATION_COUNCIL_OUTPUT:
  ...
```

## POST-MORTEM (filled later)
- Was the concept viable? YES | PARTIAL | NO
- What it missed:
- Lessons:
---
```

---

## TEMPLATE — Assessment Council Entry

```markdown
---
SESSION: ASSESSMENT-<INVENTION_ID>-<SEQ>
Date: YYYY-MM-DD
Invention: <INVENTION_ID> — <Title>
Stage: <stage being assessed>
Trigger: Stage gate | Low confidence | Escalation
---

## INPUT
- Specialist INVENTION_RESULT(s) (links)
- Assessor reports (links)
- Prototype Validator output (link)

## COUNCIL SUMMARY (5–10 lines)
- (Chronicler summary)

## ADVOCATE
...

## SKEPTIC
...

## ARBITER VERDICT (JSON)
```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "<INVENTION_ID>",
  "stage": "<stage>",
  "decision": "ADVANCE|CONDITIONAL_ADVANCE|PIVOT|REJECT",
  "novelty_score": 4,
  "feasibility_score": 3,
  "impact_score": 4,
  "risk_score": 3,
  "risk_level": "MEDIUM",
  "required_actions": [],
  "monitoring_flags": [],
  "pivot_direction": null,
  "rationale": "..."
}
```

## POST-MORTEM (filled later)
- Was the verdict accurate? YES | PARTIAL | NO
- What it missed:
- Lessons:
---
```

---

## ENTRIES

(append new entries below)

---
SESSION: ASSESSMENT-C1-001
Date: 2026-03-09
Invention: C1 — Predictive Tidal Architecture (PTA)
Stage: FEASIBILITY
Trigger: Stage gate (FEASIBILITY → DESIGN)
---

## INPUT
- Refined concept: docs/invention_logs/C1_REFINED_INVENTION_CONCEPT.yaml
- Prior art report: docs/prior_art/C1/PRIOR_ART_REPORT.json
- Landscape report: docs/prior_art/C1/landscape.md
- Science assessment: completed (all layers PARTIALLY_SOUND)
- User feedback: PTA is coordination layer only; tidal backbone is core innovation

## COUNCIL SUMMARY (10 lines)
- Assessment Council evaluated C1-PTA for FEASIBILITY stage gate.
- Advocate: tidal backbone is genuinely novel (7 gaps, no prior art on combination), phased build provides value at each stage, risk management is honest and dissent incorporated.
- Skeptic: predictive communication (feasibility 3) is unproven, 21-27mo timeline optimistic, integration across 4 subsystems compounds risk, morphogenic fields may not justify overhead at 4-agent scope, adversarial schedule exploitation not fully solved.
- Arbiter: Novelty 4 justified, Feasibility 4 slightly generous but defensible, Impact 4, Risk 5 (MEDIUM).
- Decision: CONDITIONAL_ADVANCE with 2 mandatory + 2 advisory conditions.
- Mandatory: convergence experiment first (kill criterion <5% error at 100+ agents), integration contracts with Verichain/CIOS in Phase 1.
- Advisory: predictive layer enhancing-not-required, morphogenic field gate at Phase 2 end.
- 5 monitoring flags set (1 RED, 3 AMBER, 1 INFO).
- Tidal backbone alone justifies investment even if Layers 2-3 underperform.
- Full deliberation: docs/invention_logs/C1_FEASIBILITY_VERDICT.md

## ADVOCATE
(See full transcript in docs/invention_logs/C1_FEASIBILITY_VERDICT.md — Advocate section)

Key points: Tidal backbone is genuine paradigm shift; 7 novelty gaps defensible; phased build with off-ramps; honest risk register with 6 experiments; clean integration architecture (coordination layer only).

Recommendation: ADVANCE with standard monitoring.

## SKEPTIC
(See full transcript in docs/invention_logs/C1_FEASIBILITY_VERDICT.md — Skeptic section)

Key points: Predictive communication unproven (near-zero messaging claim); timeline aggressive (6-9mo for Phase 1 with no prototype); integration complexity underestimated (cross-system failure modes unaddressed); "no prior art" claim requires scrutiny (60-65% covered); morphogenic fields may be unnecessary at 4-agent scope; adversarial robustness acknowledged but not solved.

Recommendation: CONDITIONAL_ADVANCE — require convergence experiment before full DESIGN.

## ARBITER VERDICT (JSON)
```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "C1",
  "stage": "FEASIBILITY",
  "decision": "CONDITIONAL_ADVANCE",
  "novelty_score": 4,
  "feasibility_score": 4,
  "impact_score": 4,
  "risk_score": 5,
  "risk_level": "MEDIUM",
  "required_actions": [
    "Design and schedule tidal function convergence experiment as first DESIGN deliverable, with kill criterion: <5% assignment error within 3 epoch cycles at 100+ agents",
    "Draft integration interface contracts with Verichain and CIOS in DESIGN Phase 1 before cross-system assumptions harden",
    "Scope predictive communication layer as enhancing-but-not-required in DESIGN documentation",
    "Establish formal decision gate for morphogenic field layer at end of Phase 2 build"
  ],
  "monitoring_flags": [
    "RED: Tidal function migration convergence experiment fails or delayed beyond DESIGN month 3",
    "AMBER: Integration interfaces with Verichain/CIOS reveal incompatible epoch or verification assumptions",
    "AMBER: Predictive communication prototype achieves <30% communication reduction vs baseline",
    "INFO: Morphogenic fields show no measurable improvement over simple load-balancing at 4-agent scale",
    "AMBER: Adversarial analysis finds practical schedule manipulation attack not mitigated by VRF rotation"
  ],
  "pivot_direction": null,
  "rationale": "PTA presents a genuinely novel coordination architecture grounded in proven mathematical primitives. The tidal backbone — deriving scheduling, verification, and settlement from deterministic functions — is the strongest element and represents a real paradigm shift. Seven novelty gaps are defensible and the phased build plan provides value at each stage with natural off-ramps. However, the predictive communication layer remains experimentally unvalidated (feasibility 3), integration with four subsystems introduces compounding risk, and the timeline assumes no significant experimental setbacks. The concept is sufficiently refined for DESIGN entry, but advancement is conditional on early experimental validation and prompt integration contract drafting. The tidal backbone alone justifies the investment even if Layers 2 and 3 underperform."
}
```

## POST-MORTEM (filled later)
- Was the verdict accurate? (pending)
- What it missed: (pending)
- Lessons: (pending)
---
