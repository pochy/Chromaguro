from __future__ import annotations

import asyncio
import sys
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(LAB_DIR))

from async_utils import create_client, format_row, query_collection, seed_collection


async def main() -> None:
    client = await create_client()
    heartbeat = await client.heartbeat()
    collection = await seed_collection(client)
    rows = await query_collection(collection, "FastAPI から Chroma に async で検索したい", n_results=2)

    print(f"heartbeat: {heartbeat}")
    print("\n## Async query")
    for row in rows:
        print(format_row(row))
        print(f"   {row['document']}")


if __name__ == "__main__":
    asyncio.run(main())
