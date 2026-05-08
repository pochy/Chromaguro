from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, print_results, query_records, recreate_collection


records = [
    {
        "id": "embedding_policy_001",
        "document": "embedding model を変更した場合は、既存 chunk を再 embedding して別 collection で評価します。",
        "metadata": {
            "source": "embedding_policy.md",
            "doc_type": "policy",
            "embedding_model": "tutorial-hash-embedding",
            "embedding_version": "v1",
            "chunker_version": "heading-v1",
        },
    },
    {
        "id": "chunker_policy_001",
        "document": "chunker_version を metadata に残すと、chunking 改善前後の検索品質を比較できます。",
        "metadata": {
            "source": "embedding_policy.md",
            "doc_type": "policy",
            "embedding_model": "tutorial-hash-embedding",
            "embedding_version": "v1",
            "chunker_version": "paragraph-v2",
        },
    },
]


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level03_embedding_versions")
    add_records(collection, records)

    result = query_records(
        collection,
        "embedding model を変えたら何をする？",
        n_results=2,
        where={"embedding_version": {"$eq": "v1"}},
    )
    print_results("Embedding version filter", result)

    print("\n設計メモ:")
    print("model や chunker を変えたら、同じ collection を上書きする前に別 collection で評価します。")


if __name__ == "__main__":
    main()

