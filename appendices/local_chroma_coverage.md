# Local / OSS Chroma Coverage Matrix

この表は、Chroma Cloud を除いた Chroma の主要機能について、この教材でどこまで扱っているかを確認するためのものです。

結論から言うと、Level 0-9 と Advanced Labs を終えれば、**local / single-node Chroma を RAG や agent memory の retrieval index として使う実務基礎は一通りカバー**できます。ただし、全 client 言語、全 embedding provider、HNSW tuning の詳細、大規模運用までは発展領域です。

## Coverage Summary

| 領域 | 公式 docs 上の位置づけ | 教材での扱い | 判定 |
| --- | --- | --- | --- |
| Install / Getting Started | `pip install chromadb`, client, collection, add, query | README, START_HERE, Level 1 | hands-on |
| In-memory client | `chromadb.Client()` で一時実験 | Level 1, many examples | hands-on |
| PersistentClient | ローカル path に保存 | Level 1, Level 5, Level 9 | hands-on |
| Local server / HttpClient | `chroma run` + `HttpClient` | advanced_labs/local_server_http | optional hands-on |
| AsyncHttpClient | async 版 HTTP client | 未実装 | gap |
| Collection lifecycle | create, get, list, modify, delete | Level 8 `04_collection_lifecycle.py` | hands-on |
| Collection metadata | collection の説明・設定情報 | Level 8 | hands-on |
| Collection configuration / HNSW | space, ef_search など index 設定 | Level 8 tradeoff matrix | conceptual |
| Add data | ids, documents, metadatas, embeddings | Level 1-3 | hands-on |
| Update / Upsert / Delete records | record の更新・追加・削除 | Level 2 | hands-on |
| Query | dense embedding 近傍検索 | Level 1-6, 9 | hands-on |
| Get | ID / filter 取得、pagination、include | Level 1-2 | partial hands-on |
| include | 返す field の制御 | Level 1 | hands-on |
| query result shape | `ids`, `documents`, `metadatas`, `distances` の形 | Level 1, shared helper | hands-on |
| Metadata filtering | `where` filter | Level 2, 7, 9 | hands-on |
| Full-text / regex filtering | `where_document` | Level 4 | hands-on |
| Embedding functions | collection に embedding function を持たせる | Level 3 `04_custom_embedding_function.py` | hands-on |
| Manual embeddings | embeddings / query_embeddings を自分で渡す | shared helper, most examples | hands-on |
| Default embedding function | default Sentence Transformers | 説明のみ | conceptual |
| External embedding providers | OpenAI, Cohere, Jina, Mistral など | 発展課題 | gap |
| Multi-modal inputs | images / uris など | 未実装 | gap |
| CLI browse / vacuum | collection inspection / maintenance | appendix mention only | conceptual |
| Docker local deployment | local Chroma server の container 運用 | 未実装 | gap |
| Backup / migration | path, reindex, versioning, rollback | Level 8, appendices/operations.md | conceptual |
| API integration | `/search`, `/rag` | Level 7, Level 9 capstone API | hands-on |
| LangChain / LlamaIndex | framework integration | advanced_labs/integrations | optional hands-on |
| Agent memory | semantic / procedural / episodic memory | Level 9, advanced_labs | hands-on |

## What You Can Claim After Finishing

この教材を最後まで完了したら、Cloud を除いた範囲では次のように言えます。

```text
local Chroma を使って RAG retrieval API を設計・実装できる
PersistentClient と HttpClient の使い分けを説明できる
collection / record / metadata / embedding / query / get / filter の基本を使える
chunking, embedding version, tenant filter, source display, evaluation を設計できる
Chroma を RDB の代替ではなく retrieval index として位置づけられる
```

まだ言い切らない方がよいこと:

```text
Chroma の全 API を理解した
全 client 言語を使える
HNSW configuration を実運用で tuning できる
Docker / server deployment / backup / migration を本番運用できる
全 embedding provider と multi-modal retrieval を使い分けられる
```

## Remaining Non-Cloud Gaps

### 1. AsyncHttpClient

`HttpClient` の非同期版です。非同期 Web API や async worker で Chroma を呼ぶ場合に必要になります。

この教材では、まず同期 `HttpClient` で client-server mode の役割を学びます。async は API framework の実装方針に強く依存するため、発展課題にしています。

### 2. Real Embedding Providers

Level 3 と shared helper では、教材を API キー不要にするため deterministic な tutorial embedding を使います。Level 3 `04_custom_embedding_function.py` では Chroma の embedding function 機構そのものを使いますが、OpenAI / Cohere / Jina / Mistral などの本物の provider 比較は扱いません。

発展でやるなら、同じ gold questions を使い、embedding provider ごとに recall@k / latency / cost / failure type を比較します。

### 3. Collection Configuration / HNSW Tuning

Level 8 では `space`, `ef_search`, metadata index, sparse vector index の tradeoff を扱います。ただし、HNSW パラメータを実際に変更して大規模 corpus で比較する lab はありません。

これは小さな教材データでは差が見えづらく、誤った一般化をしやすいためです。

### 4. Docker / Server Deployment

advanced_labs/local_server_http は local CLI server を扱います。Docker deployment、process supervision、backup、observability までは扱いません。

### 5. Multi-modal Retrieval

Chroma API には image / uri 系の入力もありますが、この教材は text RAG に集中しています。

## Recommended Next Labs

優先度順です。

```text
1. real embedding comparison lab
2. AsyncHttpClient lab
3. Docker local server lab
4. HNSW configuration experiment
5. image / URI retrieval appendix
```

まず足すなら、`real embedding comparison lab` が最も実務価値があります。ただし API key や model download が必要になりやすいため、標準ルートではなく optional lab に分けるのが安全です。

## Official Docs Used For This Matrix

- [Getting Started](https://docs.trychroma.com/docs/overview/getting-started)
- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients)
- [Client-Server Mode](https://docs.trychroma.com/docs/run-chroma/client-server)
- [Manage Collections](https://docs.trychroma.com/docs/collections/manage-collections)
- [Configure Collections](https://docs.trychroma.com/docs/collections/configure)
- [Adding Data](https://docs.trychroma.com/docs/collections/add-data)
- [Update Data](https://docs.trychroma.com/docs/collections/update-data)
- [Delete Data](https://docs.trychroma.com/docs/collections/delete-data)
- [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get)
- [Metadata Filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering)
- [Full Text Search](https://docs.trychroma.com/docs/querying-collections/full-text-search)
- [Embedding Functions](https://docs.trychroma.com/docs/embeddings/embedding-functions)
