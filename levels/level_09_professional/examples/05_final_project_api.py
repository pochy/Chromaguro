from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from levels.level_09_professional.capstone_api import app, health


def main() -> None:
    print("app:", app.title)
    print("health:", health())
    print("run with:")
    print("uvicorn levels.level_09_professional.capstone_api:app --reload")
    print("endpoints:")
    print("GET  /health")
    print("GET  /search?q=Chroma の永続化")
    print("POST /rag")


if __name__ == "__main__":
    main()
