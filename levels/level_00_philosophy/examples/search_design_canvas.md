# Search Design Canvas

## 1. ユーザーと質問

```text
対象ユーザー:
代表的な質問:
質問の粒度:
回答に必要な正確性:
```

## 2. 検索対象

```text
文書の種類:
文書の更新頻度:
文書の権限境界:
文書の信頼度:
```

## 3. Chunk 設計

```text
検索単位:
chunk size の目安:
overlap の有無:
parent document への戻し方:
```

## 4. Metadata 設計

```json
{
  "source": "",
  "doc_type": "",
  "section": "",
  "page": 0,
  "lang": "ja",
  "tenant_id": "",
  "created_at": "",
  "embedding_model": "",
  "chunker_version": ""
}
```

## 5. 検索戦略

```text
vector search が効く質問:
full-text / regex が必要な質問:
metadata filter が必須の条件:
reranking が必要な場面:
```

## 6. 評価

```text
gold question:
relevant chunk ids:
失敗分類:
改善前後で見る指標:
```

