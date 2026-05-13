# Level 5 Exercises

## 1. source 表示を改善する

`examples/01_minimal_rag.py` の出力に、`source`, `section`, `chunk_id` を必ず表示してください。

考えること:

```text
ユーザーはその source を見て信頼できるか
page や section は十分か
```

## 2. query expansion を追加する

`examples/02_query_expansion.py` に「権限」「アクセス制御」「tenant」の expansion を追加してください。

## 3. Reranking 前後を比較する

`examples/03_reranking.py` で、Chroma の順位と rerank 後の順位を比較してください。

観察すること:

```text
上位文書は質問に直接答えているか
遠いが重要な文書が落ちていないか
```

## 4. context budget を設計する

次を実行してください。

```bash
python levels/level_05_rag/examples/04_context_budget_mmr.py
```

top-k を全部入れる場合と、MMR で選ぶ場合の違いを説明してください。

## 提出物

次の内容をメモしてください。

```text
1. 01_minimal_rag.py で作られた Prompt for LLM
2. Mock answer に表示された source
3. query expansion 前後の query
4. reranking 前後で順位が変わった record
```

## 進級チェック

次の質問に答えられたら Level 6 へ進みます。

```text
RAG で LLM に渡す context はどう作るのか？
なぜ source / chunk_id を表示する必要があるのか？
query expansion と reranking はそれぞれ何を改善するのか？
```
