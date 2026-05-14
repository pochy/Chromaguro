# AsyncHttpClient Lab

この lab では、Chroma server を別プロセスで起動し、Python の `AsyncHttpClient` から非同期に接続します。

同期 `HttpClient` とできることはほぼ同じです。違いは、Chroma への network I/O を `await` できるため、FastAPI や async worker の中で他の処理を止めにくいことです。

## この lab でできるようになること

```text
chroma run で local server を起動できる
AsyncHttpClient で collection/add/query を実行できる
FastAPI endpoint から async Chroma query を呼べる
複数 query を asyncio.gather で並列に投げる実験ができる
同期 client と async client の使い分けを説明できる
```

## まず知るべき言葉

```text
client-server mode:
  アプリとは別プロセスで Chroma server を動かし、HTTP で接続する構成。

AsyncHttpClient:
  Chroma server に非同期 HTTP で接続する client。

await:
  network I/O などの完了を待つ間、event loop に他の仕事を進めさせるための Python 構文。

concurrency:
  複数の query を同時に進めること。必ず速くなるとは限らないが、API server では重要な設計要素。
```

## なぜこれを学ぶのか

`PersistentClient` は学習や小さな local tool に向いています。`HttpClient` は Chroma を application process から分ける時に向いています。さらに Web API や worker が async で書かれている場合は、Chroma 呼び出しも async にすると設計が自然になります。

初心者は「async にすれば速い」と考えがちです。実務では、async は主に **待ち時間をどう扱うか** の設計です。1 query の latency が劇的に下がるとは限りません。代わりに、複数 request、複数 retrieval、timeout、cancellation、error handling を扱いやすくします。

## 手順 1: Chroma server を起動する

Terminal 1:

```bash
source .venv/bin/activate
chroma run --path ./advanced_labs/async_http_client/chroma_server_db --port 9011
```

`9011` が使われている場合は、空いている port に変えてください。

## 手順 2: 単発 async query を実行する

Terminal 2:

```bash
source .venv/bin/activate
CHROMA_PORT=9011 python advanced_labs/async_http_client/examples/01_async_query.py
```

見る場所:

```text
heartbeat が返る
collection に document を add できる
query 結果に async_http_client_001 が出る
```

## 手順 3: FastAPI endpoint から呼ぶ

```bash
CHROMA_PORT=9011 python advanced_labs/async_http_client/examples/02_fastapi_async_search.py
```

この example は `TestClient` で `/health` と `/search` を呼ぶ smoke test です。実サーバーとして起動したい場合は次を使います。

```bash
CHROMA_PORT=9011 uvicorn advanced_labs.async_http_client.examples.02_fastapi_async_search:app --reload
```

## 手順 4: 複数 query を同時に投げる

```bash
CHROMA_PORT=9011 python advanced_labs/async_http_client/examples/03_concurrent_queries.py
```

見る場所:

```text
query ごとの top_id
total_latency_ms
sequential ではなく gather で待っていること
```

## Validation

この lab まで検証する場合:

```bash
scripts/validate_tutorial.sh --async-http --port 9011
```

標準ルートの `scripts/validate_tutorial.sh` では Chroma server を起動しないため、この lab は実行されません。

## よくあるつまずき

```text
Connection refused:
  chroma run が起動していないか、CHROMA_PORT が違う。

port already in use:
  別の process が同じ port を使っている。--port と CHROMA_PORT を同じ値で変える。

await を付け忘れる:
  AsyncHttpClient の blocking 操作は await する。collection.add や collection.query も await する。

async にしても速く見えない:
  小さな local query では差が出にくい。重要なのは Web API で待ち時間を event loop に返せること。
```

## 次に進む条件

```text
HttpClient と AsyncHttpClient の違いを説明できる
FastAPI endpoint の中で await collection.query(...) を呼べる
concurrent query の結果と latency を読める
timeout、port、server process の責任分界を説明できる
```

## 公式 docs で確認する箇所

- [Client-Server Mode](https://docs.trychroma.com/docs/run-chroma/client-server): `chroma run`、`HttpClient`、`AsyncHttpClient` の基本。
- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients): in-memory、persistent、HTTP client の使い分け。
- [Python Client Reference](https://docs.trychroma.com/reference/python/client): `AsyncHttpClient` の引数と client methods。
