from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import (
    example_db_path,
    print_results,
    query_records,
    upsert_records,
)

records = [
    {
        "id": "persistent_client_001",
        "document": "Chroma の PersistentClient は指定した path に collection を保存します。",
        "metadata": {"source": "clients.md", "section": "persistent", "lang": "ja"},
    },
    {
        "id": "in_memory_client_001",
        "document": "chromadb.Client は短い実験に向いた in-memory client です。",
        "metadata": {"source": "clients.md", "section": "in-memory", "lang": "ja"},
    },
]


def main() -> None:
    client = chromadb.PersistentClient(path=example_db_path(__file__))
    collection = client.get_or_create_collection(
        name="level01_persistent",
        embedding_function=None,
    )
    upsert_records(collection, records)

    print(f"collection count: {collection.count()}")
    result = query_records(
        collection, "Chroma のデータを保存して再利用したい", n_results=2
    )
    print_results("PersistentClient", result)


if __name__ == "__main__":
    main()
