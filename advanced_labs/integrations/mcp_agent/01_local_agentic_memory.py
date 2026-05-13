from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, query_records, recreate_collection, result_rows


def main() -> None:
    client = chromadb.PersistentClient(path=str(Path(__file__).resolve().parent / "agent_memory_db"))
    collection = recreate_collection(client, "agent_memory")
    add_records(
        collection,
        [
            {
                "id": "memory_semantic_001",
                "document": "ユーザーは Chroma を SQLite ではなく retrieval 基盤として理解したい。",
                "metadata": {"type": "semantic", "scope": "user", "confidence": 0.95},
            },
            {
                "id": "memory_procedural_001",
                "document": "Chroma の説明では、chunking, metadata, evaluation の順に確認する。",
                "metadata": {"type": "procedural", "scope": "global", "confidence": 0.85},
            },
            {
                "id": "memory_episodic_001",
                "document": "README を先に整備すると、学習者が迷わず Level 1 に進めた。",
                "metadata": {"type": "episodic", "scope": "project", "confidence": 0.75},
            },
        ],
    )

    result = query_records(
        collection,
        "チュートリアル改善時に何を優先する？",
        where={"type": {"$in": ["semantic", "procedural"]}},
        n_results=3,
    )
    for row in result_rows(result):
        print(f"{row['id']} type={row['metadata']['type']}: {row['document']}")


if __name__ == "__main__":
    main()
