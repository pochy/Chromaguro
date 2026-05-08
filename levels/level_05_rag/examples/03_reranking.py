from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, keyword_score, load_json, query_records, recreate_collection, result_rows


def rerank(question: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: keyword_score(question, str(row["document"])), reverse=True)


def print_ranking(title: str, rows: list[dict[str, object]]) -> None:
    print(f"\n## {title}")
    for index, row in enumerate(rows, start=1):
        metadata = row["metadata"]
        print(f"{index}. {row['id']} source={metadata['source']} section={metadata['section']}")


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "rag_records.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level05_reranking")
    add_records(collection, records)

    question = "回答に source と chunk_id を表示したい"
    result = query_records(collection, question, n_results=5)
    rows = result_rows(result)
    reranked_rows = rerank(question, rows)

    print_ranking("Chroma ranking", rows)
    print_ranking("Reranked", reranked_rows)


if __name__ == "__main__":
    main()

