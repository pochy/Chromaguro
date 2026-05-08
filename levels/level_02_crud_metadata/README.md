# Level 2: CRUD と metadata

## この Level でできるようになること

文書を追加するだけでなく、更新・削除・再取り込みができるようになります。さらに metadata を使って、検索する範囲を絞れるようになります。

## まず知るべき言葉

- **CRUD**: Create, Read, Update, Delete の略。追加・取得・更新・削除。
- **add**: 新規追加。
- **update**: 既存 record の更新。
- **upsert**: あれば更新、なければ追加。
- **delete**: 削除。
- **where**: metadata で検索範囲を絞る条件。

## なぜこれを学ぶのか

実務では、文書は一度入れて終わりではありません。

```text
マニュアルが更新される
古い FAQ を消す
同じ source を再取り込みする
tenant ごとに検索範囲を分ける
```

そのため、`add` だけでなく `upsert` と metadata filter が重要になります。

## 手順 1: CRUD を実行する

```bash
python levels/level_02_crud_metadata/examples/01_crud_records.py
```

見る場所は 3 つです。

```text
get doc_001
  update 後の本文と metadata が表示されるか

After update and upsert
  更新した文書と upsert した文書が検索されるか

count after delete
  delete 後に件数が減ったか
```

## 手順 2: metadata filter を実行する

```bash
python levels/level_02_crud_metadata/examples/02_metadata_filtering.py
```

同じ query でも、filter なしと filter ありで結果が変わることを見ます。

```text
No filter
  全体から検索する。

tenant_a manual only
  tenant_id と doc_type で絞った範囲から検索する。
```

## 手順 3: metadata を設計情報として見る

弱い metadata:

```json
{"source": "file"}
```

強い metadata:

```json
{
  "source": "admin_manual_v2.md",
  "doc_type": "manual",
  "section": "account",
  "page": 12,
  "lang": "ja",
  "tenant_id": "tenant_a",
  "updated_at": "2026-05-08"
}
```

metadata は飾りではありません。検索空間を制御するための設計情報です。

## よくあるつまずき

```text
Q. add と upsert はどちらを使えばいい？
A. 初回だけなら add。再取り込みや同期では upsert が安全です。

Q. tenant_id って何？
A. 会社・組織・ユーザーなど、検索してよい範囲を分けるための ID です。
```

## 次の Level に進む条件

次ができたら Level 3 に進みます。

```text
add / update / upsert / delete の違いを言える
where filter で検索結果が変わることを確認できた
metadata は検索範囲を制御する情報だと説明できる
```

## 公式 docs で確認する箇所

- [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get): `query`, `get`, `where`, `where_document` の位置づけ。
- [Metadata Filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering): metadata filter の条件指定。

