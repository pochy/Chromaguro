# Level 7 Exercises

## 1. doc_type filter を試す

`/search` に `doc_type=guide` を付けた場合と付けない場合で結果を比較してください。

## 2. RAG response を改善する

`/rag` の response に次を追加してください。

```text
used_query
expanded_query
sources
context_preview
```

## 3. UI 表示を設計する

検索結果カードに最低限表示する metadata を決めてください。

```text
source
section
page
updated_at
tenant_id は表示するべきか
```

## 提出物

次の内容をメモしてください。

```text
1. /health の response
2. /search の response に含まれる id と source
3. /rag の answer と sources
4. API response に追加したい field
```

## 進級チェック

次の質問に答えられたら Level 8 へ進みます。

```text
/search と /rag は何が違うか？
tenant filter が漏れると何が危険か？
UI で source を表示する理由は何か？
```
