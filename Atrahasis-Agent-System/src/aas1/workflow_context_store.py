from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from aas1.common import CommandRequest, ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class WorkflowContextStore:
    """Persists resumable AAS3 workflow context outside task artifacts."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "workflows")

    def start_workflow(
        self,
        *,
        request: CommandRequest,
        workflow_id: str,
        execution_profile: dict[str, object],
    ) -> dict[str, Any]:
        payload = {
            "type": "WORKFLOW_CONTEXT",
            "workflow_id": workflow_id,
            "task_id": request.task_id,
            "modifier": request.command_modifier,
            "prompt": request.prompt,
            "scope": request.scope,
            "execution_profile": execution_profile,
            "operator_constraints": list(request.operator_constraints),
            "hitl_requirements": list(request.hitl_requirements),
            "request": asdict(request),
            "status": "RUNNING",
            "created_at": request.created_at,
            "updated_at": utc_now(),
            "artifacts": {},
            "stages": {},
        }
        self._write_context(request.task_id, workflow_id, payload)
        return payload

    def record_stage(
        self,
        *,
        task_id: str,
        workflow_id: str,
        stage_name: str,
        status: str,
        produced_artifacts: list[str],
        notes: list[str] | None,
        stage_result: dict[str, Any],
        artifact_paths: dict[str, str],
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, workflow_id=workflow_id)
        payload["stages"][stage_name] = {
            "status": status,
            "produced_artifacts": produced_artifacts,
            "notes": notes or [],
            "artifact_refs": {
                name: artifact_paths[name]
                for name in produced_artifacts
                if name in artifact_paths
            },
            "result_summary": self._summarize_payload(stage_result),
            "recorded_at": utc_now(),
        }
        payload["artifacts"] = dict(artifact_paths)
        payload["updated_at"] = utc_now()
        self._write_context(task_id, workflow_id, payload)
        return payload

    def complete_workflow(
        self,
        *,
        task_id: str,
        workflow_id: str,
        status: str,
        workflow_record_path: str,
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, workflow_id=workflow_id)
        payload["status"] = status
        payload["workflow_record"] = workflow_record_path
        payload["updated_at"] = utc_now()
        self._write_context(task_id, workflow_id, payload)
        return payload

    def load(self, *, task_id: str, workflow_id: str) -> dict[str, Any]:
        return load_json(self._workflow_path(task_id, workflow_id))

    def load_latest(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        return load_json(path)

    def update_status(
        self,
        *,
        task_id: str,
        workflow_id: str,
        status: str,
        artifact_updates: dict[str, str | None] | None = None,
    ) -> dict[str, Any]:
        payload = self.load(task_id=task_id, workflow_id=workflow_id)
        payload["status"] = status
        payload["updated_at"] = utc_now()
        if artifact_updates:
            merged = dict(payload.get("artifacts", {}))
            merged.update({key: value for key, value in artifact_updates.items() if value})
            payload["artifacts"] = merged
        self._write_context(task_id, workflow_id, payload)
        return payload

    def _write_context(self, task_id: str, workflow_id: str, payload: dict[str, Any]) -> None:
        path = self._workflow_path(task_id, workflow_id)
        write_json(path, payload)
        write_json(self.root / task_id / "latest.json", payload)

    def _workflow_path(self, task_id: str, workflow_id: str) -> Path:
        return ensure_dir(self.root / task_id) / f"{workflow_id}.json"

    def _summarize_payload(self, value: Any) -> Any:
        if isinstance(value, dict):
            summary: dict[str, Any] = {"keys": sorted(value.keys())[:20]}
            if "type" in value:
                summary["type"] = value["type"]
            if "hypotheses" in value:
                summary["hypothesis_count"] = len(value["hypotheses"])
            if "contradictions" in value:
                summary["contradiction_count"] = len(value["contradictions"])
            if "candidate_paths" in value:
                summary["solution_path_count"] = len(value["candidate_paths"])
            if "active_programs" in value:
                summary["active_program_count"] = len(value["active_programs"])
            if "nodes" in value:
                summary["discovery_node_count"] = len(value["nodes"])
            return summary
        if isinstance(value, list):
            return {"count": len(value)}
        return value
