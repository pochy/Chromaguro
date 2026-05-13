from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, compact_document, load_json, mmr_select, query_records, recreate_collection, result_rows


def main() -> None:
    records = load_json(Path(__file__).resolve().parents[1] / "data" / "rag_records.json")
    client = chromadb.Client()
    collection = recreate_collection(client, "level05_context_budget")
    add_records(collection, records)

    question = "Chroma の保存方法と source 表示を知りたい"
    rows = result_rows(query_records(collection, question, n_results=5))
    selected = mmr_select(question, rows, limit=3, lambda_mult=0.65)

    token_budget_chars = 260
    used = 0
    print("\n## MMR selected context within budget")
    for row in selected:
        snippet = compact_document(row["document"], limit=120)
        if used + len(snippet) > token_budget_chars:
            continue
        used += len(snippet)
        metadata = row["metadata"]
        print(f"- {row['id']} source={metadata['source']} section={metadata['section']}")
        print(f"  {snippet}")
    print(f"\nused_chars: {used}/{token_budget_chars}")


if __name__ == "__main__":
    main()
