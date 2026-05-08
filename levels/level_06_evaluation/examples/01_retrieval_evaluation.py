from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, load_json, query_records, recreate_collection, result_rows


def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    if not relevant_ids:
        return 0.0
    return len(set(retrieved_ids) & relevant_ids) / len(relevant_ids)


def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    if not retrieved_ids:
        return 0.0
    return len(set(retrieved_ids) & relevant_ids) / len(retrieved_ids)


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    for index, record_id in enumerate(retrieved_ids, start=1):
        if record_id in relevant_ids:
            return 1.0 / index
    return 0.0


def main() -> None:
    base = Path(__file__).resolve().parents[1] / "data"
    records = load_json(base / "eval_records.json")
    questions = load_json(base / "eval_questions.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level06_evaluation")
    add_records(collection, records)

    k = 3
    rows = []
    for item in questions:
        result = query_records(collection, item["question"], n_results=k)
        retrieved_ids = [row["id"] for row in result_rows(result)]
        relevant_ids = set(item["relevant_ids"])
        rows.append(
            {
                "question": item["question"],
                "retrieved_ids": retrieved_ids,
                "recall": recall_at_k(retrieved_ids, relevant_ids),
                "precision": precision_at_k(retrieved_ids, relevant_ids),
                "mrr": reciprocal_rank(retrieved_ids, relevant_ids),
            }
        )

    for row in rows:
        print(f"\nQ: {row['question']}")
        print(f"retrieved: {row['retrieved_ids']}")
        print(f"recall@{k}: {row['recall']:.2f} precision@{k}: {row['precision']:.2f} mrr: {row['mrr']:.2f}")

    print("\n## Average")
    print(f"recall@{k}: {sum(row['recall'] for row in rows) / len(rows):.2f}")
    print(f"precision@{k}: {sum(row['precision'] for row in rows) / len(rows):.2f}")
    print(f"mrr: {sum(row['mrr'] for row in rows) / len(rows):.2f}")


if __name__ == "__main__":
    main()

