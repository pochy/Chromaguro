from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollectionSpec:
    environment: str
    tenant: str
    data_type: str
    embedding_version: str


def collection_name(spec: CollectionSpec) -> str:
    parts = [
        spec.environment,
        spec.tenant.replace("_", "-"),
        spec.data_type.replace("_", "-"),
        spec.embedding_version.replace("_", "-"),
    ]
    return "_".join(parts)


def main() -> None:
    specs = [
        CollectionSpec("prod", "tenant_a", "docs", "embed_v1"),
        CollectionSpec("stg", "tenant_a", "docs", "embed_v2"),
        CollectionSpec("prod", "shared", "faq", "embed_v1"),
    ]

    for spec in specs:
        print(collection_name(spec))


if __name__ == "__main__":
    main()

