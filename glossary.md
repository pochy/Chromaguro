# Glossary: Chroma 初心者用語集

## client

Chroma に命令を送る入口です。

```python
client = chromadb.Client()
```

`Client()` は一時的な実験用、`PersistentClient()` はローカル保存用です。

## collection

検索対象を入れる箱です。ただし、単なるフォルダではありません。どの embedding model で検索するか、どの文書種類を入れるか、どの tenant を扱うかを決める検索単位です。

## record

Chroma に保存される 1 件のデータです。主に `id`, `document`, `metadata`, `embedding` で構成されます。

## id

record を識別する名前です。評価や再取り込みで使うので、`id1` より `persistent_client_001` のような意味のある名前が扱いやすいです。

## document

検索したい本文です。RAG では、最終的に LLM に渡す context の候補になります。

## metadata

record に付ける説明情報です。`source`, `section`, `page`, `tenant_id`, `doc_type` などを入れます。検索結果の説明や、検索範囲の絞り込みに使います。

## embedding

文章を数値のリストに変換したものです。Chroma は embedding 同士の距離を見て、意味的に近い document を探します。

## query

検索したい質問や検索文です。

```python
collection.query(query_texts=["Chroma の保存方法は？"])
```

この教材では API キー不要にするため、教材用のローカル embedding を使っています。

## distance

query と document の距離です。基本的には小さいほど近いと読みます。ただし、距離が近いことと、質問に答えていることは同じではありません。

## persistent

永続化のことです。プログラムを終了しても、データをディスクに残すという意味です。

## chunk

長い文書を検索しやすい単位に分けたものです。PDF 全体を 1 record にするのではなく、見出し・段落・FAQ などに分けます。

## RAG

Retrieval-Augmented Generation の略です。検索で関連文書を取り出し、その文書を LLM に渡して回答を作る構成です。

## reranking

Chroma で広めに取った候補を、質問に本当に答えている順に並べ替える処理です。

## evaluation

検索品質を測ることです。感覚ではなく、`recall@k`, `precision@k`, `MRR` などの数値で改善を判断します。

## dense search

通常の embedding による意味検索です。「同じ単語が入っているか」ではなく、意味的に近い文書を探します。

## sparse search

keyword retrieval に近い検索です。SKU、エラーコード、関数名、法律番号のような exact term に強いです。Chroma Cloud では sparse vector index を設定して使えます。この教材ではローカル疑似 sparse で考え方を学びます。

## hybrid search

dense search と sparse / keyword search など、複数の検索結果を組み合わせる方法です。片方だけでは取り逃す文書を拾いやすくします。

## RRF

Reciprocal Rank Fusion の略です。複数の ranking を、score の絶対値ではなく順位を使って統合します。dense と sparse の score scale が違う時に便利です。

## MMR

Maximal Marginal Relevance の略です。質問への関連性だけでなく、検索結果同士の重複を減らして多様な context を選ぶ方法です。

## HNSW

近似最近傍探索の index です。Chroma の single-node collection では、embedding の近い record を高速に探すために使われます。

## distance space

embedding 同士の距離の測り方です。`l2`, `cosine`, `ip` などがあります。embedding model と用途に合った距離を選ぶ必要があります。

## Search API

Chroma Cloud の composable な検索 API です。`Search`, `K`, `Knn`, `Rrf` などで filter、ranking、field selection、pagination を組み立てます。Local Chroma では現在 `query` / `get` が中心です。

## Schema

Chroma Cloud で、どの field にどの index を作るかを制御する仕組みです。dense vector、sparse vector、metadata inverted index、full-text index などの設計に関係します。

## MCP

Model Context Protocol の略です。AI host が外部 tool や data source と接続するための標準化された仕組みです。Chroma MCP server を使うと、agent が Chroma を memory / knowledge base として使えます。

## agentic search

1 回だけ検索するのではなく、agent が query plan を作り、複数回検索し、結果を評価しながら追加検索する方式です。

## agentic memory

agent が過去の事実、手順、実行結果を Chroma collection に保存し、次回以降の計画や実行に使う設計です。
