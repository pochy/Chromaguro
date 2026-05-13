# Operations Runbook

## Reindex Plan

source document、chunker_version、embedding_version のどれかが変わったら reindex を検討します。新しい index を作って evaluation を通し、問題がなければ API の参照先を切り替えます。

## Query Logging

query、expanded_query、tenant_id、retrieved_ids、selected_context_ids、latency、failure_type をログに残します。検索失敗を分析できる形で残すことが、運用品質の土台です。

## Access Control

Chroma の metadata filter は retrieval index の検索範囲を絞るために使います。ただし権限の source of truth は RDB や認可サービスに置き、API 層で tenant_id と permission を強制してから Chroma を検索します。
