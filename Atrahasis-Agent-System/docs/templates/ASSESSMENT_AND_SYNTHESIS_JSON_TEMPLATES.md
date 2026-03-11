# Assessment & Synthesis Report Templates (v1.0)

## Specialist Assessor Report (JSON)
```json
{
  "type": "TECHNICAL_FEASIBILITY_REPORT",
  "invention_id": "C1",
  "overall": "FEASIBLE|PARTIALLY_FEASIBLE|INFEASIBLE",
  "findings": [
    {"severity":"MINOR","area":"...","detail":"...","recommendation":"..."}
  ],
  "feasibility_score": 4,
  "confidence": 4
}
```

Other specialist report types follow the same structure with `type` set to:
- `NOVELTY_REPORT`
- `IMPACT_REPORT`
- `SPEC_COMPLETENESS_REPORT`
- `COMMERCIAL_VIABILITY_REPORT`
- `PROTOTYPE_VALIDATOR_REPORT`

## Prior Art Report (JSON)
```json
{
  "type": "PRIOR_ART_REPORT",
  "invention_id": "C1",
  "search_queries": ["..."],
  "patents_found": [{"id":"...","title":"...","relevance":"HIGH","summary":"..."}],
  "papers_found": [{"title":"...","authors":"...","year":2025,"relevance":"MEDIUM","summary":"..."}],
  "products_found": [{"name":"...","company":"...","relevance":"LOW","summary":"..."}],
  "open_source_found": [{"name":"...","url":"...","relevance":"MEDIUM","summary":"..."}],
  "closest_prior_art": {"reference":"...","similarity":"...","differentiators":["..."]},
  "novelty_assessment": "...",
  "gaps_identified": ["..."],
  "confidence": 4
}
```

## Assessment Council Verdict (JSON)
```json
{
  "type": "ASSESSMENT_COUNCIL_VERDICT",
  "invention_id": "C1",
  "stage": "ASSESSMENT",
  "decision": "ADVANCE|CONDITIONAL_ADVANCE|PIVOT|REJECT",
  "novelty_score": 4,
  "feasibility_score": 3,
  "impact_score": 4,
  "risk_score": 3,
  "risk_level": "MEDIUM",
  "required_actions": [
    {"id":"ACT-1","detail":"...","owner":"Specification Writer","blocking":true}
  ],
  "monitoring_flags": [
    {"id":"MON-1","detail":"..."}
  ],
  "pivot_direction": null,
  "rationale": "..."
}
```

## Synthesis Result (JSON)
```json
{
  "type": "SYNTHESIS_RESULT",
  "invention_id": "C1",
  "contributions_applied": ["docs/contribution_requests/C1.yaml"],
  "shared_artifacts_modified": ["docs/specifications/C1/claims.md"],
  "conflicts_resolved": [],
  "consistency_checks": [{"check":"...","result":"PASS|FAIL"}],
  "notes": "..."
}
```

## Invention Result (JSON)
```json
{
  "type": "INVENTION_RESULT",
  "invention_id": "C1",
  "stage": "DESIGN",
  "role": "Architecture Designer",
  "status": "COMPLETE|PARTIAL|BLOCKED",
  "confidence": 4,
  "summary": "one paragraph max",
  "artifacts_created": [{"path":"...","description":"..."}],
  "artifacts_modified": [{"path":"...","description":"..."}],
  "contribution_request_created": true,
  "contribution_request_path": "docs/contribution_requests/C1.yaml",
  "validation_evidence": ["..."],
  "novelty_observations": [],
  "feasibility_observations": [],
  "known_issues": [],
  "low_confidence_areas": [],
  "blockers": [],
  "next_recommended_action": "..."
}
```
