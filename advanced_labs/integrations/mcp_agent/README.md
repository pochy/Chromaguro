# MCP / Agent Memory Lab

この lab は Chroma を agent の memory / tool として考えるためのものです。

## ローカル疑似 agentic memory

```bash
python advanced_labs/integrations/mcp_agent/01_local_agentic_memory.py
```

## Chroma MCP server の設定例

Claude Desktop などの MCP host で使う場合の概念例です。

```json
{
  "mcpServers": {
    "chroma": {
      "command": "uvx",
      "args": [
        "chroma-mcp",
        "--client-type",
        "persistent",
        "--data-dir",
        "/absolute/path/to/chroma-data"
      ]
    }
  }
}
```

## 設計メモ

```text
semantic memory:
  ユーザーや業務に関する再利用可能な事実。

procedural memory:
  tool 選択や実行手順のルール。

episodic memory:
  過去の実行結果や成功した query plan。
```

記憶を増やしすぎると retrieval noise になります。`type`, `scope`, `confidence`, `source`, `created_at` を metadata に入れて、検索時に filter します。
