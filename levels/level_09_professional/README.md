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

まず starter を実行し、小さな完成形を確認します。

```bash
python levels/level_09_professional/examples/04_final_project_starter.py
```

見る場所:

```text
Markdown が何 chunk になったか
dense ranking と keyword ranking の違い
RRF 後の fused ranking
MMR で選ばれた context
回答に source / section / chunk_id が出ているか
mini evaluation の recall@5
```

次に、同じ retrieval pipeline を API として公開します。

```bash
python levels/level_09_professional/examples/05_final_project_api.py
python levels/level_09_professional/examples/06_final_project_api_probe.py
```

実際に server として起動する場合:

```bash
uvicorn levels.level_09_professional.capstone_api:app --reload
```

見る場所:

```text
GET /health で ingest 済み chunk 数が返るか
GET /search で expanded query, dense_ids, keyword_ids, fused_ids が返るか
POST /rag で answer, sources, diagnostics が返るか
API 層で tenant_id を受け取り Chroma の where filter に渡しているか
```

いきなり全部作る必要はありません。自分の final project では、まずは次だけで十分です。

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

## 次の Level に進む条件

Level 9 の次に番号付き Level はありません。ここからは、自分のアプリやチームの検索基盤に進みます。次を説明できる状態になったら、このチュートリアルの本編は完了です。

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

## 発展: agentic search / memory

追加で次を実行します。

```bash
python levels/level_09_professional/examples/03_agentic_memory.py
```

production AI app では、1 回検索して終わりでは足りないことがあります。

```text
agentic search
  query plan を作り、複数回検索し、足りなければ再検索する。

agentic memory
  semantic / procedural / episodic memory を Chroma collection に保存し、次回以降の計画に使う。
```

さらに進む場合は [advanced_labs/integrations/mcp_agent](../../advanced_labs/integrations/mcp_agent/README.md) と [appendices/integrations.md](../../appendices/integrations.md) を確認してください。
