from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, query_records, recreate_collection, result_rows


memory_records = [
    {
        "id": "mem_semantic_user_pref",
        "document": "ユーザーは簡潔な回答より、判断理由と tradeoff がある回答を好みます。",
        "metadata": {"type": "semantic", "phase": "planning", "scope": "user", "confidence": 0.9},
    },
    {
        "id": "mem_procedural_chroma",
        "document": "Chroma の質問では、まず collection, metadata, embedding, evaluation の観点に分けて回答します。",
        "metadata": {"type": "procedural", "phase": "execution", "scope": "global", "confidence": 0.8},
    },
    {
        "id": "mem_episodic_success",
        "document": "前回は hybrid search と source 表示を組み合わせた説明が役に立ちました。",
        "metadata": {"type": "episodic", "phase": "evaluation", "scope": "user", "confidence": 0.7},
    },
]


def memories_for_phase(collection: Any, query: str, phase: str) -> list[dict[str, Any]]:
    result = query_records(
        collection,
        query,
        n_results=3,
        where={
            "$or": [
                {"phase": {"$eq": phase}},
                {"type": {"$eq": "semantic"}},
            ]
        },
    )
    return result_rows(result)


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level09_agentic_memory")
    add_records(collection, memory_records)

    query = "Chroma の tutorial 改善計画を立てたい"
    for phase in ["planning", "execution", "evaluation"]:
        print(f"\n## memories for {phase}")
        for row in memories_for_phase(collection, query, phase):
            print(f"- {row['id']} type={row['metadata']['type']} confidence={row['metadata']['confidence']}")
            print(f"  {row['document']}")


if __name__ == "__main__":
    main()
