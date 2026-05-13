# Operations

Chroma を本番で使う時は、検索できることよりも「更新できる」「測れる」「戻せる」「漏らさない」ことが重要です。

## 運用チェックリスト

```text
collection naming:
  environment / tenant / data_type / embedding_version を含める。

metadata:
  source / section / page / tenant_id / doc_type / updated_at / chunker_version / embedding_version を持つ。

ingestion:
  source_hash を保存し、本文が変わった時だけ reindex する。

evaluation:
  gold question と relevant_ids を保存し、変更前後で recall / precision / MRR を比較する。

access control:
  API 層で tenant filter を強制し、client から渡された tenant_id を信用しない。

backup:
  persistent path、source documents、ingestion config、evaluation logs を別々に保全する。

rollback:
  embedding_version / chunker_version ごとに切り替えられるようにする。
```

## RDB と Chroma の分担

```text
RDB:
  users, permissions, billing, original source metadata, audit logs

Object storage:
  PDF, images, raw source files

Chroma:
  chunked document, embedding, retrieval metadata, retrieval index
```

Chroma を source of truth にしすぎると、削除・監査・復旧が難しくなります。Chroma は retrieval index と考えると設計しやすくなります。
