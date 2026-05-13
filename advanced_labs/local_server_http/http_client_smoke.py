from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, query_records, recreate_collection, result_rows


def main() -> None:
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = recreate_collection(client, "http_client_smoke")
    add_records(
        collection,
        [
            {
                "id": "http_client_001",
                "document": "HttpClient は別プロセスで動く Chroma server に接続します。",
                "metadata": {"source": "local_server_http"},
            }
        ],
    )

    for row in result_rows(query_records(collection, "Chroma server に接続したい", n_results=1)):
        print(f"{row['id']}: {row['document']}")


if __name__ == "__main__":
    main()
