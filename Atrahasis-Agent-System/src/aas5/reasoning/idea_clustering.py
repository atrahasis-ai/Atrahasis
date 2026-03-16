from __future__ import annotations

from collections import defaultdict
from typing import Any


class IdeaClusteringEngine:
    def run(self, *, hypothesis_packet: dict[str, Any]) -> dict[str, Any]:
        buckets: dict[str, list[str]] = defaultdict(list)
        for hypothesis in hypothesis_packet["hypotheses"]:
            buckets[hypothesis["opportunity_zone"]].append(hypothesis["id"])
        return {
            "type": "IDEA_CLUSTER_REPORT",
            "clusters": [{"cluster": cluster, "hypotheses": hypothesis_ids} for cluster, hypothesis_ids in buckets.items()],
        }
