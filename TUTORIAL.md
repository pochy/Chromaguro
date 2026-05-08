# Chroma DB チュートリアル

> 実際の教材コンテンツは `levels/` 配下に Level 0 から Level 9 まで分割して配置しています。初心者はまず `START_HERE.md`、用語が不安な場合は `glossary.md` から始めてください。

## 全体方針

このチュートリアルのゴールは、単に Chroma の API を覚えることではありません。

最終的には、次のような力を身につけることを目的にします。

> ユーザーの質問に対して、本当に役に立つ情報を検索し、RAG や AI エージェントに渡せる検索基盤を設計・実装・評価できるようになる。

Chroma は公式に「AI のためのオープンソース検索インフラ」と説明されており、vector search だけでなく、full-text search、regex search、metadata search も扱う検索基盤として位置づけられています。([Chroma][1])
そのため、チュートリアルも「ベクトルDBの使い方」だけでなく、**検索設計・データ設計・評価・運用**まで含めるべきです。

---

# 0. まず学ぶべき設計思想・哲学

## 0-1. Chroma は「LLM の記憶装置」ではなく「検索基盤」

Chroma はよく「ベクトルDB」と呼ばれますが、実務では **LLM に渡す文脈を選ぶための検索基盤** と考えるほうが正確です。

LLM は、渡されたコンテキストが悪ければ良い回答を作れません。
つまり RAG の品質は、かなりの部分が **検索品質** で決まります。

Chroma の基本思想は次のように整理できます。

```text
データを embedding 化する
↓
検索可能な collection に保存する
↓
質問に関連する候補を取り出す
↓
必要なら metadata / full-text / reranking で絞る
↓
LLM に渡す
```

Chroma の collection は、embedding、document、metadata を保存し、それらを index 化して検索や filtering を可能にする単位です。([Chroma Docs][2])

---

## 0-2. 「意味的に近い」ことと「答えとして有用」は違う

ベクトル検索は、意味的に近い文書を返すのが得意です。
しかし、意味的に近い文書が必ず質問の答えになるとは限りません。

たとえば、次の質問を考えます。

```text
この商品のアレルゲン情報は？
```

ベクトル検索だけだと、以下のような文書が返る可能性があります。

```text
この商品は人気の焼き菓子です。
小麦粉、卵、乳を使用しています。
保存方法は直射日光を避けてください。
```

これは関連していますが、アレルゲン欄だけを正確に取りたい場合には、もっとピンポイントな検索が必要です。

そのため実務では、Chroma をこう使います。

```text
vector search
+ metadata filtering
+ full-text search
+ hybrid search
+ reranking
+ evaluation
```

Chroma の `query` は dense embedding に対する近傍検索を行い、`get` は similarity ranking なしでレコードを取得する用途に使われます。また `where` による metadata filtering や `where_document` による full-text / regex 条件も利用できます。([Chroma Docs][3])

---

## 0-3. Collection は「フォルダ」ではなく「検索単位」

初心者が間違えやすい点は、collection を単なるフォルダのように考えることです。

実際には collection は、次のような設計単位です。

```text
どの embedding model を使うか
どのデータ型を入れるか
どの検索単位で検索するか
どの metadata で絞るか
どのユーザー・組織のデータか
```

Chroma 公式ガイドでも、同じ embedding model で全体検索したい場合や metadata filtering で区別できる場合は単一 collection、異なるデータ型・異なる embedding model・マルチテナント要件がある場合は複数 collection を使う、という考え方が示されています。([Chroma Docs][4])

---

# チュートリアル全体構成

## Level 1: 入門編 — Chroma に触る

### Chapter 1. Chroma DB とは何か

**学ぶこと**

* Chroma DB の役割
* ベクトル検索とは何か
* embedding とは何か
* RAG における Chroma の位置づけ
* Chroma と通常の RDB / Elasticsearch / Pinecone / Qdrant との違い

**設計思想**

ここでは、Chroma を「データベース」としてではなく、**AI アプリケーションが外部知識へアクセスするための検索レイヤー**として説明します。

通常の DB は「正確に一致するデータ」を探すのが得意です。
Chroma は「意味的に近い情報」「質問に関連する情報」を探すために使います。

---

### Chapter 2. Hello Chroma

**実装内容**

```bash
pip install chromadb
```

```python
import chromadb

client = chromadb.Client()

collection = client.create_collection(name="my_collection")

collection.add(
    ids=["id1", "id2"],
    documents=[
        "これはコーヒー豆についての文書です。",
        "これは紅茶についての文書です。"
    ]
)

results = collection.query(
    query_texts=["エスプレッソに使う豆について知りたい"],
    n_results=2
)

print(results)
```

Chroma の公式 Getting Started でも、`pip install chromadb`、`Client()`、collection 作成、document 追加、query という流れが基本として紹介されています。([Chroma Docs][2])

**学ぶこと**

* client
* collection
* add
* query
* ids
* documents
* distances
* n_results

**設計思想**

最初に重要なのは、Chroma では document を追加すると、embedding と indexing を自動で処理できる点です。
ただし、プロフェッショナルな用途では「自動で便利」なまま終わらず、後で embedding model や metadata 設計を自分で制御していきます。

---

### Chapter 3. In-memory と Persistent の違い

**学ぶこと**

* `chromadb.Client()`
* `chromadb.PersistentClient()`
* データが消える環境と残る環境
* Notebook 実験と実アプリの違い

**実装内容**

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="docs")
```

Chroma の Python `Client()` は in-memory で実験しやすい一方、データ永続化が必要な場合は `PersistentClient` を使い、指定 path に DB ファイルを保存・読み込みできます。([Chroma Docs][5])

**設計思想**

```text
in-memory = 実験用
persistent = ローカル開発・小規模アプリ用
client-server = チーム開発・本番に近い構成
cloud = 本番運用・スケーラビリティ重視
```

最初は in-memory でよいですが、RAG アプリを作るならすぐ persistent に移るべきです。

---

## Level 2: 基礎実装編 — CRUD と検索の基本

### Chapter 4. Collection と Record の基本操作

**学ぶこと**

* `create_collection`
* `get_collection`
* `get_or_create_collection`
* `add`
* `update`
* `upsert`
* `delete`
* `get`

**実装内容**

```python
collection.upsert(
    ids=["doc_001"],
    documents=["Chroma は AI アプリ向けの検索基盤です。"],
    metadatas=[{
        "source": "tutorial",
        "category": "intro",
        "lang": "ja"
    }]
)
```

Chroma では `update` により既存 record を更新でき、`upsert` は存在すれば更新、存在しなければ追加する操作です。embedding の次元が collection と合わない場合は例外になります。([Chroma Docs][6])

**設計思想**

実務では `add` よりも `upsert` を多用します。

理由は、ドキュメント再取り込み時に同じ ID が来ることが多いからです。

```text
add     = 新規追加向き
upsert  = 再取り込み・同期向き
update  = 明示的な更新向き
delete  = データ削除・再構築向き
```

---

### Chapter 5. Metadata 設計

**学ぶこと**

* metadata の役割
* `where` filter
* `$eq`
* `$gt`
* `$gte`
* `$lt`
* `$lte`
* `$and`
* `$or`
* source / page / author / tenant / created_at / doc_type の設計

**実装内容**

```python
results = collection.query(
    query_texts=["Chroma の永続化について"],
    where={
        "$and": [
            {"lang": "ja"},
            {"doc_type": "tutorial"}
        ]
    },
    n_results=5
)
```

Chroma の metadata filtering は `where` を使い、単純な等価条件だけでなく、比較演算子や `$and` / `$or` による論理条件も扱えます。([Chroma Docs][7])

**設計思想**

metadata は「検索結果を絞るためのタグ」ではなく、**検索空間を制御するための設計情報**です。

悪い metadata 設計：

```json
{
  "source": "file"
}
```

良い metadata 設計：

```json
{
  "source": "manual_v2.pdf",
  "doc_type": "manual",
  "section": "installation",
  "page": 12,
  "lang": "ja",
  "tenant_id": "company_a",
  "created_at": "2026-05-08"
}
```

RAG の精度は、embedding model より metadata 設計で大きく改善することがあります。

---

## Level 3: データ設計編 — Chunking と Embedding

### Chapter 6. Chunking の考え方

**学ぶこと**

* なぜ全文を1レコードにしないのか
* chunk size
* overlap
* section-based chunking
* Markdown / PDF / HTML / code の chunking
* chunk metadata
* parent document reconstruction

**設計思想**

Chroma に入れる単位は「ファイル」ではなく「検索される意味単位」です。

悪い例：

```text
1つの PDF 全体を1 record にする
```

良い例：

```text
見出し単位
段落単位
FAQ 単位
コード関数単位
マニュアルの節単位
```

Chroma 公式ガイドでも、embedding model は1入力から1ベクトルを作るため、文書全体を1 record にすると複数の概念がぼやけ、検索品質が下がると説明されています。chunking によって、ユーザーが実際に探す段落・節・関数・メッセージ単位で index でき、precision と recall を改善できます。([Chroma Docs][4])

---

### Chapter 7. Embedding Function を理解する

**学ぶこと**

* embedding とは何か
* default embedding
* OpenAI embedding
* local embedding
* custom embedding function
* embedding 次元
* model 変更時の再 index

**実装内容**

```python
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

embedding_function = OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="docs_openai",
    embedding_function=embedding_function
)
```

Chroma では embedding function を collection に紐づけることができ、`add`、`update`、`upsert`、`query` の際に利用されます。また独自の embedding function を実装することもできます。([Chroma Docs][8])

**設計思想**

embedding model は「検索の価値観」を決めます。

```text
一般文書検索       → 汎用 embedding
コード検索         → code 向け embedding
日本語文書検索     → 多言語・日本語に強い embedding
画像検索           → multimodal embedding
機密性重視         → local embedding
```

重要なのは、embedding model を変えたら、基本的には既存データを再 embedding / 再 index する必要があるということです。

---

## Level 4: 検索改善編 — Vector だけに頼らない

### Chapter 8. Vector Search の限界

**学ぶこと**

* semantic similarity の強み
* semantic similarity の弱み
* 固有名詞、型番、SKU、法律番号、関数名の検索
* 類似しているが答えではない問題

**実験**

次のようなデータを入れて比較します。

```text
A: React の useEffect の使い方
B: React の useMemo の使い方
C: useEffect の cleanup 関数
D: Vue の watchEffect
```

質問：

```text
useEffect の cleanup はいつ実行される？
```

vector search だけで top-k を見て、どの文書が返るか観察します。

**設計思想**

プロの検索設計では、最初にこう考えます。

```text
この質問は意味検索で解けるか？
キーワード一致が必要か？
metadata filter が必要か？
reranking が必要か？
```

---

### Chapter 9. Full-text Search と Regex Search

**学ぶこと**

* `where_document`
* `$contains`
* exact keyword search
* regex search の用途
* vector search との使い分け

**実装イメージ**

```python
results = collection.query(
    query_texts=["React の副作用について"],
    where_document={"$contains": "useEffect"},
    n_results=5
)
```

Chroma の `query` と `get` は、metadata filtering の `where` に加えて、document に対する full-text / regex 条件の `where_document` もサポートしています。([Chroma Docs][3])

**設計思想**

固有名詞・型番・コード・法律・商品 SKU などは、embedding より text search のほうが強い場合があります。

```text
意味検索が強いもの:
- 「退職時の手続き」
- 「エラーの原因」
- 「似た質問」

キーワード検索が強いもの:
- SKU-12345
- useEffect
- Article 12
- text-embedding-3-small
```

---

### Chapter 10. Hybrid Search

**学ぶこと**

* dense search
* sparse search
* BM25
* SPLADE
* RRF
* semantic search と lexical search の融合

Chroma の公式ガイドでは、hybrid search は dense search と lexical search を並列に実行し、その結果を統合する方法として説明されています。特に技術文書や専門的な内容では、どちらか単独より hybrid が有効なことが多いとされています。([Chroma Docs][4])

**設計思想**

hybrid search の哲学はこうです。

```text
意味で探す
+
文字列でも探す
+
両方の順位を統合する
```

Chroma Cloud の Search API では、RRF、つまり Reciprocal Rank Fusion によって複数 ranking を統合できます。RRF は raw score ではなく順位を使うため、dense embedding と sparse embedding のように score scale が違う ranking を統合しやすい方法です。([Chroma Docs][9])

---

## Level 5: RAG 実装編 — AI アプリとして使う

### Chapter 11. 最小 RAG アプリを作る

**構成**

```text
ユーザー質問
↓
Chroma query
↓
top-k documents
↓
LLM prompt に context として挿入
↓
回答生成
```

**実装課題**

* 自分の Markdown メモを Chroma に入れる
* 質問を投げる
* 関連 chunk を取得する
* LLM に渡して回答させる
* 参照元 metadata を表示する

**設計思想**

RAG の基本は「LLM に何を読ませるか」です。

悪い RAG：

```text
検索結果 top 10 をそのまま全部 LLM に渡す
```

良い RAG：

```text
検索
↓
filter
↓
rerank
↓
重複除去
↓
必要な chunk だけ渡す
↓
source を明示する
```

---

### Chapter 12. Query Expansion

**学ぶこと**

* query rewriting
* synonym expansion
* domain-specific expansion
* HyDE 的アプローチ
* 複数 query の統合

**例**

元の質問：

```text
Chroma の保存方法は？
```

拡張後：

```text
Chroma persistent client local storage database path save load persistence
```

**設計思想**

ユーザーの質問は短く、曖昧で、検索に向いていないことが多いです。

そのため検索前に、LLM を使って検索向けクエリに変換します。

```text
ユーザー向けの自然文
↓
検索向けのクエリ
↓
Chroma で検索
```

---

### Chapter 13. Reranking

**学ぶこと**

* bi-encoder と cross-encoder の違い
* Chroma で top 30 取得
* reranker で top 5 に絞る
* precision を上げる
* latency とのトレードオフ

**設計思想**

Chroma は候補を高速に集める役割。
reranker は、その候補を「質問に本当に答えている順」に並べ替える役割です。

```text
Chroma:
広く速く候補を集める

Reranker:
遅いが精密に並べ替える
```

プロの RAG では、Chroma の検索結果をそのまま LLM に渡さず、reranking で品質を上げることが多いです。

---

## Level 6: 評価編 — 検索品質を測る

### Chapter 14. Retrieval Evaluation

**学ぶこと**

* 検索結果をどう評価するか
* recall@k
* precision@k
* MRR
* nDCG
* answer faithfulness
* context relevance
* gold dataset 作成

**実装課題**

以下のような評価データを作ります。

```json
[
  {
    "question": "Chroma でデータを永続化するには？",
    "relevant_ids": ["chunk_persistent_client_001", "chunk_client_server_002"]
  },
  {
    "question": "metadata で page を絞るには？",
    "relevant_ids": ["chunk_metadata_filter_003"]
  }
]
```

そして、検索結果が relevant_ids を含むかを測定します。

**設計思想**

感覚で「検索がよくなった」と判断しないことが重要です。

```text
Before:
top 5 に正解が 2 件

After:
top 5 に正解が 4 件
```

このように数値で評価します。

---

### Chapter 15. Failure Analysis

**学ぶこと**

* なぜ検索に失敗したのかを分類する
* chunk が悪い
* query が悪い
* embedding model が悪い
* metadata が足りない
* reranking が必要
* source document がそもそも不足している

**設計思想**

RAG の失敗は、LLM の失敗とは限りません。

多くの場合、原因は retrieval 側にあります。

```text
質問に答える文書が DB にない
↓
LLM は正しく答えられない

文書はあるが検索されていない
↓
retrieval 改善が必要

文書は検索されたが回答が間違う
↓
prompt / generation 改善が必要
```

---

## Level 7: アプリケーション編 — 実務レベルにする

### Chapter 16. API サーバー化

**構成例**

```text
FastAPI / Express
↓
Chroma Client
↓
Collection
↓
LLM
↓
Frontend
```

**学ぶこと**

* Chroma をバックエンドから呼ぶ
* 検索 API を作る
* RAG API を作る
* streaming response
* source 表示
* エラー処理

---

### Chapter 17. Client-server Mode

**学ぶこと**

* ローカル Chroma server
* `chroma run --path`
* `HttpClient`
* Docker
* フロントエンド / バックエンドからの接続

**実装例**

```bash
chroma run --path ./chroma_db
```

```python
import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)
```

Chroma は client-server mode でも動かせます。この場合、Chroma client は別プロセスで動作する Chroma server に接続します。公式ドキュメントでは `chroma run --path /db_path` で server を起動し、Python では `HttpClient(host='localhost', port=8000)` で接続する例が示されています。([Chroma Docs][10])

**設計思想**

Notebook や個人ツールでは embedded / persistent で十分です。
チーム開発や本番に近い構成では、Chroma server を分けたほうが設計しやすくなります。

---

### Chapter 18. TypeScript / Next.js 連携

**学ぶこと**

* Next.js から検索 UI を作る
* API Route から Chroma に接続する
* 検索結果カード表示
* source / score / metadata 表示
* RAG チャット UI

**構成**

```text
Next.js UI
↓
/api/search
↓
Chroma server
↓
results
```

フロントエンド寄りの実装では、検索結果をただテキストで出すのではなく、metadata を UI に反映することが重要です。

```text
タイトル
該当 chunk
source
page
score
更新日
タグ
```

---

## Level 8: 運用・本番編

### Chapter 19. Production 設計

**学ぶこと**

* collection naming
* tenant 分離
* metadata による access control
* embedding model versioning
* 再 index 戦略
* migration
* backup
* latency
* batch insert
* monitoring

**設計思想**

本番では「検索できる」だけでは不十分です。

必要なのは以下です。

```text
再現性
権限管理
評価可能性
更新可能性
障害時の復旧
モデル変更への対応
```

特に embedding model の version は metadata に入れるべきです。

```json
{
  "embedding_model": "text-embedding-3-small",
  "embedding_version": "2026-05",
  "chunker_version": "v2",
  "source_hash": "..."
}
```

Chroma は schema や data format の変更時には migration tool を提供する方針を示しており、v1.0.0 では Rust への大きな書き換えと性能改善、設定変更などが行われています。運用では migration 情報を追うことも重要です。([Chroma Docs][11])

---

### Chapter 20. Index 設定とパフォーマンス

**学ぶこと**

* HNSW
* distance function
* cosine
* L2
* inner product
* accuracy / latency trade-off
* batch insert
* top-k 設計

Chroma の single node collection では、近似最近傍探索のために HNSW index が使われます。また collection の configuration により、embedding index の構築・使用方法が決まり、accuracy と performance の要件に応じて設定を調整できます。([Chroma Docs][12])

**設計思想**

プロレベルでは、次の問いを常に考えます。

```text
top_k は本当に 5 でよいか？
top_k 50 で取って rerank すべきか？
distance function は適切か？
chunk size は検索意図に合っているか？
batch size は十分か？
```

---

## Level 9: プロフェッショナル編 — 高度検索システム

### Chapter 21. Advanced Retrieval Pipeline

**最終的な構成**

```text
User Query
↓
Query Rewrite
↓
Query Expansion
↓
Dense Search
↓
Sparse / Full-text Search
↓
Metadata Filtering
↓
RRF / Hybrid Fusion
↓
Cross-encoder Reranking
↓
Context Compression
↓
LLM Answer
↓
Citation / Source Display
↓
Evaluation Logging
```

**設計思想**

プロの RAG では、Chroma は単独で完結するものではありません。

Chroma は retrieval pipeline の中核ですが、周辺に以下を組み合わせます。

```text
query processing
document processing
reranking
evaluation
observability
access control
UI
```

---

### Chapter 22. Multi-tenant RAG

**学ぶこと**

* ユーザーごとの collection
* 組織ごとの collection
* metadata による tenant filter
* access control
* filtering overhead
* data isolation

**設計思想**

マルチテナントでは、単に metadata に `tenant_id` を入れればよいとは限りません。

```text
小規模:
1 collection + tenant_id metadata

中規模:
organization ごとに collection

大規模:
tenant / data type / embedding model ごとに分離
```

Chroma の collection 設計では、マルチテナント要件がある場合、ユーザーまたは組織ごとに collection を分けることで query 時の filtering overhead を避けられる、という考え方が示されています。([Chroma Docs][4])

---

### Chapter 23. Versioning と A/B Testing

**学ぶこと**

* chunker v1 vs v2
* embedding model A vs B
* collection fork
* evaluation dataset
* production rollout
* rollback

**設計思想**

検索システムは一度作って終わりではありません。

```text
chunking を変える
embedding model を変える
metadata を増やす
reranker を変える
prompt を変える
```

これらを比較するには、A/B testing と versioning が必要です。

---

# 最終課題: Production-grade RAG Search App

最後の課題として、以下のアプリを作るとよいです。

## アプリ内容

```text
自分の技術メモ、PDF、Markdown、Web記事を取り込み、
Chroma に保存し、
検索 UI と RAG チャット UI を提供する。
```

## 必須要件

* Chroma PersistentClient または client-server mode
* metadata 設計
* chunking
* embedding function の明示
* vector search
* metadata filtering
* full-text filtering
* query expansion
* reranking
* source 表示
* evaluation dataset
* 検索失敗ログ

## 完成イメージ

```text
質問:
Chroma で永続化するには？

検索結果:
1. persistent client の説明
2. client-server mode の説明
3. path 指定の説明

回答:
Chroma でローカル永続化するには PersistentClient を使います...
参照:
- docs/chroma_clients.md
- page: 3
- chunk_id: persistent_client_001
```

---

# 推奨カリキュラム順

| 段階      | 内容                   | 到達目標                                 |
| ------- | -------------------- | ------------------------------------ |
| Level 1 | Chroma 入門            | collection に document を入れて query できる |
| Level 2 | CRUD / metadata      | 実務的なデータ保存と絞り込みができる                   |
| Level 3 | chunking / embedding | 検索品質を意識したデータ設計ができる                   |
| Level 4 | full-text / hybrid   | vector search の限界を補える                |
| Level 5 | RAG                  | Chroma を LLM アプリに組み込める               |
| Level 6 | evaluation           | 検索品質を数値で評価できる                        |
| Level 7 | app 化                | API / UI と接続できる                      |
| Level 8 | production           | 運用・再 index・migration を考慮できる          |
| Level 9 | advanced retrieval   | 高精度な検索 pipeline を設計できる               |

---

# このチュートリアルで一番大事な考え方

Chroma DB を学ぶときに一番大事なのは、次の発想です。

```text
ベクトルDBを使う
ではなく、
検索品質を設計する
```

初心者はこう考えがちです。

```text
document を入れる
query する
LLM に渡す
```

プロはこう考えます。

```text
どの単位で chunk するか
どの metadata を付けるか
どの embedding model を使うか
どの collection に分けるか
vector search だけで十分か
keyword search も必要か
reranking すべきか
検索品質をどう評価するか
本番でどう更新・再 index するか
```

この流れで学べば、Chroma の API を覚えるだけでなく、**RAG / AI エージェント向けの検索基盤を設計できるレベル**までステップアップできます。

[1]: https://www.trychroma.com/ "Chroma - open-source search infrastructure for AI"
[2]: https://docs.trychroma.com/docs/overview/getting-started "Getting Started - Chroma Docs"
[3]: https://docs.trychroma.com/docs/querying-collections/query-and-get "Query and Get - Chroma Docs"
[4]: https://docs.trychroma.com/guides/build/look-at-your-data "Look at Your Data - Chroma Docs"
[5]: https://docs.trychroma.com/docs/run-chroma/clients "Chroma Clients - Chroma Docs"
[6]: https://docs.trychroma.com/docs/collections/update-data?utm_source=chatgpt.com "Update Data - Chroma Docs"
[7]: https://docs.trychroma.com/docs/querying-collections/metadata-filtering "Metadata Filtering - Chroma Docs"
[8]: https://docs.trychroma.com/docs/embeddings/embedding-functions "Embedding Functions - Chroma Docs"
[9]: https://docs.trychroma.com/cloud/search-api/hybrid-search "Hybrid Search with RRF - Chroma Docs"
[10]: https://docs.trychroma.com/docs/run-chroma/client-server "Client-Server Mode - Chroma Docs"
[11]: https://docs.trychroma.com/docs/overview/migration "Migration - Chroma Docs"
[12]: https://docs.trychroma.com/docs/collections/configure "Configure Collections - Chroma Docs"
