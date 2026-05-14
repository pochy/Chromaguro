from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from async_utils import create_client, query_collection, seed_collection


async def search_one(collection: object, query: str) -> dict[str, object]:
    started = time.perf_counter()
    rows = await query_collection(collection, query, n_results=1)
    latency_ms = (time.perf_counter() - started) * 1000
    top = rows[0]
    return {
        "query": query,
        "top_id": top["id"],
        "source": top["metadata"].get("source"),
        "latency_ms": latency_ms,
    }


async def main() -> None:
    client = await create_client()
    collection = await seed_collection(client)
    queries = [
        "FastAPI endpoint から Chroma を await したい",
        "Chroma server に同期 client で接続するには？",
        "ローカルに保存する client は？",
        "tenant_id で検索範囲を絞りたい",
        "RAG API で source を返したい",
    ]

    started = time.perf_counter()
    results = await asyncio.gather(*(search_one(collection, query) for query in queries))
    total_latency_ms = (time.perf_counter() - started) * 1000

    print("## Concurrent async queries")
    for result in results:
        print(
            f"{result['top_id']} source={result['source']} "
            f"latency_ms={result['latency_ms']:.1f} query={result['query']}"
        )
    print(f"total_latency_ms={total_latency_ms:.1f}")


if __name__ == "__main__":
    asyncio.run(main())
