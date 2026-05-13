from __future__ import annotations

import ast
import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, print_results, query_records, recreate_collection


def chunk_python_by_symbol(path: Path) -> list[dict[str, object]]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    lines = source.splitlines()
    chunks: list[dict[str, object]] = []

    for node in tree.body:
        if isinstance(node, ast.ClassDef | ast.FunctionDef):
            start = node.lineno
            end = getattr(node, "end_lineno", start)
            document = "\n".join(lines[start - 1 : end])
            chunks.append(
                {
                    "id": f"{path.stem}_{node.name}",
                    "document": document,
                    "metadata": {
                        "source": path.name,
                        "symbol": node.name,
                        "kind": node.__class__.__name__,
                        "start_line": start,
                        "end_line": end,
                        "chunker_version": "python-ast-v1",
                    },
                }
            )

    return chunks


def main() -> None:
    source_path = Path(__file__).resolve().parents[1] / "data" / "code_sample.py"
    records = chunk_python_by_symbol(source_path)

    client = chromadb.Client()
    collection = recreate_collection(client, "level03_code_chunks")
    add_records(collection, records)

    print(f"created code chunks: {collection.count()}")
    print_results("Code chunks", query_records(collection, "RAG の answer と sources を返す処理", n_results=2))


if __name__ == "__main__":
    main()
