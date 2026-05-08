from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, load_json, print_results, query_records, recreate_collection


EXPANSIONS = {
    "保存": "PersistentClient path persistence local storage 永続化",
    "永続": "PersistentClient path persistence local storage 保存",
    "出典": "source citation reference page section chunk_id 参照",
    "参照": "source citation reference page section chunk_id 出典",
    "並べ替え": "reranking rank precision top-k cross-encoder",
}


def expand_query(question: str) -> str:
    terms = [question]
    for key, expansion in EXPANSIONS.items():
        if key in question:
            terms.append(expansion)
    return " ".join(terms)


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "rag_records.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level05_query_expansion")
    add_records(collection, records)

    question = "Chroma の保存方法は？"
    expanded = expand_query(question)

    original_result = query_records(collection, question, n_results=3)
    expanded_result = query_records(collection, expanded, n_results=3)

    print(f"original query: {question}")
    print(f"expanded query: {expanded}")
    print_results("Original", original_result)
    print_results("Expanded", expanded_result)


if __name__ == "__main__":
    main()

