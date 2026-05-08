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

