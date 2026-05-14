# Next Steps Roadmap

このドキュメントは、現段階のチュートリアルをさらに Chroma らしく、実務で使える教材に近づけるための次の作業をまとめます。

Level 0-9 と Advanced Labs は、すでに local / OSS Chroma を RAG retrieval index として使う基礎を一通り扱っています。次に足すべきものは、API の暗記ではなく、**embedding、client mode、運用、評価の判断力を強くする optional lab** です。

## 現段階の評価

今のチュートリアルで十分に学べること:

```text
Chroma を SQLite や PostgreSQL の代替ではなく retrieval index として説明できる
collection / record / metadata / embedding / query / get / where / where_document を使える
chunking, source display, tenant filter, evaluation, reindex の設計を考えられる
PersistentClient と local server / HttpClient の違いを説明できる
RAG API と agent memory の小さな実装を作れる
```

まだ「Chroma の全てを理解した」とまでは言わない方がよいこと:

```text
全 embedding provider を比較して選べる
AsyncHttpClient を実務 API に組み込める
Docker / server process / backup / restore を本番運用できる
HNSW configuration をデータ規模に応じて tuning できる
image / URI / multimodal retrieval を使い分けられる
Cloud 専用 API まで実運用できる
```

したがって、次の目標は「Chroma の全 API を暗記すること」ではありません。目標は、**Chroma を採用する意味、採用しない場面、検索品質を改善する手順を説明できる状態**にすることです。

## 実装方針

- 標準ルートは API キー不要・完全ローカルのまま保つ。
- 外部 API、Docker、大きな model download が必要なものは `advanced_labs/` に置く。
- 追加 lab は必ず「何を比較するか」と「何を見て判断するか」を持たせる。
- 新しい機能を足すたびに、`appendices/local_chroma_coverage.md` の gap を更新する。
- runnable example、README、exercise、validation command をセットで追加する。

## 追加済み: Local Embedding Comparison Lab

最初の optional lab として追加済みです。

### なぜ必要か

今の標準ルートは、教材を安定して動かすために deterministic な tutorial embedding を使っています。これは学習には向いていますが、実務では embedding model の選択が retrieval quality、latency、cost、言語対応に直結します。

この lab では、Chroma そのものだけでなく、**Chroma に入れる embedding が検索結果をどう変えるか**を学びます。

追加先:

```text
advanced_labs/local_embedding_comparison/
```

### 追加する内容

```text
advanced_labs/local_embedding_comparison/
  README.md
  data/
    records.json
    gold_questions.json
  examples/
    01_prepare_gold_questions.py
    02_compare_tutorial_embedding.py
    03_compare_local_embedding_model.py
    04_report_metrics.py
  exercises.md
```

標準では既存 helper による tutorial embedding baseline だけで動かし、Sentence Transformers のローカル embedding model は `LOCAL_EMBEDDING_MODEL` がある場合だけ実行します。OpenAI / Cohere / Jina / Mistral などの外部 provider は、さらに後の optional appendix に分けます。

### 見るべき出力

```text
provider_name
recall@k
precision@k
MRR
latency_ms
retrieved_ids
```

### 完了条件

- 同じ document set と gold questions で複数 embedding を比較できる。
- model を変えると retrieved IDs が変わることを観察できる。
- 「品質」「速度」「コスト」「日本語対応」の tradeoff を説明できる。
- API key がない環境でも validation が通る。

## 追加済み: AsyncHttpClient Lab

### なぜ必要か

FastAPI、async worker、並列 retrieval pipeline では、同期 `HttpClient` だけでは設計判断が足りません。Chroma server を別 process として動かし、async な application code から呼ぶ形を学びます。

追加先:

```text
advanced_labs/async_http_client/
```

### 追加する内容

```text
advanced_labs/async_http_client/
  README.md
  examples/
    01_async_query.py
    02_fastapi_async_search.py
    03_concurrent_queries.py
  exercises.md
```

### 完了条件

- `chroma run` で local server を起動し、async client から query できる。
- 同期 client と async client の使い分けを説明できる。
- timeout、concurrency、error handling の最低限の設計を説明できる。

## 優先度 3: Docker Local Server Lab

### なぜ必要か

`PersistentClient` は学習と小規模開発に便利ですが、実務では Chroma を application process から分けて動かしたい場面があります。Docker lab では、local server を container として起動し、data volume、health check、backup の入口を学びます。

### 追加する内容

```text
advanced_labs/docker_local_server/
  README.md
  docker-compose.yml
  examples/
    01_http_client_against_docker.py
    02_backup_volume_notes.md
  exercises.md
```

### 完了条件

- Docker 上の Chroma に `HttpClient` で接続できる。
- data volume を消した場合と残した場合の違いを確認できる。
- local file path、server process、container volume の責任分界を説明できる。

## 優先度 4: HNSW Configuration Experiment

### なぜ必要か

Level 8 では index setting の tradeoff を概念として扱っています。ただし、実務では corpus size、embedding dimension、latency target によって設定の意味が変わります。

小さな教材データでは差が出づらいため、この lab は「結論を覚える」のではなく、**測り方を学ぶ**ことを目的にします。

### 追加する内容

```text
advanced_labs/hnsw_configuration/
  README.md
  examples/
    01_generate_synthetic_corpus.py
    02_compare_collection_settings.py
    03_measure_latency_and_recall.py
  exercises.md
```

### 完了条件

- collection configuration を変えた比較実験を実行できる。
- recall と latency の両方を見る理由を説明できる。
- 小規模実験の結果を本番にそのまま一般化してはいけない理由を説明できる。

## 優先度 5: Image / URI / Multimodal Appendix

### なぜ必要か

この教材は text RAG を中心にしています。一方で、Chroma API には image / URI 系の入力もあり、画像や file reference を retrieval target にしたい場面があります。

ただし、初心者にとっては text retrieval の理解が先なので、これは Level 本体ではなく appendix に置きます。

### 追加する内容

```text
appendices/multimodal_retrieval.md
advanced_labs/multimodal_retrieval/
  README.md
  examples/
    01_uri_metadata_index.py
    02_image_embedding_optional.py
  exercises.md
```

### 完了条件

- text document、URI、image reference の違いを説明できる。
- Chroma に保存するものと、object storage や file system に置くものを分けて考えられる。
- multi-modal retrieval を標準 text RAG と混同しない。

## 進める順番

```text
1. local_embedding_comparison を追加する: done
2. local_chroma_coverage.md の Local embedding model comparison を optional hands-on にする: done
3. AsyncHttpClient lab を追加する: done
4. Docker local server lab を追加する
5. HNSW experiment を追加する
6. multimodal appendix を追加する
```

次に着手するなら、`Docker local server lab` です。local embedding comparison で retrieval quality、AsyncHttpClient で async application integration を扱った後は、Chroma server を container と volume で動かす運用入口に進むのが自然です。

## 完了後に言えること

上の next steps まで終えたら、Cloud 専用機能を除いて次のように言えます。

```text
local / OSS Chroma を使った RAG retrieval system を設計、実装、評価、改善できる
embedding model の違いが検索品質に与える影響を実験で確認できる
同期 / 非同期 / server process / Docker の使い分けを説明できる
collection configuration を測定対象として扱える
Chroma が向いている問題と、RDB や全文検索 engine を優先すべき問題を区別できる
```

それでも、「Chroma の全てを理解した」という表現は避けます。Chroma 本体、Cloud、client SDK、embedding provider、周辺 framework は変化し続けるためです。より正確には、**Chroma を実務で使うための判断軸と検証方法を身につけた**と言えます。
