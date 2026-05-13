# Cloud Search API / Schema / Sparse Vector

この教材の標準実行は完全ローカルです。ここでは Chroma Cloud 専用機能を、ローカルで学んだ概念と対応させて理解します。

## Search API

従来の local Chroma では主に次を使います。

```python
collection.query(query_embeddings=[...], where={...}, where_document={...})
collection.get(ids=[...], where={...})
```

Cloud Search API では、検索を composable な object として組み立てます。

```python
from chromadb import Search, K, Knn

search = (
    Search()
    .where((K("category") == "science") & (K("year") >= 2020))
    .limit(5)
    .select(K.DOCUMENT, K.SCORE, "title")
)

result = collection.search(search.rank(Knn(query="recent quantum computing")))
```

読み替え:

```text
Search().where(...)   -> local の where / where_document
.rank(Knn(...))       -> local の query
.select(...)          -> local の include
.limit(...)           -> local の n_results / get limit
```

## Schema

Schema は「どの field にどの index を作るか」を制御します。

```text
K.DOCUMENT   document 本文。full-text search の対象。
K.EMBEDDING  dense vector search の対象。
metadata     tenant_id, doc_type, source など filter の対象。
```

実務判断:

```text
頻繁に filter する field:
  index する価値が高い。

ほぼ filter しない field:
  write cost や index size のため、index しない選択もある。

embedding model を変える:
  距離の意味が変わるので別 collection / version で評価する。
```

## Sparse Vector

Dense embedding は意味的な近さに強い一方、固有名詞・型番・エラーコードには弱いことがあります。

Sparse vector は keyword retrieval に近い性質を持ちます。

```text
Dense:
  「退職時の手続き」から関連する社内規程を見つける。

Sparse:
  SKU-12345, ERR_PAYMENT_TIMEOUT, useEffect などを正確に拾う。

Hybrid:
  dense と sparse の ranking を RRF で統合する。
```

Level 4 の `04_pseudo_sparse_hybrid.py` は、Cloud sparse vector の概念をローカルで疑似体験するための例です。
