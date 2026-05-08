from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import (
    add_records,
    keyword_score,
    load_json,
    query_records,
    reciprocal_rank_fusion,
    recreate_collection,
    result_rows,
)


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "react_records.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level04_hybrid")
    add_records(collection, records)

    query = "useEffect cleanup はいつ実行される？"

    dense_result = query_records(collection, query, n_results=4)
    dense_ranking = [row["id"] for row in result_rows(dense_result)]

    all_records = collection.get(include=["documents", "metadatas"])
    keyword_pairs = sorted(
        zip(all_records["ids"], all_records["documents"], strict=True),
        key=lambda item: keyword_score(query, item[1]),
        reverse=True,
    )
    keyword_ranking = [record_id for record_id, _document in keyword_pairs]

    fused = reciprocal_rank_fusion([dense_ranking, keyword_ranking])

    print("\n## Dense ranking")
    for index, record_id in enumerate(dense_ranking, start=1):
        print(f"{index}. {record_id}")

    print("\n## Keyword ranking")
    for index, record_id in enumerate(keyword_ranking, start=1):
        print(f"{index}. {record_id}")

    print("\n## RRF fused ranking")
    for index, (record_id, score) in enumerate(fused, start=1):
        print(f"{index}. {record_id} rrf={score:.4f}")


if __name__ == "__main__":
    main()

