# Local Embedding Comparison Exercises

## 1. Gold question を 1 つ追加する

`data/gold_questions.json` に、metadata filtering または source display に関する質問を 1 つ追加してください。

確認すること:

```text
relevant_ids が data/records.json に存在する
追加後に 01_prepare_gold_questions.py が成功する
baseline の metrics が変わるか確認する
```

## 2. 失敗 query を分類する

`02_compare_tutorial_embedding.py` の出力を見て、retrieved_ids の 1 位が relevant_ids に含まれない質問を探してください。

分類例:

```text
query_vocabulary_gap:
  質問と文書で使っている言葉が違う。

chunk_boundary_issue:
  正解情報が複数文書や複数 chunk に分かれている。

metadata_needed:
  vector search だけでなく metadata filter が必要。
```

## 3. ローカル embedding model と比較する

`LOCAL_EMBEDDING_MODEL` に手元の Sentence Transformers model path または model ID を指定して、`03_compare_local_embedding_model.py` を実行してください。

比較する観点:

```text
recall@3 は上がったか
MRR は上がったか
latency_ms は許容できるか
日本語 query で改善したか
英語混じりの query で改善したか
```

## 4. Collection を分ける理由を書く

embedding model を変えた時、なぜ同じ collection に追加で upsert し続けるのではなく、新しい collection に分けて評価するべきかを書いてください。

観点:

```text
embedding dimension
distance distribution
rollback
A/B testing
評価前の本番影響
```

## 提出物

```text
追加した gold question
tutorial embedding の metrics
local embedding model の metrics または skip 理由
失敗 query の分類
embedding model 変更時の collection strategy
```

## 進級チェック

次を自分の言葉で説明できれば完了です。

```text
Chroma の検索品質は Chroma だけで決まらないと言える
embedding model を同じ gold questions で比較できる
recall と latency の tradeoff を説明できる
model を変えたら collection を分ける理由を説明できる
```
