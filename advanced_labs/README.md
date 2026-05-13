# Advanced Labs

このフォルダは任意の発展演習です。標準チュートリアルは `levels/` だけで完了できます。

## Labs

```text
local_server_http/
  Chroma server と HttpClient をローカルで試す。

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
