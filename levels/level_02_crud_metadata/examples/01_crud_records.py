from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import embed_texts, example_db_path, print_results, query_records, recreate_collection


def main() -> None:
    client = chromadb.PersistentClient(path=example_db_path(__file__))
    collection = recreate_collection(client, "level02_crud")

    first_document = "Chroma は AI アプリケーション向けの検索基盤です。"
    collection.add(
        ids=["doc_001"],
        documents=[first_document],
        metadatas=[{"source": "tutorial.md", "doc_type": "intro", "lang": "ja"}],
        embeddings=embed_texts([first_document]),
    )

    updated_document = "Chroma は RAG に渡す context を選ぶための検索基盤です。"
    collection.update(
        ids=["doc_001"],
        documents=[updated_document],
        metadatas=[{"source": "tutorial.md", "doc_type": "intro", "lang": "ja", "version": 2}],
        embeddings=embed_texts([updated_document]),
    )

    upsert_document = "upsert は既存 record があれば更新し、なければ追加します。"
    collection.upsert(
        ids=["doc_002"],
        documents=[upsert_document],
        metadatas=[{"source": "tutorial.md", "doc_type": "operation", "lang": "ja"}],
        embeddings=embed_texts([upsert_document]),
    )

    print("get doc_001:")
    print(collection.get(ids=["doc_001"]))

    result = query_records(collection, "RAG の context を選ぶには？", n_results=2)
    print_results("After update and upsert", result)

    collection.delete(ids=["doc_002"])
    print(f"\ncount after delete: {collection.count()}")


if __name__ == "__main__":
    main()

