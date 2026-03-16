from __future__ import annotations

import copy
import re
from collections import Counter
from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json
from aas1.redesign_memory_store import RedesignMemoryStore
from aas1.stage_contracts import StageContractRegistry


FULL_PIPELINE_TRACK = [
    "IDEATION",
    "RESEARCH",
    "FEASIBILITY",
    "DESIGN",
    "SPECIFICATION",
    "ASSESSMENT",
]

TASK_TRACKS = {
    "FULL_PIPELINE": FULL_PIPELINE_TRACK,
    "DIRECT_SPEC": ["RESEARCH", "SPECIFICATION", "ASSESSMENT"],
    "GOVERNANCE": ["RESEARCH", "DESIGN", "ASSESSMENT"],
    "ANALYSIS": ["RESEARCH", "ASSESSMENT"],
    "PACKAGING": ["DESIGN", "SPECIFICATION", "ASSESSMENT"],
    "VALIDATION": ["ASSESSMENT"],
    "DEMO": ["DESIGN", "ASSESSMENT"],
}

STAGE_TEAM_ROLES = {
    "IDEATION": ["visionary", "systems_thinker", "critic"],
    "RESEARCH": ["prior_art_researcher", "landscape_analyst", "science_advisor"],
    "FEASIBILITY": ["systems_thinker", "adversarial_analyst", "pre_mortem_analyst"],
    "DESIGN": ["architecture_designer", "systems_thinker"],
    "SPECIFICATION": ["specification_writer", "critic"],
    "ASSESSMENT": ["assessment_council", "critic"],
}

TASK_STAGE_ROLE_OVERRIDES = {
    "DIRECT_SPEC": {
        "RESEARCH": ["prior_art_researcher", "critic"],
        "SPECIFICATION": ["specification_writer", "critic"],
        "ASSESSMENT": ["assessment_council", "critic"],
    },
    "GOVERNANCE": {
        "RESEARCH": ["systems_thinker", "critic"],
        "DESIGN": ["systems_thinker", "specification_writer"],
        "ASSESSMENT": ["assessment_council", "critic"],
    },
    "ANALYSIS": {
        "RESEARCH": ["systems_thinker", "critic"],
        "ASSESSMENT": ["assessment_council", "critic"],
    },
    "PACKAGING": {
        "DESIGN": ["systems_thinker", "specification_writer"],
        "SPECIFICATION": ["specification_writer", "critic"],
        "ASSESSMENT": ["assessment_council", "critic"],
    },
}

FUTURE_BRANCH_LIBRARY = {
    "visionary": [
        {
            "branch_kind": "conservative",
            "branch_label": "Conservative Future",
            "lane_id": "alpha",
            "objective_template": "Explore the highest-leverage minimal-change future for the current {stage} problem.",
        },
        {
            "branch_kind": "aggressive",
            "branch_label": "Aggressive Future",
            "lane_id": "beta",
            "objective_template": "Explore the strongest capability-maximizing future for the current {stage} problem.",
        },
        {
            "branch_kind": "radical",
            "branch_label": "Radical Future",
            "lane_id": "gamma",
            "objective_template": "Explore the most discontinuous redesign future for the current {stage} problem.",
        },
    ],
    "systems_thinker": [
        {
            "branch_kind": "minimal_change",
            "branch_label": "Minimal-Change Topology",
            "lane_id": "alpha",
            "objective_template": "Explore the smallest viable topology shift that still resolves the current {stage} problem.",
        },
        {
            "branch_kind": "modular",
            "branch_label": "Modular Topology",
            "lane_id": "beta",
            "objective_template": "Explore a modular decomposition future for the current {stage} problem.",
        },
        {
            "branch_kind": "full_restructure",
            "branch_label": "Full-Restructure Topology",
            "lane_id": "gamma",
            "objective_template": "Explore an end-to-end topology rewrite future for the current {stage} problem.",
        },
    ],
    "critic": [
        {
            "branch_kind": "failure",
            "branch_label": "Failure Future",
            "lane_id": "alpha",
            "objective_template": "Explore the most plausible failure cascade future for the current {stage} problem.",
        },
        {
            "branch_kind": "abuse",
            "branch_label": "Abuse Future",
            "lane_id": "beta",
            "objective_template": "Explore the strongest misuse or adversarial-abuse future for the current {stage} problem.",
        },
        {
            "branch_kind": "governance_break",
            "branch_label": "Governance-Break Future",
            "lane_id": "gamma",
            "objective_template": "Explore the strongest authority, doctrine, or governance-break future for the current {stage} problem.",
        },
    ],
}

IDEATION_RADICAL_BRANCH_LIBRARY = {
    "visionary": [
        {
            "branch_kind": "frame_replacement",
            "branch_label": "Frame-Replacement Future",
            "lane_id": "radical",
            "objective_template": "Challenge the current architectural frame itself and explore a replacement future for the current {stage} problem.",
        }
    ],
    "systems_thinker": [
        {
            "branch_kind": "authority_reset",
            "branch_label": "Authority-Reset Topology",
            "lane_id": "radical",
            "objective_template": "Challenge the current module, authority, and topology boundaries and explore a replacement operating structure for the current {stage} problem.",
        }
    ],
    "critic": [
        {
            "branch_kind": "foundational_invalidity",
            "branch_label": "Foundational-Invalidity Future",
            "lane_id": "radical",
            "objective_template": "Challenge whether the current architectural frame is fundamentally invalid for the current {stage} problem.",
        }
    ],
}

IMPROVEMENT_LANE_CATALOG = {
    "alpha": {
        "lane_label": "Alpha Lane",
        "lane_strategy": "Improve the current task path without breaking core assumptions.",
    },
    "beta": {
        "lane_label": "Beta Lane",
        "lane_strategy": "Explore a materially different framing or topology for the current task.",
    },
    "gamma": {
        "lane_label": "Gamma Lane",
        "lane_strategy": "Break one core assumption and test a high-novelty replacement for the current task.",
    },
    "radical": {
        "lane_label": "Radical Lane",
        "lane_strategy": "Challenge topology, authority boundaries, or core primitives instead of merely optimizing the current frame.",
    },
}

RADICAL_BRANCH_KINDS = {"radical", "full_restructure", "governance_break"}

FUTURE_EXPLORATION_POLICY = {
    "ANALYSIS": {
        "RESEARCH": {
            "team_mode": "FUTURE_BRANCH_SWARM",
            "branch_roles": ["visionary", "systems_thinker", "critic"],
            "max_depth": 2,
            "convergence_owner": "parent",
            "program_title": "Research Improvement Lanes",
            "program_goal": "Explore bounded Alpha/Beta/Gamma improvement lanes before the parent commits to a research path.",
        }
    },
    "GOVERNANCE": {
        "DESIGN": {
            "team_mode": "FUTURE_BRANCH_SWARM",
            "branch_roles": ["visionary", "systems_thinker", "critic"],
            "max_depth": 2,
            "convergence_owner": "parent",
            "program_title": "Governance Improvement Lanes",
            "program_goal": "Explore bounded Alpha/Beta/Gamma governance improvements and reconcile them in the parent session.",
        }
    },
    "FULL_PIPELINE": {
        "IDEATION": {
            "team_mode": "FUTURE_BRANCH_SWARM",
            "branch_roles": ["visionary", "systems_thinker", "critic"],
            "include_radical_lane": True,
            "max_depth": 2,
            "convergence_owner": "parent",
            "program_title": "Ideation Improvement Lanes",
            "program_goal": "Explore bounded Alpha/Beta/Gamma/Radical invention improvements before concept promotion or selection.",
        },
        "DESIGN": {
            "team_mode": "FUTURE_BRANCH_SWARM",
            "branch_roles": ["visionary", "systems_thinker", "critic"],
            "max_depth": 2,
            "convergence_owner": "parent",
            "program_title": "Design Improvement Lanes",
            "program_goal": "Explore bounded Alpha/Beta/Gamma design improvements before the parent converges on one path.",
        },
    },
}

AUTO_DISPATCH_ALLOWED = {
    "FULL_PIPELINE": {"RESEARCH", "FEASIBILITY", "DESIGN"},
    "DIRECT_SPEC": {"RESEARCH", "SPECIFICATION"},
    "GOVERNANCE": {"RESEARCH", "DESIGN"},
    "ANALYSIS": {"RESEARCH"},
    "PACKAGING": {"DESIGN", "SPECIFICATION"},
    "VALIDATION": set(),
    "DEMO": {"DESIGN"},
}

APPROVAL_DECISIONS = {
    "APPROVE",
    "APPROVED",
    "ACCEPT",
    "ACCEPTED",
    "ADVANCE",
    "CONTINUE",
    "COMPLETE",
    "COMPLETED",
}
BLOCK_DECISIONS = {"BLOCK", "BLOCKED", "REJECT", "REJECTED", "STOP", "FAIL"}
REVISION_DECISIONS = {"CHANGES_REQUESTED", "REQUEST_CHANGES", "REVISE", "REVISION_REQUIRED"}
CONVERGENCE_DECISION_DISPOSITIONS = {
    "REJECT",
    "ADOPT",
    "HYBRIDIZE",
    "ESCALATE_TO_HITL",
    "PROMOTE",
}


def stage_team_roles_for(task_class: str, stage: str) -> list[str]:
    return list(TASK_STAGE_ROLE_OVERRIDES.get(task_class, {}).get(stage, STAGE_TEAM_ROLES.get(stage, [])))


def future_exploration_for(task_class: str, stage: str) -> dict[str, Any] | None:
    policy = FUTURE_EXPLORATION_POLICY.get(task_class, {}).get(stage)
    if policy is None:
        return None
    cloned = copy.deepcopy(policy)
    include_radical_lane = bool(cloned.get("include_radical_lane"))
    branches = []
    for role in cloned.get("branch_roles", []):
        for item in FUTURE_BRANCH_LIBRARY.get(role, []):
            branch_kind = str(item["branch_kind"])
            lane_id = str(item["lane_id"])
            lane = IMPROVEMENT_LANE_CATALOG[lane_id]
            branches.append(
                {
                    "branch_id": f"{role}:{branch_kind}",
                    "parent_role": role,
                    "branch_kind": branch_kind,
                    "branch_label": item["branch_label"],
                    "lane_id": lane_id,
                    "lane_label": lane["lane_label"],
                    "lane_strategy": lane["lane_strategy"],
                    "objective": item["objective_template"].format(stage=stage.lower()),
                    "radical_candidate": branch_kind in RADICAL_BRANCH_KINDS,
                }
            )
        if include_radical_lane:
            for item in IDEATION_RADICAL_BRANCH_LIBRARY.get(role, []):
                branch_kind = str(item["branch_kind"])
                lane_id = str(item["lane_id"])
                lane = IMPROVEMENT_LANE_CATALOG[lane_id]
                branches.append(
                    {
                        "branch_id": f"{role}:{branch_kind}",
                        "parent_role": role,
                        "branch_kind": branch_kind,
                        "branch_label": item["branch_label"],
                        "lane_id": lane_id,
                        "lane_label": lane["lane_label"],
                        "lane_strategy": lane["lane_strategy"],
                        "objective": item["objective_template"].format(stage=stage.lower()),
                        "radical_candidate": True,
                    }
                )
    cloned["branches"] = branches
    lane_ids = {str(item.get("lane_id")) for item in branches if item.get("lane_id")}
    cloned["lane_ids"] = sorted(lane_ids)
    cloned["lane_order"] = [lane_id for lane_id in ["alpha", "beta", "gamma", "radical"] if lane_id in lane_ids]
    return cloned


def _normalized_policy_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().upper().replace(" ", "_")


def redesign_memory_policy_signals(redesign_memory: dict[str, Any] | None) -> dict[str, Any]:
    snapshot = redesign_memory or {}
    current_entry = snapshot.get("current_entry")
    related_entries = list(snapshot.get("related_entries", []))
    entries = []
    if isinstance(current_entry, dict) and current_entry:
        entries.append(current_entry)
    entries.extend(item for item in related_entries if isinstance(item, dict) and item)

    disposition_counts: Counter[str] = Counter()
    trigger_counts: Counter[str] = Counter()
    disagreement_counts: Counter[str] = Counter()
    lane_counts: Counter[str] = Counter()
    adversarial_reviewed_count = 0
    adversarial_issue_count = 0

    for entry in entries:
        disposition = _normalized_policy_value(entry.get("selected_disposition"))
        if not disposition:
            disposition = _normalized_policy_value(entry.get("final_outcome"))
        if disposition:
            disposition_counts[disposition] += 1
        recommended_action = _normalized_policy_value(entry.get("recommended_parent_action"))
        if recommended_action == "ESCALATE_TO_HITL":
            disposition_counts["ESCALATE_TO_HITL"] += 1
        for reason in entry.get("trigger_reasons", []):
            normalized_reason = str(reason).strip()
            if normalized_reason:
                trigger_counts[normalized_reason] += 1
        for signal in entry.get("disagreement_signals", []):
            normalized_signal = str(signal).strip()
            if normalized_signal:
                disagreement_counts[normalized_signal] += 1
        for lane_id in entry.get("lane_ids", []):
            normalized_lane = str(lane_id).strip().lower()
            if normalized_lane:
                lane_counts[normalized_lane] += 1
        adversarial_status = _normalized_policy_value(entry.get("adversarial_review_status"))
        if adversarial_status:
            adversarial_reviewed_count += 1
        if adversarial_status in {"REVIEW_BLOCKED", "REVIEW_CHANGES_REQUESTED", "REVIEW_FAILED"}:
            adversarial_issue_count += 1

    adopt_count = disposition_counts["ADOPT"]
    hybridize_count = disposition_counts["HYBRIDIZE"]
    promote_count = disposition_counts["PROMOTE"]
    reject_count = disposition_counts["REJECT"]
    continue_count = disposition_counts["CONTINUE_EXPLORATION"] + disposition_counts["CONTINUED"]
    escalate_count = disposition_counts["ESCALATE_TO_HITL"]
    successful_count = adopt_count + hybridize_count + promote_count

    preferred_parent_action = None
    if hybridize_count >= max(adopt_count, promote_count, 1):
        preferred_parent_action = "hybridize"
    elif adopt_count >= max(promote_count, 1):
        preferred_parent_action = "adopt"
    elif promote_count > 0:
        preferred_parent_action = "promote"

    recurring_trigger_reasons = [item for item, count in trigger_counts.most_common(3) if count >= 1]
    recurring_disagreement_signals = [item for item, count in disagreement_counts.most_common(3) if count >= 1]

    historical_pressure_high = bool(
        (reject_count + continue_count + escalate_count) >= 2
        or adversarial_issue_count >= 1
    )
    full_branch_coverage_recommended = bool(
        lane_counts.get("gamma", 0) > 0
        and (historical_pressure_high or adversarial_issue_count > 0 or continue_count > 0)
    )

    return {
        "history_available": bool(entries),
        "sample_size": len(entries),
        "related_entry_count": len(related_entries),
        "successful_count": successful_count,
        "adopt_count": adopt_count,
        "hybridize_count": hybridize_count,
        "promote_count": promote_count,
        "reject_count": reject_count,
        "continue_count": continue_count,
        "escalate_count": escalate_count,
        "gamma_related_count": int(lane_counts.get("gamma", 0)),
        "adversarial_reviewed_count": adversarial_reviewed_count,
        "adversarial_issue_count": adversarial_issue_count,
        "historical_pressure_high": historical_pressure_high,
        "proven_improvement_available": successful_count > 0,
        "preferred_parent_action": preferred_parent_action,
        "full_branch_coverage_recommended": full_branch_coverage_recommended,
        "recurring_trigger_reasons": recurring_trigger_reasons,
        "recurring_disagreement_signals": recurring_disagreement_signals,
    }


def _dedupe_strings(values: list[str]) -> list[str]:
    result = []
    seen = set()
    for item in values:
        text = str(item).strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(text)
    return result


def improvement_trigger_policy_for(
    task_class: str,
    stage: str,
    *,
    human_decision_record: dict[str, Any] | None = None,
    redesign_memory: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    future_policy = future_exploration_for(task_class, stage)
    if future_policy is None:
        return None
    contradiction_count = int(((human_decision_record or {}).get("evidence_summary") or {}).get("contradiction_count", 0))
    novelty_scores = [
        float(item["novelty_score"])
        for item in (human_decision_record or {}).get("top_hypotheses", [])
        if item.get("novelty_score") is not None
    ]
    highest_novelty = max(novelty_scores) if novelty_scores else None
    triggers = []
    if stage in {"IDEATION", "RESEARCH", "DESIGN"}:
        triggers.append("stage_supports_task_improvement")
    if task_class in {"FULL_PIPELINE", "ANALYSIS", "GOVERNANCE"}:
        triggers.append("task_class_has_design_surface")
    if contradiction_count >= 2:
        triggers.append("contradiction_pressure_high")
    if highest_novelty is not None and highest_novelty < 6.0:
        triggers.append("novelty_pressure_low")
    if highest_novelty is not None and highest_novelty >= 8.0:
        triggers.append("high_upside_hypothesis_detected")
    memory_signals = redesign_memory_policy_signals(redesign_memory)
    if memory_signals.get("historical_pressure_high"):
        triggers.append("historical_redesign_pressure_detected")
    if memory_signals.get("proven_improvement_available"):
        triggers.append("historical_improvement_pattern_available")
    if memory_signals.get("hybridize_count", 0) >= 2:
        triggers.append("historical_hybrid_pattern_detected")
    triggers = _dedupe_strings(triggers)
    enabled = bool(triggers)
    lane_ids = sorted({str(item.get("lane_id")) for item in future_policy.get("branches", []) if item.get("lane_id")})
    lane_order = [lane_id for lane_id in ["alpha", "beta", "gamma", "radical"] if lane_id in lane_ids]
    return {
        "enabled": enabled,
        "contradiction_count": contradiction_count,
        "highest_novelty_score": highest_novelty,
        "trigger_reasons": triggers,
        "decision_options": ["reject", "adopt", "hybridize", "escalate_to_hitl"],
        "lane_ids": lane_ids,
        "lane_order": lane_order,
        "redesign_memory_signals": memory_signals,
    }


def radical_redesign_policy_for(
    task_class: str,
    stage: str,
    *,
    human_decision_record: dict[str, Any] | None = None,
    redesign_memory: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    future_policy = future_exploration_for(task_class, stage)
    if future_policy is None:
        return None
    contradiction_count = int(((human_decision_record or {}).get("evidence_summary") or {}).get("contradiction_count", 0))
    novelty_scores = [
        float(item["novelty_score"])
        for item in (human_decision_record or {}).get("top_hypotheses", [])
        if item.get("novelty_score") is not None
    ]
    highest_novelty = max(novelty_scores) if novelty_scores else None
    triggers = []
    if stage in {"IDEATION", "DESIGN"}:
        triggers.append("stage_supports_core_assumption_rewrite")
    if task_class in {"ANALYSIS", "GOVERNANCE"}:
        triggers.append("task_class_requires_architecture_pressure")
    if contradiction_count >= 3:
        triggers.append("contradiction_pressure_high")
    if highest_novelty is not None and highest_novelty < 4.0:
        triggers.append("novelty_pressure_low")
    memory_signals = redesign_memory_policy_signals(redesign_memory)
    if memory_signals.get("historical_pressure_high") and (
        memory_signals.get("continue_count", 0) > 0 or memory_signals.get("reject_count", 0) >= 2
    ):
        triggers.append("historical_plateau_detected")
    if memory_signals.get("gamma_related_count", 0) > 0 and memory_signals.get("successful_count", 0) > 0:
        triggers.append("historical_gamma_upside_detected")
    triggers = _dedupe_strings(triggers)
    enabled = bool(triggers)
    radical_branches = [item for item in future_policy.get("branches", []) if item.get("radical_candidate")]
    return {
        "enabled": enabled,
        "contradiction_count": contradiction_count,
        "highest_novelty_score": highest_novelty,
        "trigger_reasons": triggers,
        "decision_options": ["reject", "hybridize", "promote"],
        "radical_branch_ids": [item["branch_id"] for item in radical_branches],
        "redesign_memory_signals": memory_signals,
    }


def adversarial_review_policy_for(
    task_class: str,
    stage: str,
    *,
    human_decision_record: dict[str, Any] | None = None,
    redesign_memory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    contradiction_count = int(((human_decision_record or {}).get("evidence_summary") or {}).get("contradiction_count", 0))
    improvement_policy = improvement_trigger_policy_for(
        task_class,
        stage,
        human_decision_record=human_decision_record,
        redesign_memory=redesign_memory,
    )
    radical_policy = radical_redesign_policy_for(
        task_class,
        stage,
        human_decision_record=human_decision_record,
        redesign_memory=redesign_memory,
    )
    memory_signals = redesign_memory_policy_signals(redesign_memory)
    trigger_reasons: list[str] = []
    required = False
    if task_class == "FULL_PIPELINE" and stage == "FEASIBILITY":
        trigger_reasons.append("full_pipeline_feasibility_requires_adversarial_review")
        required = True
    if task_class == "GOVERNANCE" and stage == "DESIGN":
        trigger_reasons.append("governance_design_requires_adversarial_review")
        required = True
    if stage == "DESIGN" and (((improvement_policy or {}).get("enabled")) or ((radical_policy or {}).get("enabled"))):
        trigger_reasons.append("architecture_improvement_pressure_detected")
        required = True
    if task_class == "DIRECT_SPEC" and stage == "SPECIFICATION" and contradiction_count >= 3:
        trigger_reasons.append("specification_contradiction_pressure_high")
        required = True
    recommended = bool(
        contradiction_count >= 2
        and task_class in {"FULL_PIPELINE", "DIRECT_SPEC", "GOVERNANCE"}
        and stage in {"RESEARCH", "DESIGN", "SPECIFICATION", "ASSESSMENT"}
    )
    if memory_signals.get("adversarial_issue_count", 0) > 0 and stage in {"FEASIBILITY", "DESIGN"}:
        trigger_reasons.append("historical_adversarial_findings_detected")
        required = True
    elif memory_signals.get("adversarial_issue_count", 0) > 0 and stage in {"SPECIFICATION", "ASSESSMENT"}:
        trigger_reasons.append("historical_adversarial_findings_detected")
        recommended = True
    if memory_signals.get("recurring_disagreement_signals") and stage in {"DESIGN", "FEASIBILITY"}:
        trigger_reasons.append("historical_disagreement_pattern_detected")
        recommended = True
    if recommended and not required:
        if contradiction_count >= 2:
            trigger_reasons.append("contradiction_pressure_recommends_adversarial_review")
        else:
            trigger_reasons.append("historical_or_structural_pressure_recommends_adversarial_review")
    trigger_reasons = _dedupe_strings(trigger_reasons)
    return {
        "enabled": required or recommended,
        "required_before_stage_close": required,
        "review_role": "adversarial_analyst",
        "contradiction_count": contradiction_count,
        "trigger_reasons": trigger_reasons,
        "recommended_only": recommended and not required,
        "redesign_memory_signals": memory_signals,
    }


def convergence_policy_for(
    task_class: str,
    stage: str,
    *,
    future_convergence_report: dict[str, Any] | None = None,
    task_improvement_report: dict[str, Any] | None = None,
    radical_redesign_report: dict[str, Any] | None = None,
    redesign_memory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    branch_summaries = list((future_convergence_report or {}).get("branch_summaries", []))
    branch_count = int((future_convergence_report or {}).get("branch_count") or len(branch_summaries))
    completed_branch_count = sum(1 for item in branch_summaries if str(item.get("status", "")).upper() == "COMPLETED")
    disagreement_signals = [
        str(item).strip()
        for item in (future_convergence_report or {}).get("disagreement_signals", [])
        if str(item).strip()
    ]
    future_branching_enabled = future_exploration_for(task_class, stage) is not None
    enabled = bool(branch_count or task_improvement_report or radical_redesign_report)
    required = enabled and future_branching_enabled
    gamma_present = any(str(item.get("lane_id", "")).lower() == "gamma" for item in branch_summaries) or bool(
        (radical_redesign_report or {}).get("radical_branch_summaries")
    )
    decision_options: list[str] = []
    for item in (
        list((task_improvement_report or {}).get("parent_decision_options", []))
        + list((radical_redesign_report or {}).get("parent_decision_options", []))
        + ["continue_exploration"]
    ):
        normalized = str(item).strip().lower().replace(" ", "_")
        if normalized and normalized not in decision_options:
            decision_options.append(normalized)
    minimum_completed_branches = 0
    if branch_count > 0:
        minimum_completed_branches = 2 if branch_count >= 2 else 1
    memory_signals = redesign_memory_policy_signals(redesign_memory)
    if memory_signals.get("full_branch_coverage_recommended") and branch_count >= 3:
        minimum_completed_branches = min(branch_count, 3)
    trigger_reasons: list[str] = []
    if required:
        trigger_reasons.append("future_branching_requires_parent_convergence")
    if branch_count:
        trigger_reasons.append("future_branch_reports_present")
    if disagreement_signals:
        trigger_reasons.append("disagreement_signals_present")
    if gamma_present:
        trigger_reasons.append("gamma_lane_present")
    if minimum_completed_branches and completed_branch_count < minimum_completed_branches:
        trigger_reasons.append("minimum_branch_coverage_not_met")
    if memory_signals.get("full_branch_coverage_recommended") and branch_count >= 3:
        trigger_reasons.append("historical_pressure_requires_fuller_branch_coverage")
    recommended_parent_action = (task_improvement_report or {}).get("recommended_parent_action") or (future_convergence_report or {}).get("recommended_parent_action")
    preferred_parent_action = str(memory_signals.get("preferred_parent_action") or "").strip().lower()
    if not recommended_parent_action and preferred_parent_action:
        recommended_parent_action = preferred_parent_action
    if preferred_parent_action and preferred_parent_action not in decision_options:
        decision_options.append(preferred_parent_action)
    trigger_reasons = _dedupe_strings(trigger_reasons)
    return {
        "enabled": enabled,
        "required_before_stage_close": required,
        "branch_count": branch_count,
        "minimum_completed_branches": minimum_completed_branches,
        "completed_branch_count": completed_branch_count,
        "disagreement_signals": disagreement_signals,
        "recommended_parent_action": recommended_parent_action,
        "decision_options": decision_options,
        "gamma_present": gamma_present,
        "requires_gamma_disposition": gamma_present and bool(radical_redesign_report),
        "trigger_reasons": trigger_reasons,
        "redesign_memory_signals": memory_signals,
        "source_refs": {
            "future_convergence_report": f"docs/task_workspaces/{(future_convergence_report or {}).get('task_id')}/FUTURE_CONVERGENCE_REPORT.json"
            if future_convergence_report
            else None,
            "task_improvement_report": f"docs/task_workspaces/{(task_improvement_report or {}).get('task_id')}/TASK_IMPROVEMENT_REPORT.json"
            if task_improvement_report
            else None,
            "radical_redesign_report": f"docs/task_workspaces/{(radical_redesign_report or {}).get('task_id')}/RADICAL_REDESIGN_REPORT.json"
            if radical_redesign_report
            else None,
        },
    }


class WorkflowPolicyEngine:
    """Controller-enforced workflow policy, stage transitions, and dispatch hooks."""

    TASK_ROW_RE = re.compile(r"^\|\s*`?(T-[A-Z0-9-]+)`?\s*\|", re.IGNORECASE)

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.docs_root = repo_root / "docs"
        self.root = ensure_dir(runtime_state_dir(repo_root) / "workflow_policy")
        self.stage_contracts = StageContractRegistry(repo_root)
        self.redesign_memory = RedesignMemoryStore(repo_root)

    def redesign_memory_state(self, snapshot: dict[str, Any] | None) -> dict[str, Any]:
        payload = dict(snapshot or {})
        payload["policy_signals"] = redesign_memory_policy_signals(snapshot)
        return payload

    def evaluate(
        self,
        *,
        task_id: str,
        workflow_context: dict[str, Any],
        run: dict[str, Any] | None,
        review_gate_record: dict[str, Any] | None,
        adversarial_review_record: dict[str, Any] | None,
        future_convergence_report: dict[str, Any] | None = None,
        task_improvement_report: dict[str, Any] | None = None,
        radical_redesign_report: dict[str, Any] | None = None,
        convergence_gate_record: dict[str, Any] | None = None,
        human_decision_record: dict[str, Any] | None = None,
        closeout_execution_record: dict[str, Any] | None = None,
        controller_run_result: dict[str, Any] | None = None,
        claim: dict[str, Any] | None = None,
        pending_hitl_count: int = 0,
    ) -> dict[str, Any]:
        existing = self.load(task_id) or {}
        profile = self._task_profile(task_id=task_id, workflow_context=workflow_context, existing=existing)
        track = list(TASK_TRACKS[profile["task_class"]])
        state = self._seed_state(existing=existing, task_id=task_id, profile=profile, track=track)

        review_status = str((review_gate_record or {}).get("review_status", "")).upper()
        adversarial_review_status = str((adversarial_review_record or {}).get("review_status", "")).upper()
        operator_decision = self._normalize((human_decision_record or {}).get("operator_decision"))
        workflow_status = (
            self._normalize((human_decision_record or {}).get("workflow_status"))
            or self._normalize((workflow_context.get("workflow_record") or {}).get("status"))
            or self._normalize((run or {}).get("status"))
        )
        run_status = self._normalize((run or {}).get("status"))

        current_stage = state["current_stage"]
        current_index = track.index(current_stage)
        next_stage = track[current_index + 1] if current_index + 1 < len(track) else None
        active_stage_entry = self._active_stage_entry(state=state, stage=current_stage)
        stage_opened_at = str((active_stage_entry or {}).get("opened_at") or state.get("created_at") or utc_now())
        redesign_memory_snapshot = self.redesign_memory.snapshot_for_task(
            task_id=task_id,
            workflow_context=workflow_context,
            workflow_policy={
                "task_profile": profile,
                "current_stage": current_stage,
            },
            human_decision_record=human_decision_record,
        )
        redesign_memory_state = self.redesign_memory_state(redesign_memory_snapshot)
        contract_report = self.stage_contracts.evaluate(
            task_id=task_id,
            task_class=profile["task_class"],
            current_stage=current_stage,
        )
        adversarial_review = adversarial_review_policy_for(
            profile["task_class"],
            current_stage,
            human_decision_record=human_decision_record,
            redesign_memory=redesign_memory_state,
        )
        convergence = self._convergence_state(
            task_id=task_id,
            task_class=profile["task_class"],
            current_stage=current_stage,
            stage_opened_at=stage_opened_at,
            future_convergence_report=future_convergence_report,
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            convergence_gate_record=convergence_gate_record,
            redesign_memory=redesign_memory_state,
        )

        lifecycle_status = "READY"
        current_stage_status = "READY"
        transition_reason = None

        if (
            (adversarial_review.get("required_before_stage_close") and adversarial_review_status == "REVIEW_BLOCKED")
            or review_status == "REVIEW_BLOCKED"
            or operator_decision in BLOCK_DECISIONS
        ):
            lifecycle_status = "BLOCKED"
            current_stage_status = "BLOCKED"
            transition_reason = "review_or_operator_block"
        elif (
            (adversarial_review.get("required_before_stage_close") and adversarial_review_status == "REVIEW_CHANGES_REQUESTED")
            or review_status == "REVIEW_CHANGES_REQUESTED"
            or operator_decision in REVISION_DECISIONS
        ):
            lifecycle_status = "REVISION_REQUIRED"
            current_stage_status = "REVISION_REQUIRED"
            transition_reason = "review_changes_requested"
        elif self._stage_is_complete(
            review_status=review_status,
            adversarial_review_policy=adversarial_review,
            adversarial_review_record=adversarial_review_record,
            convergence=convergence,
            operator_decision=operator_decision,
            workflow_status=workflow_status,
            review_gate_record=review_gate_record,
            human_decision_record=human_decision_record,
            stage_opened_at=stage_opened_at,
            contract_report=contract_report,
        ):
            self._complete_stage(state, current_stage=current_stage, reason="review_and_operator_approved")
            if next_stage:
                current_stage = next_stage
                self._ensure_stage_entry(state, stage=current_stage, status="READY", reason="advanced_from_previous_stage")
                lifecycle_status = "NEXT_STAGE_READY"
                current_stage_status = "READY"
                transition_reason = "advanced_to_next_stage"
            else:
                lifecycle_status = "READY_FOR_CLOSEOUT"
                current_stage_status = "COMPLETED"
                transition_reason = "final_stage_completed"
        elif convergence.get("required_before_stage_close") and not convergence.get("satisfied"):
            lifecycle_status = (
                "CONVERGENCE_CONTINUE_EXPLORATION"
                if convergence.get("status") == "CONTINUE_EXPLORATION"
                else "CONVERGENCE_PENDING"
            )
            current_stage_status = "WAITING_APPROVAL" if convergence.get("ready_for_decision") else "IN_PROGRESS"
            transition_reason = "convergence_gate_pending"
        elif adversarial_review.get("enabled") and adversarial_review_status in {"REVIEW_PENDING", "REVIEW_READY_FOR_OPERATOR", "REVIEW_FAILED", "REVIEW_COMPLETED"}:
            lifecycle_status = f"ADVERSARIAL_{adversarial_review_status}"
            current_stage_status = "UNDER_REVIEW"
        elif review_status in {"REVIEW_PENDING", "REVIEW_READY_FOR_OPERATOR", "REVIEW_FAILED", "REVIEW_COMPLETED"}:
            lifecycle_status = review_status
            current_stage_status = "UNDER_REVIEW"
        elif run_status in {"TURN_RUNNING", "THREAD_READY", "THREAD_STARTING", "TURN_COMPLETED", "REVIEW_PENDING"}:
            lifecycle_status = "RUNNING"
            current_stage_status = "IN_PROGRESS"
        elif workflow_status in {"PENDING_HUMAN_REVIEW", "REVIEW_READY_FOR_OPERATOR"} or operator_decision == "PENDING":
            lifecycle_status = "AWAITING_HITL"
            current_stage_status = "WAITING_APPROVAL"

        if closeout_execution_record and closeout_execution_record.get("validation", {}).get("valid") and not next_stage:
            lifecycle_status = "COMPLETE"
            current_stage_status = "COMPLETED"

        self._ensure_stage_entry(state, stage=current_stage, status=current_stage_status, reason=transition_reason)
        dispatch = self._dispatch_state(
            task_id=task_id,
            task_class=profile["task_class"],
            current_stage=current_stage,
            existing=existing,
            human_decision_record=human_decision_record,
            pending_hitl_count=pending_hitl_count,
            review_status=review_status,
            adversarial_review_status=adversarial_review_status,
            convergence=convergence,
            settings=state["settings"],
            redesign_memory=redesign_memory_state,
        )
        next_actions = self._next_actions(
            task_id=task_id,
            current_stage=current_stage,
            next_stage=next_stage,
            lifecycle_status=lifecycle_status,
            review_status=review_status,
            adversarial_review_policy=adversarial_review,
            adversarial_review_status=adversarial_review_status,
            convergence=convergence,
            operator_decision=operator_decision,
            closeout_execution_record=closeout_execution_record,
            pending_hitl_count=pending_hitl_count,
            dispatch=dispatch,
            contract_report=contract_report,
            settings=state["settings"],
        )

        state.update(
            {
                "current_stage": current_stage,
                "next_stage": next_stage,
                "lifecycle_status": lifecycle_status,
                "gate_state": self._gate_state(
                    review_status=review_status,
                    adversarial_review_status=adversarial_review_status,
                    convergence=convergence,
                    operator_decision=operator_decision,
                    pending_hitl_count=pending_hitl_count,
                ),
                "review_status": review_status or None,
                "adversarial_review": {
                    **adversarial_review,
                    "status": adversarial_review_status or None,
                    "record_ref": f"docs/task_workspaces/{task_id}/ADVERSARIAL_REVIEW_RECORD.json"
                    if adversarial_review_record
                    else None,
                },
                "convergence": convergence,
                "run_status": run_status or None,
                "workflow_status": workflow_status or None,
                "operator_decision": operator_decision or None,
                "artifacts": {
                    "workflow_run_record": ((workflow_context.get("workflow_record") or {}).get("artifacts") or {}).get("workflow_run_record")
                    or f"docs/task_workspaces/{task_id}/WORKFLOW_RUN_RECORD.json",
                    "human_decision_record": f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json"
                    if human_decision_record
                    else None,
                    "review_gate_record": f"docs/task_workspaces/{task_id}/REVIEW_GATE_RECORD.json"
                    if review_gate_record
                    else None,
                    "adversarial_review_record": f"docs/task_workspaces/{task_id}/ADVERSARIAL_REVIEW_RECORD.json"
                    if adversarial_review_record
                    else None,
                    "convergence_gate_record": f"docs/task_workspaces/{task_id}/CONVERGENCE_GATE_RECORD.json"
                    if convergence_gate_record
                    else None,
                    "controller_run_result": f"docs/task_workspaces/{task_id}/CONTROLLER_RUN_RESULT.json"
                    if controller_run_result
                    else None,
                    "closeout_execution_record": f"docs/task_workspaces/{task_id}/CLOSEOUT_EXECUTION_RECORD.json"
                    if closeout_execution_record
                    else None,
                    "future_convergence_report": f"docs/task_workspaces/{task_id}/FUTURE_CONVERGENCE_REPORT.json"
                    if future_convergence_report
                    else None,
                    "task_improvement_report": f"docs/task_workspaces/{task_id}/TASK_IMPROVEMENT_REPORT.json"
                    if task_improvement_report
                    else None,
                    "radical_redesign_report": f"docs/task_workspaces/{task_id}/RADICAL_REDESIGN_REPORT.json"
                    if radical_redesign_report
                    else None,
                },
                "claim_status": (claim or {}).get("status"),
                "pending_hitl_count": pending_hitl_count,
                "dispatch": dispatch,
                "stage_contract": contract_report,
                "redesign_memory": redesign_memory_state,
                "next_actions": next_actions,
                "updated_at": utc_now(),
            }
        )
        self._write(task_id=task_id, payload=state)
        return state

    def update_settings(
        self,
        *,
        task_id: str,
        dispatch_mode: str | None = None,
        auto_closeout: bool | None = None,
        monitor_enabled: bool | None = None,
    ) -> dict[str, Any]:
        state = self.load(task_id) or self._seed_state(existing={}, task_id=task_id, profile=self._task_profile(task_id=task_id, workflow_context={}, existing={}), track=list(TASK_TRACKS["ANALYSIS"]))
        settings = dict(state.get("settings", {}))
        if dispatch_mode is not None:
            settings["dispatch_mode"] = dispatch_mode
        if auto_closeout is not None:
            settings["auto_closeout"] = auto_closeout
        if monitor_enabled is not None:
            settings["monitor_enabled"] = monitor_enabled
        state["settings"] = settings
        state["updated_at"] = utc_now()
        self._write(task_id=task_id, payload=state)
        return state

    def load(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def list_task_ids(self) -> list[str]:
        if not self.root.exists():
            return []
        return sorted(path.name for path in self.root.iterdir() if path.is_dir())

    def _seed_state(
        self,
        *,
        existing: dict[str, Any],
        task_id: str,
        profile: dict[str, Any],
        track: list[str],
    ) -> dict[str, Any]:
        state = copy.deepcopy(existing) if existing else {}
        state.setdefault("type", "WORKFLOW_POLICY_STATE")
        state.setdefault("task_id", task_id)
        state.setdefault("created_at", utc_now())
        state["task_profile"] = profile
        state.setdefault(
            "settings",
            {
                "dispatch_mode": "hook_only",
                "auto_closeout": False,
                "monitor_enabled": True,
            },
        )
        state.setdefault("stage_history", [])
        state.setdefault("current_stage", track[0])
        state.setdefault("next_stage", track[1] if len(track) > 1 else None)
        self._ensure_stage_entry(state, stage=state["current_stage"], status="READY", reason="seeded")
        return state

    def _task_profile(
        self,
        *,
        task_id: str,
        workflow_context: dict[str, Any],
        existing: dict[str, Any],
    ) -> dict[str, Any]:
        workflow = workflow_context.get("workflow") or {}
        request = workflow.get("request") or {}
        modifier = str(request.get("command_modifier") or (workflow_context.get("workflow_record") or {}).get("modifier") or existing.get("task_profile", {}).get("modifier") or "")
        scope = str(request.get("scope") or existing.get("task_profile", {}).get("scope") or "")
        todo_entry = self._todo_entry(task_id)
        todo_type = str((todo_entry or {}).get("type", "")).strip()
        task_class = self._task_class(todo_type=todo_type, scope=scope, modifier=modifier)
        return {
            "task_id": task_id,
            "title": (todo_entry or {}).get("title"),
            "todo_type": todo_type or None,
            "modifier": modifier or None,
            "scope": scope or None,
            "task_class": task_class,
            "stage_track": list(TASK_TRACKS[task_class]),
        }

    def _task_class(self, *, todo_type: str, scope: str, modifier: str) -> str:
        normalized_type = todo_type.strip().upper().replace(" ", "_")
        if normalized_type in {"FULL_PIPELINE", "FULL_SYSTEM_DESIGN"}:
            return "FULL_PIPELINE"
        if normalized_type in {"DIRECT_SPEC", "DIRECT_SPEC_EDIT"}:
            return "DIRECT_SPEC"
        if normalized_type == "GOVERNANCE":
            return "GOVERNANCE"
        if normalized_type == "PACKAGING":
            return "PACKAGING"
        normalized_scope = scope.strip().lower()
        if normalized_scope in {"architecture_question", "full_system_analysis"}:
            return "ANALYSIS"
        if normalized_scope == "new_idea_integration":
            return "FULL_PIPELINE"
        if normalized_scope == "buildout_task":
            return "DIRECT_SPEC"
        normalized_modifier = modifier.strip().upper()
        if normalized_modifier == "AASA":
            return "ANALYSIS"
        if normalized_modifier == "AASNI":
            return "FULL_PIPELINE"
        if normalized_modifier == "AASBT":
            return "DIRECT_SPEC"
        return "ANALYSIS"

    def _todo_entry(self, task_id: str) -> dict[str, Any] | None:
        todo_path = self.docs_root / "TODO.md"
        if not todo_path.exists():
            return None
        for line in todo_path.read_text(encoding="utf-8").splitlines():
            if not self.TASK_ROW_RE.match(line.strip()):
                continue
            parts = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
            if parts and parts[0].upper() == task_id.upper():
                return {
                    "task_id": parts[0],
                    "title": parts[1] if len(parts) > 1 else "",
                    "type": parts[2] if len(parts) > 2 else "",
                    "priority": parts[3] if len(parts) > 3 else "",
                    "dependencies": parts[4] if len(parts) > 4 else "",
                    "notes": parts[5] if len(parts) > 5 else "",
                }
        return None

    def _stage_is_complete(
        self,
        *,
        review_status: str,
        adversarial_review_policy: dict[str, Any],
        adversarial_review_record: dict[str, Any] | None,
        convergence: dict[str, Any],
        operator_decision: str,
        workflow_status: str,
        review_gate_record: dict[str, Any] | None,
        human_decision_record: dict[str, Any] | None,
        stage_opened_at: str,
        contract_report: dict[str, Any],
    ) -> bool:
        stage_review_record = adversarial_review_record if adversarial_review_policy.get("required_before_stage_close") else review_gate_record
        stage_review_status = (
            str((adversarial_review_record or {}).get("review_status", "")).upper()
            if adversarial_review_policy.get("required_before_stage_close")
            else review_status
        )
        review_recorded_at = str(
            (stage_review_record or {}).get("completed_at")
            or (stage_review_record or {}).get("updated_at")
            or ""
        )
        decision_recorded_at = str(
            (human_decision_record or {}).get("controller_recorded_at")
            or (human_decision_record or {}).get("updated_at")
            or ""
        )
        stage_bound_approval = (
            self._timestamp_at_or_after(review_recorded_at, stage_opened_at)
            or self._timestamp_at_or_after(decision_recorded_at, stage_opened_at)
        )
        if not contract_report.get("satisfied", False):
            return False
        if adversarial_review_policy.get("required_before_stage_close") and stage_review_status != "REVIEW_APPROVED":
            return False
        if convergence.get("required_before_stage_close") and not convergence.get("satisfied"):
            return False
        if stage_review_status == "REVIEW_APPROVED" and operator_decision in APPROVAL_DECISIONS and stage_bound_approval:
            return True
        return workflow_status in {"COMPLETED", "REVIEW_APPROVED"} and stage_bound_approval

    def _complete_stage(self, state: dict[str, Any], *, current_stage: str, reason: str) -> None:
        for entry in state.get("stage_history", []):
            if entry.get("stage") == current_stage and entry.get("closed_at") is None:
                entry["status"] = "COMPLETED"
                entry["closed_at"] = utc_now()
                entry["transition_reason"] = reason
                return

    def _ensure_stage_entry(self, state: dict[str, Any], *, stage: str, status: str, reason: str | None) -> None:
        now = utc_now()
        for entry in state.get("stage_history", []):
            if entry.get("stage") == stage and entry.get("closed_at") is None:
                entry["status"] = status
                if reason:
                    entry["transition_reason"] = reason
                entry["updated_at"] = now
                return
        state.setdefault("stage_history", []).append(
            {
                "stage": stage,
                "status": status,
                "opened_at": now,
                "updated_at": now,
                "closed_at": None,
                "transition_reason": reason,
            }
        )

    def _active_stage_entry(self, *, state: dict[str, Any], stage: str) -> dict[str, Any] | None:
        for entry in state.get("stage_history", []):
            if entry.get("stage") == stage and entry.get("closed_at") is None:
                return entry
        return None

    def _dispatch_state(
        self,
        *,
        task_id: str,
        task_class: str,
        current_stage: str,
        existing: dict[str, Any],
        human_decision_record: dict[str, Any] | None,
        pending_hitl_count: int,
        review_status: str,
        adversarial_review_status: str,
        convergence: dict[str, Any],
        settings: dict[str, Any],
        redesign_memory: dict[str, Any] | None,
    ) -> dict[str, Any]:
        candidates: list[dict[str, Any]] = []
        dispatch_record = ((existing.get("artifacts") or {}).get("dispatch_record")) or {}
        team_plan = ((existing.get("artifacts") or {}).get("team_plan")) or {}
        for item in (human_decision_record or {}).get("dispatch_recommendations", []):
            candidate = dict(item)
            candidate.setdefault("source", "human_decision_record")
            candidate.setdefault("auto_executable", candidate.get("action_label") == "spawn_program")
            candidates.append(candidate)
        if not candidates:
            candidate = self._policy_dispatch_candidate(
                task_class=task_class,
                current_stage=current_stage,
                human_decision_record=human_decision_record,
                redesign_memory=redesign_memory,
            )
            if candidate is not None:
                candidates.append(candidate)
        primary = candidates[0] if candidates else None
        operator_decision = self._normalize((human_decision_record or {}).get("operator_decision"))
        dispatch_mode = str(settings.get("dispatch_mode", "hook_only"))
        last_executed_instruction = ((existing.get("dispatch") or {}).get("last_executed") or {}).get("instruction")
        auto_execute_allowed = current_stage in AUTO_DISPATCH_ALLOWED.get(task_class, set())
        auto_execute_ready = bool(
            primary
            and dispatch_mode == "auto_execute"
            and auto_execute_allowed
            and primary.get("auto_executable")
            and operator_decision == f"{primary.get('action_label', '').upper()}:{str(primary.get('instruction', '')).upper()}"
            and primary.get("instruction") != last_executed_instruction
            and pending_hitl_count == 0
            and not review_status
            and not adversarial_review_status
            and not (convergence.get("enabled") and not convergence.get("satisfied"))
        )
        return {
            "dispatch_mode": dispatch_mode,
            "available": candidates,
            "primary": primary,
            "team_plan_ref": "docs/task_workspaces/{}/TEAM_PLAN.yaml".format(task_id) if team_plan else None,
            "dispatch_record_ref": "docs/task_workspaces/{}/TEAM_DISPATCH_RECORD.json".format(task_id) if dispatch_record else None,
            "last_executed": (existing.get("dispatch") or {}).get("last_executed"),
            "auto_execute_ready": auto_execute_ready,
            "auto_execute_allowed": auto_execute_allowed,
        }

    def _policy_dispatch_candidate(
        self,
        *,
        task_class: str,
        current_stage: str,
        human_decision_record: dict[str, Any] | None,
        redesign_memory: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        future_policy = future_exploration_for(task_class, current_stage)
        auto_execute_allowed = current_stage in AUTO_DISPATCH_ALLOWED.get(task_class, set())
        improvement_policy = improvement_trigger_policy_for(
            task_class,
            current_stage,
            human_decision_record=human_decision_record,
            redesign_memory=redesign_memory,
        )
        if future_policy is not None and (improvement_policy or {}).get("enabled"):
            future_policy["current_stage"] = current_stage
            future_policy["improvement_trigger_policy"] = improvement_policy
            future_policy["radical_trigger_policy"] = radical_redesign_policy_for(
                task_class,
                current_stage,
                human_decision_record=human_decision_record,
                redesign_memory=redesign_memory,
            )
            return {
                "source": "workflow_policy_engine",
                "action_label": "explore_futures",
                "instruction": f"future_swarm:{current_stage.lower()}",
                "spawn_id": f"future_swarm:{current_stage.lower()}",
                "program_title": future_policy.get("program_title", f"{current_stage.title()} Future Exploration"),
                "target_domain": current_stage.lower(),
                "program_goal": future_policy.get("program_goal"),
                "team_mode": future_policy.get("team_mode", "FUTURE_BRANCH_SWARM"),
                "dispatch_readiness": "READY",
                "approval_status": "POLICY_READY",
                "child_roles": [item["branch_id"] for item in future_policy.get("branches", [])],
                "future_exploration": future_policy,
                "auto_executable": auto_execute_allowed,
            }
        return {
            "source": "workflow_policy_engine",
            "action_label": "stage_team",
            "instruction": f"stage:{current_stage.lower()}",
            "spawn_id": f"stage:{current_stage.lower()}",
            "program_title": f"{current_stage.title()} Stage Team",
            "target_domain": current_stage.lower(),
            "program_goal": f"Run the bounded {current_stage.lower()} stage team and merge in the parent session.",
            "team_mode": "STAGE_TEAM",
            "dispatch_readiness": "READY",
            "approval_status": "POLICY_READY",
            "child_roles": stage_team_roles_for(task_class, current_stage),
            "auto_executable": auto_execute_allowed,
        }

    def _next_actions(
        self,
        *,
        task_id: str,
        current_stage: str,
        next_stage: str | None,
        lifecycle_status: str,
        review_status: str,
        adversarial_review_policy: dict[str, Any],
        adversarial_review_status: str,
        convergence: dict[str, Any],
        operator_decision: str,
        closeout_execution_record: dict[str, Any] | None,
        pending_hitl_count: int,
        dispatch: dict[str, Any],
        contract_report: dict[str, Any],
        settings: dict[str, Any],
    ) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []
        if convergence.get("required_before_stage_close") and not convergence.get("satisfied"):
            convergence_status = str(convergence.get("status") or "")
            if convergence_status == "PENDING_BRANCH_COMPLETION":
                actions.append(
                    {
                        "action": "continue_exploration",
                        "reason": "Future branches have not yet met the minimum coverage required for a convergence decision.",
                        "priority": "high",
                        "missing_branch_count": convergence.get("missing_branch_count", 0),
                    }
                )
            elif convergence_status == "CONTINUE_EXPLORATION":
                actions.append(
                    {
                        "action": "continue_exploration",
                        "reason": "The current convergence disposition requires another round of exploration before stage closure.",
                        "priority": "high",
                        "selected_disposition": convergence.get("selected_disposition"),
                    }
                )
            elif convergence.get("record_ref"):
                actions.append(
                    {
                        "action": "finalize_convergence_decision",
                        "reason": "Convergence is ready for parent disposition before the stage can close.",
                        "priority": "high",
                        "recommended_parent_action": convergence.get("recommended_parent_action"),
                        "decision_options": list(convergence.get("decision_options", [])),
                    }
                )
            else:
                actions.append(
                    {
                        "action": "start_convergence_decision",
                        "reason": "Convergence gating is required before the current stage can close.",
                        "priority": "high",
                        "recommended_parent_action": convergence.get("recommended_parent_action"),
                        "decision_options": list(convergence.get("decision_options", [])),
                    }
                )
        if adversarial_review_policy.get("required_before_stage_close"):
            if not adversarial_review_status:
                actions.append(
                    {
                        "action": "start_adversarial_review",
                        "reason": "This stage requires adversarial review before it can close.",
                        "priority": "high",
                        "review_role": adversarial_review_policy.get("review_role"),
                        "trigger_reasons": list(adversarial_review_policy.get("trigger_reasons", [])),
                    }
                )
            elif adversarial_review_status == "REVIEW_READY_FOR_OPERATOR":
                actions.append(
                    {
                        "action": "finalize_adversarial_review",
                        "reason": "Adversarial review output is available and needs operator disposition.",
                        "priority": "high",
                    }
                )
        if not contract_report.get("satisfied", False):
            actions.append(
                {
                    "action": "satisfy_stage_contract",
                    "reason": "The current stage is missing required artifacts or validator passes.",
                    "priority": "high",
                    "missing_requirements": list(contract_report.get("missing_requirements", [])),
                }
            )
        if lifecycle_status == "REVIEW_READY_FOR_OPERATOR":
            actions.append({"action": "finalize_review", "reason": "Review output is available and needs operator disposition.", "priority": "high"})
        if lifecycle_status == "AWAITING_HITL" and operator_decision in {"", "PENDING"}:
            actions.append({"action": "record_human_decision", "reason": "The current stage is waiting on operator guidance.", "priority": "high"})
        if lifecycle_status == "NEXT_STAGE_READY" and next_stage:
            actions.append({"action": "start_next_stage", "stage": next_stage, "reason": f"{current_stage} closed successfully and {next_stage} is ready to begin.", "priority": "high"})
        if lifecycle_status == "READY_FOR_CLOSEOUT" and not closeout_execution_record:
            actions.append({"action": "execute_closeout", "reason": "The final stage is approved and the task can close out.", "priority": "high"})
            if settings.get("auto_closeout"):
                actions.append({"action": "auto_closeout_ready", "reason": "Workflow policy allows controller-managed closeout execution.", "priority": "medium"})
        if lifecycle_status == "REVISION_REQUIRED":
            actions.append({"action": "start_task_turn", "reason": "Review requested changes for the current stage.", "priority": "high"})
        if pending_hitl_count:
            actions.append({"action": "resolve_hitl", "reason": "Pending HITL queue entries remain unresolved.", "priority": "medium"})
        if dispatch.get("primary"):
            actions.append(
                {
                    "action": "dispatch_team",
                    "reason": f"Dispatch candidate available for {current_stage}.",
                    "priority": "medium",
                    "instruction": dispatch["primary"].get("instruction"),
                    "auto_execute_ready": dispatch.get("auto_execute_ready", False),
                }
            )
        if not actions:
            actions.append({"action": "observe", "reason": "No immediate operator action is required.", "priority": "low"})
        return actions

    def _gate_state(
        self,
        *,
        review_status: str,
        adversarial_review_status: str,
        convergence: dict[str, Any],
        operator_decision: str,
        pending_hitl_count: int,
    ) -> str:
        if pending_hitl_count > 0:
            return "HITL_PENDING"
        if convergence.get("required_before_stage_close") and not convergence.get("satisfied"):
            return f"CONVERGENCE_{str(convergence.get('status') or 'PENDING')}"
        if adversarial_review_status in {"REVIEW_PENDING", "REVIEW_READY_FOR_OPERATOR", "REVIEW_FAILED"}:
            return f"ADVERSARIAL_{adversarial_review_status}"
        if review_status in {"REVIEW_PENDING", "REVIEW_READY_FOR_OPERATOR", "REVIEW_FAILED"}:
            return review_status
        if operator_decision in {"", "PENDING"}:
            return "DECISION_PENDING"
        return "CLEAR"

    def _convergence_state(
        self,
        *,
        task_id: str,
        task_class: str,
        current_stage: str,
        stage_opened_at: str,
        future_convergence_report: dict[str, Any] | None,
        task_improvement_report: dict[str, Any] | None,
        radical_redesign_report: dict[str, Any] | None,
        convergence_gate_record: dict[str, Any] | None,
        redesign_memory: dict[str, Any] | None,
    ) -> dict[str, Any]:
        base = convergence_policy_for(
            task_class,
            current_stage,
            future_convergence_report=future_convergence_report,
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            redesign_memory=redesign_memory,
        )
        if not base.get("enabled"):
            return {
                **base,
                "status": "NOT_REQUIRED",
                "ready_for_decision": False,
                "satisfied": True,
                "missing_branch_count": 0,
                "selected_disposition": None,
                "rationale": None,
                "record_ref": None,
            }
        record = convergence_gate_record or {}
        selected_disposition = self._normalize(record.get("selected_disposition"))
        completed_at = str(record.get("completed_at") or record.get("updated_at") or "")
        recorded_for_stage = (
            (str(record.get("current_stage") or "").upper() in {"", current_stage})
            and self._timestamp_at_or_after(completed_at, stage_opened_at)
        )
        ready_for_decision = base.get("completed_branch_count", 0) >= base.get("minimum_completed_branches", 0)
        missing_branch_count = max(0, int(base.get("minimum_completed_branches", 0)) - int(base.get("completed_branch_count", 0)))
        satisfied = bool(
            base.get("required_before_stage_close")
            and ready_for_decision
            and recorded_for_stage
            and selected_disposition in CONVERGENCE_DECISION_DISPOSITIONS
        )
        if not base.get("required_before_stage_close"):
            status = "NOT_REQUIRED"
        elif selected_disposition == "CONTINUE_EXPLORATION":
            status = "CONTINUE_EXPLORATION"
        elif satisfied:
            status = "DECIDED"
        elif not ready_for_decision:
            status = "PENDING_BRANCH_COMPLETION"
        elif record:
            status = "DRAFT"
        else:
            status = "READY_FOR_DECISION"
        return {
            **base,
            "task_id": task_id,
            "status": status,
            "ready_for_decision": ready_for_decision,
            "satisfied": satisfied,
            "missing_branch_count": missing_branch_count,
            "selected_disposition": selected_disposition or None,
            "rationale": record.get("rationale"),
            "record_ref": f"docs/task_workspaces/{task_id}/CONVERGENCE_GATE_RECORD.json" if convergence_gate_record else None,
        }

    def _normalize(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip().upper().replace(" ", "_")

    def _timestamp_at_or_after(self, lhs: str, rhs: str) -> bool:
        if not lhs or not rhs:
            return False
        return lhs >= rhs

    def _write(self, *, task_id: str, payload: dict[str, Any]) -> None:
        task_root = ensure_dir(self.root / task_id)
        write_json(task_root / "latest.json", payload)

    def _stage_team_roles(self, *, task_class: str, stage: str) -> list[str]:
        return stage_team_roles_for(task_class, stage)
