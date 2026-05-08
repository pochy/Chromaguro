# Level 6 Exercises

## 1. 評価質問を増やす

`data/eval_questions.json` に質問を 2 件追加してください。

条件:

```text
1 件は metadata filtering が必要な質問
1 件は keyword / full-text が必要な質問
```

## 2. recall@3 を比較する

`examples/01_retrieval_evaluation.py` の `n_results` を 1, 3, 5 に変えて、recall がどう変わるか確認してください。

## 3. 失敗分類を改善する

`examples/02_failure_analysis.py` の分類に、次を追加してください。

```text
metadata_filter_missing
chunk_too_large
query_too_short
```

## 提出物

次の内容をメモしてください。

```text
1. evaluation script の average recall@3
2. average precision@3
3. MRR が低かった質問
4. 追加したい gold question を 2 つ
```

## 進級チェック

次の質問に答えられたら Level 7 へ進みます。

```text
gold dataset はなぜ必要か？
recall@k と precision@k は何が違うか？
検索失敗を LLM のせいにする前に何を確認するか？
```
