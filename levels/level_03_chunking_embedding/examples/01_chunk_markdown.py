from __future__ import annotations

import re
import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, print_results, query_records, recreate_collection


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9一-龥ぁ-んァ-ン]+", "_", text).strip("_").lower()


def chunk_markdown_by_heading(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    chunks: list[dict[str, object]] = []
    current_heading = "root"
    buffer: list[str] = []
    chunk_index = 0

    def flush() -> None:
        nonlocal chunk_index
        body = "\n".join(line for line in buffer if line.strip()).strip()
        if not body:
            return
        chunk_id = f"{path.stem}_{slugify(current_heading)}_{chunk_index:03d}"
        chunks.append(
            {
                "id": chunk_id,
                "document": body,
                "metadata": {
                    "source": path.name,
                    "section": current_heading,
                    "chunk_index": chunk_index,
                    "parent_id": path.stem,
                    "lang": "ja",
                    "chunker_version": "heading-v1",
                    "embedding_model": "tutorial-hash-embedding",
                },
            }
        )
        chunk_index += 1

    for line in text.splitlines():
        if line.startswith("## "):
            flush()
            current_heading = line.removeprefix("## ").strip()
            buffer = []
        elif not line.startswith("# "):
            buffer.append(line)

    flush()
    return chunks


def main() -> None:
    markdown_path = Path(__file__).resolve().parents[1] / "data" / "markdown_note.md"
    records = chunk_markdown_by_heading(markdown_path)

    client = chromadb.Client()
    collection = recreate_collection(client, "level03_chunks")
    add_records(collection, records)

    print(f"created chunks: {collection.count()}")
    result = query_records(collection, "Chroma でデータを保存するには？", n_results=3)
    print_results("Heading chunks", result)


if __name__ == "__main__":
    main()

