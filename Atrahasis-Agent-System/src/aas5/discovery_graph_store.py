from __future__ import annotations

from pathlib import Path
from typing import Any

from aas5.common import ensure_dir, load_json, runtime_state_dir, utc_now, write_json


class DiscoveryGraphStore:
    """Durable discovery graph persistence for AAS5."""

    def __init__(self, repo_root: Path) -> None:
        self.root = ensure_dir(runtime_state_dir(repo_root) / "discovery_graphs")

    def load_latest(self, task_id: str) -> dict[str, Any] | None:
        path = self.root / task_id / "latest.json"
        if not path.exists():
            return None
        payload = load_json(path)
        return payload.get("graph")

    def persist(
        self,
        *,
        task_id: str,
        workflow_id: str,
        stage_name: str,
        discovery_map: dict[str, Any],
    ) -> tuple[dict[str, Any], str]:
        merged = self.merge_graphs(
            prior_graph=self.load_latest(task_id) or {},
            current_graph=discovery_map,
        )
        payload = {
            "type": "DISCOVERY_GRAPH_SNAPSHOT",
            "task_id": task_id,
            "workflow_id": workflow_id,
            "stage": stage_name,
            "updated_at": utc_now(),
            "graph": merged,
        }
        task_root = ensure_dir(self.root / task_id)
        path = task_root / f"{workflow_id}-{stage_name}.json"
        write_json(path, payload)
        write_json(task_root / "latest.json", payload)
        return merged, str(path)

    def merge_graphs(
        self,
        *,
        prior_graph: dict[str, Any],
        current_graph: dict[str, Any],
    ) -> dict[str, Any]:
        if not prior_graph:
            return dict(current_graph)
        nodes_by_id = {
            node["id"]: dict(node)
            for node in prior_graph.get("nodes", prior_graph.get("entities", []))
        }
        for node in current_graph.get("nodes", current_graph.get("entities", [])):
            nodes_by_id[node["id"]] = {**nodes_by_id.get(node["id"], {}), **dict(node)}
        edges_by_key = {
            (edge["from"], edge["to"], edge["type"]): dict(edge)
            for edge in prior_graph.get("edges", prior_graph.get("relationships", []))
        }
        for edge in current_graph.get("edges", current_graph.get("relationships", [])):
            edges_by_key[(edge["from"], edge["to"], edge["type"])] = dict(edge)
        merged = dict(prior_graph)
        merged.update({key: value for key, value in current_graph.items() if key not in {"nodes", "edges", "entities", "relationships"}})
        merged["nodes"] = list(nodes_by_id.values())
        merged["edges"] = list(edges_by_key.values())
        merged["entities"] = merged["nodes"]
        merged["relationships"] = merged["edges"]
        return merged
