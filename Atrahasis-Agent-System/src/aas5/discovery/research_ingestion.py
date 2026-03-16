from __future__ import annotations

from typing import Any

from aas5.common import category_for_path


class ResearchIngestionEngine:
    def run(self, *, manifest: list[dict[str, Any]], task_workspace: list[dict[str, Any]]) -> dict[str, Any]:
        evidence = []
        for item in manifest:
            evidence.append(
                {
                    "path": item["path"],
                    "category": item["category"],
                    "summary": item["summary"],
                    "word_count": item["word_count"],
                    "invention_ids": item["invention_ids"],
                    "task_ids": item["task_ids"],
                    "text": item["text"],
                }
            )
        return {
            "type": "RESEARCH_INGESTION_REPORT",
            "evidence": evidence,
            "task_workspace_records": task_workspace,
            "inventory": {
                "documents": len(manifest),
                "categories": sorted({item["category"] for item in manifest}),
            },
        }
