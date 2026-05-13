from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import chromadb
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import compact_document, example_db_path, load_json, query_records, result_rows, upsert_records


app = FastAPI(title="Chroma Tutorial Search API")

client = chromadb.PersistentClient(path=example_db_path(__file__))
collection = client.get_or_create_collection(
    name="level07_api",
    embedding_function=None,
)


class SearchResult(BaseModel):
    id: str
    document: str
    metadata: dict[str, Any]
    distance: float | None


class RagRequest(BaseModel):
    question: str
    tenant_id: str = "tenant_a"
    doc_type: str | None = None
    n_results: int = Field(default=3, ge=1, le=10)


class RagResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]
    context: list[SearchResult]


def seed() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "api_records.json")
    upsert_records(collection, records)


def build_where(tenant_id: str | None, doc_type: str | None) -> dict[str, Any] | None:
    filters: list[dict[str, Any]] = []
    if tenant_id:
        filters.append({"tenant_id": {"$eq": tenant_id}})
    if doc_type:
        filters.append({"doc_type": {"$eq": doc_type}})
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return {"$and": filters}


def to_search_results(rows: list[dict[str, Any]]) -> list[SearchResult]:
    return [
        SearchResult(
            id=row["id"],
            document=row["document"],
            metadata=row["metadata"],
            distance=row["distance"],
        )
        for row in rows
    ]


seed()


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "count": collection.count()}


@app.get("/search", response_model=list[SearchResult])
def search(
    q: str = Query(min_length=1),
    tenant_id: str | None = "tenant_a",
    doc_type: str | None = None,
    n_results: int = Query(default=3, ge=1, le=10),
) -> list[SearchResult]:
    result = query_records(
        collection,
        q,
        n_results=n_results,
        where=build_where(tenant_id=tenant_id, doc_type=doc_type),
    )
    return to_search_results(result_rows(result))


@app.post("/rag", response_model=RagResponse)
def rag(request: RagRequest) -> RagResponse:
    result = query_records(
        collection,
        request.question,
        n_results=request.n_results,
        where=build_where(tenant_id=request.tenant_id, doc_type=request.doc_type),
    )
    rows = result_rows(result)
    context = to_search_results(rows)
    sources = [
        {
            "chunk_id": row["id"],
            "source": row["metadata"].get("source"),
            "section": row["metadata"].get("section"),
            "page": row["metadata"].get("page"),
        }
        for row in rows
    ]
    answer = " ".join(compact_document(row["document"], limit=120) for row in rows[:2])
    return RagResponse(answer=answer, sources=sources, context=context)
