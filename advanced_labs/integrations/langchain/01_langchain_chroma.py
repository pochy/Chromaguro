from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import embed_text, example_db_path


class TutorialEmbeddings:
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return embed_text(text)


def main() -> None:
    try:
        from langchain_chroma import Chroma
        from langchain_core.documents import Document
    except ImportError:
        print("Install optional dependencies first: pip install -r requirements-integrations.txt")
        return

    vector_store = Chroma(
        collection_name="langchain_chroma_lab",
        embedding_function=TutorialEmbeddings(),
        persist_directory=example_db_path(__file__, "langchain_chroma_db"),
    )
    vector_store.reset_collection()
    vector_store.add_documents(
        [
            Document(page_content="Chroma は RAG の context を検索するために使います。", metadata={"source": "lab"}),
            Document(page_content="SQLite は transaction と structured query に強いです。", metadata={"source": "lab"}),
        ],
        ids=["lc_chroma", "lc_sqlite"],
    )

    for doc, score in vector_store.similarity_search_with_score("RAG の検索基盤", k=2):
        print(f"{score:.4f} {doc.metadata['source']} {doc.page_content}")


if __name__ == "__main__":
    main()
