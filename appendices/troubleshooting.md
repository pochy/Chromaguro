# Troubleshooting

## `embedding runtime returned status 400`

この教材の標準 example は `embeddings` と `query_embeddings` を明示するため、通常は外部 embedding runtime を呼びません。

起きる場合:

```text
公式 docs 風の query_texts example を直接実行した
collection に default embedding function が付いている
必要な model / runtime / API key がない
```

対応:

```text
levels/*/examples を使う
embedding_function=None で collection を作る
add/query で embeddings/query_embeddings を明示する
```

## `No such file or directory`

リポジトリルートで実行しているか確認します。

```bash
pwd
ls
```

`README.md`, `TUTORIAL.md`, `levels/` が見える場所で実行します。

## `collection already exists`

教材の `recreate_collection()` は既存 collection を削除して作り直します。自分で `create_collection()` を直接使う場合は、同名 collection があると失敗します。

対応:

```python
client.get_or_create_collection(...)
client.delete_collection(...)
```

## 検索結果が直感と違う

正常です。原因を分けます。

```text
chunk が粗すぎる
metadata filter が足りない
query の語彙が document と合わない
keyword / regex が必要
embedding model が用途に合っていない
evaluation dataset が不足している
```

Level 6 の failure analysis で原因を分類してください。
