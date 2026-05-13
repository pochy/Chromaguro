from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import (
    add_records,
    compact_document,
    example_db_path,
    keyword_score,
    mmr_select,
    query_records,
    recreate_collection,
    result_rows,
    weighted_reciprocal_rank_fusion,
    write_jsonl,
)


DOCS_DIR = Path(__file__).resolve().parents[1] / "data" / "final_project_docs"
COLLECTION_NAME = "level09_final_project"
CHUNKER_VERSION = "heading-v1"
EMBEDDING_MODEL = "tutorial-hash-embedding"


def doc_type_for(path: Path) -> str:
    if "client" in path.stem:
        return "client_guide"
    if "quality" in path.stem:
        return "retrieval_design"
    return "operations"


def split_markdown(path: Path) -> list[dict[str, Any]]:
    title = path.stem
    current_heading = "Overview"
    current_lines: list[str] = []
    chunks: list[dict[str, Any]] = []

    def flush() -> None:
        if not current_lines:
            return
        body = "\n".join(line for line in current_lines if line.strip()).strip()
        if not body:
            return
        chunk_index = len(chunks)
        chunks.append(
            {
                "id": f"capstone_{path.stem}_{chunk_index:03d}",
                "document": f"{title}\n{current_heading}\n{body}",
                "metadata": {
                    "tenant_id": "personal",
                    "source": f"final_project_docs/{path.name}",
                    "title": title,
                    "section": current_heading,
                    "doc_type": doc_type_for(path),
                    "chunk_index": chunk_index,
                    "chunker_version": CHUNKER_VERSION,
                    "embedding_model": EMBEDDING_MODEL,
                },
            }
        )

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            title = line.removeprefix("# ").strip()
            continue
        if line.startswith("## "):
            flush()
            current_heading = line.removeprefix("## ").strip()
            current_lines = []
            continue
        current_lines.append(line)

    flush()
    return chunks


def load_project_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        records.extend(split_markdown(path))
    return records


def expand_query(question: str) -> str:
    expansions = []
    if re.search(r"永続|保存|client|server|path", question, re.IGNORECASE):
        expansions.append("PersistentClient HttpClient path local storage collection")
    if re.search(r"tenant|権限|filter|metadata", question, re.IGNORECASE):
        expansions.append("tenant_id metadata where access control permission")
    if re.search(r"source|参照|根拠|citation", question, re.IGNORECASE):
        expansions.append("source section chunk_id citation display")
    if re.search(r"評価|品質|recall|失敗|ログ", question, re.IGNORECASE):
        expansions.append("evaluation recall precision MRR failure_type query logging")
    if re.search(r"SKU|エラー|関数|keyword|hybrid", question, re.IGNORECASE):
        expansions.append("keyword exact full-text hybrid RRF dense sparse")
    return " ".join([question, *expansions])


def build_where(tenant_id: str, doc_type: str | None = None) -> dict[str, Any]:
    filters: list[dict[str, Any]] = [{"tenant_id": {"$eq": tenant_id}}]
    if doc_type:
        filters.append({"doc_type": {"$eq": doc_type}})
    if len(filters) == 1:
        return filters[0]
    return {"$and": filters}


def keyword_ranking(collection: Any, query: str, where: dict[str, Any]) -> list[str]:
    records = collection.get(where=where, include=["documents"])
    scored = sorted(
        zip(records["ids"], records["documents"], strict=True),
        key=lambda item: keyword_score(query, item[1]),
        reverse=True,
    )
    return [record_id for record_id, _document in scored]


def rows_by_id(collection: Any, ids: list[str]) -> dict[str, dict[str, Any]]:
    records = collection.get(ids=ids, include=["documents", "metadatas"])
    return {
        record_id: {
            "id": record_id,
            "document": document,
            "metadata": metadata or {},
        }
        for record_id, document, metadata in zip(
            records["ids"],
            records["documents"],
            records["metadatas"],
            strict=True,
        )
    }


def retrieve(
    collection: Any,
    question: str,
    tenant_id: str = "personal",
    doc_type: str | None = None,
    n_candidates: int = 6,
) -> dict[str, Any]:
    expanded = expand_query(question)
    where = build_where(tenant_id=tenant_id, doc_type=doc_type)
    dense_result = query_records(collection, expanded, n_results=n_candidates, where=where)
    dense_ids = [row["id"] for row in result_rows(dense_result)]
    keyword_ids = keyword_ranking(collection, expanded, where)
    fused = weighted_reciprocal_rank_fusion([dense_ids, keyword_ids], weights=[0.7, 0.3])
    fused_ids = [record_id for record_id, _score in fused[:n_candidates]]
    by_id = rows_by_id(collection, fused_ids)
    fused_rows = [by_id[record_id] for record_id in fused_ids if record_id in by_id]
    selected_context = mmr_select(expanded, fused_rows, limit=3)

    return {
        "question": question,
        "expanded": expanded,
        "dense_ids": dense_ids,
        "keyword_ids": keyword_ids[:n_candidates],
        "fused_ids": fused_ids,
        "context": selected_context,
    }


def print_context(context: list[dict[str, Any]]) -> None:
    for index, row in enumerate(context, start=1):
        metadata = row["metadata"]
        print(f"{index}. {row['id']} source={metadata['source']} section={metadata['section']}")
        print(f"   {compact_document(row['document'], limit=160)}")


def evaluate(collection: Any) -> list[dict[str, Any]]:
    gold_cases = [
        {
            "question": "Chroma をローカルで永続化するには？",
            "relevant_ids": {"capstone_chroma_clients_000"},
        },
        {
            "question": "tenant ごとの検索漏れを防ぐには？",
            "relevant_ids": {"capstone_retrieval_quality_000", "capstone_operations_runbook_002"},
        },
        {
            "question": "検索品質をどう評価してログに残す？",
            "relevant_ids": {"capstone_retrieval_quality_003", "capstone_operations_runbook_001"},
        },
    ]

    report = []
    for case in gold_cases:
        retrieval = retrieve(collection, case["question"])
        retrieved = retrieval["fused_ids"][:5]
        relevant = case["relevant_ids"]
        hits = [record_id for record_id in retrieved if record_id in relevant]
        report.append(
            {
                "question": case["question"],
                "retrieved_ids": retrieved,
                "relevant_ids": sorted(relevant),
                "recall_at_5": len(hits) / len(relevant),
            }
        )
    return report


def main() -> None:
    records = load_project_records()
    client = chromadb.PersistentClient(path=example_db_path(__file__))
    collection = recreate_collection(client, COLLECTION_NAME)
    add_records(collection, records)

    question = "Chroma で永続化して、回答に source を出すには？"
    retrieval = retrieve(collection, question)

    print("\n## Ingest")
    print(f"documents: {len(list(DOCS_DIR.glob('*.md')))}")
    print(f"chunks: {len(records)}")
    print(f"collection: {COLLECTION_NAME}")

    print("\n## Retrieval Pipeline")
    print(f"question: {retrieval['question']}")
    print(f"expanded: {retrieval['expanded']}")
    print(f"dense: {retrieval['dense_ids'][:3]}")
    print(f"keyword: {retrieval['keyword_ids'][:3]}")
    print(f"fused: {retrieval['fused_ids'][:3]}")

    print("\n## Selected Context")
    print_context(retrieval["context"])

    first = retrieval["context"][0]
    print("\n## Mock Answer")
    print(compact_document(first["document"], limit=180))
    print(f"参照: {first['metadata']['source']} section={first['metadata']['section']} chunk_id={first['id']}")

    report = evaluate(collection)
    print("\n## Mini Evaluation")
    for row in report:
        print(f"recall@5={row['recall_at_5']:.2f} question={row['question']}")

    write_jsonl(
        Path(__file__).resolve().parent / "eval_logs.jsonl",
        [
            {
                "question": retrieval["question"],
                "expanded": retrieval["expanded"],
                "retrieved_ids": retrieval["fused_ids"][:5],
                "selected_context_ids": [row["id"] for row in retrieval["context"]],
            },
            *report,
        ],
    )


if __name__ == "__main__":
    main()
