from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, recreate_collection, result_rows, query_records


records = [
    {
        "id": "doc_persistence",
        "document": "PersistentClient は Chroma のデータをローカルディスクに保存します。",
        "metadata": {"topic": "client", "page": 1},
    },
    {
        "id": "doc_filtering",
        "document": "where filter は metadata を使って検索範囲を絞ります。",
        "metadata": {"topic": "filter", "page": 2},
    },
    {
        "id": "doc_fulltext",
        "document": "where_document は document 本文に含まれる文字列や正規表現を条件にできます。",
        "metadata": {"topic": "filter", "page": 3},
    },
]


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level01_query_vs_get")
    add_records(collection, records)

    print("\n## get: ID や filter で取り出す。similarity ranking はしない")
    get_result = collection.get(ids=["doc_filtering"], include=["documents", "metadatas"])
    print(get_result)

    print("\n## query: embedding 距離で近い順に探す")
    query_result = query_records(collection, "本文検索と metadata filter の違いは？", n_results=3)
    for row in result_rows(query_result):
        print(f"{row['rank']}. {row['id']} distance={row['distance']:.4f} topic={row['metadata']['topic']}")

    print("\n## include: 返す field を選ぶ")
    include_result = collection.query(
        query_embeddings=[[0.0] * 64],
        n_results=1,
        include=["metadatas"],
    )
    print(include_result)


if __name__ == "__main__":
    main()
