from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, load_json, print_results, query_records, recreate_collection


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level02_metadata")

    records = load_json(Path(__file__).resolve().parents[1] / "data" / "support_records.json")
    add_records(collection, records)

    query = "ユーザーを招待する方法を知りたい"
    all_results = query_records(collection, query, n_results=3)
    print_results("No filter", all_results)

    filtered_results = query_records(
        collection,
        query,
        n_results=3,
        where={
            "$and": [
                {"tenant_id": {"$eq": "tenant_a"}},
                {"doc_type": {"$eq": "manual"}},
            ]
        },
    )
    print_results("tenant_a manual only", filtered_results)


if __name__ == "__main__":
    main()

