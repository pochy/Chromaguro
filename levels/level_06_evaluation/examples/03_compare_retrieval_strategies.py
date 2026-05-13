from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import (
    add_records,
    load_json,
    query_records,
    recreate_collection,
    result_rows,
    sparse_keyword_scores,
    weighted_reciprocal_rank_fusion,
)


def recall(retrieved: list[str], expected: set[str]) -> float:
    return len(set(retrieved) & expected) / len(expected)


def main() -> None:
    base = Path(__file__).resolve().parents[1] / "data"
    records = load_json(base / "eval_records.json")
    questions = load_json(base / "eval_questions.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level06_compare_strategies")
    add_records(collection, records)

    for item in questions:
        question = item["question"]
        expected = set(item["relevant_ids"])
        dense_ids = [row["id"] for row in result_rows(query_records(collection, question, n_results=3))]
        sparse_ids = [record_id for record_id, _score in sparse_keyword_scores(question, records)[:3]]
        hybrid_ids = [
            record_id
            for record_id, _score in weighted_reciprocal_rank_fusion([dense_ids, sparse_ids], weights=[0.7, 0.3])[:3]
        ]

        print(f"\nQ: {question}")
        print(f"dense  recall@3={recall(dense_ids, expected):.2f} {dense_ids}")
        print(f"sparse recall@3={recall(sparse_ids, expected):.2f} {sparse_ids}")
        print(f"hybrid recall@3={recall(hybrid_ids, expected):.2f} {hybrid_ids}")


if __name__ == "__main__":
    main()
