from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndexConfig:
    embedding_model: str
    embedding_version: str
    chunker_version: str


@dataclass(frozen=True)
class IndexedDocument:
    id: str
    source_hash: str
    embedding_model: str
    embedding_version: str
    chunker_version: str


def needs_reindex(document: IndexedDocument, desired: IndexConfig, current_source_hash: str) -> list[str]:
    reasons: list[str] = []
    if document.source_hash != current_source_hash:
        reasons.append("source_changed")
    if document.embedding_model != desired.embedding_model:
        reasons.append("embedding_model_changed")
    if document.embedding_version != desired.embedding_version:
        reasons.append("embedding_version_changed")
    if document.chunker_version != desired.chunker_version:
        reasons.append("chunker_version_changed")
    return reasons


def main() -> None:
    desired = IndexConfig(
        embedding_model="tutorial-hash-embedding",
        embedding_version="v2",
        chunker_version="heading-v2",
    )
    indexed = [
        IndexedDocument("doc_001", "sha256:old", "tutorial-hash-embedding", "v1", "heading-v1"),
        IndexedDocument("doc_002", "sha256:same", "tutorial-hash-embedding", "v2", "heading-v2"),
    ]
    source_hashes = {
        "doc_001": "sha256:new",
        "doc_002": "sha256:same",
    }

    for document in indexed:
        reasons = needs_reindex(document, desired, source_hashes[document.id])
        if reasons:
            print(f"{document.id}: reindex required -> {', '.join(reasons)}")
        else:
            print(f"{document.id}: up to date")


if __name__ == "__main__":
    main()

