# Final Project: Production-grade RAG Search App

## 作るもの

自分の技術メモ、Markdown、PDF 由来テキスト、Web 記事を取り込み、Chroma に保存し、検索 UI と RAG チャット UI を提供するアプリを作ります。

まずは完成形を小さくします。次を実行してください。

```bash
python levels/level_09_professional/examples/04_final_project_starter.py
```

この starter は、`data/final_project_docs/` の Markdown を取り込み、見出し単位で chunk 化し、metadata を付け、Chroma に保存し、dense + keyword の hybrid retrieval、RRF、MMR、source 表示、mini evaluation までを 1 回で通します。

見る場所:

```text
Ingest
  Markdown document 数と chunk 数。

Retrieval Pipeline
  expanded query, dense ranking, keyword ranking, fused ranking。

Selected Context
  LLM に渡す context 候補。

Mock Answer
  回答本文と source / section / chunk_id。

Mini Evaluation
  gold question に対する recall@5。
```

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

starter では、これらのうち次をすでに含めています。

```text
PersistentClient
heading-based chunking
embedding function の明示
tenant_id / source / section / doc_type / version metadata
vector search
keyword ranking
RRF fusion
MMR context selection
source 表示
mini evaluation
eval log
```

あなたの final project では、starter の sample Markdown を自分の文書に差し替え、足りない要件を 1 つずつ足してください。

## 最小完成スライス

最初に作る範囲はこれだけです。

```text
1. 自分の Markdown を 3-5 ファイル置く
2. 見出し単位で chunk にする
3. tenant_id, source, section, doc_type, chunker_version, embedding_model を metadata にする
4. Chroma に upsert する
5. 1 つの質問で検索する
6. context と source を表示する
7. gold question を 5 件作り、recall@5 を測る
```

ここまでできれば、Chroma を「保存先」ではなく「RAG の context を選ぶ retrieval index」として使う最小形ができています。

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

評価データは最初から完璧でなくて構いません。まず 5 件作り、検索失敗を見つけるたびに追加します。

```text
good:
  question: Chroma をローカルで永続化するには？
  relevant_ids: [capstone_chroma_clients_000]

bad:
  question: Chroma について
  relevant_ids: []
```

曖昧すぎる query だけを増やしても改善判断ができません。実際のユーザーが聞く具体的な質問を gold question にしてください。

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

## 実装の進め方

### Phase 1: local CLI

`04_final_project_starter.py` をコピーせず、まずそのまま動かします。出力の dense / keyword / fused / selected context の違いを説明できるようにします。

### Phase 2: 自分の文書に差し替える

`data/final_project_docs/` に自分の Markdown を置きます。最初は 3 ファイルで十分です。PDF や Web 記事は、まずテキスト化して Markdown と同じ pipeline に入れます。

### Phase 3: API にする

Level 7 の `/search` と `/rag` を参考に、final project の retrieval 関数を API から呼びます。API 層で tenant_id と permission を決め、Chroma の `where` に渡します。

### Phase 4: 評価を増やす

gold question を 5 件から 20 件へ増やします。検索 pipeline を変えるたびに recall@5 と失敗分類を比較します。

### Phase 5: 本番化を考える

embedding_version / chunker_version を変えた時の reindex plan、rollback、query log、latency、tenant isolation を確認します。
