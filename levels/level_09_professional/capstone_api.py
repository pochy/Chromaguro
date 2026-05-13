from __future__ import annotations

from typing import Any

import chromadb
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from levels.level_09_professional.capstone_pipeline import (
    COLLECTION_NAME,
    DOCS_DIR,
    retrieve,
    seed_collection,
)
from shared.chroma_helpers import compact_document, example_db_path


app = FastAPI(title="Level 9 Capstone RAG API")
API_COLLECTION_NAME = f"{COLLECTION_NAME}_api"

client = chromadb.PersistentClient(path=example_db_path(__file__))
collection, seeded_records = seed_collection(client, collection_name=API_COLLECTION_NAME, recreate=False)


class ContextChunk(BaseModel):
    id: str
    document: str
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    question: str
    expanded: str
    dense_ids: list[str]
    keyword_ids: list[str]
    fused_ids: list[str]
    context: list[ContextChunk]


class RagRequest(BaseModel):
    question: str = Field(min_length=1)
    tenant_id: str = "personal"
    doc_type: str | None = None
    n_candidates: int = Field(default=6, ge=1, le=10)


class RagResponse(BaseModel):
    answer: str
    sources: list[dict[str, Any]]
    context: list[ContextChunk]
    diagnostics: dict[str, Any]


def to_context_chunks(rows: list[dict[str, Any]]) -> list[ContextChunk]:
    return [
        ContextChunk(
            id=row["id"],
            document=row["document"],
            metadata=row["metadata"],
        )
        for row in rows
    ]


def run_search(question: str, tenant_id: str, doc_type: str | None, n_candidates: int) -> dict[str, Any]:
    return retrieve(
        collection,
        question,
        tenant_id=tenant_id,
        doc_type=doc_type,
        n_candidates=n_candidates,
    )


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "collection": API_COLLECTION_NAME,
        "documents": len(list(DOCS_DIR.glob("*.md"))),
        "chunks": len(seeded_records),
        "count": collection.count(),
    }


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(min_length=1),
    tenant_id: str = "personal",
    doc_type: str | None = None,
    n_candidates: int = Query(default=6, ge=1, le=10),
) -> SearchResponse:
    retrieval = run_search(q, tenant_id=tenant_id, doc_type=doc_type, n_candidates=n_candidates)
    return SearchResponse(
        question=retrieval["question"],
        expanded=retrieval["expanded"],
        dense_ids=retrieval["dense_ids"],
        keyword_ids=retrieval["keyword_ids"],
        fused_ids=retrieval["fused_ids"],
        context=to_context_chunks(retrieval["context"]),
    )


@app.post("/rag", response_model=RagResponse)
def rag(request: RagRequest) -> RagResponse:
    retrieval = run_search(
        request.question,
        tenant_id=request.tenant_id,
        doc_type=request.doc_type,
        n_candidates=request.n_candidates,
    )
    context = retrieval["context"]
    sources = [
        {
            "chunk_id": row["id"],
            "source": row["metadata"].get("source"),
            "section": row["metadata"].get("section"),
            "doc_type": row["metadata"].get("doc_type"),
        }
        for row in context
    ]
    answer = " ".join(compact_document(row["document"], limit=140) for row in context[:2])
    return RagResponse(
        answer=answer,
        sources=sources,
        context=to_context_chunks(context),
        diagnostics={
            "expanded": retrieval["expanded"],
            "dense_ids": retrieval["dense_ids"],
            "keyword_ids": retrieval["keyword_ids"],
            "fused_ids": retrieval["fused_ids"],
        },
    )
