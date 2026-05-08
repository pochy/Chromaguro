# Level 6: 検索品質を測る

## この Level でできるようになること

検索が良くなったかどうかを、感覚ではなく数値で比較できるようになります。

## まず知るべき言葉

- **gold dataset**: 質問と正解 chunk id の一覧。
- **relevant_ids**: その質問に答える正解 chunk の id。
- **recall@k**: 正解が top-k に含まれた割合。
- **precision@k**: top-k のうち正解だった割合。
- **MRR**: 最初の正解が何位に出たかを見る指標。
- **failure analysis**: 検索失敗の原因を分類すること。

## なぜこれを学ぶのか

RAG の失敗は、LLM の失敗とは限りません。

```text
文書が DB にない
  source 問題

文書はあるが検索されない
  retrieval 問題

検索されたが回答が間違う
  prompt / generation 問題
```

この切り分けのために retrieval evaluation を行います。

## 手順 1: 検索評価を実行する

```bash
python levels/level_06_evaluation/examples/01_retrieval_evaluation.py
```

出力では、質問ごとに次を見ます。

```text
retrieved
  実際に検索された ids。

recall@3
  正解が top 3 に入ったか。

precision@3
  top 3 のうち正解がどれだけあるか。

mrr
  最初の正解が何位か。
```

## 手順 2: 失敗分析を実行する

```bash
python levels/level_06_evaluation/examples/02_failure_analysis.py
```

検索に失敗した時、原因を分類します。

```text
source_document_missing
query_vocabulary_gap
retrieval_ranking_failure
```

## 手順 3: gold dataset を読む

`data/eval_questions.json` を開きます。

```json
{
  "question": "Chroma でデータを永続化するには？",
  "relevant_ids": ["chunk_persistent_client_001"]
}
```

このペアがあるから、検索改善を数値で比較できます。

## よくあるつまずき

```text
Q. recall と precision の違いがわからない。
A. recall は正解を取り逃していないか。precision は余計なものを混ぜていないかです。

Q. まずどちらを重視する？
A. RAG では、最初は recall を重視することが多いです。正解候補が取れなければ LLM は答えられません。
```

## 次の Level に進む条件

次ができたら Level 7 に進みます。

```text
gold dataset の意味を説明できる
recall@k / precision@k / MRR をざっくり説明できる
検索失敗が LLM だけの問題ではないと説明できる
```

## 公式 docs で確認する箇所

Chroma 公式 docs に評価指標の詳細チュートリアルは少ないため、この Level は教材内の実装を主教材にします。Chroma 側は [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get) を見て、取得結果の形を確認してください。

