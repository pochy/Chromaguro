from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, keyword_score, load_json, query_records, recreate_collection, result_rows


def classify_failure(question: str, retrieved_ids: list[str], relevant_ids: set[str], records_by_id: dict[str, str]) -> str:
    if set(retrieved_ids) & relevant_ids:
        return "no_failure"

    expected_documents = [records_by_id[record_id] for record_id in relevant_ids if record_id in records_by_id]
    if not expected_documents:
        return "source_document_missing"

    best_expected_score = max(keyword_score(question, document) for document in expected_documents)
    if best_expected_score == 0:
        return "query_vocabulary_gap"

    return "retrieval_ranking_failure"


def main() -> None:
    base = Path(__file__).resolve().parents[1] / "data"
    records = load_json(base / "eval_records.json")
    questions = load_json(base / "eval_questions.json")
    records_by_id = {record["id"]: record["document"] for record in records}

    client = chromadb.Client()
    collection = recreate_collection(client, "level06_failure_analysis")
    add_records(collection, records)

    k = 1
    for item in questions:
        result = query_records(collection, item["question"], n_results=k)
        retrieved_ids = [row["id"] for row in result_rows(result)]
        relevant_ids = set(item["relevant_ids"])
        failure_type = classify_failure(item["question"], retrieved_ids, relevant_ids, records_by_id)

        print(f"\nQ: {item['question']}")
        print(f"expected: {sorted(relevant_ids)}")
        print(f"retrieved@{k}: {retrieved_ids}")
        print(f"failure_type: {failure_type}")


if __name__ == "__main__":
    main()

