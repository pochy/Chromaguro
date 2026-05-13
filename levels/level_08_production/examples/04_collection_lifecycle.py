from __future__ import annotations

import chromadb


def collection_names(client: chromadb.ClientAPI) -> list[str]:
    return sorted(collection.name for collection in client.list_collections())


def main() -> None:
    client = chromadb.Client()
    name = "level08_lifecycle_docs_v1"
    renamed = "level08_lifecycle_docs_v2"

    for collection_name in [name, renamed]:
        try:
            client.delete_collection(collection_name)
        except Exception:
            pass

    collection = client.create_collection(
        name=name,
        metadata={
            "environment": "dev",
            "embedding_version": "v1",
            "owner": "tutorial",
        },
        embedding_function=None,
    )
    print("created:", collection.name, collection.metadata)
    print("listed:", collection_names(client))

    collection.modify(
        name=renamed,
        metadata={
            "environment": "dev",
            "embedding_version": "v2",
            "owner": "tutorial",
            "reason": "reindex candidate",
        },
    )

    updated = client.get_collection(renamed, embedding_function=None)
    print("modified:", updated.name, updated.metadata)

    client.delete_collection(renamed)
    print("deleted:", renamed)
    print("remaining:", collection_names(client))


if __name__ == "__main__":
    main()
