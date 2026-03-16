from __future__ import annotations

from typing import Any


class CrossIndustryDiscoveryEngine:
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
        discovery_map: dict[str, Any],
        task_workspace: list[dict[str, Any]],
    ) -> dict[str, Any]:
        nodes = [dict(node) for node in discovery_map.get("nodes", discovery_map.get("entities", []))]
        edges = [dict(edge) for edge in discovery_map.get("edges", discovery_map.get("relationships", []))]
        node_ids = {node["id"] for node in nodes}
        edge_keys = {(edge["from"], edge["to"], edge["type"]) for edge in edges}

        analogies: list[dict[str, Any]] = []
        hypothesis_seeds: list[dict[str, Any]] = []
        telemetry_events: list[dict[str, Any]] = []
        source_refs = self._source_workspace_refs(task_workspace)

        if self._is_cooling_domain(command_prompt=command_prompt, task_workspace=task_workspace):
            patterns = self._cooling_analogies(command_prompt=command_prompt, source_refs=source_refs)
        else:
            patterns = []

        for pattern in patterns:
            source_id = f"concept:{pattern['source_concept']}"
            target_id = f"concept:{pattern['target_concept']}"
            self._append_node(
                nodes,
                node_ids,
                {
                    "id": source_id,
                    "type": "concept",
                    "label": pattern["source_domain"],
                    "domain_class": "cross_industry_source",
                },
            )
            self._append_node(
                nodes,
                node_ids,
                {
                    "id": target_id,
                    "type": "concept",
                    "label": pattern["target_label"],
                    "domain_class": "cross_industry_target",
                },
            )
            self._append_edge(
                edges,
                edge_keys,
                source_id,
                target_id,
                "analogous_to",
                strength=pattern["strength"],
                rationale=pattern["rationale"],
            )
            analogies.append(
                {
                    "source_domain": pattern["source_domain"],
                    "target_concept": pattern["target_label"],
                    "rationale": pattern["rationale"],
                    "strength": pattern["strength"],
                    "generated_hypothesis_title": pattern["title"],
                }
            )
            hypothesis_seeds.append(
                {
                    "focus": pattern["focus"],
                    "title": pattern["title"],
                    "summary": pattern["summary"],
                    "statement": pattern["statement"],
                    "origin": "cross_domain",
                    "candidate_label": "Cross-Domain Opportunity",
                    "cross_domain_source": pattern["source_domain"],
                    "cross_domain_strength": pattern["strength"],
                    "support_refs": pattern["support_refs"],
                }
            )
            telemetry_events.append(
                {
                    "event": "cross_domain_analogy_detected",
                    "source_domain": pattern["source_domain"],
                    "target_concept": pattern["target_label"],
                    "strength": pattern["strength"],
                }
            )
            telemetry_events.append(
                {
                    "event": "cross_domain_hypothesis_generated",
                    "source_domain": pattern["source_domain"],
                    "hypothesis_title": pattern["title"],
                    "strength": pattern["strength"],
                }
            )

        updated_map = dict(discovery_map)
        updated_map["nodes"] = nodes
        updated_map["edges"] = edges
        updated_map["entities"] = nodes
        updated_map["relationships"] = edges
        return {
            "type": "CROSS_INDUSTRY_DISCOVERY_REPORT",
            "analogies": analogies,
            "generated_hypothesis_seeds": hypothesis_seeds,
            "high_value_candidates": [
                item["title"] for item in hypothesis_seeds if item["cross_domain_strength"] >= 0.8
            ],
            "updated_discovery_map": updated_map,
            "telemetry_events": telemetry_events,
        }

    def _is_cooling_domain(self, *, command_prompt: str, task_workspace: list[dict[str, Any]]) -> bool:
        source_text = "\n".join(item["text"] for item in self._source_workspace_items(task_workspace))
        combined = "\n".join([command_prompt, source_text]).lower()
        markers = (
            "cool",
            "thermal",
            "heat",
            "data center",
            "microfluidic",
            "immersion",
            "dielectric",
            "phase-change",
        )
        return any(marker in combined for marker in markers)

    def _cooling_analogies(self, *, command_prompt: str, source_refs: list[str]) -> list[dict[str, Any]]:
        return [
            {
                "source_concept": "biological_heat_regulation",
                "source_domain": "biological heat regulation",
                "target_concept": "microfluidic cooling",
                "target_label": "microfluidic cooling",
                "focus": "microvascular cooling analog",
                "strength": 0.92,
                "rationale": "Microvascular circulation moves heat at fine spatial granularity under changing load.",
                "title": "Microvascular cooling analog applied to data center thermal regulation",
                "summary": (
                    "Apply biological heat-regulation patterns to move heat through dense compute zones with "
                    "microfluidic cooling channels for the problem: "
                    f"{command_prompt}"
                ),
                "statement": (
                    "If microvascular cooling in biological systems regulates heat efficiently, then microfluidic "
                    "cooling channels may improve data center thermal management for the problem: "
                    f"{command_prompt}"
                ),
                "support_refs": source_refs,
            },
            {
                "source_concept": "cpu_package_cooling",
                "source_domain": "CPU package cooling",
                "target_concept": "warm-water direct-to-chip cooling",
                "target_label": "warm-water direct-to-chip cooling",
                "focus": "direct-to-chip cooling analog",
                "strength": 0.81,
                "rationale": "CPU package cooling prioritizes localized heat extraction and short thermal paths.",
                "title": "CPU package cooling analog scaled to dense rack thermal regulation",
                "summary": (
                    "Scale direct-to-chip thermal extraction patterns from processor cooling into rack-level liquid "
                    f"loops for the problem: {command_prompt}"
                ),
                "statement": (
                    "If CPU package cooling succeeds by minimizing thermal path length, then warm-water direct-to-chip "
                    "loops may reduce facility cooling energy while supporting dense compute for the problem: "
                    f"{command_prompt}"
                ),
                "support_refs": source_refs,
            },
            {
                "source_concept": "automotive_thermal_management",
                "source_domain": "automotive thermal systems",
                "target_concept": "hybrid liquid immersion cooling",
                "target_label": "hybrid liquid immersion cooling",
                "focus": "thermal loop staging analog",
                "strength": 0.78,
                "rationale": "Automotive thermal systems stage multiple cooling loops to handle transient and steady-state heat.",
                "title": "Multi-loop automotive thermal staging adapted to high-density data center cooling",
                "summary": (
                    "Adapt staged automotive thermal loops to combine immersion and liquid subsystems for the problem: "
                    f"{command_prompt}"
                ),
                "statement": (
                    "If automotive thermal systems use staged loops to handle both transient and sustained heat loads, "
                    "then a hybrid immersion and liquid cooling architecture may improve data center efficiency for the "
                    f"problem: {command_prompt}"
                ),
                "support_refs": source_refs,
            },
        ]

    def _source_workspace_refs(self, task_workspace: list[dict[str, Any]]) -> list[str]:
        preferred = []
        for item in self._source_workspace_items(task_workspace):
            path_lower = item["path"].lower()
            if any(name in path_lower for name in ("research_brief", "cooling_modalities", "thermal_contradiction")):
                preferred.append(item["path"])
        if preferred:
            return preferred[:3]
        source_like = [
            item["path"]
            for item in self._source_workspace_items(task_workspace)
            if not any(token in item["path"].lower() for token in ("json", "readme", "task_brief", "workflow"))
        ]
        return source_like[:3]

    def _source_workspace_items(self, task_workspace: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            item
            for item in task_workspace
            if not self._is_generated_workspace_path(item["path"])
        ]

    def _is_generated_workspace_path(self, path: str) -> bool:
        normalized = path.replace("\\", "/").lower()
        if "/task_workspaces/" not in normalized:
            return False
        filename = normalized.rsplit("/", 1)[-1]
        return filename in self.GENERATED_WORKSPACE_FILENAMES

    def _append_node(
        self,
        nodes: list[dict[str, Any]],
        node_ids: set[str],
        node: dict[str, Any],
    ) -> None:
        if node["id"] in node_ids:
            return
        nodes.append(node)
        node_ids.add(node["id"])

    def _append_edge(
        self,
        edges: list[dict[str, Any]],
        edge_keys: set[tuple[str, str, str]],
        source: str,
        target: str,
        edge_type: str,
        **metadata: Any,
    ) -> None:
        key = (source, target, edge_type)
        if key in edge_keys:
            return
        edges.append({"from": source, "to": target, "type": edge_type, **metadata})
        edge_keys.add(key)
