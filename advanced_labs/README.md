# Advanced Labs

このフォルダは任意の発展演習です。標準チュートリアルは `levels/` だけで完了できます。

## Labs

```text
local_server_http/
  Chroma server と HttpClient をローカルで試す。

local_embedding_comparison/
  tutorial embedding とローカル embedding model の検索品質を比較する。

async_http_client/
  AsyncHttpClient を FastAPI や concurrent query から試す。

integrations/langchain/
  LangChain の vector store abstraction から Chroma を使う。

integrations/llamaindex/
  LlamaIndex の vector store として Chroma を使う。

integrations/mcp_agent/
  MCP / agentic memory の考え方をローカル Chroma で試す。
```

## Optional dependencies

```bash
pip install -r requirements-integrations.txt
```

ローカル embedding model を比較する場合:

```bash
pip install -r requirements-local-embeddings.txt
```

## Validation

標準ルートの検証:

```bash
scripts/validate_tutorial.sh
```

integration lab も含める場合:

```bash
scripts/validate_tutorial.sh --optional-integrations
```

local embedding comparison lab も含める場合:

```bash
scripts/validate_tutorial.sh --optional-local-embeddings
```

local server / `HttpClient` lab も含める場合:

```bash
scripts/validate_tutorial.sh --http --port 9010
```

`AsyncHttpClient` lab も含める場合:

```bash
scripts/validate_tutorial.sh --async-http --port 9011
```

`localhost:8000` や `8001` が既に使われている環境もあるため、local server lab では空いている port を明示することを推奨します。

GitHub Actions では `Optional labs` workflow を手動実行すると、integration lab、local embedding comparison lab、local server / `HttpClient` lab、`AsyncHttpClient` lab を標準 CI とは分けて確認できます。
