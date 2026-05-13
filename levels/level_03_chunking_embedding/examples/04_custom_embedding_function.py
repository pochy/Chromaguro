from __future__ import annotations

import sys
from pathlib import Path

import chromadb
from chromadb.api.types import Documents, EmbeddingFunction, Embeddings

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import embed_texts, print_results


class TutorialEmbeddingFunction(EmbeddingFunction[Documents]):
    def __init__(self) -> None:
        pass

    def __call__(self, input: Documents) -> Embeddings:
        return embed_texts(input)

    @staticmethod
    def name() -> str:
        return "tutorial-hash-embedding"

    def get_config(self) -> dict[str, object]:
        return {"dimensions": 64}

    @staticmethod
    def build_from_config(config: dict[str, object]) -> "TutorialEmbeddingFunction":
        return TutorialEmbeddingFunction()


def main() -> None:
    client = chromadb.Client()
    try:
        client.delete_collection("level03_custom_embedding_function")
    except Exception:
        pass

    collection = client.create_collection(
        name="level03_custom_embedding_function",
        embedding_function=TutorialEmbeddingFunction(),
    )

    collection.add(
        ids=["ef_persistent", "ef_metadata", "ef_evaluation"],
        documents=[
            "PersistentClient は path を指定して Chroma のデータを保存します。",
            "metadata の tenant_id は検索範囲と access control の設計に使います。",
            "検索品質は recall@k や MRR で評価します。",
        ],
        metadatas=[
            {"topic": "client"},
            {"topic": "metadata"},
            {"topic": "evaluation"},
        ],
    )

    result = collection.query(
        query_texts=["Chroma のデータを永続化したい"],
        n_results=2,
    )
    print_results("Collection-owned embedding function", result)


if __name__ == "__main__":
    main()
