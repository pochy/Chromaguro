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

