# Retrieval Quality

## Metadata Filtering

tenant_id、doc_type、source、section、embedding_version、chunker_version を metadata として保存します。検索時に tenant_id を必ず filter すると、別 tenant の文書が context に混ざる事故を防げます。

## Hybrid Retrieval

自然文の質問は vector search が強く、SKU、エラーコード、関数名、法律番号のような exact keyword は keyword search が強いです。dense ranking と keyword ranking を RRF で統合すると、両方の弱点を補えます。

## Source Display

RAG の回答では、本文だけでなく source、section、chunk_id、page を表示します。source がない回答は、ユーザーが根拠を検証できません。

## Evaluation

検索品質は感覚で判断しません。gold question、relevant_ids、recall@k、precision@k、MRR、failure_type を記録し、pipeline の変更前後を比較します。
