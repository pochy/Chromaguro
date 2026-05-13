from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from levels.level_09_professional.capstone_api import app


def main() -> None:
    client = TestClient(app)

    health = client.get("/health")
    print(f"GET /health -> {health.status_code} {health.json()}")

    empty_query = client.get("/search", params={"q": ""})
    print(f"GET /search?q= -> {empty_query.status_code}")

    search = client.get("/search", params={"q": "Chroma で永続化して source を出すには？"})
    print(f"GET /search -> {search.status_code}")
    search_json = search.json()
    print(search_json["context"][0])

    rag = client.post("/rag", json={"question": "tenant ごとの検索漏れを防ぐには？"})
    print(f"POST /rag -> {rag.status_code}")
    rag_json = rag.json()
    print(rag_json["sources"])
    print(rag_json["diagnostics"]["fused_ids"][:3])


if __name__ == "__main__":
    main()
