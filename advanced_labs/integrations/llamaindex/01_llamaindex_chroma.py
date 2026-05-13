from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, query_records, recreate_collection, result_rows


def main() -> None:
    try:
        from llama_index.vector_stores.chroma import ChromaVectorStore
    except ImportError:
        print("Install optional dependencies first: pip install -r requirements-integrations.txt")
        return

    client = chromadb.PersistentClient(path=str(Path(__file__).resolve().parent / "llamaindex_chroma_db"))
    collection = recreate_collection(client, "llamaindex_chroma_lab")
    add_records(
        collection,
        [
            {
                "id": "li_node_001",
                "document": "LlamaIndex は Chroma を vector store として利用できます。",
                "metadata": {"source": "llamaindex_lab"},
            },
            {
                "id": "li_node_002",
                "document": "Chroma collection 設計では metadata と chunk 単位が検索品質を左右します。",
                "metadata": {"source": "llamaindex_lab"},
            },
        ],
    )

    vector_store = ChromaVectorStore(chroma_collection=collection)
    print(f"wrapped vector store: {vector_store.__class__.__name__}")
    for row in result_rows(query_records(collection, "vector store と metadata 設計", n_results=2)):
        print(f"{row['id']}: {row['document']}")


if __name__ == "__main__":
    main()
