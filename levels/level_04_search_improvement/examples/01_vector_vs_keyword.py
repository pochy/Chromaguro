from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, load_json, print_results, query_records, recreate_collection


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "react_records.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level04_vector_vs_keyword")
    add_records(collection, records)

    query = "React の副作用 cleanup はいつ動く？"
    vector_result = query_records(collection, query, n_results=4)
    print_results("Vector search only", vector_result)

    keyword_filtered_result = query_records(
        collection,
        query,
        n_results=4,
        where_document={"$contains": "useEffect"},
    )
    print_results("Vector search + where_document contains useEffect", keyword_filtered_result)


if __name__ == "__main__":
    main()

