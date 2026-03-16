from __future__ import annotations

import hashlib
import re
from typing import Any


class KnowledgeDistillationEngine:
    DISTILLATION_INTERVAL = 20
    NODE_COUNT_THRESHOLD = 120
    SIMILARITY_THRESHOLD = 0.42

    def run(
        self,
        *,
        discovery_map: dict[str, Any],
        hypothesis_archive: list[dict[str, Any]],
        cycle_count: int,
    ) -> dict[str, Any]:
        node_count = len(discovery_map.get("nodes", discovery_map.get("entities", [])))
        triggered = (
            (cycle_count > 0 and cycle_count % self.DISTILLATION_INTERVAL == 0)
            or node_count > self.NODE_COUNT_THRESHOLD
        )
        updated_map = dict(discovery_map)
        telemetry_events: list[dict[str, Any]] = []
        if not triggered:
            return {
                "type": "KNOWLEDGE_DISTILLATION_REPORT",
                "triggered": False,
                "cycle_count": cycle_count,
                "node_count": node_count,
                "trigger_reason": None,
                "distilled_clusters": [],
                "updated_discovery_map": updated_map,
                "telemetry_events": telemetry_events,
            }

        telemetry_events.append(
            {
                "event": "distillation_cycle_started",
                "cycle_count": cycle_count,
                "node_count": node_count,
            }
        )
        clusters = self._cluster_archive(hypothesis_archive)
        nodes = [dict(node) for node in updated_map.get("nodes", updated_map.get("entities", []))]
        edges = [dict(edge) for edge in updated_map.get("edges", updated_map.get("relationships", []))]
        node_ids = {node["id"] for node in nodes}
        edge_keys = {(edge["from"], edge["to"], edge["type"]) for edge in edges}

        distilled_clusters = []
        for cluster in clusters:
            cluster_id = cluster["cluster_id"]
            representative = cluster["representative"]
            rep_hypothesis = representative["hypothesis"]
            cluster_node_id = f"distilled:{cluster_id}"
            self._append_node(
                nodes,
                node_ids,
                {
                    "id": cluster_node_id,
                    "type": "distilled_cluster",
                    "label": cluster["title"],
                    "representative_hypothesis": rep_hypothesis["id"],
                    "supporting_hypotheses": [item["hypothesis"]["id"] for item in cluster["supporting"]],
                    "summary": cluster["summary"],
                },
            )
            rep_node_id = f"archive:{representative['task_id']}:{rep_hypothesis['id']}"
            self._append_node(
                nodes,
                node_ids,
                {
                    "id": rep_node_id,
                    "type": "hypothesis_reference",
                    "label": rep_hypothesis["title"],
                    "task_id": representative["task_id"],
                    "novelty_score": rep_hypothesis.get("novelty_score"),
                    "feasibility_score": rep_hypothesis.get("feasibility_score"),
                },
            )
            self._append_edge(edges, edge_keys, cluster_node_id, rep_node_id, "represented_by")
            if rep_hypothesis.get("opportunity_zone"):
                concept_id = f"concept:{rep_hypothesis['opportunity_zone']}"
                self._append_node(
                    nodes,
                    node_ids,
                    {
                        "id": concept_id,
                        "type": "concept",
                        "label": rep_hypothesis["opportunity_zone"],
                    },
                )
                self._append_edge(edges, edge_keys, concept_id, cluster_node_id, "distills_hypothesis_family")

            contradiction = rep_hypothesis.get("contradiction")
            if contradiction:
                contradiction_id = contradiction["id"]
                self._append_node(
                    nodes,
                    node_ids,
                    {
                        "id": contradiction_id,
                        "type": "contradiction",
                        "label": contradiction["statement"],
                        "severity": contradiction["severity"],
                    },
                )
                self._append_edge(edges, edge_keys, cluster_node_id, contradiction_id, "tracks_contradiction")

            for path in rep_hypothesis.get("solution_paths", []):
                self._append_node(
                    nodes,
                    node_ids,
                    {
                        "id": path["id"],
                        "type": "solution_path",
                        "label": path["title"],
                    },
                )
                self._append_edge(edges, edge_keys, cluster_node_id, path["id"], "tracks_solution_path")

            telemetry_events.append(
                {
                    "event": "distillation_cluster_created",
                    "cluster_id": cluster_id,
                    "representative_hypothesis": rep_hypothesis["id"],
                    "supporting_count": len(cluster["supporting"]),
                }
            )
            distilled_clusters.append(
                {
                    "cluster_id": cluster_id,
                    "title": cluster["title"],
                    "representative_hypothesis": rep_hypothesis["id"],
                    "supporting_hypotheses": [item["hypothesis"]["id"] for item in cluster["supporting"]],
                    "summary": cluster["summary"],
                }
            )

        updated_map["nodes"] = nodes
        updated_map["edges"] = edges
        updated_map["entities"] = nodes
        updated_map["relationships"] = edges
        return {
            "type": "KNOWLEDGE_DISTILLATION_REPORT",
            "triggered": True,
            "cycle_count": cycle_count,
            "node_count": node_count,
            "trigger_reason": "cycle_interval" if cycle_count % self.DISTILLATION_INTERVAL == 0 else "node_threshold",
            "distilled_clusters": distilled_clusters,
            "updated_discovery_map": updated_map,
            "telemetry_events": telemetry_events,
        }

    def _cluster_archive(self, hypothesis_archive: list[dict[str, Any]]) -> list[dict[str, Any]]:
        working = [item for item in hypothesis_archive if item["hypothesis"].get("statement")]
        consumed: set[int] = set()
        clusters = []
        for index, item in enumerate(working):
            if index in consumed:
                continue
            group = [item]
            consumed.add(index)
            base_tokens = self._tokens(item["hypothesis"]["title"] + " " + item["hypothesis"]["statement"])
            for other_index, other in enumerate(working[index + 1 :], start=index + 1):
                if other_index in consumed:
                    continue
                similarity = self._similarity(
                    base_tokens,
                    self._tokens(other["hypothesis"]["title"] + " " + other["hypothesis"]["statement"]),
                )
                if similarity >= self.SIMILARITY_THRESHOLD:
                    group.append(other)
                    consumed.add(other_index)
            if len(group) < 2:
                continue
            representative = max(
                group,
                key=lambda entry: (
                    entry["hypothesis"].get("novelty_score", 0),
                    entry["hypothesis"].get("feasibility_score", 0),
                    entry["hypothesis"].get("confidence", 0.0),
                ),
            )
            signature = representative["hypothesis"]["title"] + representative["hypothesis"]["statement"]
            cluster_id = f"D-{int(hashlib.md5(signature.encode('utf-8')).hexdigest(), 16) % 1000:03d}"
            supporting = [entry for entry in group if entry is not representative]
            clusters.append(
                {
                    "cluster_id": cluster_id,
                    "title": representative["hypothesis"]["title"],
                    "representative": representative,
                    "supporting": supporting,
                    "summary": (
                        f"Distilled hypothesis family centered on {representative['hypothesis']['title']} "
                        f"with {len(supporting)} supporting variants."
                    ),
                }
            )
        return clusters

    def _similarity(self, left: set[str], right: set[str]) -> float:
        if not left or not right:
            return 0.0
        return len(left & right) / len(left | right)

    def _tokens(self, text: str) -> set[str]:
        return {
            token
            for token in re.findall(r"[a-z][a-z0-9_-]{3,}", text.lower())
        }

    def _append_node(self, nodes: list[dict[str, Any]], node_ids: set[str], node: dict[str, Any]) -> None:
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
    ) -> None:
        key = (source, target, edge_type)
        if key in edge_keys:
            return
        edges.append({"from": source, "to": target, "type": edge_type})
        edge_keys.add(key)
