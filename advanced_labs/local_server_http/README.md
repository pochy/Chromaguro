# Local Server / HttpClient Lab

この lab では Chroma server を別プロセスで起動し、Python から `HttpClient` で接続します。

## 手順

Terminal 1:

```bash
source .venv/bin/activate
chroma run --path ./advanced_labs/local_server_http/chroma_server_db
```

Terminal 2:

```bash
source .venv/bin/activate
python advanced_labs/local_server_http/http_client_smoke.py
```

`localhost:8000` が既に使われている場合は、両方の terminal で同じ port を指定します。

```bash
chroma run --path ./advanced_labs/local_server_http/chroma_server_db --port 8001
CHROMA_PORT=8001 python advanced_labs/local_server_http/http_client_smoke.py
```

## 見る場所

```text
client-server mode でも collection/add/query の考え方は同じ
アプリ process と Chroma process が分かれる
PersistentClient より本番構成に近い
```
