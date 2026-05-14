from __future__ import annotations

import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

from fastapi import FastAPI, HTTPException, Query
from fastapi.testclient import TestClient

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from async_utils import create_client, query_collection, seed_collection

_state: dict[str, Any] = {"collection": None}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    client = await create_client()
    _state["collection"] = await seed_collection(client)
    yield
    _state["collection"] = None


app = FastAPI(title="Async Chroma Search Lab", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, Any]:
    collection = _state.get("collection")
    if collection is None:
        return {"ok": False, "count": 0}
    return {"ok": True, "count": await collection.count()}


@app.get("/search")
async def search(q: str = Query(min_length=1), limit: int = Query(default=3, ge=1, le=5)) -> dict[str, Any]:
    collection = _state.get("collection")
    if collection is None:
        raise HTTPException(status_code=503, detail="Chroma collection is not ready")

    rows = await query_collection(collection, q, n_results=limit)
    return {
        "query": q,
        "results": [
            {
                "id": row["id"],
                "document": row["document"],
                "source": row["metadata"].get("source"),
                "topic": row["metadata"].get("topic"),
                "distance": row["distance"],
            }
            for row in rows
        ],
    }


def smoke_test() -> None:
    with TestClient(app) as client:
        health_response = client.get("/health")
        print(f"GET /health -> {health_response.status_code} {health_response.json()}")

        search_response = client.get("/search", params={"q": "async endpoint から検索する", "limit": 2})
        print(f"GET /search -> {search_response.status_code}")
        body = search_response.json()
        for row in body["results"]:
            print(f"{row['id']} source={row['source']} topic={row['topic']}")


if __name__ == "__main__":
    asyncio.run(asyncio.to_thread(smoke_test))
