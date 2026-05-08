# Level 9: Advanced Retrieval Pipeline

## この Level でできるようになること

プロフェッショナルな RAG / AI エージェント向け検索 pipeline を設計できるようになります。

## まず知るべき言葉

- **retrieval pipeline**: query を受け取り、context を作るまでの一連の流れ。
- **query rewrite**: ユーザー質問を検索に向く形へ書き換えること。
- **hybrid fusion**: 複数の検索結果を統合すること。
- **context compression**: LLM に渡す context を短く整えること。
- **A/B testing**: 2 つの方式を評価データで比較すること。

## なぜこれを学ぶのか

プロの RAG では、Chroma は重要な中核ですが、単独で完結しません。

```text
User Query
↓
Query Rewrite
↓
Query Expansion
↓
Dense Search
↓
Full-text / Keyword Search
↓
Metadata Filtering
↓
RRF / Hybrid Fusion
↓
Reranking
↓
Context Compression
↓
Answer
↓
Citation / Source Display
↓
Evaluation Logging
```

ここまでの Level で学んだ部品を、1 本の pipeline として組み合わせます。

## 手順 1: advanced pipeline を実行する

```bash
python levels/level_09_professional/examples/01_advanced_pipeline.py
```

見る場所:

```text
question
rewritten
expanded
fused context
mock answer
参照 source
```

## 手順 2: multi-tenant と A/B を見る

```bash
python levels/level_09_professional/examples/02_multi_tenant_ab_test.py
```

見る場所:

```text
tenant_a と tenant_b の結果が混ざらないか
chunker v1 と v2 で結果が変わるか
```

## 手順 3: final project brief を読む

`final_project_brief.md` を読み、自分の技術メモやドキュメントを検索するアプリを設計します。

いきなり全部作る必要はありません。まずは次だけで十分です。

```text
自分の Markdown を 3 ファイル用意する
chunk に分ける
Chroma に入れる
質問で検索する
source を表示する
```

## よくあるつまずき

```text
Q. pipeline が複雑すぎる。
A. 全部を常に使うわけではありません。失敗分析を見て、必要な部品だけ足します。

Q. 何から本番化すればいい？
A. まず evaluation dataset と source 表示です。測れない検索は改善できません。
```

## 到達条件

この Level が終わると、次を説明できる状態を目指します。

```text
query expansion が必要な理由
vector と full-text を組み合わせる理由
reranking の役割
tenant filter と access control の関係
versioning / A/B testing / evaluation logging の必要性
```

## 公式 docs で確認する箇所

- [Query and Get](https://docs.trychroma.com/docs/querying-collections/query-and-get): dense search と filter の基本。
- [Full Text Search](https://docs.trychroma.com/docs/querying-collections/full-text-search): exact keyword 検索。
- [Metadata Filtering](https://docs.trychroma.com/docs/querying-collections/metadata-filtering): access control の土台になる filter。

