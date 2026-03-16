from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from aas5.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class GovernanceKernel:
    """Authoritative scope/domain lock state for AAS5 research programs."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "governance")
        self.lock_path = self.root / "locks.json"

    def apply(
        self,
        *,
        task_id: str,
        workflow_id: str,
        program_report: dict[str, Any],
    ) -> dict[str, Any]:
        state = self._load_state()
        locks = {
            key: value
            for key, value in state.get("locks", {}).items()
            if value.get("task_id") != task_id
        }
        programs = []
        telemetry_events = list(program_report.get("telemetry_events", []))

        for program in program_report.get("active_programs", []):
            item = dict(program)
            item["governance_notes"] = list(item.get("governance_notes", []))
            lock_key = self._lock_key(item)
            if item.get("execution_state") == "active":
                existing = locks.get(lock_key)
                if existing and existing.get("program_id") != item["program_id"]:
                    item["execution_state"] = "paused_by_scope_lock"
                    item["dependency_state"] = f"locked_by_{existing['program_id']}"
                    item["governance_notes"].append(
                        f"Paused because authoritative scope lock {lock_key} is held by {existing['program_id']}."
                    )
                    telemetry_events.append(
                        {
                            "event": "program_paused_by_scope_lock",
                            "program_id": item["program_id"],
                            "blocking_program_id": existing["program_id"],
                            "lock_key": lock_key,
                        }
                    )
                else:
                    locks[lock_key] = {
                        "task_id": task_id,
                        "workflow_id": workflow_id,
                        "program_id": item["program_id"],
                        "scope_level": item["scope_level"],
                        "target_domain": item["target_domain"],
                        "granted_at": utc_now(),
                    }
                    item["governance_lock"] = lock_key
                    item["governance_notes"].append(f"Authoritative scope lock granted: {lock_key}.")
            item["governance_notes"] = self._unique(item["governance_notes"])
            programs.append(item)

        l0_programs = [
            program
            for program in programs
            if program.get("scope_level") == "L0" and program.get("execution_state") == "active"
        ]
        if l0_programs:
            blocker = l0_programs[0]
            for program in programs:
                if program.get("scope_level") == "L0":
                    continue
                if program.get("execution_state") != "active":
                    continue
                if self._depends_on_l0(program=program, blocker=blocker):
                    program["execution_state"] = "paused_by_l0_governance"
                    program["dependency_state"] = f"blocked_by_{blocker['program_id']}"
                    program["governance_notes"].append(
                        f"Paused because L0 architecture program {blocker['program_id']} is unresolved."
                    )
                    program["governance_notes"] = self._unique(program["governance_notes"])
                    telemetry_events.append(
                        {
                            "event": "program_paused_for_l0_kernel",
                            "program_id": program["program_id"],
                            "blocking_program_id": blocker["program_id"],
                        }
                    )

        updated = dict(program_report)
        updated["active_programs"] = programs
        updated["telemetry_events"] = telemetry_events
        updated["governance_summary"] = {
            **program_report.get("governance_summary", {}),
            "governance_kernel": "active",
            "authoritative_lock_count": len(locks),
            "lock_keys": sorted(locks),
        }
        self._write_state(task_id=task_id, workflow_id=workflow_id, locks=locks, program_report=updated)
        return updated

    def _load_state(self) -> dict[str, Any]:
        if not self.lock_path.exists():
            return {"locks": {}}
        return load_json(self.lock_path)

    def _write_state(
        self,
        *,
        task_id: str,
        workflow_id: str,
        locks: dict[str, dict[str, Any]],
        program_report: dict[str, Any],
    ) -> None:
        payload = {
            "type": "GOVERNANCE_STATE",
            "updated_at": utc_now(),
            "locks": locks,
        }
        write_json(self.lock_path, payload)
        task_root = ensure_dir(self.root / task_id)
        write_json(
            task_root / f"{workflow_id}.json",
            {
                "type": "GOVERNANCE_SNAPSHOT",
                "task_id": task_id,
                "workflow_id": workflow_id,
                "updated_at": utc_now(),
                "locks": locks,
                "governance_summary": program_report.get("governance_summary", {}),
            },
        )
        write_json(task_root / "latest.json", program_report)

    def _lock_key(self, program: dict[str, Any]) -> str:
        domain = re.sub(r"[^a-z0-9]+", "-", program["target_domain"].lower()).strip("-")
        return f"{program['scope_level']}::{domain}"

    def _depends_on_l0(self, *, program: dict[str, Any], blocker: dict[str, Any]) -> bool:
        program_tokens = self._tokens(program["target_domain"] + " " + program["program_title"])
        blocker_tokens = self._tokens(blocker["target_domain"] + " " + blocker["program_title"])
        return bool({"system", "architecture", "platform"} & blocker_tokens or program_tokens & blocker_tokens)

    def _tokens(self, text: str) -> set[str]:
        return {token for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())}

    def _unique(self, values: list[str]) -> list[str]:
        ordered: list[str] = []
        seen: set[str] = set()
        for value in values:
            if value in seen:
                continue
            ordered.append(value)
            seen.add(value)
        return ordered
