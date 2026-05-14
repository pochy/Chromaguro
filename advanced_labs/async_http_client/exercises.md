# AsyncHttpClient Exercises

## 1. Query を 1 つ追加する

`examples/03_concurrent_queries.py` の `queries` に、metadata filter または RAG source に関する query を 1 つ追加してください。

確認すること:

```text
top_id が期待する document に近いか
total_latency_ms が大きく変わるか
結果の順番に依存しない書き方になっているか
```

## 2. FastAPI の response shape を変える

`examples/02_fastapi_async_search.py` の `/search` response に、`source` と `topic` を追加してください。

確認すること:

```text
metadata から source を取り出せる
metadata から topic を取り出せる
document 本文だけを返す API になっていない
```

## 3. Timeout 方針を書く

Chroma server が遅い、または落ちている時に、API server 側でどう扱うべきかを書いてください。

観点:

```text
request timeout
retry するかどうか
ユーザーに返す error message
ログに残す情報
fallback するかどうか
```

## 提出物

```text
追加した query
FastAPI response shape の変更内容
concurrent query の出力
timeout / retry / error handling の方針
```

## 進級チェック

次を自分の言葉で説明できれば完了です。

```text
AsyncHttpClient は何を async にするのか説明できる
async が 1 query の検索品質を改善するものではないと言える
FastAPI endpoint から Chroma を await して呼べる
concurrency と latency の見方を説明できる
```
