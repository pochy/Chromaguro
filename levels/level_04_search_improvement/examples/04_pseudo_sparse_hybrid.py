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


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "react_records.json")
    client = chromadb.Client()
    collection = recreate_collection(client, "level04_pseudo_sparse")
    add_records(collection, records)

    query = "useEffect cleanup exact keyword"
    dense_ids = [row["id"] for row in result_rows(query_records(collection, query, n_results=4))]
    sparse_ids = [record_id for record_id, _score in sparse_keyword_scores(query, records)]
    fused = weighted_reciprocal_rank_fusion([dense_ids, sparse_ids], weights=[0.7, 0.3])

    print("\n## Dense")
    print(dense_ids)
    print("\n## Pseudo sparse keyword")
    print(sparse_ids)
    print("\n## Weighted RRF")
    for record_id, score in fused:
        print(f"{record_id}: {score:.4f}")

    print("\nNote: Chroma Cloud の sparse vector + Search API RRF はこれを native index として実行する考え方です。")


if __name__ == "__main__":
    main()
