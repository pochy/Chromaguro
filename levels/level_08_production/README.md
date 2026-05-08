# Level 8: 運用・本番設計

## この Level でできるようになること

「動く検索」から一歩進んで、更新・評価・権限・復旧を考えた検索基盤を設計できるようになります。

## まず知るべき言葉

- **production**: 本番環境。
- **reindex**: 文書を再度 embedding / index し直すこと。
- **versioning**: embedding model や chunker の版を管理すること。
- **migration**: データ形式や設定変更へ移行すること。
- **backup**: 障害時に戻せるよう保存しておくこと。

## なぜこれを学ぶのか

本番では「検索できる」だけでは足りません。

```text
再現性
権限管理
評価可能性
更新可能性
障害時の復旧
モデル変更への対応
```

検索基盤は、作った後も更新され続けます。

## 手順 1: collection naming を見る

```bash
python levels/level_08_production/examples/01_collection_naming.py
```

出力例:

```text
prod_tenant-a_docs_embed-v1
stg_tenant-a_docs_embed-v2
prod_shared_faq_embed-v1
```

collection 名から、環境・tenant・データ種類・embedding 版が推測できるようにします。

## 手順 2: reindex plan を見る

```bash
python levels/level_08_production/examples/02_reindex_plan.py
```

次の変更が起きたら、検索結果が変わる可能性があります。

```text
source document が変わった
embedding model が変わった
embedding version が変わった
chunker version が変わった
```

## 手順 3: access control を考える

metadata に `tenant_id` を入れるだけでは不十分です。API 層で必ず認証済み tenant の filter を強制します。

```text
小規模:
  1 collection + tenant_id filter

中規模:
  organization ごとに collection

大規模:
  tenant / data type / embedding model ごとに分離
```

## よくあるつまずき

```text
Q. metadata を追加しただけでも reindex が必要？
A. 検索に使う embedding が変わらないなら不要なことがあります。ただし filter 設計と評価は見直します。

Q. embedding model を変えたら？
A. 基本的には再 embedding / 再 index し、評価してから切り替えます。
```

## 次の Level に進む条件

次ができたら Level 9 に進みます。

```text
collection naming の意図を説明できる
reindex が必要な変更を判別できる
tenant filter を API 層で強制すべき理由を説明できる
embedding / chunker version を metadata に残す理由を説明できる
```

## 公式 docs で確認する箇所

- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients): persistent / server / cloud の使い分け。
- [Configure Collections](https://docs.trychroma.com/docs/collections/configure): collection 設定。
- [Migration](https://docs.trychroma.com/docs/overview/migration): バージョン変更時の移行情報。

