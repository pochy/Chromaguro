from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, print_results, query_records, recreate_collection


records = [
    {
        "id": "err_timeout",
        "document": "ERR_PAYMENT_TIMEOUT が発生した場合は決済 gateway の retry queue を確認します。",
        "metadata": {"kind": "error"},
    },
    {
        "id": "sku_return",
        "document": "SKU-12345 の返品条件は購入日から 30 日以内です。",
        "metadata": {"kind": "policy"},
    },
    {
        "id": "generic_payment",
        "document": "決済に失敗した場合は、カード情報と残高を確認してください。",
        "metadata": {"kind": "faq"},
    },
]


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level04_regex")
    add_records(collection, records)

    print_results(
        "regex ERR_*",
        query_records(
            collection,
            "決済タイムアウトのエラーコードは？",
            where_document={"$regex": "ERR_[A-Z_]+"},
            n_results=3,
        ),
    )

    print_results(
        "contains SKU",
        query_records(
            collection,
            "SKU-12345 の返品条件",
            where_document={"$contains": "SKU-12345"},
            n_results=3,
        ),
    )


if __name__ == "__main__":
    main()
