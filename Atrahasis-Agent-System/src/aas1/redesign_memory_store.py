from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from aas1.common import ensure_dir, keyword_profile, load_json, runtime_state_dir, utc_now, write_json


class RedesignMemoryStore:
    """Distilled cross-task memory for redesign, improvement, and convergence cycles."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.root = ensure_dir(runtime_state_dir(repo_root) / "redesign_memory")
        self.entries_root = ensure_dir(self.root / "entries")
        self.tasks_root = ensure_dir(self.root / "tasks")

    def ingest_task(
        self,
        *,
        task_id: str,
        workflow_context: dict[str, Any] | None = None,
        workflow_policy: dict[str, Any] | None = None,
        human_decision_record: dict[str, Any] | None = None,
        future_convergence_report: dict[str, Any] | None = None,
        task_improvement_report: dict[str, Any] | None = None,
        radical_redesign_report: dict[str, Any] | None = None,
        convergence_gate_record: dict[str, Any] | None = None,
        adversarial_review_record: dict[str, Any] | None = None,
        closeout_execution_record: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        if not any([future_convergence_report, task_improvement_report, radical_redesign_report]):
            return None
        task_profile = dict((workflow_policy or {}).get("task_profile") or {})
        task_class = str(task_profile.get("task_class") or self._task_class_from_context(workflow_context) or "ANALYSIS")
        task_title = str(task_profile.get("title") or self._task_title_from_context(workflow_context) or task_id)
        current_stage = str(
            (workflow_policy or {}).get("current_stage")
            or (task_improvement_report or {}).get("current_stage")
            or (radical_redesign_report or {}).get("current_stage")
            or (future_convergence_report or {}).get("current_stage")
            or "UNKNOWN"
        )
        workflow = (workflow_context or {}).get("workflow") or {}
        workflow_id = str(
            workflow.get("workflow_id")
            or (future_convergence_report or {}).get("workflow_id")
            or (task_improvement_report or {}).get("workflow_id")
            or (radical_redesign_report or {}).get("workflow_id")
            or ""
        )
        dispatch_id = str(
            (future_convergence_report or {}).get("dispatch_id")
            or (task_improvement_report or {}).get("dispatch_id")
            or (radical_redesign_report or {}).get("dispatch_id")
            or ""
        )
        memory_id = self._memory_id(
            task_id=task_id,
            workflow_id=workflow_id,
            current_stage=current_stage,
            dispatch_id=dispatch_id,
        )
        path = self.entries_root / f"{memory_id}.json"
        existing = load_json(path) if path.exists() else None

        trigger_reasons = self._trigger_reasons(
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
            adversarial_review_record=adversarial_review_record,
        )
        lane_ids = self._lane_ids(
            task_improvement_report=task_improvement_report,
            radical_redesign_report=radical_redesign_report,
        )
        summaries = {
            "improvement": str((task_improvement_report or {}).get("summary") or ""),
            "radical": str((radical_redesign_report or {}).get("summary") or ""),
            "convergence": str((future_convergence_report or {}).get("convergence_summary") or ""),
        }
        disagreement_signals = [
            str(item).strip()
            for item in (future_convergence_report or {}).get("disagreement_signals", [])
            if str(item).strip()
        ]
        query_text = self._query_text(
            task_id=task_id,
            task_title=task_title,
            task_class=task_class,
            current_stage=current_stage,
            workflow_context=workflow_context,
            human_decision_record=human_decision_record,
            summaries=summaries,
            trigger_reasons=trigger_reasons,
            disagreement_signals=disagreement_signals,
        )
        keywords = keyword_profile(
            [
                task_title,
                query_text,
                summaries["improvement"],
                summaries["radical"],
                summaries["convergence"],
                " ".join(trigger_reasons),
                " ".join(disagreement_signals),
            ],
            limit=18,
        )
        entry = {
            "type": "REDESIGN_MEMORY_ENTRY",
            "memory_id": memory_id,
            "task_id": task_id,
            "task_title": task_title,
            "task_class": task_class,
            "current_stage": current_stage,
            "workflow_id": workflow_id or None,
            "dispatch_id": dispatch_id or None,
            "trigger_reasons": trigger_reasons,
            "lane_ids": lane_ids,
            "recommended_parent_action": str(
                (task_improvement_report or {}).get("recommended_parent_action")
                or (future_convergence_report or {}).get("recommended_parent_action")
                or ""
            )
            or None,
            "selected_disposition": self._normalize((convergence_gate_record or {}).get("selected_disposition")) or None,
            "convergence_status": str((convergence_gate_record or {}).get("convergence_status") or "") or None,
            "adversarial_review_status": str((adversarial_review_record or {}).get("review_status") or "") or None,
            "workflow_status": str((closeout_execution_record or {}).get("workflow_status") or "") or None,
            "closeout_status": str((closeout_execution_record or {}).get("status") or "") or None,
            "final_outcome": self._final_outcome(
                convergence_gate_record=convergence_gate_record,
                closeout_execution_record=closeout_execution_record,
            ),
            "improvement_summary": summaries["improvement"] or None,
            "radical_summary": summaries["radical"] or None,
            "convergence_summary": summaries["convergence"] or None,
            "disagreement_signals": disagreement_signals,
            "keywords": keywords,
            "query_text": query_text,
            "source_refs": {
                "future_convergence_report": self._artifact_ref(task_id, "FUTURE_CONVERGENCE_REPORT.json", future_convergence_report),
                "task_improvement_report": self._artifact_ref(task_id, "TASK_IMPROVEMENT_REPORT.json", task_improvement_report),
                "radical_redesign_report": self._artifact_ref(task_id, "RADICAL_REDESIGN_REPORT.json", radical_redesign_report),
                "convergence_gate_record": self._artifact_ref(task_id, "CONVERGENCE_GATE_RECORD.json", convergence_gate_record),
                "adversarial_review_record": self._artifact_ref(task_id, "ADVERSARIAL_REVIEW_RECORD.json", adversarial_review_record),
                "closeout_execution_record": self._artifact_ref(task_id, "CLOSEOUT_EXECUTION_RECORD.json", closeout_execution_record),
            },
            "created_at": (existing or {}).get("created_at") or utc_now(),
            "updated_at": utc_now(),
        }
        changed = self._has_entry_changed(existing=existing, candidate=entry)
        if changed:
            write_json(path, entry)
            self._update_task_index(task_id=task_id, memory_id=memory_id, entry=entry)
            return {"entry": entry, "changed": True}
        return {"entry": existing, "changed": False}

    def load_latest(self, *, task_id: str) -> dict[str, Any] | None:
        path = self.tasks_root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def search(
        self,
        *,
        query: str,
        task_class: str | None = None,
        current_stage: str | None = None,
        limit: int = 10,
        exclude_memory_ids: set[str] | None = None,
    ) -> list[dict[str, Any]]:
        tokens = self._tokens(query)
        results = []
        excluded = exclude_memory_ids or set()
        for entry in self._all_entries():
            if entry.get("memory_id") in excluded:
                continue
            if task_class and str(entry.get("task_class")) != task_class:
                continue
            score = self._score_entry(
                entry,
                tokens=tokens,
                task_class=task_class,
                current_stage=current_stage,
            )
            if score <= 0:
                continue
            results.append({"score": round(score, 3), "entry": entry})
        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:limit]

    def snapshot_for_task(
        self,
        *,
        task_id: str,
        workflow_context: dict[str, Any] | None = None,
        workflow_policy: dict[str, Any] | None = None,
        human_decision_record: dict[str, Any] | None = None,
        limit_related: int = 5,
    ) -> dict[str, Any]:
        task_profile = dict((workflow_policy or {}).get("task_profile") or {})
        current_stage = str((workflow_policy or {}).get("current_stage") or task_profile.get("stage_track", ["UNKNOWN"])[0])
        task_class = str(task_profile.get("task_class") or self._task_class_from_context(workflow_context) or "ANALYSIS")
        task_title = str(task_profile.get("title") or self._task_title_from_context(workflow_context) or task_id)
        query_text = self._query_text(
            task_id=task_id,
            task_title=task_title,
            task_class=task_class,
            current_stage=current_stage,
            workflow_context=workflow_context,
            human_decision_record=human_decision_record,
            summaries={},
            trigger_reasons=[],
            disagreement_signals=[],
        )
        current_entry = self.load_latest(task_id=task_id)
        related = self.search(
            query=query_text,
            task_class=task_class,
            current_stage=current_stage,
            limit=limit_related + 2,
            exclude_memory_ids={str(current_entry.get("memory_id"))} if current_entry else None,
        )
        if not related:
            related = self.search(
                query=query_text,
                task_class=None,
                current_stage=current_stage,
                limit=limit_related + 2,
                exclude_memory_ids={str(current_entry.get("memory_id"))} if current_entry else None,
            )
        related_entries = []
        for item in related:
            entry = item["entry"]
            if str(entry.get("task_id")) == task_id and str(entry.get("memory_id")) == str((current_entry or {}).get("memory_id")):
                continue
            related_entries.append(self._brief_entry(entry, score=item["score"]))
            if len(related_entries) >= limit_related:
                break
        return {
            "task_id": task_id,
            "query_terms": keyword_profile([query_text], limit=10),
            "current_entry": self._brief_entry(current_entry) if current_entry else None,
            "related_entry_count": len(related_entries),
            "related_entries": related_entries,
        }

    def _update_task_index(self, *, task_id: str, memory_id: str, entry: dict[str, Any]) -> None:
        task_root = ensure_dir(self.tasks_root / task_id)
        index_path = task_root / "index.json"
        index = load_json(index_path) if index_path.exists() else {
            "type": "REDESIGN_MEMORY_TASK_INDEX",
            "task_id": task_id,
            "memory_ids": [],
            "created_at": utc_now(),
        }
        memory_ids = [str(item) for item in index.get("memory_ids", []) if str(item)]
        if memory_id not in memory_ids:
            memory_ids.append(memory_id)
        index["memory_ids"] = memory_ids[-50:]
        index["latest_memory_id"] = memory_id
        index["updated_at"] = utc_now()
        write_json(index_path, index)
        write_json(task_root / "latest.json", entry)

    def _all_entries(self) -> list[dict[str, Any]]:
        entries = []
        for path in sorted(self.entries_root.glob("*.json")):
            try:
                entries.append(load_json(path))
            except Exception:
                continue
        return entries

    def _has_entry_changed(self, *, existing: dict[str, Any] | None, candidate: dict[str, Any]) -> bool:
        if existing is None:
            return True
        current = dict(existing)
        proposed = dict(candidate)
        current.pop("updated_at", None)
        proposed.pop("updated_at", None)
        return current != proposed

    def _score_entry(
        self,
        entry: dict[str, Any],
        *,
        tokens: set[str],
        task_class: str | None,
        current_stage: str | None,
    ) -> float:
        if not tokens:
            return 0.0
        haystack = " ".join(
            [
                str(entry.get("task_title") or ""),
                str(entry.get("query_text") or ""),
                str(entry.get("improvement_summary") or ""),
                str(entry.get("radical_summary") or ""),
                str(entry.get("convergence_summary") or ""),
                " ".join(str(item) for item in entry.get("trigger_reasons", [])),
                " ".join(str(item) for item in entry.get("disagreement_signals", [])),
            ]
        ).lower()
        keywords = {str(item).lower() for item in entry.get("keywords", [])}
        score = 0.0
        for token in tokens:
            if token in keywords:
                score += 3.0
            score += float(haystack.count(token))
        if task_class and str(entry.get("task_class")) == task_class:
            score += 2.0
        if current_stage and str(entry.get("current_stage")) == current_stage:
            score += 1.0
        if entry.get("selected_disposition") in {"HYBRIDIZE", "ADOPT", "PROMOTE"}:
            score += 0.5
        return score

    def _brief_entry(self, entry: dict[str, Any] | None, *, score: float | None = None) -> dict[str, Any] | None:
        if not entry:
            return None
        payload = {
            "memory_id": entry.get("memory_id"),
            "task_id": entry.get("task_id"),
            "task_title": entry.get("task_title"),
            "task_class": entry.get("task_class"),
            "current_stage": entry.get("current_stage"),
            "recommended_parent_action": entry.get("recommended_parent_action"),
            "selected_disposition": entry.get("selected_disposition"),
            "final_outcome": entry.get("final_outcome"),
            "adversarial_review_status": entry.get("adversarial_review_status"),
            "summary": entry.get("improvement_summary")
            or entry.get("radical_summary")
            or entry.get("convergence_summary"),
            "trigger_reasons": list(entry.get("trigger_reasons", [])),
            "disagreement_signals": list(entry.get("disagreement_signals", []))[:6],
            "lane_ids": list(entry.get("lane_ids", [])),
            "keywords": list(entry.get("keywords", []))[:10],
            "updated_at": entry.get("updated_at"),
        }
        if score is not None:
            payload["score"] = score
        return payload

    def _query_text(
        self,
        *,
        task_id: str,
        task_title: str,
        task_class: str,
        current_stage: str,
        workflow_context: dict[str, Any] | None,
        human_decision_record: dict[str, Any] | None,
        summaries: dict[str, str],
        trigger_reasons: list[str],
        disagreement_signals: list[str],
    ) -> str:
        workflow = (workflow_context or {}).get("workflow") or {}
        request = workflow.get("request") or {}
        values = [
            task_id,
            task_title,
            task_class,
            current_stage,
            str(request.get("prompt") or ""),
            str(request.get("scope") or ""),
            str(request.get("command_modifier") or ""),
            str((human_decision_record or {}).get("research_strategy_summary") or ""),
            summaries.get("improvement", ""),
            summaries.get("radical", ""),
            summaries.get("convergence", ""),
            " ".join(trigger_reasons),
            " ".join(disagreement_signals),
        ]
        return " ".join(item for item in values if item).strip()

    def _trigger_reasons(
        self,
        *,
        task_improvement_report: dict[str, Any] | None,
        radical_redesign_report: dict[str, Any] | None,
        adversarial_review_record: dict[str, Any] | None,
    ) -> list[str]:
        values = []
        for item in (task_improvement_report or {}).get("trigger_policy", {}).get("trigger_reasons", []):
            text = str(item).strip()
            if text:
                values.append(text)
        for item in (radical_redesign_report or {}).get("trigger_policy", {}).get("trigger_reasons", []):
            text = str(item).strip()
            if text:
                values.append(text)
        for item in (adversarial_review_record or {}).get("adversarial_policy", {}).get("trigger_reasons", []):
            text = str(item).strip()
            if text:
                values.append(text)
        return self._dedupe(values)

    def _lane_ids(
        self,
        *,
        task_improvement_report: dict[str, Any] | None,
        radical_redesign_report: dict[str, Any] | None,
    ) -> list[str]:
        values = []
        for item in (task_improvement_report or {}).get("lane_summaries", []):
            lane_id = str(item.get("lane_id") or "").strip().lower()
            if lane_id:
                values.append(lane_id)
        for item in (radical_redesign_report or {}).get("radical_branch_summaries", []):
            lane_id = str(item.get("lane_id") or "").strip().lower()
            if lane_id:
                values.append(lane_id)
        return self._dedupe(values)

    def _memory_id(
        self,
        *,
        task_id: str,
        workflow_id: str,
        current_stage: str,
        dispatch_id: str,
    ) -> str:
        base = "::".join(
            [
                task_id.upper(),
                workflow_id or "workflow",
                current_stage.upper(),
                dispatch_id or "dispatch",
            ]
        )
        digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
        return f"{task_id.lower()}-{self._slug(current_stage)}-{digest}"

    def _artifact_ref(self, task_id: str, filename: str, payload: dict[str, Any] | None) -> str | None:
        if payload is None:
            return None
        return f"docs/task_workspaces/{task_id}/{filename}"

    def _final_outcome(
        self,
        *,
        convergence_gate_record: dict[str, Any] | None,
        closeout_execution_record: dict[str, Any] | None,
    ) -> str | None:
        disposition = self._normalize((convergence_gate_record or {}).get("selected_disposition"))
        if disposition == "CONTINUE_EXPLORATION":
            return "CONTINUED"
        if disposition in {"ADOPT", "HYBRIDIZE", "PROMOTE", "REJECT"}:
            return disposition
        closeout_status = self._normalize((closeout_execution_record or {}).get("workflow_status"))
        return closeout_status or None

    def _task_class_from_context(self, workflow_context: dict[str, Any] | None) -> str | None:
        workflow = (workflow_context or {}).get("workflow") or {}
        request = workflow.get("request") or {}
        modifier = str(request.get("command_modifier") or "").upper()
        scope = str(request.get("scope") or "").lower()
        if modifier == "AASNI":
            return "FULL_PIPELINE"
        if modifier in {"AASA", "AASAQ"} or "architecture" in scope:
            return "ANALYSIS"
        return None

    def _task_title_from_context(self, workflow_context: dict[str, Any] | None) -> str | None:
        workflow_record = (workflow_context or {}).get("workflow_record") or {}
        task_brief = (workflow_context or {}).get("operator_session") or {}
        return str(workflow_record.get("title") or task_brief.get("task_title") or "").strip() or None

    def _tokens(self, text: str) -> set[str]:
        return {
            item.lower()
            for item in keyword_profile([text], limit=24)
            if item
        }

    def _dedupe(self, values: list[str]) -> list[str]:
        result = []
        seen = set()
        for item in values:
            key = item.lower()
            if key in seen:
                continue
            seen.add(key)
            result.append(item)
        return result

    def _slug(self, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"

    def _normalize(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value).strip().upper().replace(" ", "_")
