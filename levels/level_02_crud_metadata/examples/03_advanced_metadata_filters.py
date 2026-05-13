from __future__ import annotations

import sys
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

from shared.chroma_helpers import add_records, print_results, query_records, recreate_collection


records = [
    {
        "id": "policy_public_2024",
        "document": "公開 FAQ は全ユーザーが閲覧できます。Basic plan では月間 1000 件まで検索できます。",
        "metadata": {"visibility": "public", "plan": "basic", "year": 2024, "tags": ["faq", "billing"]},
    },
    {
        "id": "policy_private_2025",
        "document": "管理者向け手順は private 文書です。Enterprise plan では監査ログも検索対象にできます。",
        "metadata": {"visibility": "private", "plan": "enterprise", "year": 2025, "tags": ["admin", "audit"]},
    },
    {
        "id": "policy_public_2026",
        "document": "公開マニュアル v3 では tenant filter と doc_type filter を必須にします。",
        "metadata": {"visibility": "public", "plan": "enterprise", "year": 2026, "tags": ["manual", "tenant"]},
    },
]


def main() -> None:
    client = chromadb.Client()
    collection = recreate_collection(client, "level02_advanced_filters")
    add_records(collection, records)

    print_results(
        "public AND year >= 2025",
        query_records(
            collection,
            "tenant filter の新しいマニュアル",
            where={"$and": [{"visibility": "public"}, {"year": {"$gte": 2025}}]},
            n_results=3,
        ),
    )

    print_results(
        "plan IN enterprise/basic",
        query_records(
            collection,
            "監査ログと検索プラン",
            where={"plan": {"$in": ["enterprise", "basic"]}},
            n_results=3,
        ),
    )

    print_results(
        "tags contains audit",
        query_records(
            collection,
            "監査ログを検索したい",
            where={"tags": {"$contains": "audit"}},
            n_results=3,
        ),
    )


if __name__ == "__main__":
    main()
