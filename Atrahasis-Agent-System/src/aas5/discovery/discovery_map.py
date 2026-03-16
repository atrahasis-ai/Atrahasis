from __future__ import annotations

from collections import Counter
from typing import Any


class DiscoveryMap:
    def run(self, *, synthesis_report: dict[str, Any], quality_report: dict[str, Any]) -> dict[str, Any]:
        evidence = quality_report["ranked_evidence"][:60]
        category_counts = Counter(item["category"] for item in evidence)
        problem_clusters = [
            {"name": category, "signal": count}
            for category, count in category_counts.most_common(8)
        ]
        cluster_evidence: dict[str, list[str]] = {}
        for cluster in problem_clusters:
            cluster_evidence[cluster["name"]] = [
                item["path"] for item in evidence if item["category"] == cluster["name"]
            ][:8]

        domain_links = (
            [
                {"domain": keyword, "linked_cluster": problem_clusters[index % len(problem_clusters)]["name"]}
                for index, keyword in enumerate(synthesis_report["top_keywords"][:8])
            ]
            if problem_clusters
            else []
        )

        nodes = [
            {
                "id": f"cluster:{cluster['name']}",
                "type": "cluster",
                "label": cluster["name"],
                "signal": cluster["signal"],
            }
            for cluster in problem_clusters
        ]
        concept_nodes = []
        concept_edges = []
        for link in domain_links:
            concept_id = f"concept:{link['domain']}"
            concept_nodes.append(
                {
                    "id": concept_id,
                    "type": "concept",
                    "label": link["domain"],
                    "linked_cluster": link["linked_cluster"],
                }
            )
            concept_edges.append(
                {
                    "from": concept_id,
                    "to": f"cluster:{link['linked_cluster']}",
                    "type": "belongs_to_cluster",
                }
            )

        evidence_nodes = []
        evidence_edges = []
        for item in evidence[:30]:
            evidence_id = f"evidence:{item['path']}"
            evidence_nodes.append(
                {
                    "id": evidence_id,
                    "type": "evidence",
                    "label": item["path"],
                    "category": item["category"],
                }
            )
            evidence_edges.append(
                {
                    "from": evidence_id,
                    "to": f"cluster:{item['category']}",
                    "type": "supports_cluster",
                }
            )

        nodes.extend(concept_nodes)
        nodes.extend(evidence_nodes)
        edges = concept_edges + evidence_edges
        return {
            "type": "DISCOVERY_MAP",
            "nodes": nodes,
            "edges": edges,
            "entities": nodes,
            "relationships": edges,
            "problem_clusters": problem_clusters,
            "domain_links": domain_links,
            "evidence_refs": [item["path"] for item in evidence[:40]],
            "cluster_evidence": cluster_evidence,
        }

    def link_invention_graph(
        self,
        *,
        discovery_map: dict[str, Any],
        hypothesis_packet: dict[str, Any],
        contradiction_map: dict[str, Any],
        solution_paths: dict[str, Any],
    ) -> dict[str, Any]:
        nodes = [dict(node) for node in discovery_map.get("nodes", discovery_map.get("entities", []))]
        edges = [dict(edge) for edge in discovery_map.get("edges", discovery_map.get("relationships", []))]
        node_ids = {node["id"] for node in nodes}
        edge_keys = {(edge["from"], edge["to"], edge["type"]) for edge in edges}

        contradictions_by_hypothesis = {
            item["hypothesis_id"]: item for item in contradiction_map["contradictions"]
        }
        solution_paths_by_hypothesis: dict[str, list[dict[str, Any]]] = {}
        for path in solution_paths["candidate_paths"]:
            solution_paths_by_hypothesis.setdefault(path["hypothesis_id"], []).append(path)

        for hypothesis in hypothesis_packet["hypotheses"]:
            concept_id = f"concept:{hypothesis['opportunity_zone']}"
            hypothesis_id = hypothesis["id"]
            if concept_id not in node_ids:
                nodes.append(
                    {
                        "id": concept_id,
                        "type": "concept",
                        "label": hypothesis["opportunity_zone"],
                    }
                )
                node_ids.add(concept_id)
            if hypothesis_id not in node_ids:
                nodes.append(
                    {
                        "id": hypothesis_id,
                        "type": "hypothesis",
                        "label": hypothesis["title"],
                        "statement": hypothesis["statement"],
                        "novelty_score": hypothesis["novelty_score"],
                        "feasibility_score": hypothesis["feasibility_score"],
                    }
                )
                node_ids.add(hypothesis_id)
            self._append_edge(edges, edge_keys, concept_id, hypothesis_id, "generates_hypothesis")

            for research_item in hypothesis["supporting_research"]:
                evidence_id = f"evidence:{research_item['evidence_ref']}"
                if evidence_id not in node_ids:
                    nodes.append(
                        {
                            "id": evidence_id,
                            "type": "evidence",
                            "label": research_item["evidence_ref"],
                        }
                    )
                    node_ids.add(evidence_id)
                self._append_edge(edges, edge_keys, evidence_id, hypothesis_id, "supports_hypothesis")

            contradiction = contradictions_by_hypothesis.get(hypothesis_id)
            if contradiction is not None:
                contradiction_id = contradiction["id"]
                if contradiction_id not in node_ids:
                    nodes.append(
                        {
                            "id": contradiction_id,
                            "type": "contradiction",
                            "label": contradiction["contradiction"],
                            "severity": contradiction["severity"],
                        }
                    )
                    node_ids.add(contradiction_id)
                self._append_edge(edges, edge_keys, contradiction_id, hypothesis_id, "challenges_hypothesis")

            for path in solution_paths_by_hypothesis.get(hypothesis_id, []):
                path_id = path["id"]
                if path_id not in node_ids:
                    nodes.append(
                        {
                            "id": path_id,
                            "type": "solution_path",
                            "label": path["title"],
                            "tradeoffs": path["tradeoffs"],
                        }
                    )
                    node_ids.add(path_id)
                self._append_edge(edges, edge_keys, hypothesis_id, path_id, "proposes_solution_path")

        enriched_map = dict(discovery_map)
        enriched_map["nodes"] = nodes
        enriched_map["edges"] = edges
        enriched_map["entities"] = nodes
        enriched_map["relationships"] = edges
        enriched_map["graph_stats"] = {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "concept_count": sum(1 for node in nodes if node["type"] == "concept"),
            "hypothesis_count": sum(1 for node in nodes if node["type"] == "hypothesis"),
            "contradiction_count": sum(1 for node in nodes if node["type"] == "contradiction"),
            "solution_path_count": sum(1 for node in nodes if node["type"] == "solution_path"),
        }
        return enriched_map

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
