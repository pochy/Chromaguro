# Level 8 Exercises

## 1. collection naming を決める

自分のアプリに次の collection name を設計してください。

```text
production
staging
tenant_a
tenant_b
docs
faq
embedding v1
embedding v2
```

## 2. reindex 条件を書く

次の変更が起きたとき、reindex が必要か判断してください。

```text
metadata に updated_at を追加
chunk size を 800 から 400 に変更
embedding model を変更
source document の本文が変更
reranker を変更
```

## 3. access control を点検する

検索 API で tenant filter が漏れる可能性がある場所を列挙してください。

## 4. index tradeoff を説明する

次を実行してください。

```bash
python levels/level_08_production/examples/03_index_tradeoff_matrix.py
```

`space`, `ef_search`, metadata index, sparse vector index の tradeoff を説明してください。

## 5. collection lifecycle を確認する

次を実行してください。

```bash
python levels/level_08_production/examples/04_collection_lifecycle.py
```

record の `update` / `upsert` / `delete` と、collection の `create` / `modify` / `delete` の違いを説明してください。

## 提出物

次の内容をメモしてください。

```text
1. 自分のアプリ用 collection naming 案
2. reindex が必要な変更と不要な変更
3. tenant filter を強制する場所
4. metadata に残す version 情報
5. collection を新しく作るべき変更と、record 更新で済む変更
```

## 進級チェック

次の質問に答えられたら Level 9 へ進みます。

```text
embedding model を変えたらなぜ reindex が必要なのか？
chunker_version を残す理由は何か？
tenant ごとに collection を分ける判断基準は何か？
```
