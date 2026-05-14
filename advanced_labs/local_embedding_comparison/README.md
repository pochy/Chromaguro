# Local Embedding Comparison Lab

この lab では、Chroma に入れる embedding model を変えると retrieval quality がどう変わるかを比較します。

Level 0-9 では、教材を API キー不要で安定して動かすために deterministic な tutorial embedding を使っています。この lab ではそれを baseline とし、任意で Sentence Transformers のローカル embedding model と比較します。

## この lab でできるようになること

```text
同じ documents / gold questions で embedding model を比較できる
recall@k / precision@k / MRR / latency を同じ表で見られる
embedding model を変えたら collection を分ける理由を説明できる
Chroma の検索品質は Chroma だけでなく embedding model と chunking に依存すると説明できる
```

## まず知るべき言葉

```text
baseline:
  比較の基準。ここでは tutorial embedding の結果。

local embedding model:
  API ではなく手元の machine で動く embedding model。

gold questions:
  評価用の質問と、正解として期待する relevant_ids のセット。

latency:
  1 query にかかった時間。品質が高くても遅すぎる model は実務で使いにくい。
```

## なぜこれを学ぶのか

Chroma は vector index と retrieval API を提供します。ただし、検索結果のかなりの部分は「どの embedding model で document と query を vector にしたか」で決まります。

初心者は「Chroma に入れれば意味で検索できる」と考えがちです。実務では、同じ Chroma でも embedding model、chunking、metadata、filter、reranking を変えると結果が変わります。この lab は、そのうち embedding model の影響を独立して観察するためのものです。

## 手順 1: Gold data を確認する

```bash
python advanced_labs/local_embedding_comparison/examples/01_prepare_gold_questions.py
```

見る場所:

```text
documents の ID
questions の relevant_ids
どの質問にどの document が正解として期待されているか
```

## 手順 2: Tutorial embedding baseline を測る

```bash
python advanced_labs/local_embedding_comparison/examples/02_compare_tutorial_embedding.py
```

見る場所:

```text
retrieved_ids
recall@3
precision@3
mrr
latency_ms
```

この値は比較の基準です。新しい model が本当に良いかは、baseline と同じ gold questions で比べます。

## 手順 3: ローカル embedding model と比較する

この手順は任意です。`sentence-transformers` とローカル model が必要です。

```bash
pip install -r requirements-local-embeddings.txt
LOCAL_EMBEDDING_MODEL=/path/to/local/sentence-transformers-model \
  python advanced_labs/local_embedding_comparison/examples/03_compare_local_embedding_model.py
```

model ID を指定することもできますが、環境によっては初回に model download が発生します。

```bash
LOCAL_EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 \
  python advanced_labs/local_embedding_comparison/examples/03_compare_local_embedding_model.py
```

API キーなし、model download なしで教材を検証したい場合は、この手順を skip して構いません。

## 手順 4: 比較レポートを見る

```bash
python advanced_labs/local_embedding_comparison/examples/04_report_metrics.py
```

`LOCAL_EMBEDDING_MODEL` が設定されていれば local model も含めます。設定されていない場合は tutorial embedding だけを表示し、local model は skipped と表示します。

## よくあるつまずき

```text
sentence_transformers が見つからない:
  pip install -r requirements-local-embeddings.txt を実行する。

model download が始まる:
  model ID ではなく、事前に download 済みの local path を LOCAL_EMBEDDING_MODEL に指定する。

collection を使い回して結果がおかしい:
  embedding dimension や model が違う vector を同じ collection に混ぜない。

local model が tutorial embedding より悪く見える:
  小さな gold dataset では model の一般性能を断定できない。失敗 query を見て原因を分類する。
```

## 次に進む条件

```text
tutorial embedding の baseline metrics を説明できる
同じ questions / relevant_ids で比較する理由を説明できる
embedding model を変えたら collection を分ける理由を説明できる
recall, precision, MRR, latency の tradeoff を説明できる
```

## 公式 docs で確認する箇所

- [Embedding Functions](https://docs.trychroma.com/docs/embeddings/embedding-functions): collection に embedding function を紐づけ、add / query 時に使う考え方。
- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients): local client と server client の使い分け。
- [Configure Collections](https://docs.trychroma.com/docs/collections/configure): collection 設定と、index の考え方。
