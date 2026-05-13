from __future__ import annotations


def main() -> None:
    rows = [
        {
            "setting": "space=cosine",
            "use_when": "text embedding の方向の近さを重視する",
            "risk": "既存 collection の距離値と比較できなくなる",
        },
        {
            "setting": "ef_search high",
            "use_when": "recall を上げたい",
            "risk": "query latency と CPU 使用量が増える",
        },
        {
            "setting": "metadata inverted index",
            "use_when": "tenant_id や doc_type で頻繁に絞る",
            "risk": "write 時の index 更新コストが増える",
        },
        {
            "setting": "sparse vector index",
            "use_when": "SKU, error code, technical term を正確に拾いたい",
            "risk": "Cloud/Search API 前提の設計になりやすい",
        },
    ]

    print("setting,use_when,risk")
    for row in rows:
        print(f"{row['setting']},{row['use_when']},{row['risk']}")


if __name__ == "__main__":
    main()
