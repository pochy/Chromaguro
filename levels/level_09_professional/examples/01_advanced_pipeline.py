from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import (
    add_records,
    compact_document,
    keyword_score,
    load_json,
    query_records,
    reciprocal_rank_fusion,
    recreate_collection,
    result_rows,
    write_jsonl,
)


def rewrite_query(question: str) -> str:
    return question.strip().replace("保存方法", "永続化 方法")


def expand_query(query: str) -> str:
    expansions = []
    if "永続" in query or "保存" in query:
        expansions.append("PersistentClient path local storage persistence")
    if "SKU" in query or "useEffect" in query:
        expansions.append("exact keyword where_document contains")
    if "metadata" in query or "tenant" in query:
        expansions.append("where filter access control")
    return " ".join([query, *expansions])


def tenant_where(tenant_id: str) -> dict[str, Any]:
    return {"tenant_id": {"$eq": tenant_id}}


def keyword_ranking(collection: Any, query: str, tenant_id: str) -> list[str]:
    records = collection.get(where=tenant_where(tenant_id), include=["documents", "metadatas"])
    pairs = sorted(
        zip(records["ids"], records["documents"], strict=True),
        key=lambda item: keyword_score(query, item[1]),
        reverse=True,
    )
    return [record_id for record_id, _document in pairs]


def build_context(fused_ids: list[str], records_by_id: dict[str, dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    context = []
    for record_id in fused_ids[:limit]:
        record = records_by_id[record_id]
        context.append(
            {
                "id": record_id,
                "document": compact_document(record["document"], limit=180),
                "metadata": record["metadata"],
            }
        )
    return context


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "advanced_records.json")
    records_by_id = {record["id"]: record for record in records}

    client = chromadb.Client()
    collection = recreate_collection(client, "level09_advanced")
    add_records(collection, records)

    question = "Chroma の保存方法は？"
    tenant_id = "tenant_a"
    rewritten = rewrite_query(question)
    expanded = expand_query(rewritten)

    dense_result = query_records(collection, expanded, n_results=5, where=tenant_where(tenant_id))
    dense_ranking = [row["id"] for row in result_rows(dense_result)]
    lexical_ranking = keyword_ranking(collection, expanded, tenant_id)
    fused = reciprocal_rank_fusion([dense_ranking, lexical_ranking])
    fused_ids = [record_id for record_id, _score in fused]
    context = build_context(fused_ids, records_by_id)

    print("\n## Pipeline")
    print(f"question: {question}")
    print(f"rewritten: {rewritten}")
    print(f"expanded: {expanded}")

    print("\n## Fused context")
    for index, item in enumerate(context, start=1):
        metadata = item["metadata"]
        print(f"{index}. {item['id']} source={metadata['source']} section={metadata['section']}")
        print(f"   {item['document']}")

    answer = context[0]["document"]
    print("\n## Mock answer")
    print(answer)
    print(f"参照: {context[0]['metadata']['source']} chunk_id={context[0]['id']}")

    write_jsonl(
        Path(__file__).resolve().parent / "eval_logs.jsonl",
        [
            {
                "question": question,
                "tenant_id": tenant_id,
                "rewritten": rewritten,
                "expanded": expanded,
                "retrieved_ids": fused_ids[:5],
            }
        ],
    )


if __name__ == "__main__":
    main()

