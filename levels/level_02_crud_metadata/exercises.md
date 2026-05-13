# Level 2 Exercises

## 1. upsert の意味を確認する

`examples/01_crud_records.py` の `doc_001` の本文を変えて、再実行してください。

確認すること:

```text
同じ id が増殖しない
本文と metadata が更新される
```

## 2. tenant filter を追加する

`examples/02_metadata_filtering.py` に `tenant_b` の文書を追加し、`tenant_a` の検索結果に混ざらないことを確認してください。

## 3. metadata 設計を改善する

`data/support_records.json` に以下の metadata を追加するなら、どの型で持つべきか考えてください。

```text
公開/非公開
更新日
重要度
言語
文書の版
```

## 4. advanced filter を試す

次を実行し、どの条件でどの record が返るか確認してください。

```bash
python levels/level_02_crud_metadata/examples/03_advanced_metadata_filters.py
```

`$and`, `$in`, array metadata の `$contains` を自分の言葉で説明してください。

## 提出物

次の内容をメモしてください。

```text
1. add / update / upsert / delete の違い
2. filter なしで返った検索結果
3. tenant_a manual only で返った検索結果
4. 自分なら追加したい metadata を 3 つ
```

## 進級チェック

次の質問に答えられたら Level 3 へ進みます。

```text
再取り込みではなぜ add より upsert が便利なのか？
where filter は何を絞っているのか？
metadata はなぜ source 表示だけでなく検索品質にも関係するのか？
```
