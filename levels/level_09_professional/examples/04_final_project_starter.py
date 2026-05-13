from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from levels.level_09_professional.capstone_pipeline import (
    COLLECTION_NAME,
    DOCS_DIR,
    evaluate,
    print_context,
    retrieve,
    seed_collection,
)
from shared.chroma_helpers import compact_document, example_db_path, write_jsonl


def main() -> None:
    client = chromadb.PersistentClient(path=example_db_path(__file__))
    collection, records = seed_collection(client)

    question = "Chroma で永続化して、回答に source を出すには？"
    retrieval = retrieve(collection, question)

    print("\n## Ingest")
    print(f"documents: {len(list(DOCS_DIR.glob('*.md')))}")
    print(f"chunks: {len(records)}")
    print(f"collection: {COLLECTION_NAME}")

    print("\n## Retrieval Pipeline")
    print(f"question: {retrieval['question']}")
    print(f"expanded: {retrieval['expanded']}")
    print(f"dense: {retrieval['dense_ids'][:3]}")
    print(f"keyword: {retrieval['keyword_ids'][:3]}")
    print(f"fused: {retrieval['fused_ids'][:3]}")

    print("\n## Selected Context")
    print_context(retrieval["context"])

    first = retrieval["context"][0]
    print("\n## Mock Answer")
    print(compact_document(first["document"], limit=180))
    print(f"参照: {first['metadata']['source']} section={first['metadata']['section']} chunk_id={first['id']}")

    report = evaluate(collection)
    print("\n## Mini Evaluation")
    for row in report:
        print(f"recall@5={row['recall_at_5']:.2f} question={row['question']}")

    write_jsonl(
        Path(__file__).resolve().parent / "eval_logs.jsonl",
        [
            {
                "question": retrieval["question"],
                "expanded": retrieval["expanded"],
                "retrieved_ids": retrieval["fused_ids"][:5],
                "selected_context_ids": [row["id"] for row in retrieval["context"]],
            },
            *report,
        ],
    )


if __name__ == "__main__":
    main()
