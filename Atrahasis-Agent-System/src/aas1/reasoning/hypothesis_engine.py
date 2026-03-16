from __future__ import annotations

from collections import defaultdict
import re
from typing import Any


class HypothesisEngine:
    GENERATED_WORKSPACE_FILENAMES = {
        "analogy_report.json",
        "command_request.yaml",
        "contradiction_map.json",
        "cross_industry_discovery_report.json",
        "decision_ranking_report.json",
        "discovery_gap_report.json",
        "discovery_map.json",
        "experiment_simulation_report.json",
        "exploration_control_record.json",
        "feasibility_report.json",
        "human_decision_record.json",
        "hypothesis_packet.json",
        "idea_cluster_report.json",
        "knowledge_distillation_report.json",
        "novelty_report.json",
        "opportunity_report.json",
        "platform_alignment_report.json",
        "readme.md",
        "research_ingestion_report.json",
        "research_program_report.json",
        "research_quality_report.json",
        "research_strategy_report.json",
        "research_synthesis_report.json",
        "solution_path_set.json",
        "task_brief.md",
        "technology_frontier_model.json",
        "value_alignment_report.json",
        "workflow_run_record.json",
        "workflow_summary.md",
    }

    def run(
        self,
        *,
        command_prompt: str,
        opportunity_report: dict[str, Any],
        analogy_report: dict[str, Any],
        cross_industry_report: dict[str, Any],
        synthesis_report: dict[str, Any],
        discovery_map: dict[str, Any],
        task_workspace: list[dict[str, Any]],
    ) -> dict[str, Any]:
        hypotheses = []
        domain_context = self._domain_context(
            command_prompt=command_prompt,
            synthesis_report=synthesis_report,
            discovery_map=discovery_map,
            task_workspace=task_workspace,
        )
        candidate_frames = self._merge_candidate_frames(
            cross_industry_report=cross_industry_report,
            domain_frames=domain_context["hypothesis_frames"],
        )
        for index, frame in enumerate(candidate_frames, start=1):
            analogy = analogy_report["analogies"][(index - 1) % max(len(analogy_report["analogies"]), 1)]
            supporting_refs = self._supporting_refs(
                frame=frame,
                task_workspace=task_workspace,
                discovery_map=discovery_map,
                fallback_refs=domain_context["fallback_evidence"],
            )
            hypotheses.append(
                {
                    "id": f"H-{index:03d}",
                    "title": frame["title"],
                    "summary": frame["summary"].format(
                        source_domain=analogy["source_domain"],
                        prompt=command_prompt[:120],
                    ),
                    "statement": frame["statement"].format(
                        source_domain=analogy["source_domain"],
                        prompt=command_prompt[:160],
                    ),
                    "supporting_research": [
                        {
                            "evidence_ref": ref,
                            "link_reason": f"Evidence aligned with {frame['focus']} for the active problem domain.",
                        }
                        for ref in supporting_refs
                    ],
                    "contradiction": None,
                    "solution_paths": [],
                    "novelty_score": 0,
                    "feasibility_score": 0,
                    "opportunity_zone": frame["focus"],
                    "confidence": round(max(0.78 - index * 0.06, 0.45), 2),
                    "origin": frame.get("origin", "domain"),
                    "candidate_label": frame.get("candidate_label", "Top Exploration Candidate"),
                    "cross_domain_source": frame.get("cross_domain_source"),
                    "cross_domain_strength": frame.get("cross_domain_strength"),
                    "program_id": None,
                    "scope_level": None,
                    "domain": frame["focus"],
                    "artifact_links": {
                        "contradiction_map": None,
                        "solution_path_set": [],
                        "novelty_report": None,
                        "feasibility_report": None,
                    },
                }
            )
        return {
            "type": "HYPOTHESIS_PACKET",
            "hypotheses": hypotheses,
            "supporting_evidence": [frame["focus"] for frame in candidate_frames],
            "opportunity_zone_refs": [frame["focus"] for frame in candidate_frames],
            "confidence": round(sum(item["confidence"] for item in hypotheses) / max(len(hypotheses), 1), 2),
        }

    def link_artifacts(
        self,
        *,
        hypothesis_packet: dict[str, Any],
        contradiction_map: dict[str, Any],
        solution_paths: dict[str, Any],
        novelty_report: dict[str, Any],
        feasibility_report: dict[str, Any],
    ) -> dict[str, Any]:
        contradictions_by_hypothesis = {
            item["hypothesis_id"]: item for item in contradiction_map["contradictions"]
        }
        solution_paths_by_hypothesis: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for path in solution_paths["candidate_paths"]:
            solution_paths_by_hypothesis[path["hypothesis_id"]].append(path)

        novelty_by_hypothesis = {
            item["hypothesis_id"]: item for item in novelty_report.get("hypothesis_assessments", [])
        }
        feasibility_by_hypothesis = {
            item["hypothesis_id"]: item for item in feasibility_report.get("hypothesis_assessments", [])
        }

        linked_hypotheses = []
        for hypothesis in hypothesis_packet["hypotheses"]:
            contradiction = contradictions_by_hypothesis.get(hypothesis["id"])
            paths = solution_paths_by_hypothesis.get(hypothesis["id"], [])
            novelty = novelty_by_hypothesis.get(hypothesis["id"], {})
            feasibility = feasibility_by_hypothesis.get(hypothesis["id"], {})
            contradiction_payload = (
                {
                    "id": contradiction["id"],
                    "statement": contradiction["contradiction"],
                    "severity": contradiction["severity"],
                    "artifact_ref": f"CONTRADICTION_MAP.json#{contradiction['id']}",
                }
                if contradiction is not None
                else None
            )
            solution_payload = [
                {
                    "id": path["id"],
                    "title": path["title"],
                    "tradeoffs": path["tradeoffs"],
                    "artifact_ref": f"SOLUTION_PATH_SET.json#{path['id']}",
                }
                for path in paths
            ]
            linked_hypotheses.append(
                {
                    **hypothesis,
                    "contradiction": contradiction_payload,
                    "solution_paths": solution_payload,
                    "novelty_score": novelty.get("novelty_score", 0),
                    "feasibility_score": feasibility.get("feasibility_score", 0),
                    "artifact_links": {
                        "contradiction_map": contradiction_payload["artifact_ref"] if contradiction_payload else None,
                        "solution_path_set": [item["artifact_ref"] for item in solution_payload],
                        "novelty_report": novelty.get("artifact_ref"),
                        "feasibility_report": feasibility.get("artifact_ref"),
                    },
                }
            )

        linked_packet = dict(hypothesis_packet)
        linked_packet["hypotheses"] = linked_hypotheses
        return linked_packet

    def _domain_context(
        self,
        *,
        command_prompt: str,
        synthesis_report: dict[str, Any],
        discovery_map: dict[str, Any],
        task_workspace: list[dict[str, Any]],
    ) -> dict[str, Any]:
        prompt_lower = command_prompt.lower()
        source_workspace_items = self._source_workspace_items(task_workspace)
        task_text = "\n".join(item["text"] for item in source_workspace_items)
        synthesis_keywords = synthesis_report.get("top_keywords", [])
        discovery_terms = [item["domain"] for item in discovery_map.get("domain_links", [])]
        source_workspace_refs = [item["path"] for item in source_workspace_items]
        discovery_evidence_refs = [
            ref for ref in discovery_map.get("evidence_refs", [])
            if not self._is_generated_workspace_path(ref)
        ]
        fallback_evidence = source_workspace_refs[:3] + discovery_evidence_refs[:3]

        if self._is_cooling_domain(prompt_lower, task_text):
            frames = self._cooling_hypothesis_frames(prompt_lower, task_text)
        else:
            frames = self._generic_frames(
                command_prompt=command_prompt,
                synthesis_keywords=synthesis_keywords,
                discovery_terms=discovery_terms,
            )

        return {
            "hypothesis_frames": frames,
            "fallback_evidence": fallback_evidence,
        }

    def _merge_candidate_frames(
        self,
        *,
        cross_industry_report: dict[str, Any],
        domain_frames: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        merged: list[dict[str, str]] = []
        seen_titles: set[str] = set()
        for frame in cross_industry_report.get("generated_hypothesis_seeds", []) + domain_frames:
            title = frame["title"].lower()
            if title in seen_titles:
                continue
            merged.append(frame)
            seen_titles.add(title)
        return merged

    def _is_cooling_domain(self, prompt_lower: str, task_text: str) -> bool:
        combined = f"{prompt_lower}\n{task_text.lower()}"
        markers = ("cool", "thermal", "heat", "data center", "immersion", "microfluidic", "phase-change", "dielectric")
        return any(marker in combined for marker in markers)

    def _cooling_hypothesis_frames(self, prompt_lower: str, task_text: str) -> list[dict[str, str]]:
        combined = f"{prompt_lower}\n{task_text.lower()}"
        catalog = [
            {
                "focus": "microfluidic cooling",
                "title": "Microfluidic cooling channels embedded in server boards",
                "summary": "Use {source_domain} style reasoning to embed microfluidic cooling near high-heat devices for prompt: {prompt}",
                "statement": (
                    "Use microfluidic cooling channels embedded in server boards to remove heat locally while preserving "
                    "high computational density for the problem: {prompt}"
                ),
                "terms": ("microfluidic", "microchannel", "cold plate"),
            },
            {
                "focus": "immersion cooling",
                "title": "Immersion cooling with dielectric fluids",
                "summary": "Use {source_domain} style reasoning to apply dielectric immersion cooling for prompt: {prompt}",
                "statement": (
                    "Use immersion cooling with dielectric fluids to reduce airflow energy while supporting dense rack-scale "
                    "compute for the problem: {prompt}"
                ),
                "terms": ("immersion", "dielectric"),
            },
            {
                "focus": "phase-change cooling",
                "title": "Phase-change cooling plates integrated with processors",
                "summary": "Use {source_domain} style reasoning to absorb thermal spikes with phase-change structures for prompt: {prompt}",
                "statement": (
                    "Use phase-change cooling plates integrated with processors to reduce active cooling energy while "
                    "buffering heat spikes in high-density compute for the problem: {prompt}"
                ),
                "terms": ("phase change", "phase-change", "vapor chamber"),
            },
            {
                "focus": "hybrid liquid immersion cooling",
                "title": "Hybrid liquid and immersion cooling architecture",
                "summary": "Use {source_domain} style reasoning to combine localized liquid loops with immersion cooling for prompt: {prompt}",
                "statement": (
                    "Use a hybrid liquid and immersion cooling architecture to balance cooling energy, serviceability, and "
                    "thermal density for the problem: {prompt}"
                ),
                "terms": ("hybrid", "liquid", "immersion"),
            },
            {
                "focus": "warm-water direct-to-chip cooling",
                "title": "Warm-water direct-to-chip liquid cooling loops",
                "summary": "Use {source_domain} style reasoning to shift toward warm-water direct-to-chip cooling for prompt: {prompt}",
                "statement": (
                    "Use warm-water direct-to-chip liquid cooling loops to reduce chiller energy while sustaining high "
                    "processor density for the problem: {prompt}"
                ),
                "terms": ("warm-water", "direct-to-chip", "liquid cooling"),
            },
        ]

        selected = [
            item for item in catalog
            if any(term in combined for term in item["terms"])
        ]
        if len(selected) < 3:
            selected = catalog[:5]
        return [{key: value for key, value in item.items() if key != "terms"} for item in selected[:5]]

    def _generic_frames(
        self,
        *,
        command_prompt: str,
        synthesis_keywords: list[str],
        discovery_terms: list[str],
    ) -> list[dict[str, str]]:
        prompt_tokens = {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", command_prompt.lower())
            if token not in {"design", "architecture", "that", "while", "reduces", "reduce", "increasing"}
        }
        candidates = []
        for term in synthesis_keywords + discovery_terms:
            if term in prompt_tokens or any(token in term or term in token for token in prompt_tokens):
                candidates.append(term)
        if not candidates:
            candidates = list(dict.fromkeys(synthesis_keywords[:5] + list(prompt_tokens)[:5]))
        frames = []
        for term in candidates[:5]:
            frames.append(
                {
                    "focus": term,
                    "title": f"{term.title()} invention pathway",
                    "summary": "Use {source_domain} style reasoning to explore " + term + " for prompt: {prompt}",
                    "statement": (
                        "Explore " + term + " as an invention opportunity by transferring {source_domain} coordination "
                        "patterns into the problem: {prompt}"
                    ),
                }
            )
        return frames

    def _supporting_refs(
        self,
        *,
        frame: dict[str, str],
        task_workspace: list[dict[str, Any]],
        discovery_map: dict[str, Any],
        fallback_refs: list[str],
    ) -> list[str]:
        explicit_refs = frame.get("support_refs", [])
        if explicit_refs:
            return explicit_refs[:3]
        focus_terms = set(re.findall(r"[a-z][a-z0-9_-]{3,}", frame["focus"].lower()))
        matched_workspace = []
        for item in self._source_workspace_items(task_workspace):
            haystack = f"{item['summary']} {item['text']}".lower()
            if any(term in haystack for term in focus_terms):
                matched_workspace.append(item["path"])
        if matched_workspace:
            return matched_workspace[:3]

        matched_evidence = []
        for ref in discovery_map.get("evidence_refs", []):
            if self._is_generated_workspace_path(ref):
                continue
            ref_lower = ref.lower()
            if any(term in ref_lower for term in focus_terms):
                matched_evidence.append(ref)
        if matched_evidence:
            return matched_evidence[:3]
        return fallback_refs[:3]

    def _source_workspace_items(self, task_workspace: list[dict[str, Any]]) -> list[dict[str, Any]]:
        source_items = []
        for item in task_workspace:
            if self._is_generated_workspace_path(item["path"]):
                continue
            source_items.append(item)
        return source_items

    def _is_generated_workspace_path(self, path: str) -> bool:
        normalized = path.replace("\\", "/").lower()
        if "/task_workspaces/" not in normalized:
            return False
        filename = normalized.rsplit("/", 1)[-1]
        return filename in self.GENERATED_WORKSPACE_FILENAMES
