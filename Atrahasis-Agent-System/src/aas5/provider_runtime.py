from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from aas5.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


ROLE_TIER_MAP = {
    "director": "primary",
    "visionary": "primary",
    "systems_thinker": "primary",
    "critic": "primary",
    "science_advisor": "primary",
    "adversarial_analyst": "primary",
    "pre_mortem_analyst": "primary",
    "synthesis_engineer": "primary",
    "assessment_council": "primary",
    "architecture_designer": "primary",
    "specification_writer": "primary",
    "research_director": "primary",
    "lane_manager": "primary",
    "lane_convergence_reporter": "primary",
    "auditor": "primary",
    "chronicler": "operational",
    "prior_art_researcher": "operational",
    "landscape_analyst": "operational",
    "domain_translator": "operational",
    "simplification_agent": "operational",
    "commercial_viability_assessor": "operational",
    "research_synthesizer": "operational",
    "operator_proxy": "operational",
    "memory_reuse_analyst": "operational",
    "coder": "code_only",
    "code_implementer": "code_only",
    "schema_validator": "code_only",
    "tooling_agent": "code_only",
    "refactor_agent": "code_only",
    "automation_agent": "code_only",
    "background_worker": "fast_background",
    "queue_worker": "fast_background",
    "index_refresh_worker": "fast_background",
    "fast_background": "fast_background",
    "primary": "primary",
    "operational": "operational",
    "code_only": "code_only",
}


SUPPORTED_BACKENDS = {
    "codex": {
        "display_name": "OpenAI Codex",
        "cli_command": "codex",
        "available_models": [
            "gpt-5.4",
            "gpt-5.3-codex",
            "gpt-5.3-codex-spark",
            "gpt-5.2-codex",
            "gpt-5.2",
            "gpt-5.1-codex-max",
            "gpt-5.1-codex-mini",
        ],
        "routing": {
            "primary": {
                "model": "gpt-5.4",
                "reasoning_effort": "xhigh",
                "notes": "Use for highest-capability invention, architecture, and council roles.",
            },
            "operational": {
                "model": "gpt-5.4",
                "reasoning_effort": "medium",
                "notes": "Default Codex model for non-peak roles that still need strong reasoning.",
            },
            "code_only": {
                "model": "gpt-5.3-codex",
                "reasoning_effort": "high",
                "notes": "Codex-optimized path for code-heavy implementation and validation work.",
            },
            "fast_background": {
                "model": "gpt-5.3-codex-spark",
                "reasoning_effort": "low",
                "notes": "Use only for low-risk background or acceleration tasks.",
            },
        },
    },
    "gemini": {
        "display_name": "Gemini CLI",
        "cli_command": "gemini",
        "available_models": [
            "gemini-3.1-pro-preview",
            "gemini-3-flash-preview",
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
        ],
        "routing": {
            "primary": {
                "model": "gemini-3.1-pro-preview",
                "reasoning_effort": "high",
                "notes": "Use for highest-capability research, architecture, and invention roles.",
            },
            "operational": {
                "model": "gemini-3-flash-preview",
                "reasoning_effort": "medium",
                "notes": "Default Gemini model for operational and analysis roles.",
            },
            "code_only": {
                "model": "gemini-3-flash-preview",
                "reasoning_effort": "medium",
                "notes": "Gemini does not have a separate code-only family in the current routing policy.",
            },
            "fast_background": {
                "model": "gemini-2.5-flash-lite",
                "reasoning_effort": "low",
                "notes": "Use for low-cost background fan-out only.",
            },
        },
    },
}


class ProviderRuntimeRegistry:
    """Provider/runtime abstraction for multi-terminal AAS execution."""

    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.root = ensure_dir(runtime_state_dir(repo_root) / "provider_runtime")
        self.sessions_root = ensure_dir(self.root / "sessions")
        self.registry_path = self.root / "registry.json"

    def supported_backends(self) -> dict[str, Any]:
        return SUPPORTED_BACKENDS

    def register_backend(
        self,
        *,
        provider: str,
        agent_name: str,
        session_id: str,
        agent_types: list[str] | None = None,
        current_task: str | None = None,
        status: str = "ACTIVE",
        notes: str = "",
    ) -> dict[str, Any]:
        provider_key = self._provider_key(provider)
        normalized_types = self._normalize_agent_types(agent_types or ["operational"])
        routing_manifest = [
            self.resolve_model_route(provider_key, agent_type)
            for agent_type in normalized_types
        ]
        payload = {
            "type": "PROVIDER_BACKEND_SESSION",
            "provider": provider_key,
            "display_name": SUPPORTED_BACKENDS[provider_key]["display_name"],
            "agent_name": agent_name,
            "session_id": session_id,
            "status": status,
            "current_task": current_task,
            "registered_at": utc_now(),
            "updated_at": utc_now(),
            "notes": notes,
            "supported_agent_types": normalized_types,
            "routing_manifest": routing_manifest,
            "available_models": list(SUPPORTED_BACKENDS[provider_key]["available_models"]),
        }
        provider_root = ensure_dir(self.sessions_root / provider_key)
        path = provider_root / f"{session_id}.json"
        write_json(path, payload)
        write_json(provider_root / "latest.json", payload)
        self._refresh_registry()
        return payload

    def resolve_model_route(self, provider: str, agent_type: str) -> dict[str, str]:
        provider_key = self._provider_key(provider)
        tier = self._tier_for_agent_type(agent_type)
        route = SUPPORTED_BACKENDS[provider_key]["routing"][tier]
        return {
            "agent_type": self._normalize_token(agent_type),
            "tier": tier,
            "provider": provider_key,
            "model": route["model"],
            "reasoning_effort": route["reasoning_effort"],
            "notes": route["notes"],
        }

    def list_active_sessions(self) -> list[dict[str, Any]]:
        if not self.registry_path.exists():
            return []
        payload = load_json(self.registry_path)
        return payload.get("active_sessions", [])

    def clear_current_task_references(self, task_ids: list[str], *, note: str = "") -> list[dict[str, str]]:
        retired = {self._normalize_token(task_id) for task_id in task_ids}
        updates: list[dict[str, str]] = []
        for provider_root in sorted(self.sessions_root.glob("*")):
            if not provider_root.is_dir():
                continue
            latest_payload: dict[str, Any] | None = None
            latest_registered_at = ""
            for path in sorted(provider_root.glob("*.json")):
                if path.name == "latest.json":
                    continue
                payload = load_json(path)
                current_task = payload.get("current_task")
                if current_task and self._normalize_token(current_task) in retired:
                    payload["current_task"] = None
                    payload["updated_at"] = utc_now()
                    if note:
                        existing = payload.get("notes", "").strip()
                        payload["notes"] = f"{existing} {note}".strip()
                    write_json(path, payload)
                    updates.append(
                        {
                            "provider": payload["provider"],
                            "agent_name": payload["agent_name"],
                            "session_id": payload["session_id"],
                        }
                    )
                registered_at = payload.get("registered_at", "")
                if registered_at >= latest_registered_at:
                    latest_registered_at = registered_at
                    latest_payload = payload
            if latest_payload is not None:
                write_json(provider_root / "latest.json", latest_payload)
        self._refresh_registry()
        return updates

    def _refresh_registry(self) -> None:
        sessions = []
        for provider_root in sorted(self.sessions_root.glob("*")):
            if not provider_root.is_dir():
                continue
            for path in sorted(provider_root.glob("*.json")):
                if path.name == "latest.json":
                    continue
                payload = load_json(path)
                if payload.get("status") == "ACTIVE":
                    sessions.append(
                        {
                            "provider": payload["provider"],
                            "agent_name": payload["agent_name"],
                            "session_id": payload["session_id"],
                            "current_task": payload.get("current_task"),
                            "supported_agent_types": payload.get("supported_agent_types", []),
                            "registered_at": payload["registered_at"],
                        }
                    )
        write_json(
            self.registry_path,
            {
                "type": "PROVIDER_RUNTIME_REGISTRY",
                "updated_at": utc_now(),
                "supported_backends": SUPPORTED_BACKENDS,
                "active_sessions": sessions,
            },
        )

    def _provider_key(self, provider: str) -> str:
        key = self._normalize_token(provider)
        if key not in SUPPORTED_BACKENDS:
            raise ValueError(f"Unsupported provider backend: {provider}")
        return key

    def _normalize_agent_types(self, values: list[str]) -> list[str]:
        ordered = []
        seen = set()
        for value in values:
            normalized = self._normalize_token(value)
            if normalized in seen:
                continue
            ordered.append(normalized)
            seen.add(normalized)
        return ordered

    def _tier_for_agent_type(self, agent_type: str) -> str:
        normalized = self._normalize_token(agent_type)
        return ROLE_TIER_MAP.get(normalized, "operational")

    def _normalize_token(self, value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
