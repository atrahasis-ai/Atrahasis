from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from aas1.control_plane import AtrahasisControlPlane


JSON = dict[str, Any]
PROTOCOL_VERSION = "2025-06-18"


@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: JSON
    handler: Callable[[JSON], JSON]
    title: str | None = None


class AtrahasisMcpServer:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.control = AtrahasisControlPlane(repo_root)
        self.tools = self._build_tools()

    def run(self) -> int:
        for raw_line in sys.stdin:
            line = raw_line.strip()
            if not line:
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError as exc:
                self._write_message(self._error_response(None, -32700, f"Parse error: {exc.msg}"))
                continue
            if isinstance(message, list):
                responses = [response for item in message if (response := self._handle_message(item)) is not None]
                if responses:
                    self._write_message(responses)
                continue
            response = self._handle_message(message)
            if response is not None:
                self._write_message(response)
        return 0

    def _build_tools(self) -> dict[str, ToolSpec]:
        return {
            "get_session_brief": ToolSpec(
                name="get_session_brief",
                title="Get Session Brief",
                description="Return the current repo session brief and the next dispatchable canonical task.",
                input_schema={"type": "object", "additionalProperties": False},
                handler=lambda _args: self.control.get_session_brief(),
            ),
            "get_dispatchable_tasks": ToolSpec(
                name="get_dispatchable_tasks",
                title="Get Dispatchable Tasks",
                description="Return the next dispatchable canonical task plus the current simplified user dispatch order.",
                input_schema={
                    "type": "object",
                    "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": 20}},
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_dispatchable_tasks(limit=int(args.get("limit", 5))),
            ),
            "get_task_claims": ToolSpec(
                name="get_task_claims",
                title="Get Task Claims",
                description="Return current task claim records, optionally filtering to active claims only.",
                input_schema={
                    "type": "object",
                    "properties": {"active_only": {"type": "boolean"}},
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_task_claims(active_only=bool(args.get("active_only", True))),
            ),
            "get_task_workspace_manifest": ToolSpec(
                name="get_task_workspace_manifest",
                title="Get Task Workspace Manifest",
                description="Return the task workspace document manifest for a specific task id.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "include_text": {"type": "boolean"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 500},
                    },
                    "required": ["task_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_task_workspace_manifest(
                    task_id=str(args["task_id"]).upper(),
                    include_text=bool(args.get("include_text", False)),
                    limit=int(args.get("limit", 100)),
                ),
            ),
            "get_decisions": ToolSpec(
                name="get_decisions",
                title="Get Decisions",
                description="Search or list ADR entries from DECISIONS.md.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "keyword": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                        "include_text": {"type": "boolean"},
                    },
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_decisions(
                    keyword=args.get("keyword"),
                    limit=int(args.get("limit", 5)),
                    include_text=bool(args.get("include_text", False)),
                ),
            ),
            "get_spec": ToolSpec(
                name="get_spec",
                title="Get Spec",
                description="Return a canonical master spec by invention id, resolving titled spec directories automatically.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "spec_id": {"type": "string"},
                        "include_text": {"type": "boolean"},
                    },
                    "required": ["spec_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_spec(
                    spec_id=str(args["spec_id"]).upper(),
                    include_text=bool(args.get("include_text", True)),
                ),
            ),
            "resolve_spec_path": ToolSpec(
                name="resolve_spec_path",
                title="Resolve Spec Path",
                description="Resolve a spec id like C42 to its actual canonical master spec path under docs/specifications.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "spec_id": {"type": "string"},
                    },
                    "required": ["spec_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.resolve_spec_path(spec_id=str(args["spec_id"]).upper()),
            ),
            "get_latest_workflow_context": ToolSpec(
                name="get_latest_workflow_context",
                title="Get Latest Workflow Context",
                description="Return the latest workflow context and task-local decision artifacts for a task id.",
                input_schema={
                    "type": "object",
                    "properties": {"task_id": {"type": "string"}},
                    "required": ["task_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_latest_workflow_context(task_id=str(args["task_id"]).upper()),
            ),
            "search_canonical_artifacts": ToolSpec(
                name="search_canonical_artifacts",
                title="Search Canonical Artifacts",
                description="Search the repo's canonical docs manifest by keyword and optional category.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                        "category": {"type": "string"},
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.search_canonical_artifacts(
                    query=str(args["query"]),
                    limit=int(args.get("limit", 10)),
                    category=args.get("category"),
                ),
            ),
            "validate_artifact": ToolSpec(
                name="validate_artifact",
                title="Validate Artifact",
                description="Validate a repo artifact against one of the local AAS schemas.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "schema_name": {"type": "string"},
                        "artifact_path": {"type": "string"},
                    },
                    "required": ["schema_name", "artifact_path"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.validate_artifact(
                    schema_name=str(args["schema_name"]),
                    artifact_path=str(args["artifact_path"]),
                ),
            ),
            "get_active_provider_sessions": ToolSpec(
                name="get_active_provider_sessions",
                title="Get Active Provider Sessions",
                description="Return currently registered active backend sessions from the provider runtime registry.",
                input_schema={"type": "object", "additionalProperties": False},
                handler=lambda _args: self.control.get_active_provider_sessions(),
            ),
            "get_redesign_memory": ToolSpec(
                name="get_redesign_memory",
                title="Get Redesign Memory",
                description="Return the distilled redesign-memory snapshot for a task, including related prior redesign cycles.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "limit_related": {"type": "integer", "minimum": 1, "maximum": 20},
                    },
                    "required": ["task_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_redesign_memory(
                    task_id=str(args["task_id"]).upper(),
                    limit_related=int(args.get("limit_related", 5)),
                ),
            ),
            "search_redesign_memory": ToolSpec(
                name="search_redesign_memory",
                title="Search Redesign Memory",
                description="Search the cross-task redesign-memory layer by query, optionally narrowing by task class or stage.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "task_class": {"type": "string"},
                        "current_stage": {"type": "string"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.search_redesign_memory(
                    query=str(args["query"]),
                    task_class=str(args["task_class"]).upper() if args.get("task_class") else None,
                    current_stage=str(args["current_stage"]).upper() if args.get("current_stage") else None,
                    limit=int(args.get("limit", 10)),
                ),
            ),
            "get_workflow_policy": ToolSpec(
                name="get_workflow_policy",
                title="Get Workflow Policy",
                description="Return the latest workflow policy state for a task id.",
                input_schema={
                    "type": "object",
                    "properties": {"task_id": {"type": "string"}},
                    "required": ["task_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_workflow_policy(task_id=str(args["task_id"]).upper()),
            ),
            "get_audit_timeline": ToolSpec(
                name="get_audit_timeline",
                title="Get Audit Timeline",
                description="Return the audit timeline for a task id.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "after_id": {"type": "integer", "minimum": 0},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 500},
                    },
                    "required": ["task_id"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.get_audit_timeline(
                    task_id=str(args["task_id"]).upper(),
                    after_id=int(args.get("after_id", 0)),
                    limit=int(args.get("limit", 200)),
                ),
            ),
            "create_claim": ToolSpec(
                name="create_claim",
                title="Create Claim",
                description="Create a narrow task claim in docs/task_claims using current Atrahasis claim conventions.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "title": {"type": "string"},
                        "platform": {"type": "string"},
                        "agent_name": {"type": "string"},
                        "safe_zone_paths": {"type": "array", "items": {"type": "string"}},
                        "pipeline_type": {"type": "string"},
                        "invention_ids": {"type": "array", "items": {"type": "string"}},
                        "target_specs": {"type": "array", "items": {"type": "string"}},
                        "notes": {"type": "string"},
                        "status": {"type": "string"},
                    },
                    "required": ["task_id", "agent_name"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.create_claim(
                    task_id=str(args["task_id"]).upper(),
                    title=args.get("title"),
                    platform=str(args.get("platform", "CODEX")),
                    agent_name=str(args["agent_name"]),
                    safe_zone_paths=[str(item) for item in args.get("safe_zone_paths", [])] or None,
                    pipeline_type=str(args.get("pipeline_type", "AAS")),
                    invention_ids=[str(item) for item in args.get("invention_ids", [])] or None,
                    target_specs=[str(item) for item in args.get("target_specs", [])] or None,
                    notes=str(args.get("notes", "")),
                    status=str(args.get("status", "CLAIMED")),
                ),
            ),
            "write_handoff": ToolSpec(
                name="write_handoff",
                title="Write Handoff",
                description="Write a task handoff markdown file under docs/handoffs or docs/handoffs/applied.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "title": {"type": "string"},
                        "platform": {"type": "string"},
                        "pipeline_verdict": {"type": "string"},
                        "notes": {"type": "string"},
                        "artifacts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "path": {"type": "string"},
                                    "description": {"type": "string"},
                                },
                                "required": ["path", "description"],
                                "additionalProperties": False,
                            },
                        },
                        "applied": {"type": "boolean"},
                    },
                    "required": ["task_id", "title", "platform", "pipeline_verdict"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.write_handoff(
                    task_id=str(args["task_id"]).upper(),
                    title=str(args["title"]),
                    platform=str(args["platform"]),
                    pipeline_verdict=str(args["pipeline_verdict"]),
                    notes=str(args.get("notes", "")),
                    artifacts=args.get("artifacts"),
                    applied=bool(args.get("applied", False)),
                ),
            ),
            "record_human_decision": ToolSpec(
                name="record_human_decision",
                title="Record Human Decision",
                description="Update HUMAN_DECISION_RECORD, WORKFLOW_RUN_RECORD, and workflow status with a human decision.",
                input_schema={
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string"},
                        "operator_decision": {"type": "string"},
                        "workflow_status": {"type": "string"},
                        "constraints": {"type": "array", "items": {"type": "string"}},
                        "notes": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["task_id", "operator_decision"],
                    "additionalProperties": False,
                },
                handler=lambda args: self.control.record_human_decision(
                    task_id=str(args["task_id"]).upper(),
                    operator_decision=str(args["operator_decision"]),
                    workflow_status=str(args["workflow_status"]) if args.get("workflow_status") else None,
                    constraints=[str(item) for item in args.get("constraints", [])] or None,
                    notes=[str(item) for item in args.get("notes", [])] or None,
                ),
            ),
        }

    def _handle_message(self, message: Any) -> JSON | None:
        if not isinstance(message, dict):
            return self._error_response(None, -32600, "Invalid Request")
        method = message.get("method")
        message_id = message.get("id")
        params = message.get("params", {})
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": {"name": "atrahasis-mcp", "version": "0.1.0"},
                    "instructions": (
                        "Use these tools for structured Atrahasis state access. "
                        "Phase 2 adds narrow writes for claims, handoffs, and human decisions."
                    ),
                },
            }
        if method == "notifications/initialized":
            return None
        if method == "ping":
            return {"jsonrpc": "2.0", "id": message_id, "result": {}}
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "tools": [
                        {
                            "name": tool.name,
                            "title": tool.title,
                            "description": tool.description,
                            "inputSchema": tool.input_schema,
                        }
                        for tool in self.tools.values()
                    ]
                },
            }
        if method == "tools/call":
            return self._handle_tool_call(message_id=message_id, params=params)
        if "id" not in message:
            return None
        return self._error_response(message_id, -32601, f"Method not found: {method}")

    def _handle_tool_call(self, *, message_id: Any, params: Any) -> JSON:
        if not isinstance(params, dict):
            return self._error_response(message_id, -32602, "Invalid params for tools/call")
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        if tool_name not in self.tools:
            return self._error_response(message_id, -32602, f"Unknown tool: {tool_name}")
        if not isinstance(arguments, dict):
            return self._tool_error(message_id, "Tool arguments must be an object.")
        tool = self.tools[tool_name]
        try:
            Draft202012Validator(tool.input_schema).validate(arguments)
            payload = tool.handler(arguments)
        except Exception as exc:
            return self._tool_error(message_id, str(exc))
        rendered = json.dumps(payload, indent=2, sort_keys=True)
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": {
                "content": [{"type": "text", "text": rendered}],
                "structuredContent": payload,
                "isError": False,
            },
        }

    def _tool_error(self, message_id: Any, message: str) -> JSON:
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": {
                "content": [{"type": "text", "text": message}],
                "structuredContent": {"error": message},
                "isError": True,
            },
        }

    def _error_response(self, message_id: Any, code: int, message: str) -> JSON:
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "error": {
                "code": code,
                "message": message,
            },
        }

    def _write_message(self, payload: JSON | list[JSON]) -> None:
        sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
        sys.stdout.flush()
