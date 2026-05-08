from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any, Iterable


VECTOR_DIMENSIONS = 64
ASCII_TOKEN_RE = re.compile(r"[a-zA-Z0-9_+#.-]+")
CJK_BLOCK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]+")

CONCEPT_TERMS: dict[str, tuple[str, ...]] = {
    "concept:persistence": (
        "persistent",
        "persistence",
        "persist",
        "save",
        "保存",
        "永続",
        "path",
        "chroma_db",
        "client-server",
    ),
    "concept:metadata": (
        "metadata",
        "where",
        "filter",
        "tenant",
        "page",
        "source",
        "メタデータ",
        "絞り込み",
        "権限",
    ),
    "concept:chunking": (
        "chunk",
        "chunking",
        "section",
        "paragraph",
        "overlap",
        "チャンク",
        "見出し",
        "段落",
    ),
    "concept:embedding": (
        "embedding",
        "vector",
        "dense",
        "semantic",
        "埋め込み",
        "ベクトル",
        "意味",
    ),
    "concept:rag": (
        "rag",
        "context",
        "citation",
        "source",
        "回答",
        "参照",
        "コンテキスト",
    ),
    "concept:evaluation": (
        "evaluation",
        "recall",
        "precision",
        "mrr",
        "ndcg",
        "評価",
        "正解",
        "失敗分析",
    ),
    "concept:react_effect": (
        "react",
        "useeffect",
        "cleanup",
        "副作用",
        "クリーンアップ",
    ),
    "concept:hybrid": (
        "hybrid",
        "rrf",
        "bm25",
        "keyword",
        "regex",
        "full-text",
        "全文",
        "キーワード",
    ),
}


def repo_root_from(file: str | Path) -> Path:
    path = Path(file).resolve()
    for parent in path.parents:
        if (parent / "TUTORIAL.md").exists():
            return parent
    raise RuntimeError(f"Could not find repository root from {file}")


def example_db_path(file: str | Path, name: str = "chroma_db") -> str:
    return str(Path(file).resolve().parent / name)


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    with Path(path).open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def tokenize(text: str) -> list[str]:
    lowered = text.lower()
    tokens = ASCII_TOKEN_RE.findall(lowered)

    for block in CJK_BLOCK_RE.findall(text):
        chars = [char for char in block if not char.isspace()]
        if len(chars) <= 2:
            tokens.append("".join(chars))
        else:
            tokens.extend("".join(chars[index : index + 2]) for index in range(len(chars) - 1))

    return tokens or [lowered[:32]]


def expand_tokens(text: str) -> list[str]:
    tokens = tokenize(text)
    normalized = " ".join(tokens)
    expanded = list(tokens)

    for concept, terms in CONCEPT_TERMS.items():
        if any(term.lower() in normalized or term in text for term in terms):
            expanded.append(concept)

    return expanded


def embed_text(text: str, dimensions: int = VECTOR_DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions

    for token in expand_tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        weight = 1.8 if token.startswith("concept:") else 1.0
        vector[index] += sign * weight

    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def embed_texts(texts: Iterable[str], dimensions: int = VECTOR_DIMENSIONS) -> list[list[float]]:
    return [embed_text(text, dimensions=dimensions) for text in texts]


def recreate_collection(client: Any, name: str, **kwargs: Any) -> Any:
    try:
        client.delete_collection(name)
    except Exception:
        pass
    return client.create_collection(name=name, **kwargs)


def add_records(collection: Any, records: list[dict[str, Any]]) -> None:
    documents = [record["document"] for record in records]
    collection.add(
        ids=[record["id"] for record in records],
        documents=documents,
        metadatas=[record.get("metadata", {}) for record in records],
        embeddings=embed_texts(documents),
    )


def upsert_records(collection: Any, records: list[dict[str, Any]]) -> None:
    documents = [record["document"] for record in records]
    collection.upsert(
        ids=[record["id"] for record in records],
        documents=documents,
        metadatas=[record.get("metadata", {}) for record in records],
        embeddings=embed_texts(documents),
    )


def query_records(
    collection: Any,
    query: str,
    n_results: int = 3,
    where: dict[str, Any] | None = None,
    where_document: dict[str, Any] | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "query_embeddings": embed_texts([query]),
        "n_results": n_results,
    }
    if where is not None:
        kwargs["where"] = where
    if where_document is not None:
        kwargs["where_document"] = where_document
    return collection.query(**kwargs)


def result_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    ids = result.get("ids", [[]])[0]
    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0] if result.get("distances") else [None] * len(ids)

    for index, record_id in enumerate(ids):
        rows.append(
            {
                "rank": index + 1,
                "id": record_id,
                "document": documents[index],
                "metadata": metadatas[index] or {},
                "distance": distances[index],
            }
        )
    return rows


def print_results(title: str, result: dict[str, Any]) -> None:
    print(f"\n## {title}")
    for row in result_rows(result):
        distance = row["distance"]
        distance_label = "n/a" if distance is None else f"{distance:.4f}"
        print(f"{row['rank']}. {row['id']} distance={distance_label}")
        print(f"   metadata={row['metadata']}")
        print(f"   {row['document']}")


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for index, record_id in enumerate(ranking):
            scores[record_id] = scores.get(record_id, 0.0) + 1.0 / (k + index + 1)
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


def keyword_score(query: str, document: str) -> int:
    query_tokens = set(expand_tokens(query))
    document_tokens = set(expand_tokens(document))
    return len(query_tokens & document_tokens)


def compact_document(document: str, limit: int = 220) -> str:
    normalized = " ".join(document.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1] + "..."

