# Final Project: Production-grade RAG Search App

## 作るもの

自分の技術メモ、Markdown、PDF 由来テキスト、Web 記事を取り込み、Chroma に保存し、検索 UI と RAG チャット UI を提供するアプリを作ります。

## 必須要件

```text
Chroma PersistentClient または client-server mode
metadata 設計
chunking
embedding function の明示
vector search
metadata filtering
full-text filtering
query expansion
reranking
source 表示
evaluation dataset
検索失敗ログ
```

## 完全版要件

必須要件を満たしたら、次も追加します。

```text
SQLite / RDB と Chroma の責任分界
query rewrite / expansion のログ
dense + keyword hybrid retrieval
MMR または context dedup
context budget
tenant filter の API 層での強制
embedding_version / chunker_version の metadata
reindex plan
evaluation regression report
agentic memory collection
local server + HttpClient smoke test
```

Cloud アカウントは必須ではありません。Search API / Schema / sparse vector は、`appendices/cloud_search_api_schema.md` を参考に、設計書と疑似実装で説明できれば合格です。

## 完成イメージ

```text
質問:
Chroma で永続化するには？

検索結果:
1. persistent client の説明
2. client-server mode の説明
3. path 指定の説明

回答:
Chroma でローカル永続化するには PersistentClient を使います...

参照:
- source: docs/chroma_clients.md
- section: PersistentClient
- chunk_id: persistent_client_001
```

## 評価条件

```text
gold question を 20 件以上作る
recall@5 を測る
失敗分類を記録する
検索 pipeline の変更前後を比較する
source 表示が UI に出ている
tenant filter が漏れない
```

## Professional Review Checklist

```text
RDB は source of truth、Chroma は retrieval index として分けた
source document と Chroma record の対応が追える
embedding model / chunker の変更時に rollback できる
where_document または keyword retrieval が必要な query を分類できる
context に入れる chunk の重複を減らしている
検索ログから失敗分析できる
LangChain / LlamaIndex / MCP を使う場合の利点と制約を説明できる
```
