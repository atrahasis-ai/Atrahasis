from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from aas1.audit_analytics import AuditAnalytics
from aas1.audit_timeline_store import AuditTimelineStore
from aas1.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json
from aas1.controller_run_registry import ControllerRunRegistry
from aas1.hitl_queue_store import HitlQueueStore
from aas1.notification_center import NotificationCenter
from aas1.redesign_memory_store import RedesignMemoryStore
from aas1.workflow_policy_engine import WorkflowPolicyEngine


RUN_FAILURE_STATUSES = {"FAILED", "TEAM_EXECUTION_FAILED", "CLOSEOUT_VALIDATION_FAILED"}
REVIEW_ATTENTION_STATUSES = {"REVIEW_BLOCKED", "REVIEW_CHANGES_REQUESTED"}
OBSERVER_MIN_STREAK = 2
WARNING_LOOKBACK_HOURS = 24
ACK_COOLDOWN_HOURS = 72


class ImprovementObserver:
    """Derives major AAS5 improvement advisories from durable controller state."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.index_path = ensure_dir(runtime_state_dir(repo_root) / "improvement_advisories") / "latest.json"
        self.analytics = AuditAnalytics(repo_root)
        self.timeline = AuditTimelineStore(repo_root)
        self.runs = ControllerRunRegistry(repo_root)
        self.hitl = HitlQueueStore(repo_root)
        self.notifications = NotificationCenter(repo_root)
        self.workflow_policy = WorkflowPolicyEngine(repo_root)
        self.redesign_memory = RedesignMemoryStore(repo_root)

    def load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            payload = {
                "type": "AAS5_IMPROVEMENT_ADVISORY_INDEX",
                "updated_at": utc_now(),
                "open_count": 0,
                "acknowledged_count": 0,
                "resolved_count": 0,
                "advisories": [],
            }
            write_json(self.index_path, payload)
            return payload
        return load_json(self.index_path)

    def list_advisories(
        self,
        *,
        open_only: bool = False,
        limit: int = 50,
        high_confidence_only: bool = False,
        include_observing: bool = False,
    ) -> list[dict[str, Any]]:
        payload = self.load()
        advisories = list(payload.get("advisories", []))
        if not include_observing:
            advisories = [item for item in advisories if str(item.get("status") or "").upper() != "OBSERVING"]
        if open_only:
            advisories = [item for item in advisories if str(item.get("status") or "").upper() == "OPEN"]
        if high_confidence_only:
            advisories = [item for item in advisories if str(item.get("confidence") or "").lower() == "high"]
        return advisories[:limit]

    def acknowledge(self, *, advisory_id: str) -> dict[str, Any]:
        payload = self.load()
        suppressed_until = self._future_hours(ACK_COOLDOWN_HOURS)
        for item in payload.get("advisories", []):
            if item.get("advisory_id") == advisory_id:
                item["status"] = "ACKNOWLEDGED"
                item["acknowledged_at"] = utc_now()
                item["suppressed_until"] = suppressed_until
                item["updated_at"] = utc_now()
                break
        self._write(payload)
        return payload

    def evaluate(self) -> dict[str, Any]:
        existing = self.load()
        existing_map = {str(item.get("advisory_id")): item for item in existing.get("advisories", [])}
        analytics = self.analytics.summary(limit_tasks=200)
        task_ids = sorted(self._task_ids(analytics))
        task_state = {task_id: self._task_state(task_id) for task_id in task_ids}
        redesign_entries = [entry for entry in self.redesign_memory._all_entries() if isinstance(entry, dict)]  # noqa: SLF001
        desired = []
        for builder in (
            self._controller_reliability_advisory,
            self._hitl_pressure_advisory,
            self._review_quality_advisory,
            self._convergence_tuning_advisory,
            self._stage_contract_hardening_advisory,
            self._salvage_fragment_advisory,
        ):
            advisory = builder(analytics=analytics, task_state=task_state, redesign_entries=redesign_entries)
            if advisory is not None:
                desired.append(advisory)

        advisories = self._merge(existing_map=existing_map, desired=desired)
        payload = {
            "type": "AAS5_IMPROVEMENT_ADVISORY_INDEX",
            "updated_at": utc_now(),
            "open_count": len([item for item in advisories if item.get("status") == "OPEN"]),
            "acknowledged_count": len([item for item in advisories if item.get("status") == "ACKNOWLEDGED"]),
            "resolved_count": len([item for item in advisories if item.get("status") == "RESOLVED"]),
            "advisories": advisories[:100],
        }
        changed = self._without_timestamp(existing) != self._without_timestamp(payload)
        if changed:
            self._write(payload)
            payload["changed"] = True
            return payload
        existing["changed"] = False
        return existing

    def _task_ids(self, analytics: dict[str, Any]) -> set[str]:
        task_ids = set(self.workflow_policy.list_task_ids())
        for card in analytics.get("task_cards", []):
            task_id = str(card.get("task_id") or "").upper()
            if task_id:
                task_ids.add(task_id)
        for run in self.runs.list_runs(limit=500):
            task_id = str(run.get("task_id") or "").upper()
            if task_id:
                task_ids.add(task_id)
        return task_ids

    def _task_state(self, task_id: str) -> dict[str, Any]:
        policy = self.workflow_policy.load(task_id) or {}
        run = self.runs.load_latest(task_id) or {}
        events = self.timeline.list_events(task_id=task_id, limit=100)
        warnings = [
            item
            for item in events
            if self._within_hours(item.get("timestamp"), WARNING_LOOKBACK_HOURS)
            if str(item.get("event_type") or "") == "controller_warning" or str(item.get("level") or "").upper() in {"ERROR", "WARNING"}
        ]
        stage_contract = dict(policy.get("stage_contract") or {})
        convergence = dict(policy.get("convergence") or {})
        adversarial_review = dict(policy.get("adversarial_review") or {})
        pending_hitl_count = int(policy.get("pending_hitl_count") or len(self.hitl.list_entries(task_id=task_id, include_resolved=False, limit=500)) or 0)
        return {
            "task_id": task_id,
            "policy": policy,
            "run": run,
            "warning_count": len(warnings),
            "warning_events": warnings,
            "pending_hitl_count": pending_hitl_count,
            "run_status": str(run.get("status") or policy.get("run_status") or ""),
            "review_status": str(policy.get("review_status") or ""),
            "adversarial_review_status": str(adversarial_review.get("status") or ""),
            "convergence_required": bool(convergence.get("required_before_stage_close")),
            "convergence_satisfied": bool(convergence.get("satisfied", False)),
            "convergence_status": str(convergence.get("status") or ""),
            "stage_contract_missing": list(stage_contract.get("missing_requirements", [])),
            "next_actions": list(policy.get("next_actions", [])),
        }

    def _controller_reliability_advisory(
        self,
        *,
        analytics: dict[str, Any],
        task_state: dict[str, dict[str, Any]],
        redesign_entries: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        failed_tasks = [
            task_id
            for task_id, item in task_state.items()
            if str(item.get("run_status") or "").upper() in RUN_FAILURE_STATUSES
        ]
        warning_tasks = [
            task_id
            for task_id, item in task_state.items()
            if int(item.get("warning_count") or 0) > 0
        ]
        warning_count = sum(int(item.get("warning_count") or 0) for item in task_state.values())
        if len(failed_tasks) < 2 and (warning_count < 6 or len(warning_tasks) < 2):
            return None
        confidence = "high" if len(failed_tasks) >= 2 or warning_count >= 8 else "medium"
        evidence = []
        if failed_tasks:
            evidence.append(f"Failure states were recorded for {len(failed_tasks)} task(s): {', '.join(failed_tasks[:4])}.")
        if warning_count:
            evidence.append(f"The audit timeline recorded {warning_count} controller warning/error event(s) across active tasks.")
        evidence.append(
            f"Repo-wide controller dashboard currently tracks {analytics.get('active_run_count', 0)} active run(s) and {analytics.get('terminal_run_count', 0)} terminal run(s)."
        )
        return self._advisory(
            advisory_id="aas5-update-controller-reliability",
            category="controller_reliability_hardening",
            confidence=confidence,
            headline="Controller reliability hardening is warranted.",
            summary="Recent failures or controller warnings indicate that the orchestration layer needs a focused hardening pass before more complexity is added.",
            recommended_change="Inspect the recurring failure path, add a targeted regression test, and simplify the unstable transition or closeout branch that keeps failing.",
            expected_benefit="Higher stability and fewer failed runs, reviews, or closeouts.",
            evidence=evidence,
            affected_task_ids=failed_tasks,
            supporting_metrics={"failed_task_count": len(failed_tasks), "warning_count": warning_count},
        )

    def _hitl_pressure_advisory(
        self,
        *,
        analytics: dict[str, Any],
        task_state: dict[str, dict[str, Any]],
        redesign_entries: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        pending_total = int(analytics.get("pending_hitl_count") or 0)
        congested_tasks = [
            task_id
            for task_id, item in task_state.items()
            if int(item.get("pending_hitl_count") or 0) >= 3
        ]
        if pending_total < 6 or len(congested_tasks) < 2:
            return None
        confidence = "high" if pending_total >= 8 else "medium"
        evidence = [
            f"There are {pending_total} unresolved controller-owned HITL item(s) repo-wide.",
        ]
        if congested_tasks:
            evidence.append(f"HITL pressure is concentrated in: {', '.join(congested_tasks[:5])}.")
        return self._advisory(
            advisory_id="aas5-update-hitl-pressure",
            category="hitl_queue_compaction",
            confidence=confidence,
            headline="HITL queue pressure is high enough to justify workflow compaction.",
            summary="Too many controller-owned approvals are being surfaced at once, which slows task throughput and raises operator overhead.",
            recommended_change="Bundle low-risk approvals, auto-resolve purely informational controller entries, and collapse duplicate stage-transition prompts into one operator action.",
            expected_benefit="Faster throughput with less operator interruption.",
            evidence=evidence,
            affected_task_ids=congested_tasks,
            supporting_metrics={"pending_hitl_count": pending_total, "congested_task_count": len(congested_tasks)},
        )

    def _review_quality_advisory(
        self,
        *,
        analytics: dict[str, Any],
        task_state: dict[str, dict[str, Any]],
        redesign_entries: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        pressured_tasks = []
        for task_id, item in task_state.items():
            review_status = str(item.get("review_status") or "").upper()
            adversarial_status = str(item.get("adversarial_review_status") or "").upper()
            if review_status in REVIEW_ATTENTION_STATUSES or adversarial_status in REVIEW_ATTENTION_STATUSES:
                pressured_tasks.append(task_id)
        if len(pressured_tasks) < 3:
            return None
        evidence = [f"Review or adversarial-review gates are blocked or requesting changes for {len(pressured_tasks)} task(s)."]
        evidence.append(f"Affected tasks: {', '.join(pressured_tasks[:5])}.")
        return self._advisory(
            advisory_id="aas5-update-review-quality",
            category="review_policy_tightening",
            confidence="medium",
            headline="Review quality pressure suggests earlier gate tightening.",
            summary="Multiple tasks are failing or reopening at review, which usually means earlier stage contracts or review templates are still too loose.",
            recommended_change="Push the relevant checks earlier by tightening stage contracts, strengthening review templates, or auto-running the stricter review role sooner.",
            expected_benefit="Higher accuracy and fewer late-stage rewrites.",
            evidence=evidence,
            affected_task_ids=pressured_tasks,
            supporting_metrics={"review_attention_task_count": len(pressured_tasks)},
        )

    def _convergence_tuning_advisory(
        self,
        *,
        analytics: dict[str, Any],
        task_state: dict[str, dict[str, Any]],
        redesign_entries: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        converging_tasks = []
        continue_exploration_tasks = []
        for task_id, item in task_state.items():
            if not item.get("convergence_required"):
                continue
            if not item.get("convergence_satisfied"):
                converging_tasks.append(task_id)
            if str(item.get("convergence_status") or "").upper() == "CONTINUE_EXPLORATION":
                continue_exploration_tasks.append(task_id)
        if len(converging_tasks) < 2 or not continue_exploration_tasks:
            return None
        evidence = [f"Convergence is unresolved for {len(converging_tasks)} task(s)."]
        if continue_exploration_tasks:
            evidence.append(f"Continue-exploration dispositions are still active in: {', '.join(continue_exploration_tasks[:4])}.")
        return self._advisory(
            advisory_id="aas5-update-convergence-tuning",
            category="convergence_policy_tuning",
            confidence="medium",
            headline="Convergence policy looks loose enough to warrant tuning.",
            summary="Branch-heavy work is lingering in unresolved convergence states, which suggests the branch budget or stop rules are not yet tight enough.",
            recommended_change="Tighten branch budgets, raise the minimum branch-completion contract only when justified, and shorten the path from branch output to parent disposition.",
            expected_benefit="Faster convergence without losing the best alternatives.",
            evidence=evidence,
            affected_task_ids=sorted(set(converging_tasks + continue_exploration_tasks)),
            supporting_metrics={
                "convergence_pending_task_count": len(converging_tasks),
                "continue_exploration_task_count": len(continue_exploration_tasks),
            },
        )

    def _stage_contract_hardening_advisory(
        self,
        *,
        analytics: dict[str, Any],
        task_state: dict[str, dict[str, Any]],
        redesign_entries: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        task_missing = {
            task_id: list(item.get("stage_contract_missing") or [])
            for task_id, item in task_state.items()
            if len(item.get("stage_contract_missing") or []) >= 3
        }
        if len(task_missing) < 3:
            return None
        evidence = [
            f"Stage-contract requirements are materially missing in {len(task_missing)} task(s).",
        ]
        for task_id, missing in list(task_missing.items())[:3]:
            evidence.append(f"{task_id}: {', '.join(str(item) for item in missing[:4])}.")
        return self._advisory(
            advisory_id="aas5-update-stage-contracts",
            category="stage_contract_hardening",
            confidence="medium",
            headline="Stage contracts need hardening or better artifact automation.",
            summary="Repeated missing requirements indicate that the controller still allows too much drift between stage policy and the artifacts actually produced.",
            recommended_change="Either auto-generate the missing control artifacts earlier or tighten the stage-specific prompts and validators so the required files appear by default.",
            expected_benefit="More reliable advancement and fewer stage-close surprises.",
            evidence=evidence,
            affected_task_ids=sorted(task_missing.keys()),
            supporting_metrics={"contract_pressure_task_count": len(task_missing)},
        )

    def _salvage_fragment_advisory(
        self,
        *,
        analytics: dict[str, Any],
        task_state: dict[str, dict[str, Any]],
        redesign_entries: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        salvage_candidates = [
            entry
            for entry in redesign_entries
            if str(entry.get("final_outcome") or "").upper() in {"REJECT", "CONTINUED"}
            and str(entry.get("selected_disposition") or "").upper() in {"REJECT", "CONTINUE_EXPLORATION", "HYBRIDIZE"}
        ]
        if len(salvage_candidates) < 8:
            return None
        task_ids = sorted({str(entry.get("task_id") or "").upper() for entry in salvage_candidates if entry.get("task_id")})
        evidence = [
            f"The redesign-memory layer now holds {len(salvage_candidates)} rejected or still-continued redesign cycles that may contain reusable sub-mechanisms.",
            "A dedicated salvage-fragment layer does not exist yet, so reusable subcomponents are still buried in broader redesign records.",
        ]
        return self._advisory(
            advisory_id="aas5-update-salvage-fragments",
            category="salvage_fragment_library",
            confidence="medium",
            headline="Redesign salvage fragments are now worth extracting explicitly.",
            summary="Rejected or partial redesign cycles are accumulating enough useful structure that AAS5 would benefit from a dedicated salvage-fragment layer instead of relying only on broad memory reuse.",
            recommended_change="Distill reusable mechanisms from rejected or partial redesigns into small salvage records that can be offered as advisory considerations on future tasks.",
            expected_benefit="More creativity from prior failed work without forcing whole old designs back into new tasks.",
            evidence=evidence,
            affected_task_ids=task_ids,
            supporting_metrics={"salvage_candidate_count": len(salvage_candidates)},
        )

    def _merge(self, *, existing_map: dict[str, dict[str, Any]], desired: list[dict[str, Any]]) -> list[dict[str, Any]]:
        now = utc_now()
        merged = []
        desired_ids = {item["advisory_id"] for item in desired}
        for advisory in desired:
            current = existing_map.get(advisory["advisory_id"])
            streak = 1
            if current and bool(current.get("candidate_active")):
                streak = int(current.get("candidate_streak") or 0) + 1
            advisory["candidate_active"] = True
            advisory["candidate_streak"] = streak
            if current:
                advisory["created_at"] = current.get("created_at") or now
                if current.get("acknowledged_at"):
                    advisory["acknowledged_at"] = current["acknowledged_at"]
                if current.get("suppressed_until"):
                    advisory["suppressed_until"] = current["suppressed_until"]
            else:
                advisory["created_at"] = now
            prior_status = str((current or {}).get("status") or "").upper()
            cooldown_active = self._timestamp_in_future(advisory.get("suppressed_until"))
            if prior_status == "OPEN":
                advisory["status"] = "OPEN"
            elif prior_status == "ACKNOWLEDGED":
                advisory["status"] = "ACKNOWLEDGED"
            elif cooldown_active and prior_status in {"ACKNOWLEDGED", "RESOLVED"}:
                advisory["status"] = "ACKNOWLEDGED"
            elif streak >= OBSERVER_MIN_STREAK:
                advisory["status"] = "OPEN"
            else:
                advisory["status"] = "OBSERVING"
            advisory["updated_at"] = now
            merged.append(advisory)
        for advisory_id, current in existing_map.items():
            if advisory_id in desired_ids:
                continue
            resolved = dict(current)
            resolved["candidate_active"] = False
            resolved["candidate_streak"] = 0
            if resolved.get("status") != "RESOLVED":
                resolved["status"] = "RESOLVED"
                resolved["updated_at"] = now
            merged.append(resolved)
        merged.sort(
            key=lambda item: (
                self._status_rank(item.get("status")),
                1 if str(item.get("confidence") or "").lower() == "high" else 0,
                item.get("updated_at", ""),
            ),
            reverse=True,
        )
        return merged

    def _advisory(
        self,
        *,
        advisory_id: str,
        category: str,
        confidence: str,
        headline: str,
        summary: str,
        recommended_change: str,
        expected_benefit: str,
        evidence: list[str],
        affected_task_ids: list[str],
        supporting_metrics: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "type": "AAS5_IMPROVEMENT_ADVISORY",
            "advisory_id": advisory_id,
            "category": category,
            "severity": "major",
            "confidence": confidence,
            "headline": headline,
            "summary": summary,
            "recommended_change": recommended_change,
            "expected_benefit": expected_benefit,
            "evidence": evidence,
            "affected_task_ids": affected_task_ids,
            "supporting_metrics": supporting_metrics,
        }

    def _status_rank(self, status: Any) -> int:
        value = str(status or "").upper()
        if value == "OPEN":
            return 4
        if value == "ACKNOWLEDGED":
            return 3
        if value == "OBSERVING":
            return 2
        if value == "RESOLVED":
            return 1
        return 0

    def _without_timestamp(self, payload: dict[str, Any]) -> dict[str, Any]:
        candidate = dict(payload)
        candidate.pop("updated_at", None)
        candidate.pop("changed", None)
        return candidate

    def _write(self, payload: dict[str, Any]) -> None:
        write_json(self.index_path, payload)

    def _within_hours(self, timestamp: Any, hours: int) -> bool:
        dt = self._parse_timestamp(timestamp)
        if dt is None:
            return False
        return dt >= datetime.now(timezone.utc) - timedelta(hours=hours)

    def _timestamp_in_future(self, timestamp: Any) -> bool:
        dt = self._parse_timestamp(timestamp)
        if dt is None:
            return False
        return dt > datetime.now(timezone.utc)

    def _future_hours(self, hours: int) -> str:
        return (datetime.now(timezone.utc) + timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _parse_timestamp(self, value: Any) -> datetime | None:
        if not value:
            return None
        text = str(value).strip()
        if not text:
            return None
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc)
        except ValueError:
            return None
