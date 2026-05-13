# Level 4: Vector だけに頼らない

## この Level でできるようになること

Vector search が得意な質問と、keyword / full-text search が必要な質問を見分けられるようになります。

## まず知るべき言葉

- **vector search**: 意味的に近い文書を探す検索。
- **full-text search**: 文書に特定の文字列が含まれるかで探す検索。
- **where_document**: document 本文に対する検索条件。
- **hybrid search**: vector と keyword など複数の検索を組み合わせる方法。
- **RRF**: 複数の ranking を順位ベースで統合する方法。

## なぜこれを学ぶのか

Vector search は便利ですが、万能ではありません。

```text
意味検索が強いもの:
退職時の手続き
エラーの原因
似た質問

文字列検索が強いもの:
SKU-12345
useEffect
Article 12
ERR_PAYMENT_TIMEOUT
```

固有名詞・関数名・型番・法律番号は、意味よりも文字列一致が重要です。

## 手順 1: vector search と keyword 条件を比較する

```bash
python levels/level_04_search_improvement/examples/01_vector_vs_keyword.py
```

見るのはこの 2 つです。

```text
Vector search only
  意味的に近い順。

Vector search + where_document contains useEffect
  useEffect を含む文書だけに絞った上で近い順。
```

## 手順 2: hybrid search の結果を見る

```bash
python levels/level_04_search_improvement/examples/02_hybrid_rrf.py
```

出力では、次を比較します。

```text
Dense ranking
Keyword ranking
RRF fused ranking
```

どれか 1 つが常に正しいわけではありません。質問の性質に応じて組み合わせます。

## よくあるつまずき

```text
Q. vector search だけで十分では？
A. 自然文の曖昧な質問には強いですが、useEffect や SKU のような exact keyword では弱いことがあります。

Q. where_document は metadata filter と違う？
A. はい。where は metadata、where_document は本文に対する条件です。
```

## 次の Level に進む条件

次ができたら Level 5 に進みます。

```text
vector search が強い質問を 2 つ挙げられる
keyword / full-text が必要な質問を 2 つ挙げられる
where と where_document の違いを言える
```

## 公式 docs で確認する箇所

- [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get): `where_document` の位置づけ。
- [Full Text Search](https://docs.trychroma.com/docs/querying-collections/full-text-search): document 本文検索。

## 発展: regex と sparse / hybrid の考え方

追加で次を実行します。

```bash
python levels/level_04_search_improvement/examples/03_regex_document_filter.py
python levels/level_04_search_improvement/examples/04_pseudo_sparse_hybrid.py
```

`where_document` は `$contains` だけでなく `$regex` も使えます。エラーコード、SKU、メールアドレス、法律番号などは regex が有効です。

Cloud では sparse vector index と Search API の RRF により、dense semantic search と lexical retrieval を native に組み合わせられます。この教材では API キー不要にするため、ローカル疑似 sparse と RRF で同じ判断を学びます。
