# Level 4 Exercises

## 1. 固有名詞を増やす

`data/react_records.json` に `useLayoutEffect` の文書を追加してください。

確認すること:

```text
query に useEffect と入れた場合
query に useLayoutEffect と入れた場合
where_document を使った場合
```

## 2. SKU 検索を設計する

次の query は vector search と full-text search のどちらを重視すべきか考えてください。

```text
SKU-12345 の返品条件は？
```

metadata に入れるべき項目:

```text
sku
product_category
tenant_id
updated_at
policy_version
```

## 3. RRF の意味を説明する

RRF が raw score ではなく順位を使う理由を説明してください。

## 提出物

次の内容をメモしてください。

```text
1. Vector search only の 1 位
2. where_document contains useEffect の検索結果
3. keyword search が必要だと思う query を 3 つ
4. vector search が向いている query を 3 つ
```

## 進級チェック

次の質問に答えられたら Level 5 へ進みます。

```text
useEffect や SKU-12345 はなぜ full-text search が向いているのか？
where と where_document は何が違うか？
hybrid search は何を組み合わせているのか？
```
