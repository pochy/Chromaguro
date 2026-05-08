from __future__ import annotations

import sys

import chromadb

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, print_results, query_records, recreate_collection


records = [
    {
        "id": "coffee_intro_001",
        "document": "エスプレッソは細かく挽いたコーヒー豆に高い圧力をかけて抽出します。",
        "metadata": {"source": "coffee_notes.md", "category": "coffee", "lang": "ja"},
    },
    {
        "id": "tea_intro_001",
        "document": "紅茶は茶葉を発酵させて作る飲み物で、香りと渋みが特徴です。",
        "metadata": {"source": "tea_notes.md", "category": "tea", "lang": "ja"},
    },
]


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level01_hello")
    add_records(collection, records)

    result = query_records(
        collection,
        query="エスプレッソに使う豆について知りたい",
        n_results=2,
    )
    print_results("Hello Chroma", result)


if __name__ == "__main__":
    main()

