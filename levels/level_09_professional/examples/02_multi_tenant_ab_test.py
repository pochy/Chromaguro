from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, load_json, query_records, recreate_collection, result_rows


def where_all(filters: list[dict[str, Any]]) -> dict[str, Any]:
    if len(filters) == 1:
        return filters[0]
    return {"$and": filters}


def search_ids(collection: Any, question: str, tenant_id: str, chunker_version: str | None = None) -> list[str]:
    filters = [{"tenant_id": {"$eq": tenant_id}}]
    if chunker_version:
        filters.append({"chunker_version": {"$eq": chunker_version}})
    result = query_records(collection, question, n_results=3, where=where_all(filters))
    return [row["id"] for row in result_rows(result)]


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "advanced_records.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level09_multi_tenant")
    add_records(collection, records)

    question = "Chroma の永続化方法は？"

    print("\n## Tenant isolation")
    print(f"tenant_a: {search_ids(collection, question, tenant_id='tenant_a')}")
    print(f"tenant_b: {search_ids(collection, question, tenant_id='tenant_b')}")

    print("\n## Chunker A/B")
    print(f"tenant_a chunker v1: {search_ids(collection, question, tenant_id='tenant_a', chunker_version='v1')}")
    print(f"tenant_a chunker v2: {search_ids(collection, question, tenant_id='tenant_a', chunker_version='v2')}")


if __name__ == "__main__":
    main()

