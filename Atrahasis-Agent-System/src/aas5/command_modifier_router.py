from __future__ import annotations

import re

from aas5.common import CommandRequest, utc_now


COMMAND_SPECS = {
    "AASBT": {
        "scope": "buildout_task",
        "hitl_requirements": ["PIVOT", "RESOURCE_INTENSIVE", "PATENT_RELATED"],
    },
    "AASAQ": {
        "scope": "architecture_question",
        "hitl_requirements": [],
    },
    "AASNI": {
        "scope": "new_idea_integration",
        "hitl_requirements": ["CONCEPT_SELECTION", "PIVOT"],
    },
    "AASA": {
        "scope": "full_system_analysis",
        "hitl_requirements": ["EXTERNAL_RESEARCH"],
    },
}

PROMPT_MODIFIER_RULES = [
    {
        "label": "FULL_PIPELINE_TASK",
        "pattern": re.compile(r"^\s*FULL\s+PIPELINE\s+TASK\s*:\s*", re.IGNORECASE),
        "constraints": [
            "PROMPT_MODIFIER_FULL_PIPELINE_TASK",
            "STRICT_FULL_PIPELINE_TASK",
            "TASK_ROUTING_REQUIRED",
            "ABGR_SWARM_REQUIRED",
            "NO_PARENT_ONLY_ADVISORY_FALLBACK",
            "NO_JUDGMENT_CALL_DOWNGRADE",
        ],
    }
]


def _dedupe_constraints(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = str(item).strip()
        if not text:
            continue
        key = text.upper()
        if key in seen:
            continue
        seen.add(key)
        result.append(text)
    return result


class CommandModifierRouter:
    def detect_prompt_modifier(self, prompt: str) -> dict[str, object] | None:
        text = prompt or ""
        for rule in PROMPT_MODIFIER_RULES:
            pattern = rule["pattern"]
            if pattern.match(text):
                stripped_prompt = pattern.sub("", text, count=1).strip()
                return {
                    "label": rule["label"],
                    "constraints": list(rule["constraints"]),
                    "stripped_prompt": stripped_prompt,
                }
        return None

    def parse(
        self,
        *,
        modifier: str,
        prompt: str,
        task_id: str,
        operator_constraints: list[str] | None = None,
    ) -> CommandRequest:
        normalized = modifier.strip().upper()
        if normalized not in COMMAND_SPECS:
            raise ValueError(f"Unsupported command modifier: {modifier}")
        spec = COMMAND_SPECS[normalized]
        prompt_directive = self.detect_prompt_modifier(prompt)
        effective_prompt = str((prompt_directive or {}).get("stripped_prompt") or prompt).strip()
        effective_constraints = _dedupe_constraints(
            list(operator_constraints or []) + list((prompt_directive or {}).get("constraints") or [])
        )
        return CommandRequest(
            command_modifier=normalized,
            task_id=task_id,
            prompt=effective_prompt,
            scope=spec["scope"],
            operator_constraints=effective_constraints,
            hitl_requirements=list(spec["hitl_requirements"]),
            created_at=utc_now(),
        )
