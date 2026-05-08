from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, compact_document, load_json, query_records, recreate_collection, result_rows


def build_prompt(question: str, rows: list[dict[str, object]]) -> str:
    context_blocks = []
    for row in rows:
        metadata = row["metadata"]
        context_blocks.append(
            "\n".join(
                [
                    f"[chunk_id: {row['id']}]",
                    f"source: {metadata['source']} / section: {metadata['section']} / page: {metadata['page']}",
                    str(row["document"]),
                ]
            )
        )

    context = "\n\n---\n\n".join(context_blocks)
    return f"""次の context だけを根拠に質問へ答えてください。

質問:
{question}

context:
{context}
"""


def mock_answer(rows: list[dict[str, object]]) -> str:
    top = rows[0]
    metadata = top["metadata"]
    return (
        f"{compact_document(str(top['document']))}\n"
        f"参照: {metadata['source']} section={metadata['section']} chunk_id={top['id']}"
    )


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "rag_records.json")

    client = chromadb.Client()
    collection = recreate_collection(client, "level05_minimal_rag")
    add_records(collection, records)

    question = "Chroma でデータを永続化するには？"
    result = query_records(collection, question, n_results=3)
    rows = result_rows(result)

    print("\n## Retrieved context")
    for row in rows:
        metadata = row["metadata"]
        print(f"- {row['id']} source={metadata['source']} section={metadata['section']}")

    print("\n## Prompt for LLM")
    print(build_prompt(question, rows))

    print("\n## Mock answer")
    print(mock_answer(rows))


if __name__ == "__main__":
    main()

