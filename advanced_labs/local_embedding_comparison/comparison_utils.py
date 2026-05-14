from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import chromadb

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, query_records, recreate_collection, result_rows

LAB_DIR = Path(__file__).resolve().parent
DATA_DIR = LAB_DIR / "data"


@dataclass(frozen=True)
class QuestionMetric:
    question: str
    relevant_ids: list[str]
    retrieved_ids: list[str]
    recall: float
    precision: float
    mrr: float
    latency_ms: float


@dataclass(frozen=True)
class EvaluationReport:
    provider_name: str
    k: int
    rows: list[QuestionMetric]

    @property
    def avg_recall(self) -> float:
        return average(row.recall for row in self.rows)

    @property
    def avg_precision(self) -> float:
        return average(row.precision for row in self.rows)

    @property
    def avg_mrr(self) -> float:
        return average(row.mrr for row in self.rows)

    @property
    def avg_latency_ms(self) -> float:
        return average(row.latency_ms for row in self.rows)


@dataclass(frozen=True)
class OptionalRun:
    status: str
    report: EvaluationReport | None = None
    reason: str = ""


def average(values: Any) -> float:
    items = list(values)
    if not items:
        return 0.0
    return sum(items) / len(items)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_records() -> list[dict[str, Any]]:
    return load_json(DATA_DIR / "records.json")


def load_questions() -> list[dict[str, Any]]:
    return load_json(DATA_DIR / "gold_questions.json")


def validate_gold_data() -> list[str]:
    records = load_records()
    questions = load_questions()
    record_ids = {record["id"] for record in records}
    errors: list[str] = []

    for record in records:
        if not record.get("document"):
            errors.append(f"{record['id']} has empty document")
        if not isinstance(record.get("metadata", {}), dict):
            errors.append(f"{record['id']} metadata must be an object")

    for item in questions:
        relevant_ids = item.get("relevant_ids", [])
        missing = [record_id for record_id in relevant_ids if record_id not in record_ids]
        if missing:
            errors.append(f"{item['question']} has missing relevant_ids: {missing}")
        if not relevant_ids:
            errors.append(f"{item['question']} has no relevant_ids")

    return errors


def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    if not relevant_ids:
        return 0.0
    return len(set(retrieved_ids) & relevant_ids) / len(relevant_ids)


def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    if not retrieved_ids:
        return 0.0
    return len(set(retrieved_ids) & relevant_ids) / len(retrieved_ids)


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: set[str]) -> float:
    for index, record_id in enumerate(retrieved_ids, start=1):
        if record_id in relevant_ids:
            return 1.0 / index
    return 0.0


def evaluate_retriever(
    provider_name: str,
    retrieve: Callable[[str, int], list[str]],
    k: int = 3,
) -> EvaluationReport:
    rows: list[QuestionMetric] = []

    for item in load_questions():
        started = time.perf_counter()
        retrieved_ids = retrieve(item["question"], k)
        latency_ms = (time.perf_counter() - started) * 1000
        relevant_ids = set(item["relevant_ids"])
        rows.append(
            QuestionMetric(
                question=item["question"],
                relevant_ids=item["relevant_ids"],
                retrieved_ids=retrieved_ids,
                recall=recall_at_k(retrieved_ids, relevant_ids),
                precision=precision_at_k(retrieved_ids, relevant_ids),
                mrr=reciprocal_rank(retrieved_ids, relevant_ids),
                latency_ms=latency_ms,
            )
        )

    return EvaluationReport(provider_name=provider_name, k=k, rows=rows)


def run_tutorial_embedding(k: int = 3) -> EvaluationReport:
    client = chromadb.Client()
    collection = recreate_collection(client, "local_embedding_comparison_tutorial")
    add_records(collection, load_records())

    def retrieve(question: str, n_results: int) -> list[str]:
        result = query_records(collection, question, n_results=n_results)
        return [row["id"] for row in result_rows(result)]

    return evaluate_retriever("tutorial_embedding", retrieve, k=k)


def run_sentence_transformer_embedding(k: int = 3) -> OptionalRun:
    model_name = os.getenv("LOCAL_EMBEDDING_MODEL", "").strip()
    if not model_name:
        return OptionalRun(
            status="skipped",
            reason="LOCAL_EMBEDDING_MODEL is not set. Set it to a local model path or Sentence Transformers model ID.",
        )

    device = os.getenv("LOCAL_EMBEDDING_DEVICE", "cpu")

    try:
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    except Exception as exc:
        return OptionalRun(status="error", reason=f"Could not import SentenceTransformerEmbeddingFunction: {exc}")

    try:
        embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=model_name,
            device=device,
            normalize_embeddings=True,
        )
        client = chromadb.Client()
        collection = recreate_collection(
            client,
            "local_embedding_comparison_sentence_transformer",
            embedding_function=embedding_function,
        )
        records = load_records()
        collection.add(
            ids=[record["id"] for record in records],
            documents=[record["document"] for record in records],
            metadatas=[record.get("metadata", {}) for record in records],
        )

        def retrieve(question: str, n_results: int) -> list[str]:
            result = collection.query(query_texts=[question], n_results=n_results)
            return list(result["ids"][0])

        report = evaluate_retriever(f"local_model:{model_name}", retrieve, k=k)
        return OptionalRun(status="ok", report=report)
    except Exception as exc:
        return OptionalRun(status="error", reason=f"Local embedding model failed: {exc}")


def print_report(report: EvaluationReport) -> None:
    print(f"\n## {report.provider_name}")
    for row in report.rows:
        print(f"\nQ: {row.question}")
        print(f"relevant: {row.relevant_ids}")
        print(f"retrieved: {row.retrieved_ids}")
        print(
            f"recall@{report.k}: {row.recall:.2f} "
            f"precision@{report.k}: {row.precision:.2f} "
            f"mrr: {row.mrr:.2f} "
            f"latency_ms: {row.latency_ms:.1f}"
        )

    print("\n## Average")
    print(f"recall@{report.k}: {report.avg_recall:.2f}")
    print(f"precision@{report.k}: {report.avg_precision:.2f}")
    print(f"mrr: {report.avg_mrr:.2f}")
    print(f"latency_ms: {report.avg_latency_ms:.1f}")


def print_comparison_table(reports: list[EvaluationReport]) -> None:
    print("\n## Comparison")
    print("provider,recall@k,precision@k,mrr,latency_ms")
    for report in reports:
        print(
            f"{report.provider_name},"
            f"{report.avg_recall:.2f},"
            f"{report.avg_precision:.2f},"
            f"{report.avg_mrr:.2f},"
            f"{report.avg_latency_ms:.1f}"
        )
