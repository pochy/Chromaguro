# Chroma Feature Map

Chroma は SQLite の代替ではありません。Chroma の中心は、AI アプリケーションで必要な retrieval を扱うことです。

## Core OSS / Local

| 機能 | 何をする | 教材で触る場所 |
| --- | --- | --- |
| Client | Chroma への入口 | Level 1 |
| Collection | embedding / document / metadata を入れる検索単位 | Level 1-3 |
| Collection lifecycle | create / get / list / modify / delete | Level 8 |
| Add / Update / Upsert / Delete | record の管理 | Level 2 |
| Query | embedding の近傍検索 | Level 1-6 |
| Get | ID / filter による取得 | Level 1-2 |
| Metadata Filtering | `where` で検索範囲を制御 | Level 2, 7, 9 |
| Full-text / Regex | `where_document` で本文条件をかける | Level 4 |
| PersistentClient | ローカル永続化 | Level 1 |
| HttpClient | 別プロセスの Chroma server へ接続 | Level 7, advanced_labs |
| Embedding Functions | collection に embedding model を紐づける | Level 3 |
| HNSW / distance space | ANN index と距離設計 | Level 8 |
| CLI | local server 起動・browse・vacuum など | Level 7-8, advanced_labs |

Cloud を除いた詳細なカバー状況は [local_chroma_coverage.md](local_chroma_coverage.md) を参照してください。

## Cloud / Distributed

| 機能 | 何をする | この教材での扱い |
| --- | --- | --- |
| CloudClient | managed Chroma に接続 | 付録で設計理解 |
| Search API | `query/get` より表現力の高い unified search | 疑似コードとローカル読み替え |
| Schema | index を field ごとに制御 | 付録と Level 8 |
| Sparse Vector | BM25/SPLADE 系の lexical retrieval | Level 4 のローカル疑似 sparse と比較 |
| Native Hybrid RRF | dense + sparse を Chroma 側で fusion | Level 4/9 の RRF で概念理解 |
| Group By | source/category ごとの多様化 | Level 5 の source grouping と対応 |
| Batch Search | 複数 query をまとめる | Level 6/9 の評価と対応 |
| Sync | S3/GitHub/Web/File から ingest | 付録で ingest 設計 |
| Collection Forking | copy-on-write fork | Level 9 の A/B testing と対応 |
| Tenants / Databases | 分離・quota・billing 境界 | Level 8/9 |

## 覚えるべき判断

```text
SQLite/RDB:
  正確な構造化データ、transaction、join、集計に強い。

Chroma:
  embedding 類似検索、metadata filtering、本文検索、RAG context retrieval に強い。

両方:
  実務では併用することが多い。
  RDB は source of truth、Chroma は retrieval index と考えると整理しやすい。
```
