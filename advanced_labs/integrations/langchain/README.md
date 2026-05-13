# LangChain + Chroma Lab

この lab は任意です。

```bash
pip install -r requirements-integrations.txt
python advanced_labs/integrations/langchain/01_langchain_chroma.py
```

## 学ぶこと

```text
LangChain の Chroma vector store は Chroma collection を abstraction として包む。
similarity_search / as_retriever は便利だが、Chroma 固有の where_document や Search API を全部表現するとは限らない。
検索品質を詰める時は Chroma SDK の直接利用も検討する。
```
