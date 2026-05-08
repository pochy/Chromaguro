# Chroma 運用メモ

## Client の選び方

短い実験では `chromadb.Client()` を使う。プロセス終了時にデータが消えるため、Notebook や一時的な検証に向いている。

ローカルで継続して開発する場合は `PersistentClient` を使い、`path` で保存先を明示する。

## Metadata 設計

metadata は検索空間を制御するために使う。source, doc_type, section, tenant_id, lang, created_at, embedding_model, chunker_version を持たせると、検索と運用の両方で扱いやすい。

## Chunking 設計

長い文書を 1 record にすると複数の概念が混ざる。見出し、段落、FAQ、コード関数など、ユーザーが探す単位で chunk を作る。

## 評価

検索品質は感覚で判断しない。gold question と relevant_ids を用意し、recall@k, precision@k, MRR で比較する。

