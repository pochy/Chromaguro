# Integrations

Chroma は単体でも使えますが、実務では framework や agent host から呼ばれることが多いです。

## 直接 SDK を使う場合

向いている場面:

```text
検索品質を細かく制御したい
metadata filter / where_document を明示したい
評価やログを自分で設計したい
framework の抽象化に隠されたくない
```

この教材の標準ルートはこの形です。

## LangChain

向いている場面:

```text
retriever と chain を組み合わせたい
既存 LangChain アプリに Chroma を差し込みたい
MMR など LangChain 側の retriever 機能を使いたい
```

注意:

```text
Chroma の全機能が LangChain abstraction に出ているとは限らない。
where_document や Cloud Search API のような機能は直接 SDK の方が明確なことがある。
```

## LlamaIndex

向いている場面:

```text
document ingestion / node / index の抽象化を使いたい
RAG の query engine と Chroma をつなぎたい
既存 LlamaIndex アプリに vector store として Chroma を使いたい
```

注意:

```text
chunking と metadata の責任が LlamaIndex 側にも移る。
Chroma collection の設計方針を失わないようにする。
```

## MCP / Agent

向いている場面:

```text
Claude Desktop などの host から Chroma を tool として使いたい
長期 memory や project knowledge base を agent に持たせたい
既存会話や文書を semantic search したい
```

注意:

```text
何を記憶するか、いつ削除するか、誰の memory かを設計する必要がある。
metadata に type, scope, confidence, source, created_at を入れる。
```

## Optional Labs

```bash
pip install -r requirements-integrations.txt
python advanced_labs/integrations/langchain/01_langchain_chroma.py
python advanced_labs/integrations/llamaindex/01_llamaindex_chroma.py
python advanced_labs/integrations/mcp_agent/01_local_agentic_memory.py
```
