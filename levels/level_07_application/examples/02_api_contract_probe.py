from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from levels.level_07_application.examples.api_server import app


def main() -> None:
    client = TestClient(app)

    health = client.get("/health")
    print(f"GET /health -> {health.status_code} {health.json()}")

    empty_query = client.get("/search", params={"q": ""})
    print(f"GET /search?q= -> {empty_query.status_code}")

    search = client.get("/search", params={"q": "PersistentClient", "tenant_id": "tenant_a"})
    print(f"GET /search -> {search.status_code}")
    print(search.json()[0])

    rag = client.post("/rag", json={"question": "Chroma の保存方法は？", "tenant_id": "tenant_a"})
    print(f"POST /rag -> {rag.status_code}")
    print(rag.json()["sources"])


if __name__ == "__main__":
    main()
