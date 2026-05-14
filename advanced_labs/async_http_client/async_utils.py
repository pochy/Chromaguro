from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import chromadb

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from shared.chroma_helpers import embed_texts, result_rows

COLLECTION_NAME = "async_http_client_docs"

RECORDS: list[dict[str, Any]] = [
    {
        "id": "async_http_client_001",
        "document": "AsyncHttpClient は Chroma server に非同期 HTTP で接続します。FastAPI の endpoint から await して query できます。",
        "metadata": {"topic": "async", "source": "async_http_client.md"},
    },
    {
        "id": "http_client_001",
        "document": "HttpClient は別プロセスで動く Chroma server に同期的に接続します。client-server mode の基本です。",
        "metadata": {"topic": "client-server", "source": "client_server.md"},
    },
    {
        "id": "persistent_client_001",
        "document": "PersistentClient は path を指定して Chroma のデータをローカルディスクに保存します。",
        "metadata": {"topic": "persistent", "source": "clients.md"},
    },
    {
        "id": "metadata_filter_001",
        "document": "metadata の tenant_id や doc_type を where filter に指定すると、検索対象を安全に絞り込めます。",
        "metadata": {"topic": "metadata", "source": "filters.md"},
    },
    {
        "id": "rag_source_001",
        "document": "RAG API では回答本文だけでなく source、section、chunk_id を返すと、ユーザーが根拠を確認できます。",
        "metadata": {"topic": "rag", "source": "rag_api.md"},
    },
]


def server_host() -> str:
    return os.getenv("CHROMA_HOST", "localhost")


def server_port() -> int:
    return int(os.getenv("CHROMA_PORT", "8000"))


async def create_client() -> Any:
    return await chromadb.AsyncHttpClient(host=server_host(), port=server_port())


async def recreate_collection(client: Any, name: str = COLLECTION_NAME) -> Any:
    try:
        await client.delete_collection(name)
    except Exception:
        pass
    return await client.create_collection(name=name, embedding_function=None)


async def seed_collection(client: Any, name: str = COLLECTION_NAME) -> Any:
    collection = await recreate_collection(client, name=name)
    documents = [record["document"] for record in RECORDS]
    await collection.add(
        ids=[record["id"] for record in RECORDS],
        documents=documents,
        metadatas=[record["metadata"] for record in RECORDS],
        embeddings=embed_texts(documents),
    )
    return collection


async def query_collection(collection: Any, query: str, n_results: int = 3) -> list[dict[str, Any]]:
    result = await collection.query(query_embeddings=embed_texts([query]), n_results=n_results)
    return result_rows(result)


def format_row(row: dict[str, Any]) -> str:
    source = row["metadata"].get("source", "unknown")
    return f"{row['rank']}. {row['id']} source={source} distance={row['distance']:.4f}"
