# Level 7: アプリケーションとして使う

## この Level でできるようになること

Chroma を Python スクリプトから使うだけでなく、API として呼べる形にします。

## まず知るべき言葉

- **API**: 他のプログラムから呼ぶための入口。
- **FastAPI**: Python で API を作るためのフレームワーク。
- **request**: API に送る入力。
- **response**: API から返る出力。
- **tenant filter**: 検索してよい範囲を tenant_id で絞ること。

## なぜこれを学ぶのか

実際のアプリでは、検索は UI やバックエンドから呼ばれます。

```text
Frontend / client
↓
FastAPI
↓
Chroma PersistentClient
↓
search results / RAG context
```

ここで重要なのは、検索結果だけでなく metadata と source も API response に含めることです。

## 手順 1: API を起動する

```bash
uvicorn levels.level_07_application.examples.api_server:app --reload
```

別の terminal で確認します。

```bash
curl 'http://127.0.0.1:8000/health'
```

`{"ok":true,...}` のように返れば起動できています。

## 手順 2: search API を呼ぶ

```bash
curl 'http://127.0.0.1:8000/search?q=Chroma%20%E3%81%AE%E6%B0%B8%E7%B6%9A%E5%8C%96&tenant_id=tenant_a'
```

見る場所:

```text
id
document
metadata.source
metadata.section
distance
```

## 手順 3: rag API を呼ぶ

```bash
curl -X POST 'http://127.0.0.1:8000/rag' \
  -H 'Content-Type: application/json' \
  -d '{"question":"Chroma でデータを永続化するには？","tenant_id":"tenant_a"}'
```

`answer`, `sources`, `context` が返ることを確認します。

## よくあるつまずき

```text
Q. tenant_id を URL で受け取っていいの？
A. 教材では簡略化しています。本番では認証済み user / organization から決めます。

Q. API response に document だけ返せばよい？
A. いいえ。source, section, page, score なども返すと UI で検証しやすくなります。
```

## 次の Level に進む条件

次ができたら Level 8 に進みます。

```text
/search と /rag を呼べる
request と response の意味を説明できる
tenant filter が漏れると危険な理由を説明できる
source を UI に表示する必要性を説明できる
```

## 公式 docs で確認する箇所

- [Chroma Clients](https://docs.trychroma.com/docs/run-chroma/clients): persistent / server / cloud の接続方式。
- [Client-Server Mode](https://docs.trychroma.com/docs/run-chroma/client-server): Chroma server を別プロセスで動かす構成。

## 発展: API contract と local server

追加で次を実行します。

```bash
python levels/level_07_application/examples/02_api_contract_probe.py
```

見る場所:

```text
/health
  collection が seed されているか。

/search?q=
  validation error が返るか。

/search / /rag
  response に id, document, metadata, distance, sources が含まれるか。
```

local Chroma server と `HttpClient` を試す場合は [advanced_labs/local_server_http](../../advanced_labs/local_server_http/README.md) に進みます。
