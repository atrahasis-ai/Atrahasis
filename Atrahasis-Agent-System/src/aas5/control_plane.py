from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from aas5.audit_timeline_store import AuditTimelineStore
from aas5.artifact_registry import ArtifactRegistry
from aas5.common import keyword_profile, load_json, load_yaml, summarize_text, utc_now, write_text
from aas5.gcml_memory_interface import GCMLMemoryInterface
from aas5.provider_runtime import ProviderRuntimeRegistry
from aas5.redesign_memory_store import RedesignMemoryStore
from aas5.spec_path_resolver import resolve_spec_path, resolve_spec_ref
from aas5.task_hardening import parse_todo_dispatch_state
from aas5.task_claim_coordinator import TaskClaimCoordinator
from aas5.workflow_policy_engine import WorkflowPolicyEngine
from aas5.workflow_context_store import WorkflowContextStore


class AtrahasisControlPlane:
    """Read-mostly control-plane accessors for MCP and repo tooling."""

    ADR_HEADING_RE = re.compile(r"^## (ADR-\d+)\s+—\s+(.+)$", re.MULTILINE)
    TASK_ROW_RE = re.compile(r"^\|\s*`?(T-[A-Z0-9-]+)`?\s*\|", re.IGNORECASE)

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.docs_root = repo_root / "docs"
        self.memory = GCMLMemoryInterface(repo_root)
        self.registry = ArtifactRegistry(repo_root)
        self.provider_runtime = ProviderRuntimeRegistry(repo_root)
        self.workflow_context = WorkflowContextStore(repo_root)
        self.task_claims = TaskClaimCoordinator(repo_root)
        self.workflow_policy = WorkflowPolicyEngine(repo_root)
        self.audit_timeline = AuditTimelineStore(repo_root)
        self.redesign_memory = RedesignMemoryStore(repo_root)

    def get_session_brief(self) -> dict[str, Any]:
        path = self.docs_root / "SESSION_BRIEF.md"
        text = path.read_text(encoding="utf-8")
        return {
            "path": "docs/SESSION_BRIEF.md",
            "summary": summarize_text(text),
            "next_dispatchable_canonical_task": self._extract_next_dispatchable_task(),
            "text": text,
        }

    def get_dispatchable_tasks(self, *, limit: int = 5) -> dict[str, Any]:
        todo_path = self.docs_root / "TODO.md"
        text = todo_path.read_text(encoding="utf-8")
        dispatch_state = parse_todo_dispatch_state(text)
        task_rows = dispatch_state["task_rows"]
        next_dispatchable = dispatch_state["next_dispatchable"] or {}
        primary_ids = list(next_dispatchable.get("task_ids") or [])
        if not primary_ids:
            primary_ids = list(dispatch_state["user_dispatch_order"])
        tasks = [task_rows[task_id] for task_id in primary_ids if task_id in task_rows][:limit]
        return {
            "path": "docs/TODO.md",
            "next_dispatchable_canonical_task": self._extract_next_dispatchable_task(text),
            "next_dispatchable": next_dispatchable,
            "user_dispatch_order": dispatch_state["user_dispatch_order"][:limit],
            "user_dispatch_entries": dispatch_state["user_dispatch_entries"][:limit],
            "tasks": tasks,
        }

    def get_task_claims(self, *, active_only: bool = True) -> dict[str, Any]:
        results = []
        for path in sorted((self.docs_root / "task_claims").glob("*.yaml")):
            if path.name == "CLAIM_TEMPLATE.yaml":
                continue
            payload = load_yaml(path)
            if not isinstance(payload, dict):
                continue
            if active_only and payload.get("status") not in TaskClaimCoordinator.ACTIVE_STATUSES:
                continue
            results.append(payload)
        return {
            "path": "docs/task_claims/",
            "active_only": active_only,
            "claim_count": len(results),
            "claims": results,
        }

    def get_task_workspace_manifest(
        self,
        *,
        task_id: str,
        include_text: bool = False,
        limit: int = 100,
    ) -> dict[str, Any]:
        documents = self.memory.load_task_workspace(task_id)
        normalized = [self._trim_document(item, include_text=include_text) for item in documents[:limit]]
        return {
            "task_id": task_id,
            "workspace_exists": bool(documents),
            "document_count": len(documents),
            "documents": normalized,
        }

    def get_decisions(
        self,
        *,
        keyword: str | None = None,
        limit: int = 5,
        include_text: bool = False,
    ) -> dict[str, Any]:
        path = self.docs_root / "DECISIONS.md"
        text = path.read_text(encoding="utf-8")
        entries = self._parse_decisions(text)
        ranked = self._rank_decisions(entries, keyword=keyword)[:limit]
        if not include_text:
            for item in ranked:
                item.pop("text", None)
        return {
            "path": "docs/DECISIONS.md",
            "keyword": keyword,
            "decision_count": len(entries),
            "matches": ranked,
        }

    def get_spec(self, *, spec_id: str, include_text: bool = True) -> dict[str, Any]:
        path = resolve_spec_path(self.repo_root, spec_id)
        text = path.read_text(encoding="utf-8")
        payload = {
            "spec_id": spec_id,
            "path": str(path.relative_to(self.repo_root)).replace("\\", "/"),
            "summary": summarize_text(text),
        }
        if include_text:
            payload["text"] = text
        return payload

    def resolve_spec_path(self, *, spec_id: str) -> dict[str, Any]:
        path = resolve_spec_path(self.repo_root, spec_id)
        return {
            "spec_id": spec_id,
            "path": resolve_spec_ref(self.repo_root, spec_id),
            "exists": path.exists(),
        }

    def get_latest_workflow_context(self, *, task_id: str) -> dict[str, Any]:
        workflow = self.workflow_context.load_latest(task_id)
        task_root = self.docs_root / "task_workspaces" / task_id
        workflow_record = load_json(task_root / "WORKFLOW_RUN_RECORD.json") if (task_root / "WORKFLOW_RUN_RECORD.json").exists() else None
        team_plan = load_yaml(task_root / "TEAM_PLAN.yaml") if (task_root / "TEAM_PLAN.yaml").exists() else None
        dispatch_record = load_json(task_root / "TEAM_DISPATCH_RECORD.json") if (task_root / "TEAM_DISPATCH_RECORD.json").exists() else None
        human_decision_record = load_json(task_root / "HUMAN_DECISION_RECORD.json") if (task_root / "HUMAN_DECISION_RECORD.json").exists() else None
        exploration_control_record = (
            load_json(task_root / "EXPLORATION_CONTROL_RECORD.json")
            if (task_root / "EXPLORATION_CONTROL_RECORD.json").exists()
            else None
        )
        return {
            "task_id": task_id,
            "workflow": workflow,
            "workflow_record": workflow_record,
            "team_plan": team_plan,
            "dispatch_record": dispatch_record,
            "human_decision_record": human_decision_record,
            "exploration_control_record": exploration_control_record,
        }

    def get_active_provider_sessions(self) -> dict[str, Any]:
        sessions = self.provider_runtime.list_active_sessions()
        return {
            "session_count": len(sessions),
            "sessions": sessions,
        }

    def get_workflow_policy(self, *, task_id: str) -> dict[str, Any] | None:
        return self.workflow_policy.load(task_id)

    def get_audit_timeline(self, *, task_id: str, after_id: int = 0, limit: int = 200) -> dict[str, Any]:
        events = self.audit_timeline.list_events(task_id=task_id, after_id=after_id, limit=limit)
        return {
            "task_id": task_id,
            "event_count": len(events),
            "events": events,
        }

    def get_redesign_memory(
        self,
        *,
        task_id: str,
        limit_related: int = 5,
    ) -> dict[str, Any]:
        workflow_context = self.get_latest_workflow_context(task_id=task_id)
        workflow_policy = self.workflow_policy.load(task_id)
        human_decision_record = (
            load_json(self.docs_root / "task_workspaces" / task_id / "HUMAN_DECISION_RECORD.json")
            if (self.docs_root / "task_workspaces" / task_id / "HUMAN_DECISION_RECORD.json").exists()
            else None
        )
        snapshot = self.redesign_memory.snapshot_for_task(
            task_id=task_id,
            workflow_context=workflow_context,
            workflow_policy=workflow_policy,
            human_decision_record=human_decision_record,
            limit_related=limit_related,
        )
        return {
            "task_id": task_id,
            "workflow_context": workflow_context,
            "workflow_policy": workflow_policy,
            "redesign_memory": snapshot,
        }

    def search_redesign_memory(
        self,
        *,
        query: str,
        task_class: str | None = None,
        current_stage: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        matches = self.redesign_memory.search(
            query=query,
            task_class=task_class,
            current_stage=current_stage,
            limit=limit,
        )
        return {
            "query": query,
            "task_class": task_class,
            "current_stage": current_stage,
            "match_count": len(matches),
            "matches": matches,
        }

    def search_canonical_artifacts(
        self,
        *,
        query: str,
        limit: int = 10,
        category: str | None = None,
    ) -> dict[str, Any]:
        manifest = self.memory.collect_repo_manifest()
        tokens = self._tokens(query)
        matches = []
        for item in manifest:
            if category and item.get("category") != category:
                continue
            score = self._score_manifest_entry(item, tokens)
            if score <= 0:
                continue
            matches.append(
                {
                    "path": item["path"],
                    "category": item["category"],
                    "summary": item["summary"],
                    "invention_ids": item.get("invention_ids", []),
                    "task_ids": item.get("task_ids", []),
                    "score": round(score, 3),
                }
            )
        matches.sort(key=lambda item: item["score"], reverse=True)
        return {
            "query": query,
            "category": category,
            "match_count": len(matches),
            "matches": matches[:limit],
        }

    def validate_artifact(self, *, schema_name: str, artifact_path: str) -> dict[str, Any]:
        path = self._resolve_repo_path(artifact_path)
        payload = self._load_artifact_payload(path)
        schema = self.registry.schema(schema_name)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
        return {
            "schema_name": schema_name,
            "artifact_path": str(path.relative_to(self.repo_root)).replace("\\", "/"),
            "valid": not errors,
            "error_count": len(errors),
            "errors": [
                {
                    "path": ".".join(str(part) for part in err.path) or "<root>",
                    "message": err.message,
                }
                for err in errors
            ],
        }

    def get_task_status(self, *, task_id: str) -> dict[str, Any]:
        workflow_context = self.get_latest_workflow_context(task_id=task_id)
        workspace = self.get_task_workspace_manifest(task_id=task_id, include_text=False, limit=200)
        return {
            "task_id": task_id,
            "workspace_exists": workspace["workspace_exists"],
            "workspace_document_count": workspace["document_count"],
            "latest_workflow_status": (workflow_context.get("workflow") or {}).get("status"),
            "human_review_status": (workflow_context.get("human_decision_record") or {}).get("workflow_status"),
            "team_plan_status": (workflow_context.get("team_plan") or {}).get("status"),
            "dispatch_record_status": (workflow_context.get("dispatch_record") or {}).get("status"),
            "artifact_refs": ((workflow_context.get("workflow_record") or {}).get("artifacts") or {}),
        }

    def create_claim(
        self,
        *,
        task_id: str,
        title: str | None = None,
        platform: str = "CODEX",
        agent_name: str,
        safe_zone_paths: list[str] | None = None,
        pipeline_type: str = "AAS",
        invention_ids: list[str] | None = None,
        target_specs: list[str] | None = None,
        notes: str = "",
        status: str = "CLAIMED",
    ) -> dict[str, Any]:
        resolved_title = title or self._title_for_task(task_id) or f"{task_id} task claim"
        safe_zones = safe_zone_paths or [f"docs/task_workspaces/{task_id}/"]
        payload = self.task_claims.claim_task(
            task_id=task_id,
            title=resolved_title,
            platform=platform,
            agent_name=agent_name,
            safe_zone_paths=safe_zones,
            pipeline_type=pipeline_type,
            invention_ids=invention_ids,
            target_specs=target_specs,
            notes=notes,
            status=status,
        )
        return {
            "task_id": task_id,
            "claim_path": f"docs/task_claims/{task_id}.yaml",
            "claim": payload,
        }

    def write_handoff(
        self,
        *,
        task_id: str,
        title: str,
        platform: str,
        pipeline_verdict: str,
        notes: str = "",
        artifacts: list[dict[str, str]] | None = None,
        applied: bool = False,
    ) -> dict[str, Any]:
        root = self.docs_root / "handoffs"
        if applied:
            root = root / "applied"
        path = root / f"{task_id}_{platform.strip().upper()}_HANDOFF.md"
        artifact_rows = artifacts or []
        lines = [
            f"# Task Handoff: {task_id} — {title}",
            f"**Platform:** {platform.strip().upper()}",
            f"**Completed:** {utc_now()}",
            f"**Pipeline verdict:** {pipeline_verdict}",
            "",
            "---",
            "",
            "## Invention Artifacts Created",
            "",
            "| Path | Description |",
            "|------|-------------|",
        ]
        if artifact_rows:
            for item in artifact_rows:
                lines.append(f"| `{item.get('path', '')}` | {item.get('description', '')} |")
        else:
            lines.append("| _none_ | No canonical artifacts recorded. |")
        lines.extend(
            [
                "",
                "---",
                "",
                "## Notes",
                notes or "No additional notes.",
            ]
        )
        write_text(path, "\n".join(lines))
        return {
            "task_id": task_id,
            "handoff_path": str(path.relative_to(self.repo_root)).replace("\\", "/"),
            "applied": applied,
        }

    def record_human_decision(
        self,
        *,
        task_id: str,
        operator_decision: str,
        workflow_status: str | None = None,
        constraints: list[str] | None = None,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        task_root = self.registry.task_root(task_id)
        human_path = task_root / "HUMAN_DECISION_RECORD.json"
        if not human_path.exists():
            raise FileNotFoundError(f"Human decision record not found for {task_id}: {human_path}")
        human_record = load_json(human_path)
        resolved_status = workflow_status or human_record.get("workflow_status", "PENDING_HUMAN_REVIEW")
        human_record["operator_decision"] = operator_decision
        human_record["workflow_status"] = resolved_status
        human_record["decision_recorded_at"] = utc_now()
        if constraints is not None:
            human_record["constraints"] = constraints
        if notes:
            human_record["decision_notes"] = notes
        self.registry.write_json_artifact(task_id, "HUMAN_DECISION_RECORD.json", human_record, schema_name="human_decision_record")

        workflow_path = task_root / "WORKFLOW_RUN_RECORD.json"
        workflow_record = None
        if workflow_path.exists():
            workflow_record = load_json(workflow_path)
            workflow_record["status"] = resolved_status
            workflow_record.setdefault("artifacts", {})["human_decision_record"] = f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json"
            self.registry.write_json_artifact(task_id, "WORKFLOW_RUN_RECORD.json", workflow_record, schema_name="workflow_run_record")
        latest_workflow = self.workflow_context.load_latest(task_id)
        if latest_workflow and latest_workflow.get("workflow_id"):
            self.workflow_context.update_status(
                task_id=task_id,
                workflow_id=latest_workflow["workflow_id"],
                status=resolved_status,
                artifact_updates={"human_decision_record": f"docs/task_workspaces/{task_id}/HUMAN_DECISION_RECORD.json"},
            )
        return {
            "task_id": task_id,
            "workflow_status": resolved_status,
            "human_decision_record": human_record,
            "workflow_run_record": workflow_record,
        }

    def _extract_next_dispatchable_task(self, todo_text: str | None = None) -> str | None:
        text = todo_text or (self.docs_root / "TODO.md").read_text(encoding="utf-8")
        dispatch_state = parse_todo_dispatch_state(text)
        next_dispatchable = dispatch_state["next_dispatchable"] or {}
        task_ids = list(next_dispatchable.get("task_ids") or [])
        return task_ids[0] if task_ids else None

    def _extract_user_dispatch_order(self, todo_text: str) -> list[str]:
        dispatch_state = parse_todo_dispatch_state(todo_text)
        return list(dispatch_state["user_dispatch_order"])

    def _parse_task_rows(self, todo_text: str) -> dict[str, dict[str, Any]]:
        rows: dict[str, dict[str, Any]] = {}
        for line in todo_text.splitlines():
            if not self.TASK_ROW_RE.match(line.strip()):
                continue
            parts = [part.strip().strip("`") for part in line.strip().strip("|").split("|")]
            if len(parts) < 2:
                continue
            rows[parts[0]] = {
                "task_id": parts[0],
                "title": parts[1] if len(parts) > 1 else "",
                "type": parts[2] if len(parts) > 2 else "",
                "priority": parts[3] if len(parts) > 3 else "",
                "dependencies": parts[4] if len(parts) > 4 else "",
                "notes": parts[5] if len(parts) > 5 else "",
            }
        return rows

    def _parse_decisions(self, text: str) -> list[dict[str, Any]]:
        matches = list(self.ADR_HEADING_RE.finditer(text))
        entries: list[dict[str, Any]] = []
        for index, match in enumerate(matches):
            start = match.start()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            block = text[start:end].strip()
            status_match = re.search(r"\*\*Status:\*\*\s*(.+)", block)
            entries.append(
                {
                    "adr_id": match.group(1),
                    "title": match.group(2).strip(),
                    "status": status_match.group(1).strip() if status_match else None,
                    "summary": summarize_text(block),
                    "text": block,
                }
            )
        return entries

    def _rank_decisions(self, entries: list[dict[str, Any]], *, keyword: str | None) -> list[dict[str, Any]]:
        if not keyword:
            return entries
        tokens = self._tokens(keyword)
        ranked = []
        for item in entries:
            haystack = f"{item['adr_id']} {item['title']} {item['text']}".lower()
            score = sum(haystack.count(token) for token in tokens)
            if score > 0:
                ranked.append({**item, "score": score})
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked

    def _score_manifest_entry(self, item: dict[str, Any], tokens: set[str]) -> float:
        haystack = " ".join(
            [
                item.get("path", ""),
                item.get("summary", ""),
                " ".join(item.get("invention_ids", [])),
                " ".join(item.get("task_ids", [])),
                item.get("text", ""),
            ]
        ).lower()
        if not tokens:
            return 0.0
        overlap = 0.0
        for token in tokens:
            if token in item.get("path", "").lower():
                overlap += 2.0
            overlap += haystack.count(token)
        return overlap

    def _tokens(self, text: str) -> set[str]:
        return set(keyword_profile([text], limit=24))

    def _resolve_repo_path(self, artifact_path: str) -> Path:
        candidate = Path(artifact_path)
        resolved = candidate if candidate.is_absolute() else (self.repo_root / candidate)
        resolved = resolved.resolve()
        if not resolved.is_relative_to(self.repo_root):
            raise ValueError(f"Artifact path must stay inside the repo: {artifact_path}")
        if not resolved.exists():
            raise FileNotFoundError(f"Artifact not found: {resolved}")
        return resolved

    def _title_for_task(self, task_id: str) -> str | None:
        todo_path = self.docs_root / "TODO.md"
        if not todo_path.exists():
            return None
        text = todo_path.read_text(encoding="utf-8")
        rows = self._parse_task_rows(text)
        task = rows.get(task_id)
        if not task:
            return None
        return task.get("title")

    def _load_artifact_payload(self, path: Path) -> dict[str, Any]:
        if path.suffix.lower() in {".yaml", ".yml", ".md"}:
            payload = load_yaml(path)
        else:
            payload = load_json(path)
        if not isinstance(payload, dict):
            raise TypeError(f"{path} must parse to an object-like mapping.")
        return payload

    def _trim_document(self, item: dict[str, Any], *, include_text: bool) -> dict[str, Any]:
        payload = {
            "path": item["path"],
            "summary": item.get("summary"),
            "word_count": item.get("word_count"),
        }
        if include_text:
            payload["text"] = item.get("text", "")
        return payload
